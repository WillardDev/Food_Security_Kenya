import streamlit as st
import geopandas as gpd
import pandas as pd

from dashboard.config import KEYS, DATA_DIR, JMR_DIR, SHAPEFILE_DIR, ALERT_LABELS

COUNTY_NAME_FIXES = {
    "Elgeyo Marakwet": "Elgeyo-Marakwet",
    "Trans-Nzoia": "Trans Nzoia",
    "Tharaka Nithi": "Tharaka-Nithi",
}
NON_COUNTY_AREAS = ["Dadaab", "Kakuma", "Kalobeyei"]


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
    c = df.copy()
    c.columns = c.columns.str.strip()
    c["Year"] = pd.to_numeric(c["Year"], errors="coerce").astype("Int64")
    c["Value"] = pd.to_numeric(c["Value"], errors="coerce")
    return c


@st.cache_data
def build_analysis_df(food_security, food_balances, healthy_diet):
    fsc, fbc, hdc = clean_base(food_security), clean_base(food_balances), clean_base(healthy_diet)

    def pivot(df, item_map):
        sel = df[df["Item"].isin(item_map.keys())].copy()
        sel["indicator"] = sel["Item"].map(item_map)
        wide = sel.pivot_table(index=KEYS, columns="indicator", values="Value", aggfunc="mean").reset_index()
        wide.columns.name = None
        return wide

    fsi = pivot(fsc, {
        "Average dietary energy supply adequacy (percent) (3-year average)": "dietary_energy_adequacy_pct",
        "Prevalence of undernourishment (percent) (3-year average)": "undernourishment_pct",
        "Number of people undernourished (million) (3-year average)": "undernourished_people_million",
        "Prevalence of severe food insecurity in the total population (percent) (3-year average)": "severe_food_insecurity_pct",
        "Prevalence of moderate or severe food insecurity in the total population (percent) (3-year average)": "moderate_or_severe_food_insecurity_pct",
        "Percentage of children under 5 years of age who are stunted (modelled estimates) (percent)": "under5_stunting_pct",
        "Percentage of children under 5 years affected by wasting (percent)": "under5_wasting_pct",
        "Gross domestic product per capita, PPP, (constant 2021 international $)": "gdp_per_capita_ppp",
    })
    cohd = pivot(hdc, {
        "Cost of a healthy diet (CoHD)": "healthy_diet_cost_ppp_per_day",
        "Prevalence of unaffordability (PUA)": "healthy_diet_unaffordable_pct",
        "Number of people unable to afford a healthy diet (NUA)": "people_unable_afford_healthy_diet_million",
    })

    def ext(item, element, name):
        return fbc[(fbc["Item"] == item) & (fbc["Element"] == element)][KEYS + ["Value"]].rename(columns={"Value": name})

    pop = ext("Population", "Total Population - Both sexes", "population_thousand")
    fs = ext("Grand Total", "Food supply (kcal/capita/day)", "food_supply_kcal_capita_day")
    ps = ext("Grand Total", "Protein supply quantity (g/capita/day)", "protein_supply_g_capita_day")
    fat = ext("Grand Total", "Fat supply quantity (g/capita/day)", "fat_supply_g_capita_day")

    fb = pop.merge(fs, on=KEYS, how="outer").merge(ps, on=KEYS, how="outer").merge(fat, on=KEYS, how="outer")
    return fsi.merge(fb, on=KEYS, how="outer").merge(cohd, on=KEYS, how="outer").sort_values("Year").reset_index(drop=True)


