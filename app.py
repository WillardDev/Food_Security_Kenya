import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Food Security in Kenya — Data Story",
    page_icon="🇰🇪",
    layout="wide",
)

SAFE = "#2ecc71"
WARNING = "#f39c12"
DANGER = "#e74c3c"
NEUTRAL = "#3498db"
BG = "#0e1117"
GRID = "#262730"

ALERT_COLORS = {0: SAFE, 1: WARNING, 2: DANGER}
ALERT_LABELS = {0: "Typical", 1: "Heightened", 2: "Critical"}

THRESHOLDS = {
    "dietary_energy_adequacy_pct":      (95,  90,  "higher_is_better"),
    "food_supply_kcal_capita_day":      (2100, 1800, "higher_is_better"),
    "protein_supply_g_capita_day":      (50,  40,  "higher_is_better"),
    "fat_supply_g_capita_day":          (40,  30,  "higher_is_better"),
    "undernourishment_pct":             (15,  25,  "lower_is_better"),
    "undernourished_people_million":    (10,  15,  "lower_is_better"),
    "severe_food_insecurity_pct":       (10,  20,  "lower_is_better"),
    "moderate_or_severe_food_insecurity_pct": (40, 60, "lower_is_better"),
    "under5_stunting_pct":              (20,  30,  "lower_is_better"),
    "under5_wasting_pct":               (5,   15,  "lower_is_better"),
    "healthy_diet_cost_ppp_per_day":    (3.5, 5.0, "lower_is_better"),
    "healthy_diet_unaffordable_pct":    (50,  70,  "lower_is_better"),
    "people_unable_afford_healthy_diet_million": (20, 35, "lower_is_better"),
    "gdp_per_capita_ppp":               (3000, 2000, "higher_is_better"),
}

INDICATOR_META = {
    "dietary_energy_adequacy_pct":      {"label": "Dietary Energy Supply Adequacy", "unit": "%", "category": "Availability", "tip": "% of population calorie needs met by domestic supply"},
    "food_supply_kcal_capita_day":      {"label": "Food Supply", "unit": "kcal/day", "category": "Availability", "tip": "Average calories available per person per day"},
    "protein_supply_g_capita_day":      {"label": "Protein Supply", "unit": "g/day", "category": "Availability", "tip": "Average protein available per person per day"},
    "fat_supply_g_capita_day":          {"label": "Fat Supply", "unit": "g/day", "category": "Availability", "tip": "Average fat available per person per day"},
    "undernourishment_pct":             {"label": "Prevalence of Undernourishment", "unit": "%", "category": "Access", "tip": "% of population consistently unable to meet calorie needs"},
    "undernourished_people_million":    {"label": "People Undernourished", "unit": "million", "category": "Access", "tip": "Total number of undernourished people"},
    "severe_food_insecurity_pct":       {"label": "Severe Food Insecurity", "unit": "%", "category": "Access", "tip": "% of population who went entire days without eating"},
    "moderate_or_severe_food_insecurity_pct": {"label": "Moderate/Severe Food Insecurity", "unit": "%", "category": "Access", "tip": "% of population experiencing food anxiety or meal-skipping"},
    "under5_stunting_pct":              {"label": "Child Stunting (Under-5)", "unit": "%", "category": "Utilization", "tip": "% of children too short for their age (chronic malnutrition)"},
    "under5_wasting_pct":               {"label": "Child Wasting (Under-5)", "unit": "%", "category": "Utilization", "tip": "% of children dangerously thin (acute malnutrition)"},
    "healthy_diet_cost_ppp_per_day":    {"label": "Healthy Diet Cost", "unit": "Int$/day", "category": "Access", "tip": "Cost of a nutritious diet per person per day"},
    "healthy_diet_unaffordable_pct":    {"label": "Cannot Afford Healthy Diet", "unit": "%", "category": "Access", "tip": "% of population who cannot afford a healthy diet"},
    "people_unable_afford_healthy_diet_million": {"label": "People Unable to Afford", "unit": "million", "category": "Access", "tip": "Total people who cannot afford a healthy diet"},
    "gdp_per_capita_ppp":               {"label": "GDP per Capita", "unit": "Int$", "category": "Economic", "tip": "Economic output per person, adjusted for local prices"},
}


