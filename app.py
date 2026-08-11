import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Food Security in Kenya",
    page_icon="🇰🇪",
    layout="wide",
)

DATA_DIR = Path("data")
JMR_DIR = DATA_DIR / "world_bank_jmr"
SHAPEFILE_DIR = DATA_DIR / "shapefiles"
KEYS = ["Iso3", "Area", "Year"]


@st.cache_data
def load_all():
    food_security = pd.read_csv(DATA_DIR / "ken_faostat_food_security_indicators.csv")
    food_balances = pd.read_csv(DATA_DIR / "ken_faostat_food_balances.csv")
    healthy_diet = pd.read_csv(DATA_DIR / "ken_faostat_cost_affordability_healthy_diet.csv")

    jmr_data = pd.read_csv(JMR_DIR / "KEN_JMR_data.zip", parse_dates=["date"])
    jmr_pcodes = pd.read_csv(JMR_DIR / "KEN_JMR_pcodes.zip")
    kenya_counties = gpd.read_file(SHAPEFILE_DIR / "kenya_counties.geojson").to_crs("EPSG:4326")
    kenya_counties = kenya_counties.rename(columns={"ADM1_PCODE": "adm1_pcode", "ADM1_EN": "county_name"})

    return food_security, food_balances, healthy_diet, jmr_data, jmr_pcodes, kenya_counties


@st.cache_data
def clean_base(df):
    cleaned = df.copy()
    cleaned.columns = cleaned.columns.str.strip()
    cleaned["Year"] = pd.to_numeric(cleaned["Year"], errors="coerce").astype("Int64")
    cleaned["Value"] = pd.to_numeric(cleaned["Value"], errors="coerce")
    cleaned["Area"] = cleaned["Area"].astype(str).str.strip()
    cleaned["Iso3"] = cleaned["Iso3"].astype(str).str.strip()
    return cleaned


@st.cache_data
def build_analysis_df(food_security, food_balances, healthy_diet):
    food_security_clean = clean_base(food_security)
    food_balances_clean = clean_base(food_balances)
    healthy_diet_clean = clean_base(healthy_diet)

    def pivot_indicators(df, item_map):
        selected = df[df["Item"].isin(item_map.keys())].copy()
        selected["indicator"] = selected["Item"].map(item_map)
        wide = selected.pivot_table(index=KEYS, columns="indicator", values="Value", aggfunc="mean").reset_index()
        wide.columns.name = None
        return wide

    food_security_items = {
        "Average dietary energy supply adequacy (percent) (3-year average)": "dietary_energy_adequacy_pct",
        "Prevalence of undernourishment (percent) (3-year average)": "undernourishment_pct",
        "Number of people undernourished (million) (3-year average)": "undernourished_people_million",
        "Prevalence of severe food insecurity in the total population (percent) (3-year average)": "severe_food_insecurity_pct",
        "Prevalence of moderate or severe food insecurity in the total population (percent) (3-year average)": "moderate_or_severe_food_insecurity_pct",
        "Percentage of children under 5 years of age who are stunted (modelled estimates) (percent)": "under5_stunting_pct",
        "Percentage of children under 5 years affected by wasting (percent)": "under5_wasting_pct",
        "Gross domestic product per capita, PPP, (constant 2021 international $)": "gdp_per_capita_ppp",
    }

    healthy_diet_items = {
        "Cost of a healthy diet (CoHD)": "healthy_diet_cost_ppp_per_day",
        "Prevalence of unaffordability (PUA)": "healthy_diet_unaffordable_pct",
        "Number of people unable to afford a healthy diet (NUA)": "people_unable_afford_healthy_diet_million",
    }

    fsi_wide = pivot_indicators(food_security_clean, food_security_items)
    cohd_wide = pivot_indicators(healthy_diet_clean, healthy_diet_items)

    population = food_balances_clean[
        (food_balances_clean["Item"] == "Population")
        & (food_balances_clean["Element"] == "Total Population - Both sexes")
    ][KEYS + ["Value"]].rename(columns={"Value": "population_thousand"})

    food_supply = food_balances_clean[
        (food_balances_clean["Item"] == "Grand Total")
        & (food_balances_clean["Element"] == "Food supply (kcal/capita/day)")
    ][KEYS + ["Value"]].rename(columns={"Value": "food_supply_kcal_capita_day"})

    protein_supply = food_balances_clean[
        (food_balances_clean["Item"] == "Grand Total")
        & (food_balances_clean["Element"] == "Protein supply quantity (g/capita/day)")
    ][KEYS + ["Value"]].rename(columns={"Value": "protein_supply_g_capita_day"})

    fat_supply = food_balances_clean[
        (food_balances_clean["Item"] == "Grand Total")
        & (food_balances_clean["Element"] == "Fat supply quantity (g/capita/day)")
    ][KEYS + ["Value"]].rename(columns={"Value": "fat_supply_g_capita_day"})

    food_balance_wide = population.merge(food_supply, on=KEYS, how="outer")
    food_balance_wide = food_balance_wide.merge(protein_supply, on=KEYS, how="outer")
    food_balance_wide = food_balance_wide.merge(fat_supply, on=KEYS, how="outer")

    analysis_df = fsi_wide.merge(food_balance_wide, on=KEYS, how="outer")
    analysis_df = analysis_df.merge(cohd_wide, on=KEYS, how="outer")
    return analysis_df.sort_values("Year").reset_index(drop=True)