@st.cache_data
def build_county_data(jmr_data, jmr_pcodes, _kenya_counties):
    jmr_admin = jmr_data.merge(
        jmr_pcodes[["adm1_pcode", "adm1_name", "adm2_pcode", "adm2_name"]],
        on="adm2_pcode", how="left",
    )
    jmr_alerts = jmr_admin[jmr_admin["grouping"].eq("Alert level")].copy()
    jmr_alerts["alert_level"] = jmr_alerts["value"].round().astype("Int64")

    county_alerts = jmr_alerts.groupby(
        ["adm1_pcode", "adm1_name", "date", "indicator"], as_index=False
    ).agg(
        max_alert_level=("alert_level", "max"),
        critical_admin2_count=("alert_level", lambda s: int((s == 2).sum())),
        heightened_admin2_count=("alert_level", lambda s: int((s == 1).sum())),
        admin2_count=("adm2_pcode", "nunique"),
    )

    latest_date = county_alerts["date"].max()
    latest = county_alerts[county_alerts["date"].eq(latest_date)].copy()

    summary = latest.groupby(["adm1_pcode", "adm1_name"], as_index=False).agg(
        overall_max_alert=("max_alert_level", "max"),
        total_critical_flags=("critical_admin2_count", "sum"),
        total_heightened_flags=("heightened_admin2_count", "sum"),
    )
    summary["overall_alert_label"] = summary["overall_max_alert"].map(ALERT_LABELS)
    summary = summary.sort_values(["overall_max_alert", "total_critical_flags"], ascending=False)

    geo = _kenya_counties.merge(summary, on="adm1_pcode", how="left")
    geo = gpd.GeoDataFrame(geo, geometry="geometry", crs=_kenya_counties.crs)

    pop_rows = jmr_admin[jmr_admin["grouping"].eq("Population")].copy()
    if not pop_rows.empty:
        county_pop = (
            pop_rows.groupby(["adm1_name", "adm2_pcode"])["value"].max()
            .groupby("adm1_name").sum().rename("population")
        )
        summary = summary.merge(county_pop, on="adm1_name", how="left")

    return county_alerts, summary, geo, latest_date


@st.cache_data
def load_county_external():
    dhs = pd.read_csv(DATA_DIR / "kenya_dhs_nutrition_county.csv")
    pov = pd.read_csv(DATA_DIR / "kenya_poverty_rate_county.csv")
    ipc = pd.read_csv(DATA_DIR / "kenya_ipc_area_long_latest.csv")

    def fix_names(series):
        return series.str.strip().replace(COUNTY_NAME_FIXES)

    # DHS 2022 - county-level child stunting & wasting (%)
    d22 = dhs[dhs["SurveyYear"] == 2022].copy()
    is_county = d22["CharacteristicLabel"].str.startswith("..") | (d22["CharacteristicLabel"] == "Nairobi")
    d22 = d22[is_county & d22["Indicator"].isin(["Children stunted", "Children wasted"])]
    d22["county"] = fix_names(d22["CharacteristicLabel"].str.lstrip("."))
    nutrition = d22.pivot_table(index="county", columns="Indicator", values="Value", aggfunc="first").reset_index()
    nutrition = nutrition.rename(columns={"Children stunted": "stunting_pct", "Children wasted": "wasting_pct"})

    # HAPI poverty - county level, latest round (2022)
    povc = pov[(pov["admin_level"] == 1) & (pov["reference_period_end"] == pov["reference_period_end"].max())]
    povc = povc.dropna(subset=["admin1_name"]).copy()
    povc["county"] = fix_names(povc["admin1_name"])
    povc["self_provided"] = povc["provider_admin1_name"].fillna("").eq(povc["admin1_name"])
    povc = povc.sort_values("self_provided", ascending=False).drop_duplicates(subset="county", keep="first")
    poverty = povc[["county", "mpi", "headcount_ratio", "vulnerable_to_poverty", "in_severe_poverty"]].rename(
        columns={
            "headcount_ratio": "poverty_pct",
            "vulnerable_to_poverty": "vulnerable_to_poverty_pct",
            "in_severe_poverty": "severe_poverty_pct",
        }
    )

    # IPC latest analysis - population in acute food insecurity (phase 3+) by county
    ipc_cur = ipc[ipc["Validity period"] == "current"].copy()
    ipc_cur["county"] = fix_names(ipc_cur["Area"])
    ipc_cur = ipc_cur[~ipc_cur["county"].isin(NON_COUNTY_AREAS)]
    crisis = ipc_cur[ipc_cur["Phase"] == "3+"][["county", "Number", "Percentage"]].rename(
        columns={"Number": "ipc_crisis_population", "Percentage": "ipc_crisis_pct"}
    )
    total = ipc_cur[ipc_cur["Phase"] == "all"][["county", "Number"]].rename(
        columns={"Number": "ipc_total_population"}
    )
    ipc_pivot = total.merge(crisis, on="county", how="outer")
    ipc_pivot["ipc_crisis_pct"] = ipc_pivot["ipc_crisis_pct"] * 100

    merged = poverty.merge(nutrition, on="county", how="outer").merge(ipc_pivot, on="county", how="outer")
    return merged


@st.cache_data
def build_county_stats(county_risk_summary, county_external):
    stats = county_risk_summary.merge(
        county_external, left_on="adm1_name", right_on="county", how="left"
    ).drop(columns="county", errors="ignore")
    return stats