def status_color(value, indicator):
    if indicator not in THRESHOLDS or pd.isna(value):
        return NEUTRAL
    warn, danger, direction = THRESHOLDS[indicator]
    if direction == "lower_is_better":
        if value >= danger:
            return DANGER
        elif value >= warn:
            return WARNING
        else:
            return SAFE
    else:
        if value <= danger:
            return DANGER
        elif value <= warn:
            return WARNING
        else:
            return SAFE


def status_label(value, indicator):
    if indicator not in THRESHOLDS or pd.isna(value):
        return "No data"
    warn, danger, direction = THRESHOLDS[indicator]
    if direction == "lower_is_better":
        if value >= danger:
            return "🔴 Critical"
        elif value >= warn:
            return "🟡 Warning"
        else:
            return "🟢 Acceptable"
    else:
        if value <= danger:
            return "🔴 Critical"
        elif value <= warn:
            return "🟡 Warning"
        else:
            return "🟢 Acceptable"


def styled_ax(ax):
    ax.set_facecolor(BG)
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.grid(True, alpha=0.2, color=GRID)
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
    fsc = clean_base(food_security)
    fbc = clean_base(food_balances)
    hdc = clean_base(healthy_diet)

    def pivot(df, item_map):
        sel = df[df["Item"].isin(item_map.keys())].copy()
        sel["indicator"] = sel["Item"].map(item_map)
        wide = sel.pivot_table(index=KEYS, columns="indicator", values="Value", aggfunc="mean").reset_index()
        wide.columns.name = None
        return wide

    fsi_items = {
        "Average dietary energy supply adequacy (percent) (3-year average)": "dietary_energy_adequacy_pct",
        "Prevalence of undernourishment (percent) (3-year average)": "undernourishment_pct",
        "Number of people undernourished (million) (3-year average)": "undernourished_people_million",
        "Prevalence of severe food insecurity in the total population (percent) (3-year average)": "severe_food_insecurity_pct",
        "Prevalence of moderate or severe food insecurity in the total population (percent) (3-year average)": "moderate_or_severe_food_insecurity_pct",
        "Percentage of children under 5 years of age who are stunted (modelled estimates) (percent)": "under5_stunting_pct",
        "Percentage of children under 5 years affected by wasting (percent)": "under5_wasting_pct",
        "Gross domestic product per capita, PPP, (constant 2021 international $)": "gdp_per_capita_ppp",
    }
    cohd_items = {
        "Cost of a healthy diet (CoHD)": "healthy_diet_cost_ppp_per_day",
        "Prevalence of unaffordability (PUA)": "healthy_diet_unaffordable_pct",
        "Number of people unable to afford a healthy diet (NUA)": "people_unable_afford_healthy_diet_million",
    }

    fsi_wide = pivot(fsc, fsi_items)
    cohd_wide = pivot(hdc, cohd_items)

    def extract(item, element, name):
        return fbc[(fbc["Item"] == item) & (fbc["Element"] == element)][KEYS + ["Value"]].rename(columns={"Value": name})

    pop = extract("Population", "Total Population - Both sexes", "population_thousand")
    fs = extract("Grand Total", "Food supply (kcal/capita/day)", "food_supply_kcal_capita_day")
    ps = extract("Grand Total", "Protein supply quantity (g/capita/day)", "protein_supply_g_capita_day")
    fas = extract("Grand Total", "Fat supply quantity (g/capita/day)", "fat_supply_g_capita_day")

    fb = pop.merge(fs, on=KEYS, how="outer").merge(ps, on=KEYS, how="outer").merge(fas, on=KEYS, how="outer")
    df = fsi_wide.merge(fb, on=KEYS, how="outer").merge(cohd_wide, on=KEYS, how="outer")
    return df.sort_values("Year").reset_index(drop=True)