@st.cache_data
def build_county_data(jmr_data, jmr_pcodes, kenya_counties):
    jmr_admin = jmr_data.merge(
        jmr_pcodes[["adm1_pcode", "adm1_name", "adm2_pcode", "adm2_name"]],
        on="adm2_pcode",
        how="left",
    )

    alert_labels = {0: "Typical", 1: "Heightened", 2: "Critical"}
    jmr_alerts = jmr_admin[jmr_admin["grouping"].eq("Alert level")].copy()
    jmr_alerts["alert_level"] = jmr_alerts["value"].round().astype("Int64")

    county_alerts = jmr_alerts.groupby(
        ["adm1_pcode", "adm1_name", "date", "indicator"], as_index=False
    ).agg(
        max_alert_level=("alert_level", "max"),
        mean_alert_level=("alert_level", "mean"),
        critical_admin2_count=("alert_level", lambda s: int((s == 2).sum())),
        heightened_admin2_count=("alert_level", lambda s: int((s == 1).sum())),
        admin2_count=("adm2_pcode", "nunique"),
    )

    latest_alert_date = county_alerts["date"].max()
    latest_county_alerts = county_alerts[county_alerts["date"].eq(latest_alert_date)].copy()

    county_risk_summary = latest_county_alerts.groupby(
        ["adm1_pcode", "adm1_name"], as_index=False
    ).agg(
        overall_max_alert=("max_alert_level", "max"),
        total_critical_admin2_flags=("critical_admin2_count", "sum"),
        total_heightened_admin2_flags=("heightened_admin2_count", "sum"),
        indicators_at_critical=("max_alert_level", lambda s: int((s == 2).sum())),
        indicators_at_heightened=("max_alert_level", lambda s: int((s == 1).sum())),
        indicators_available=("indicator", "nunique"),
    )
    county_risk_summary["overall_alert_label"] = county_risk_summary["overall_max_alert"].map(alert_labels)
    county_risk_summary = county_risk_summary.sort_values(
        ["overall_max_alert", "total_critical_admin2_flags", "total_heightened_admin2_flags"],
        ascending=False,
    )

    county_geo_df = kenya_counties.merge(county_risk_summary, on="adm1_pcode", how="left")
    county_geo_df = gpd.GeoDataFrame(county_geo_df, geometry="geometry", crs=kenya_counties.crs)

    return county_alerts, county_risk_summary, county_geo_df, latest_alert_date


sns.set_theme(style="whitegrid")

st.title("🇰🇪 Food Security in Kenya — National Trends & County Risk")
st.markdown("Analysis of Kenya's food security using FAOSTAT national data and World Bank JMR county-level risk indicators.")
st.markdown("---")

with st.spinner("Loading data..."):
    food_security, food_balances, healthy_diet, jmr_data, jmr_pcodes, kenya_counties = load_all()
    analysis_df = build_analysis_df(food_security, food_balances, healthy_diet)
    county_alerts, county_risk_summary, county_geo_df, latest_alert_date = build_county_data(
        jmr_data, jmr_pcodes, kenya_counties
    )

tab1, tab2, tab3, tab4 = st.tabs(["📈 National Trends", "🗺️ County Risk", "🥗 Diet Affordability", "🔍 Data Explorer"])