@st.cache_data
def build_county_data(jmr_data, jmr_pcodes, kenya_counties):
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
        indicators_at_critical=("max_alert_level", lambda s: int((s == 2).sum())),
        indicators_at_heightened=("max_alert_level", lambda s: int((s == 1).sum())),
    )
    summary["overall_alert_label"] = summary["overall_max_alert"].map(ALERT_LABELS)
    summary = summary.sort_values(["overall_max_alert", "total_critical_flags"], ascending=False)

    geo = kenya_counties.merge(summary, on="adm1_pcode", how="left")
    geo = gpd.GeoDataFrame(geo, geometry="geometry", crs=kenya_counties.crs)

    return county_alerts, summary, geo, latest_date
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "axes.edgecolor": GRID,
    "text.color": "white", "xtick.color": "white", "ytick.color": "white",
    "axes.labelcolor": "white", "axes.grid": True, "grid.alpha": 0.2,
    "grid.color": GRID, "legend.facecolor": BG, "legend.edgecolor": GRID,
    "legend.labelcolor": "white",
})

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #262730; color: white; border-radius: 4px 4px 0 0;
        padding: 8px 16px; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #e74c3c; color: white; }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px; padding: 20px; margin: 8px 0; border-left: 4px solid;
    }
    .story-box {
        background: #1a1a2e; border-radius: 8px; padding: 16px 20px;
        margin: 12px 0; border-left: 3px solid #3498db;
    }
    .danger-box {
        background: #2e1a1a; border-radius: 8px; padding: 16px 20px;
        margin: 12px 0; border-left: 3px solid #e74c3c;
    }
</style>
""", unsafe_allow_html=True)

st.title("🇰🇪 Food Security in Kenya — A Data Story")
st.markdown("*An analysis of national trends, county risk, and the affordability crisis threatening 43+ million Kenyans.*")
st.markdown("---")

with st.spinner("Loading data..."):
    food_security, food_balances, healthy_diet, jmr_data, jmr_pcodes, kenya_counties = load_all()
    analysis_df = build_analysis_df(food_security, food_balances, healthy_diet)
    county_alerts, county_risk_summary, county_geo_df, latest_alert_date = build_county_data(
        jmr_data, jmr_pcodes, kenya_counties
    )

with st.sidebar:
    st.header("📊 Dashboard Controls")
    st.markdown("---")
    st.markdown("### Status Legend")
    st.markdown(f"<span style='color:{SAFE}'>🟢 Acceptable</span> — Within safe range", unsafe_allow_html=True)
    st.markdown(f"<span style='color:{WARNING}'>🟡 Warning</span> — Needs attention", unsafe_allow_html=True)
    st.markdown(f"<span style='color:{DANGER}'>🔴 Critical</span> — Immediate action required", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### About the Data")
    st.markdown("""
    - **FAOSTAT**: UN FAO national statistics
    - **World Bank JMR**: County-level risk monitoring
    - **Coverage**: 2000–2025 (national), 2010–2026 (county)
    """)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Executive Summary", "🌾 Availability", "💰 Access & Affordability",
    "👶 Child Nutrition", "🗺️ County Risk Map",
])
# ═══════════════════════════════════════════════════════════════
# TAB 1: Executive Summary
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.header("Kenya's Food Security Crisis — At a Glance")
    st.markdown("""
    <div class="story-box">
    Kenya faces a <b>persistent food security crisis</b>. Despite economic growth, the majority of Kenyans
    cannot afford a healthy diet, and nearly 1 in 3 are undernourished. This dashboard tells the story
    through national trends, county risk maps, and diet affordability data.
    </div>
    """, unsafe_allow_html=True)

    key_indicators = [
        ("undernourishment_pct", "Undernourishment"),
        ("moderate_or_severe_food_insecurity_pct", "Food Insecurity"),
        ("healthy_diet_unaffordable_pct", "Cannot Afford Healthy Diet"),
        ("under5_stunting_pct", "Child Stunting"),
        ("dietary_energy_adequacy_pct", "Energy Adequacy"),
        ("undernourished_people_million", "People Undernourished"),
    ]

    cols = st.columns(3)
    for idx, (ind, title) in enumerate(key_indicators):
        row = analysis_df.dropna(subset=[ind]).sort_values("Year").tail(1)
        if row.empty:
            continue
        val = row[ind].iloc[0]
        year = int(row["Year"].iloc[0])
        meta = INDICATOR_META[ind]
        color = status_color(val, ind)
        status = status_label(val, ind)
        unit = meta["unit"]

        with cols[idx % 3]:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {color};">
                <h4 style="margin:0; color:{color};">{title}</h4>
                <h2 style="margin:4px 0; color:white;">{val:.1f} {unit}</h2>
                <p style="margin:0; color:{color}; font-size:0.85em;">{status}</p>
                <p style="margin:0; color:#888; font-size:0.75em;">Year: {year}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("The Big Picture: Food Security Over Two Decades")
    st.markdown("""
    <div class="danger-box">
    <b>Key insight:</b> While dietary energy adequacy has remained relatively stable (~92-97%),
    the <b>number of undernourished Kenyans has grown</b> from ~10 million (2002) to ~20 million (2025)
    — driven by population growth outpacing food system improvements.
    </div>
    """, unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    charts = [
        ("undernourished_people_million", "Undernourished People", "Million people"),
        ("moderate_or_severe_food_insecurity_pct", "Food Insecurity Rate", "% of population"),
        ("dietary_energy_adequacy_pct", "Dietary Energy Adequacy", "% of needs met"),
    ]
    for ax, (ind, title, ylabel) in zip(axes, charts):
        data = analysis_df[["Year", ind]].dropna()
        colors = [status_color(v, ind) for v in data[ind]]
        ax.bar(data["Year"], data[ind], color=colors, alpha=0.85, width=0.7)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Year")
        ax.set_ylabel(ylabel)
        for v in ax.get_yticklabels() + ax.get_xticklabels():
            v.set_color("white")
        styled_ax(ax)
        if ind in THRESHOLDS:
            warn, danger, direction = THRESHOLDS[ind]
            ax.axhline(y=warn, color=WARNING, linestyle="--", alpha=0.7, linewidth=1.2)
            ax.axhline(y=danger, color=DANGER, linestyle="--", alpha=0.7, linewidth=1.2)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    <div style="display:flex; gap:24px; justify-content:center; margin-top:-8px; flex-wrap:wrap;">
        <span style="color:{SAFE};">🟢 Acceptable</span>
        <span style="color:{WARNING};">🟡 Warning zone</span>
        <span style="color:{DANGER};">🔴 Critical zone</span>
        <span style="color:{WARNING};">--- Warning threshold</span>
        <span style="color:{DANGER};">--- Critical threshold</span>
    </div>
    """, unsafe_allow_html=True)
# ═══════════════════════════════════════════════════════════════
# TAB 2: Availability
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.header("🌾 Availability — Is There Enough Food?")
    st.markdown("""
    <div class="story-box">
    <b>What this measures:</b> Whether Kenya produces or imports enough food to meet its population's
    nutritional needs. We track calories, protein, and fat available per person per day, plus the
    overall dietary energy adequacy — the percentage of calorie needs met by the food supply.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Dietary Energy Supply Adequacy")
    st.markdown("""
    This is the **percentage of the population's daily calorie needs** that are met by the domestic food supply.
    A value of 100% means supply exactly meets demand. Below 100% means Kenya relies on imports or aid.
    """)

    fig, ax = plt.subplots(figsize=(14, 5))
    data = analysis_df[["Year", "dietary_energy_adequacy_pct"]].dropna()
    colors = [status_color(v, "dietary_energy_adequacy_pct") for v in data["dietary_energy_adequacy_pct"]]
    ax.bar(data["Year"], data["dietary_energy_adequacy_pct"], color=colors, alpha=0.85, width=0.7)
    ax.axhline(y=100, color=SAFE, linestyle="-", alpha=0.5, linewidth=1.5, label="100% target")
    ax.axhline(y=95, color=WARNING, linestyle="--", alpha=0.7, linewidth=1.2, label="95% warning")
    ax.axhline(y=90, color=DANGER, linestyle="--", alpha=0.7, linewidth=1.2, label="90% critical")
    ax.set_title("Dietary Energy Supply Adequacy — Kenya", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("% of calorie needs met")
    ax.set_ylim(85, 105)
    ax.legend(loc="lower right", facecolor=BG, edgecolor=GRID, labelcolor="white")
    for v in ax.get_yticklabels() + ax.get_xticklabels():
        v.set_color("white")
    styled_ax(ax)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    <div class="danger-box">
    <b>⚠️ Insight:</b> Kenya's energy adequacy has hovered around <b>92-97%</b> — consistently below the 100% target.
    This means Kenya's domestic food supply <b>does not fully meet</b> its population's calorie needs.
    The gap is filled through imports and food aid, making Kenya vulnerable to global price shocks.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Food Supply Breakdown (per person per day)")
    st.markdown("""
    These three metrics show the actual nutritional content available per Kenyan per day.
    Recommended minimums: **2,100 kcal**, **50g protein**, **40g fat**.
    """)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    supply_charts = [
        ("food_supply_kcal_capita_day", "Calories", "kcal/day", 2100, 1800),
        ("protein_supply_g_capita_day", "Protein", "g/day", 50, 40),
        ("fat_supply_g_capita_day", "Fat", "g/day", 40, 30),
    ]
    for ax, (ind, title, unit, warn_val, danger_val) in zip(axes, supply_charts):
        data = analysis_df[["Year", ind]].dropna()
        colors = [status_color(v, ind) for v in data[ind]]
        ax.plot(data["Year"], data[ind], color=NEUTRAL, linewidth=2, marker="o", markersize=4)
        ax.scatter(data["Year"], data[ind], color=colors, s=40, zorder=5)
        ax.axhline(y=warn_val, color=WARNING, linestyle="--", alpha=0.7, linewidth=1.2)
        ax.axhline(y=danger_val, color=DANGER, linestyle="--", alpha=0.7, linewidth=1.2)
        ax.fill_between(data["Year"], data[ind], warn_val,
                        where=data[ind] < warn_val, alpha=0.15, color=DANGER)
        ax.set_title(f"{title} Supply", fontsize=12, fontweight="bold")
        ax.set_xlabel("Year")
        ax.set_ylabel(unit)
        for v in ax.get_yticklabels() + ax.get_xticklabels():
            v.set_color("white")
        styled_ax(ax)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    <div style="display:flex; gap:24px; justify-content:center; flex-wrap:wrap;">
        <span style="color:{SAFE};">🟢 Above warning = Acceptable</span>
        <span style="color:{WARNING};">🟡 Below warning = Concerning</span>
        <span style="color:{DANGER};">🔴 Below critical = Danger</span>
        <span style="color:{WARNING};">--- Warning threshold</span>
        <span style="color:{DANGER};">--- Critical threshold</span>
    </div>
    """, unsafe_allow_html=True)