with tab1:
    st.header("National Food Security Indicators Over Time")
    st.markdown("""
    These track four dimensions of food security:
    - **Availability**: Is enough food produced? (calories, protein, fat supply)
    - **Access**: Can people afford food? (undernourishment, food insecurity rates)
    - **Utilization**: Is food nutritious? (child stunting and wasting)
    - **Stability**: Is access consistent over time?
    """)

    trend_options = {
        "Undernourishment %": "undernourishment_pct",
        "Severe Food Insecurity %": "severe_food_insecurity_pct",
        "Moderate/Severe Food Insecurity %": "moderate_or_severe_food_insecurity_pct",
        "Dietary Energy Adequacy %": "dietary_energy_adequacy_pct",
        "Under-5 Stunting %": "under5_stunting_pct",
        "Under-5 Wasting %": "under5_wasting_pct",
        "GDP per Capita (PPP)": "gdp_per_capita_ppp",
    }

    selected = st.multiselect(
        "Select indicators:",
        list(trend_options.keys()),
        default=["Undernourishment %", "Moderate/Severe Food Insecurity %", "Dietary Energy Adequacy %"],
    )

    if selected:
        cols = [trend_options[s] for s in selected]
        trend_df = analysis_df[["Year"] + cols].melt(
            id_vars="Year", var_name="indicator", value_name="value"
        ).dropna()
        trend_df["indicator"] = trend_df["indicator"].map({v: k for k, v in trend_options.items()})

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=trend_df, x="Year", y="value", hue="indicator", marker="o", ax=ax)
        ax.set_title("Kenya National Food Security Indicators")
        ax.set_xlabel("Year")
        ax.set_ylabel("Percent / Value")
        ax.legend(title="Indicator", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout()
        st.pyplot(fig)

    st.subheader("Latest Values (All Indicators)")
    latest_values = []
    for col in [c for c in analysis_df.columns if c not in KEYS]:
        latest = analysis_df.dropna(subset=[col]).sort_values("Year").tail(1)
        if not latest.empty:
            latest_values.append({
                "Indicator": col,
                "Latest Year": int(latest["Year"].iloc[0]),
                "Value": latest[col].iloc[0],
            })
    st.dataframe(pd.DataFrame(latest_values).sort_values("Indicator"), use_container_width=True)

with tab2:
    st.header("County-Level Food Security Risk")
    st.markdown(f"Latest JMR alert date: **{latest_alert_date.date()}** — showing alert levels by county.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 15 Highest-Risk Counties")
        top_counties = county_risk_summary.head(15)
        fig, ax = plt.subplots(figsize=(10, 7))
        palette = {"Typical": "#7fbf7b", "Heightened": "#fdae61", "Critical": "#d7191c"}
        sns.barplot(
            data=top_counties,
            y="adm1_name",
            x="total_critical_admin2_flags",
            hue="overall_alert_label",
            dodge=False,
            palette=palette,
            ax=ax,
        )
        ax.set_title(f"Counties with Most Critical Flags")
        ax.set_xlabel("Critical indicator count")
        ax.set_ylabel("County")
        ax.legend(title="Overall Alert")
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("County Alert Level Heatmap")
        county_indicator_matrix = county_alerts.pivot_table(
            index=["adm1_pcode", "adm1_name"],
            columns="indicator",
            values="max_alert_level",
            aggfunc="max",
        ).reset_index()
        county_indicator_matrix.columns.name = None

        heatmap_data = county_indicator_matrix.set_index("adm1_name").drop(columns="adm1_pcode")
        heatmap_data = heatmap_data.loc[county_risk_summary["adm1_name"]]
        heatmap_data = heatmap_data.astype(float)

        fig, ax = plt.subplots(figsize=(10, 12))
        sns.heatmap(
            heatmap_data,
            cmap=sns.color_palette(["#7fbf7b", "#fdae61", "#d7191c"], as_cmap=True),
            vmin=0, vmax=2,
            linewidths=0.4,
            linecolor="white",
            cbar_kws={"ticks": [0, 1, 2], "label": "Alert level"},
            ax=ax,
        )
        ax.set_title("Latest JMR Alert Levels by County")
        ax.set_xlabel("Indicator")
        ax.set_ylabel("County")
        plt.tight_layout()
        st.pyplot(fig)

with tab3:
    st.header("Healthy Diet Cost & Affordability")
    st.markdown("""
    A healthy diet provides balanced nutrition: fruits, vegetables, protein, and whole grains.
    In Kenya, a healthy diet costs **KES 74-103 per person per day** (international dollars),
    and roughly **76-78% of the population cannot afford it**.
    """)

    cohd_cols = ["healthy_diet_cost_ppp_per_day", "healthy_diet_unaffordable_pct", "people_unable_afford_healthy_diet_million"]
    cohd_labels = {
        "healthy_diet_cost_ppp_per_day": "Cost per day (Int$)",
        "healthy_diet_unaffordable_pct": "Unaffordable (%)",
        "people_unable_afford_healthy_diet_million": "People unable to afford (millions)",
    }

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for i, col in enumerate(cohd_cols):
        data = analysis_df[["Year", col]].dropna()
        axes[i].plot(data["Year"], data[col], marker="o", color="#d7191c")
        axes[i].set_title(cohd_labels[col])
        axes[i].set_xlabel("Year")
        axes[i].set_ylabel(cohd_labels[col])
    fig.suptitle("Healthy Diet Affordability in Kenya (2017-2025)", fontsize=14, y=1.02)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("What this means")
    st.info("""
    - A Kenyan needs ~$3.20/day (Int$) for a healthy diet
    - 43+ million Kenyans (76% of the population) cannot afford this
    - This means most Kenyans rely on cheap, nutrient-poor staples like maize and ugali
    """)

with tab4:
    st.header("Data Explorer")
    st.subheader("FAOSTAT National Data")
    st.dataframe(analysis_df, use_container_width=True)

    st.subheader("County Risk Summary")
    st.dataframe(county_risk_summary, use_container_width=True)

    st.markdown("---")
    st.markdown("Data sources: [FAOSTAT/HDX](https://data.humdata.org/dataset/ken-faostat-food-security-indicators) | [World Bank JMR](https://microdata.worldbank.org/catalog/8115)")