# ═══════════════════════════════════════════════════════════════
# TAB 3: Access & Affordability
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.header("💰 Access & Affordability — Can People Afford Food?")
    st.markdown("""
    <div class="story-box">
    <b>What this measures:</b> Whether Kenyans can physically and economically access the food they need.
    This is the most critical dimension — even when food is available, poverty prevents people from affording it.
    Kenya's healthy diet costs ~$3.20/day (international dollars), but 76% of the population cannot afford it.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Prevalence of Undernourishment")
    st.markdown("""
    The percentage of Kenya's population that **consistently fails to meet their daily calorie requirements**.
    WHO thresholds: <15% = acceptable, 15-25% = warning, >25% = critical.
    """)

    fig, ax = plt.subplots(figsize=(14, 5))
    data = analysis_df[["Year", "undernourishment_pct"]].dropna()
    colors = [status_color(v, "undernourishment_pct") for v in data["undernourishment_pct"]]
    ax.fill_between(data["Year"], data["undernourishment_pct"], alpha=0.3, color=DANGER)
    ax.bar(data["Year"], data["undernourishment_pct"], color=colors, alpha=0.85, width=0.7)
    ax.axhline(y=15, color=WARNING, linestyle="--", alpha=0.7, linewidth=1.2, label="15% warning")
    ax.axhline(y=25, color=DANGER, linestyle="--", alpha=0.7, linewidth=1.2, label="25% critical")
    ax.set_title("Undernourishment Rate — Kenya", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("% of population")
    ax.legend(loc="upper right", facecolor=BG, edgecolor=GRID, labelcolor="white")
    for v in ax.get_yticklabels() + ax.get_xticklabels():
        v.set_color("white")
    styled_ax(ax)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    <div class="danger-box">
    <b>🔴 Critical finding:</b> Kenya's undernourishment rate has <b>never dropped below 25%</b> in recorded data.
    It peaked at ~34-36% in recent years. This means <b>at least 1 in 4 Kenyans</b> consistently
    does not get enough food — a persistent crisis-level situation.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Food Insecurity Severity")
    st.markdown("""
    Food insecurity is measured on a spectrum:
    - **Moderate/Severe**: People who worry about food, are forced to eat less, or skip meals
    - **Severe**: People who go entire days without eating
    """)

    fig, ax = plt.subplots(figsize=(14, 5))
    mod_data = analysis_df[["Year", "moderate_or_severe_food_insecurity_pct"]].dropna()
    sev_data = analysis_df[["Year", "severe_food_insecurity_pct"]].dropna()

    ax.fill_between(mod_data["Year"], mod_data["moderate_or_severe_food_insecurity_pct"],
                    alpha=0.2, color=WARNING, label="Moderate/Severe range")
    ax.plot(mod_data["Year"], mod_data["moderate_or_severe_food_insecurity_pct"],
            color=WARNING, linewidth=2.5, marker="o", markersize=5, label="Moderate or Severe")
    ax.plot(sev_data["Year"], sev_data["severe_food_insecurity_pct"],
            color=DANGER, linewidth=2.5, marker="s", markersize=5, label="Severe only")

    ax.axhline(y=40, color=WARNING, linestyle="--", alpha=0.5, linewidth=1)
    ax.axhline(y=60, color=DANGER, linestyle="--", alpha=0.5, linewidth=1)
    ax.text(mod_data["Year"].iloc[1], 41, "Warning (40%)", color=WARNING, fontsize=9)
    ax.text(mod_data["Year"].iloc[1], 61, "Critical (60%)", color=DANGER, fontsize=9)

    ax.set_title("Food Insecurity Rates — Kenya", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("% of population")
    ax.legend(loc="upper right", facecolor=BG, edgecolor=GRID, labelcolor="white")
    for v in ax.get_yticklabels() + ax.get_xticklabels():
        v.set_color("white")
    styled_ax(ax)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    <div class="danger-box">
    <b>🔴 Alarming:</b> Over <b>70% of Kenyans</b> experience moderate or severe food insecurity,
    and ~28% experience <b>severe</b> food insecurity — going entire days without eating.
    This is not a marginal issue; it affects the <b>majority of the population</b>.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("The Affordability Crisis")
    st.markdown("""
    A **healthy diet** includes fruits, vegetables, protein, and whole grains — not just staple calories.
    In Kenya, this costs ~$3.20/day (international dollars). The charts below show how cost and
    unaffordability have worsened over time.
    """)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    afford_charts = [
        ("healthy_diet_cost_ppp_per_day", "Cost of Healthy Diet", "Int$/day", 3.5, 5.0),
        ("healthy_diet_unaffordable_pct", "Cannot Afford Healthy Diet", "% of population", 50, 70),
        ("people_unable_afford_healthy_diet_million", "People Unable to Afford", "Million people", 20, 35),
    ]
    for ax, (ind, title, unit, warn_val, danger_val) in zip(axes, afford_charts):
        data = analysis_df[["Year", ind]].dropna()
        colors = [status_color(v, ind) for v in data[ind]]
        ax.bar(data["Year"], data[ind], color=colors, alpha=0.85, width=0.7)
        ax.axhline(y=warn_val, color=WARNING, linestyle="--", alpha=0.7, linewidth=1.2)
        ax.axhline(y=danger_val, color=DANGER, linestyle="--", alpha=0.7, linewidth=1.2)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Year")
        ax.set_ylabel(unit)
        for v in ax.get_yticklabels() + ax.get_xticklabels():
            v.set_color("white")
        styled_ax(ax)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    <div class="danger-box">
    <b>🔴 The bottom line:</b> <b>43+ million Kenyans</b> (76% of the population) cannot afford a healthy diet.
    They rely on cheap, nutrient-poor staples like maize and ugali — which explains why child stunting
    remains high despite adequate calorie supply. <b>Availability without access is not food security.</b>
    </div>
    """, unsafe_allow_html=True)
# ═══════════════════════════════════════════════════════════════
# TAB 4: Child Nutrition
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.header("👶 Child Nutrition — The Human Cost")
    st.markdown("""
    <div class="story-box">
    <b>What this measures:</b> The impact of food insecurity on children under 5 years old.
    <b>Stunting</b> (too short for age) indicates chronic malnutrition — long-term nutrient deficiency.
    <b>Wasting</b> (dangerously thin) indicates acute malnutrition — recent severe food shortage.
    Both cause irreversible physical and cognitive damage.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Child Stunting & Wasting Trends")
    st.markdown("""
    **WHO thresholds:**
    - Stunting: <20% = acceptable, 20-30% = warning, >30% = very high (critical)
    - Wasting: <5% = acceptable, 5-15% = warning, >15% = critical
    """)

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    st_data = analysis_df[["Year", "under5_stunting_pct"]].dropna()
    st_colors = [status_color(v, "under5_stunting_pct") for v in st_data["under5_stunting_pct"]]
    axes[0].bar(st_data["Year"], st_data["under5_stunting_pct"], color=st_colors, alpha=0.85, width=0.7)
    axes[0].axhline(y=20, color=WARNING, linestyle="--", alpha=0.7, linewidth=1.2, label="20% warning")
    axes[0].axhline(y=30, color=DANGER, linestyle="--", alpha=0.7, linewidth=1.2, label="30% critical")
    axes[0].set_title("Child Stunting (Under-5)\nChronic Malnutrition", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("% of children")
    axes[0].legend(loc="upper right", facecolor=BG, edgecolor=GRID, labelcolor="white")
    for v in axes[0].get_yticklabels() + axes[0].get_xticklabels():
        v.set_color("white")
    styled_ax(axes[0])

    wa_data = analysis_df[["Year", "under5_wasting_pct"]].dropna()
    wa_colors = [status_color(v, "under5_wasting_pct") for v in wa_data["under5_wasting_pct"]]
    axes[1].bar(wa_data["Year"], wa_data["under5_wasting_pct"], color=wa_colors, alpha=0.85, width=0.7)
    axes[1].axhline(y=5, color=WARNING, linestyle="--", alpha=0.7, linewidth=1.2, label="5% warning")
    axes[1].axhline(y=15, color=DANGER, linestyle="--", alpha=0.7, linewidth=1.2, label="15% critical")
    axes[1].set_title("Child Wasting (Under-5)\nAcute Malnutrition", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Year")
    axes[1].set_ylabel("% of children")
    axes[1].legend(loc="upper right", facecolor=BG, edgecolor=GRID, labelcolor="white")
    for v in axes[1].get_yticklabels() + axes[1].get_xticklabels():
        v.set_color("white")
    styled_ax(axes[1])

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    <div class="danger-box">
    <b>🔴 The human cost:</b> Stunting has improved from ~38% (2000) to ~18% (2024) — significant progress.
    But it remains in the <b>warning zone</b>, meaning nearly 1 in 5 Kenyan children suffer irreversible
    growth and cognitive impairment from chronic malnutrition. Wasting fluctuates with drought cycles
    and remains a persistent threat.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Economic Context — GDP per Capita")
    st.markdown("""
    Economic growth should theoretically improve food access. Kenya's GDP per capita (PPP) has grown
    from ~$3,700 (2000) to ~$5,800 (2024), but food insecurity has worsened — showing that
    <b>growth alone does not solve food insecurity</b> without equitable distribution.
    """)

    fig, ax = plt.subplots(figsize=(14, 5))
    data = analysis_df[["Year", "gdp_per_capita_ppp"]].dropna()
    ax.plot(data["Year"], data["gdp_per_capita_ppp"], color=NEUTRAL, linewidth=2.5, marker="o", markersize=5)
    ax.fill_between(data["Year"], data["gdp_per_capita_ppp"], alpha=0.15, color=NEUTRAL)
    ax.axhline(y=3000, color=WARNING, linestyle="--", alpha=0.7, linewidth=1.2, label="$3,000 warning")
    ax.set_title("GDP per Capita (PPP, constant 2021 Int$) — Kenya", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP per capita (Int$)")
    ax.legend(loc="upper left", facecolor=BG, edgecolor=GRID, labelcolor="white")
    for v in ax.get_yticklabels() + ax.get_xticklabels():
        v.set_color("white")
    styled_ax(ax)
    plt.tight_layout()
    st.pyplot(fig)
# ═══════════════════════════════════════════════════════════════
# TAB 5: County Risk Map
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.header("🗺️ County Risk Map — Where Is the Crisis Worst?")
    st.markdown(f"""
    <div class="story-box">
    The World Bank's Joint Monitoring Report (JMR) tracks food security risk at the sub-county level
    across 7 indicators: Conflict, Drought (NDVI), Drought (rainfall), Exchange rates, Food prices,
    and volatility in exchange rates and food prices. Latest data: <b>{latest_alert_date.date()}</b>.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("County Risk Ranking")
    st.markdown("""
    Alert levels: 🟢 **Typical** (0) | 🟡 **Heightened** (1) | 🔴 **Critical** (2)
    """)

    col1, col2 = st.columns([2, 1])

    with col1:
        top = county_risk_summary.head(15)
        fig, ax = plt.subplots(figsize=(10, 7))
        bar_colors = [ALERT_COLORS.get(a, NEUTRAL) for a in top["overall_max_alert"]]
        ax.barh(top["adm1_name"], top["total_critical_flags"], color=DANGER, alpha=0.85, label="Critical flags")
        ax.barh(top["adm1_name"], top["total_heightened_flags"], left=top["total_critical_flags"],
                color=WARNING, alpha=0.85, label="Heightened flags")
        ax.set_title(f"Top 15 Highest-Risk Counties ({latest_alert_date.date()})", fontsize=12, fontweight="bold")
        ax.set_xlabel("Number of sub-county alerts")
        ax.set_ylabel("County")
        ax.legend(loc="lower right", facecolor=BG, edgecolor=GRID, labelcolor="white")
        ax.invert_yaxis()
        for v in ax.get_yticklabels() + ax.get_xticklabels():
            v.set_color("white")
        styled_ax(ax)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.markdown("### Alert Summary")
        alert_counts = county_risk_summary["overall_alert_label"].value_counts()
        for label, color in [("Critical", DANGER), ("Heightened", WARNING), ("Typical", SAFE)]:
            count = alert_counts.get(label, 0)
            st.markdown(f"<div style='color:{color}; font-size:1.1em;'><b>{label}:</b> {count} counties</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Most Affected Counties")
        for _, row in county_risk_summary.head(5).iterrows():
            alert_color = ALERT_COLORS.get(row["overall_max_alert"], NEUTRAL)
            st.markdown(f"<span style='color:{alert_color};'>●</span> **{row['adm1_name']}** — {row['overall_alert_label']}", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("County × Indicator Heatmap")
    st.markdown("""
    This heatmap shows the **maximum alert level** for each county across all JMR indicators.
    Red = at least one sub-county in that county reached critical level for that indicator.
    """)

    matrix = county_alerts.pivot_table(
        index=["adm1_pcode", "adm1_name"],
        columns="indicator",
        values="max_alert_level",
        aggfunc="max",
    ).reset_index()
    matrix.columns.name = None

    hm_data = matrix.set_index("adm1_name").drop(columns="adm1_pcode")
    hm_data = hm_data.loc[county_risk_summary["adm1_name"]]
    hm_data = hm_data.astype(float)

    fig, ax = plt.subplots(figsize=(12, 14))
    cmap = sns.color_palette([SAFE, WARNING, DANGER], as_cmap=True)
    sns.heatmap(
        hm_data, cmap=cmap, vmin=0, vmax=2,
        linewidths=0.4, linecolor="white",
        cbar_kws={"ticks": [0, 1, 2], "label": "Alert level"},
        ax=ax,
    )
    ax.set_title(f"JMR Alert Levels by County ({latest_alert_date.date()})", fontsize=12, fontweight="bold")
    ax.set_xlabel("Indicator")
    ax.set_ylabel("County")
    for v in ax.get_yticklabels() + ax.get_xticklabels():
        v.set_color("white")
    ax.set_facecolor(BG)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"""
    <div style="display:flex; gap:24px; justify-content:center; flex-wrap:wrap;">
        <span style="color:{SAFE};">🟢 Typical (0)</span>
        <span style="color:{WARNING};">🟡 Heightened (1)</span>
        <span style="color:{DANGER};">🔴 Critical (2)</span>
    </div>
    """, unsafe_allow_html=True)
