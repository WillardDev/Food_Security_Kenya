import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Food Security in Kenya",
    page_icon=":bar_chart:",
    layout="wide",
)

SAFE = "#2ecc71"
WARNING = "#f39c12"
DANGER = "#e74c3c"
NEUTRAL = "#3498db"

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
    "dietary_energy_adequacy_pct":      {"label": "Dietary Energy Supply Adequacy", "unit": "%", "tip": "% of population calorie needs met by domestic supply"},
    "food_supply_kcal_capita_day":      {"label": "Food Supply", "unit": "kcal/day", "tip": "Average calories available per person per day"},
    "protein_supply_g_capita_day":      {"label": "Protein Supply", "unit": "g/day", "tip": "Average protein available per person per day"},
    "fat_supply_g_capita_day":          {"label": "Fat Supply", "unit": "g/day", "tip": "Average fat available per person per day"},
    "undernourishment_pct":             {"label": "Prevalence of Undernourishment", "unit": "%", "tip": "% of population consistently unable to meet calorie needs"},
    "undernourished_people_million":    {"label": "People Undernourished", "unit": "million", "tip": "Total number of undernourished people"},
    "severe_food_insecurity_pct":       {"label": "Severe Food Insecurity", "unit": "%", "tip": "% of population who went entire days without eating"},
    "moderate_or_severe_food_insecurity_pct": {"label": "Moderate/Severe Food Insecurity", "unit": "%", "tip": "% of population experiencing food anxiety or meal-skipping"},
    "under5_stunting_pct":              {"label": "Child Stunting (Under-5)", "unit": "%", "tip": "% of children too short for their age (chronic malnutrition)"},
    "under5_wasting_pct":               {"label": "Child Wasting (Under-5)", "unit": "%", "tip": "% of children dangerously thin (acute malnutrition)"},
    "healthy_diet_cost_ppp_per_day":    {"label": "Healthy Diet Cost", "unit": "Int$/day", "tip": "Cost of a nutritious diet per person per day"},
    "healthy_diet_unaffordable_pct":    {"label": "Cannot Afford Healthy Diet", "unit": "%", "tip": "% of population who cannot afford a healthy diet"},
    "people_unable_afford_healthy_diet_million": {"label": "People Unable to Afford", "unit": "million", "tip": "Total people who cannot afford a healthy diet"},
    "gdp_per_capita_ppp":               {"label": "GDP per Capita", "unit": "Int$", "tip": "Economic output per person, adjusted for local prices"},
}


def status_color(value, indicator):
    if indicator not in THRESHOLDS or pd.isna(value):
        return NEUTRAL
    warn, danger, direction = THRESHOLDS[indicator]
    if direction == "lower_is_better":
        if value >= danger: return DANGER
        elif value >= warn: return WARNING
        else: return SAFE
    else:
        if value <= danger: return DANGER
        elif value <= warn: return WARNING
        else: return SAFE


def status_label(value, indicator):
    if indicator not in THRESHOLDS or pd.isna(value):
        return "No data"
    warn, danger, direction = THRESHOLDS[indicator]
    if direction == "lower_is_better":
        if value >= danger: return "Critical"
        elif value >= warn: return "Warning"
        else: return "Acceptable"
    else:
        if value <= danger: return "Critical"
        elif value <= warn: return "Warning"
        else: return "Acceptable"


def insight_text(indicator, value, year):
    if indicator not in THRESHOLDS or pd.isna(value):
        return "No data available."
    warn, danger, direction = THRESHOLDS[indicator]
    if direction == "lower_is_better":
        severity = "critical" if value >= danger else ("warning" if value >= warn else "acceptable")
    else:
        severity = "critical" if value <= danger else ("warning" if value <= warn else "acceptable")

    texts = {
        "dietary_energy_adequacy_pct": {
            "critical": f"In {year}, Kenya domestic food supply met only {value:.1f}% of calorie needs. The country depends on imports and aid, making it highly vulnerable to global price shocks and supply chain disruptions.",
            "warning": f"At {value:.1f}%, energy adequacy is below the 100% target. Kenya consistently fails to produce enough food for its population and relies on imports to fill the gap.",
            "acceptable": f"At {value:.1f}%, food supply adequately meets population needs.",
        },
        "undernourishment_pct": {
            "critical": f"{value:.1f}% of Kenyans, roughly 1 in {int(100/value)}, are chronically undernourished in {year}. This is a persistent humanitarian crisis requiring systemic intervention in food production, distribution, and affordability.",
            "warning": f"At {value:.1f}%, undernourishment remains in the warning zone. Millions of Kenyans experience chronic hunger that impairs health, productivity, and child development.",
            "acceptable": f"At {value:.1f}%, undernourishment is within manageable levels but still affects vulnerable populations.",
        },
        "moderate_or_severe_food_insecurity_pct": {
            "critical": f"Over {value:.0f}% of Kenyans experienced food insecurity in {year}. The majority of the population regularly worries about food or skips meals. This is a societal crisis affecting more than 3 in 4 people.",
            "warning": f"At {value:.0f}%, food insecurity affects a staggering portion of the population. Food anxiety and meal-skipping have become normalized experiences for most Kenyan households.",
            "acceptable": f"At {value:.0f}%, food insecurity affects a portion of the population but is not yet widespread.",
        },
        "severe_food_insecurity_pct": {
            "critical": f"{value:.1f}% of Kenyans went entire days without eating in {year}. This is extreme deprivation, people experiencing 24+ hours of zero food intake. Immediate food assistance is required.",
            "warning": f"At {value:.1f}%, severe food deprivation affects millions. Going a full day without food causes acute physical and psychological harm.",
            "acceptable": f"At {value:.1f}%, severe food deprivation is relatively contained.",
        },
        "under5_stunting_pct": {
            "critical": f"{value:.1f}% of Kenyan children under 5 are stunted, too short for their age due to chronic malnutrition. Stunting causes irreversible brain and body damage that limits these children potential for life.",
            "warning": f"At {value:.1f}%, nearly 1 in 5 children suffer chronic malnutrition with lifelong consequences for health and cognitive development.",
            "acceptable": f"At {value:.1f}%, stunting has improved significantly but remains a concern for vulnerable communities.",
        },
        "healthy_diet_unaffordable_pct": {
            "critical": f"{value:.0f}% of Kenyans cannot afford a healthy diet. They rely on cheap, nutrient-poor staples like maize and ugali, which explains high stunting despite adequate calorie supply.",
            "warning": f"At {value:.0f}%, the majority cannot afford nutritious food. Cheap staples dominate, leading to hidden hunger and micronutrient deficiencies.",
            "acceptable": f"At {value:.0f}%, a significant portion still struggles to afford nutritious food.",
        },
    }
    return texts.get(indicator, {}).get(severity, f"Value: {value:.1f} ({severity})")

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
    return county_alerts, summary, geo, latest_date


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
        margin: 12px 0; border-left: 3px solid #3498db; color: #ddd; line-height: 1.6;
    }
    .danger-box {
        background: #2e1a1a; border-radius: 8px; padding: 16px 20px;
        margin: 12px 0; border-left: 3px solid #e74c3c; color: #ddd; line-height: 1.6;
    }
    .success-box {
        background: #1a2e1a; border-radius: 8px; padding: 16px 20px;
        margin: 12px 0; border-left: 3px solid #2ecc71; color: #ddd; line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

st.title("Food Security in Kenya - A Data Story")
st.markdown("*An interactive analysis of national trends, county risk, and the affordability crisis threatening 43+ million Kenyans.*")
st.markdown("---")

with st.spinner("Loading data..."):
    food_security, food_balances, healthy_diet, jmr_data, jmr_pcodes, kenya_counties = load_all()
    analysis_df = build_analysis_df(food_security, food_balances, healthy_diet)
    county_alerts, county_risk_summary, county_geo_df, latest_alert_date = build_county_data(
        jmr_data, jmr_pcodes, kenya_counties
    )

with st.sidebar:
    st.header("Dashboard Controls")
    st.markdown("---")
    st.markdown("### Status Legend")
    st.markdown(f"<span style=\"color:{SAFE}\">Acceptable</span> - Within safe range", unsafe_allow_html=True)
    st.markdown(f"<span style=\"color:{WARNING}\">Warning</span> - Needs attention", unsafe_allow_html=True)
    st.markdown(f"<span style=\"color:{DANGER}\">Critical</span> - Immediate action required", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### About the Data")
    st.markdown("- **FAOSTAT**: UN FAO national statistics\n- **World Bank JMR**: County-level risk monitoring\n- **Coverage**: 2000-2025 (national), 2010-2026 (county)")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Summary", "Availability", "Access and Affordability",
    "Child Nutrition", "County Risk Map",
])

# TAB 1: Executive Summary
with tab1:
    st.header("Kenya Food Security Crisis - At a Glance")
    st.markdown("""
    <div class="story-box">
    Kenya faces a <b>persistent, multi-dimensional food security crisis</b>. Despite steady economic growth over two decades,
    the majority of Kenyans cannot afford a healthy diet, and nearly 1 in 3 are undernourished. This dashboard tells the story
    through interactive national trends, county risk maps, and diet affordability data.<br><br>
    <b>How to read this dashboard:</b> Every chart uses a consistent color system:
    <span style=\"color:#2ecc71\">green for acceptable</span>,
    <span style=\"color:#f39c12\">yellow for warning</span>, and
    <span style=\"color:#e74c3c\">red for critical</span>.
    Hover over any data point for detailed values and insights.
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
        color = status_color(val, ind)
        status = status_label(val, ind)
        unit = INDICATOR_META[ind]["unit"]

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
    st.subheader("The Big Picture: Two Decades of Food Security")

    # Interactive (non-animated) bar chart
    df_melted = analysis_df.melt(
        id_vars="Year",
        value_vars=["undernourished_people_million", "moderate_or_severe_food_insecurity_pct", "dietary_energy_adequacy_pct"],
        var_name="Indicator", value_name="Value"
    ).dropna()
    df_melted["Indicator"] = df_melted["Indicator"].map({
        "undernourished_people_million": "Undernourished (million)",
        "moderate_or_severe_food_insecurity_pct": "Food Insecurity (%)",
        "dietary_energy_adequacy_pct": "Energy Adequacy (%)",
    })

    fig = px.bar(
        df_melted, x="Year", y="Value", color="Indicator",
        barmode="group",
        title="Key Food Security Indicators Over Time (2000-2025)",
        labels={"Value": "Value", "Year": "Year"},
        color_discrete_map={
            "Undernourished (million)": DANGER,
            "Food Insecurity (%)": WARNING,
            "Energy Adequacy (%)": SAFE,
        },
        height=500,
    )
    fig.update_traces(hovertemplate="<b>Year %{x}</b><br>%{data.name}: %{y:.1f}<extra></extra>")
    fig.update_layout(
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
        font_color="white", legend_font_color="white",
        xaxis=dict(gridcolor="#262730"), yaxis=dict(gridcolor="#262730"),
    )
    st.plotly_chart(fig, use_container_width=True)

    latest_row = analysis_df.sort_values("Year").tail(1)
    year = int(latest_row["Year"].iloc[0])
    undernourishment = latest_row["undernourishment_pct"].iloc[0]
    food_insec = latest_row["moderate_or_severe_food_insecurity_pct"].iloc[0]
    st.markdown(f"""
    <div class="danger-box">
    <b>Key insight:</b> In {year}, <b>{food_insec:.0f}% of Kenyans</b> experienced food insecurity while
    <b>{undernourishment:.1f}% were undernourished</b>. The number of undernourished people has grown from
    ~10 million (2002) to ~20 million (2025), driven by population growth outpacing food system improvements.
    Even as GDP grew from $3,700 to $5,800 per capita, food insecurity worsened.
    <b>Economic growth alone has not solved Kenya food crisis.</b>
    </div>
    """, unsafe_allow_html=True)

# TAB 2: Availability
with tab2:
    st.header("Availability - Is There Enough Food?")
    st.markdown("""
    <div class="story-box">
    <b>What this measures:</b> Whether Kenya produces or imports enough food to meet its population
    nutritional needs. We track calories, protein, and fat available per person per day, plus the
    overall dietary energy adequacy, the percentage of calorie needs met by the food supply.<br><br>
    <b>Why this matters:</b> If a country cannot produce enough food, it must import the rest.
    Import dependence creates vulnerability to global price shocks, currency fluctuations, and supply chain disruptions.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Dietary Energy Supply Adequacy")
    st.markdown("""
    This is the **percentage of the population daily calorie needs** that are met by the domestic food supply.
    A value of 100% means supply exactly meets demand. Below 100% means Kenya relies on imports or aid.
    """)

    data = analysis_df[["Year", "dietary_energy_adequacy_pct"]].dropna()
    data["Color"] = data["dietary_energy_adequacy_pct"].apply(lambda v: status_color(v, "dietary_energy_adequacy_pct"))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data["Year"], y=data["dietary_energy_adequacy_pct"],
        marker_color=data["Color"],
        text=data["dietary_energy_adequacy_pct"].round(1),
        textposition="outside",
        textfont_color="white",
        hovertemplate="<b>Year %{x}</b><br>Energy Adequacy: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=100, line_dash="solid", line_color=SAFE, line_width=2, annotation_text="100% target", annotation_position="top left", annotation_font_color=SAFE)
    fig.add_hline(y=95, line_dash="dash", line_color=WARNING, line_width=1.5, annotation_text="95% warning", annotation_position="top left", annotation_font_color=WARNING)
    fig.add_hline(y=90, line_dash="dash", line_color=DANGER, line_width=1.5, annotation_text="90% critical", annotation_position="top left", annotation_font_color=DANGER)
    fig.update_layout(
        title="Dietary Energy Supply Adequacy - Kenya",
        xaxis_title="Year", yaxis_title="% of calorie needs met",
        yaxis_range=[85, 105],
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
        font_color="white",
        xaxis=dict(gridcolor="#262730"), yaxis=dict(gridcolor="#262730"),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

    val = data["dietary_energy_adequacy_pct"].iloc[-1]
    year = int(data["Year"].iloc[-1])
    st.markdown(f"""
    <div class="danger-box">
    {insight_text("dietary_energy_adequacy_pct", val, year)}
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Food Supply Breakdown (per person per day)")
    st.markdown("""
    These three metrics show the actual nutritional content available per Kenyan per day.
    Recommended minimums: **2,100 kcal**, **50g protein**, **40g fat**.
    """)

    fig2 = make_subplots(rows=1, cols=3, subplot_titles=("Calories (kcal/day)", "Protein (g/day)", "Fat (g/day)"))

    supply_data = [
        ("food_supply_kcal_capita_day", 2100, 1800),
        ("protein_supply_g_capita_day", 50, 40),
        ("fat_supply_g_capita_day", 40, 30),
    ]
    for i, (ind, warn_val, danger_val) in enumerate(supply_data):
        d = analysis_df[["Year", ind]].dropna()
        d["Color"] = d[ind].apply(lambda v: status_color(v, ind))
        fig2.add_trace(
            go.Scatter(x=d["Year"], y=d[ind], mode="lines+markers",
                       marker=dict(color=d["Color"], size=8),
                       line=dict(color=NEUTRAL, width=2),
                       name=INDICATOR_META[ind]["label"],
                       hovertemplate=f"<b>Year %{{x}}</b><br>{INDICATOR_META[ind]['label']}: %{{y:.1f}} {INDICATOR_META[ind]['unit']}<extra></extra>"),
            row=1, col=i+1
        )
        fig2.add_hline(y=warn_val, line_dash="dash", line_color=WARNING, line_width=1, row=1, col=i+1)
        fig2.add_hline(y=danger_val, line_dash="dash", line_color=DANGER, line_width=1, row=1, col=i+1)

    fig2.update_layout(
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
        font_color="white", showlegend=False, height=450,
    )
    fig2.update_xaxes(gridcolor="#262730")
    fig2.update_yaxes(gridcolor="#262730")
    st.plotly_chart(fig2, use_container_width=True)

# TAB 3: Access and Affordability
with tab3:
    st.header("Access and Affordability - Can People Afford Food?")
    st.markdown("""
    <div class="story-box">
    <b>What this measures:</b> Whether Kenyans can physically and economically access the food they need.
    This is the most critical dimension. Even when food is available, poverty prevents people from affording it.
    Kenya healthy diet costs ~$3.20/day (international dollars), but 76% of the population cannot afford it.<br><br>
    <b>The paradox:</b> Kenya has adequate calorie supply (~93% of needs met) yet most people are food insecure.
    The problem is not scarcity, it is poverty and affordability.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Prevalence of Undernourishment")
    st.markdown("""
    The percentage of Kenya population that **consistently fails to meet their daily calorie requirements**.
    WHO thresholds: <15% = acceptable, 15-25% = warning, >25% = critical.
    """)

    data = analysis_df[["Year", "undernourishment_pct"]].dropna()
    data["Color"] = data["undernourishment_pct"].apply(lambda v: status_color(v, "undernourishment_pct"))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data["Year"], y=data["undernourishment_pct"],
        marker_color=data["Color"],
        text=data["undernourishment_pct"].round(1),
        textposition="outside",
        textfont_color="white",
        hovertemplate="<b>Year %{x}</b><br>Undernourishment: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=15, line_dash="dash", line_color=WARNING, annotation_text="15% warning", annotation_position="top left", annotation_font_color=WARNING)
    fig.add_hline(y=25, line_dash="dash", line_color=DANGER, annotation_text="25% critical", annotation_position="top left", annotation_font_color=DANGER)
    fig.update_layout(
        title="Undernourishment Rate - Kenya",
        xaxis_title="Year", yaxis_title="% of population",
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="white",
        xaxis=dict(gridcolor="#262730"), yaxis=dict(gridcolor="#262730"),
        height=500,
    )
    st.image(fig, use_container_width=True) if False else st.plotly_chart(fig, use_container_width=True)

    val = data["undernourishment_pct"].iloc[-1]
    year = int(data["Year"].iloc[-1])
    st.markdown(f"""
    <div class="danger-box">
    {insight_text("undernourishment_pct", val, year)}
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Food Insecurity Severity")
    st.markdown("""
    Food insecurity exists on a spectrum:
    - **Moderate/Severe**: People who worry about food, are forced to eat less, or skip meals
    - **Severe**: People who go entire days without eating
    """)

    mod_data = analysis_df[["Year", "moderate_or_severe_food_insecurity_pct"]].dropna()
    sev_data = analysis_df[["Year", "severe_food_insecurity_pct"]].dropna()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=mod_data["Year"], y=mod_data["moderate_or_severe_food_insecurity_pct"],
        mode="lines+markers", name="Moderate or Severe",
        line=dict(color=WARNING, width=3), marker=dict(size=8),
        fill="tozeroy", fillcolor="rgba(243,156,18,0.1)",
        hovertemplate="<b>Year %{x}</b><br>Moderate/Severe: %{y:.1f}%<extra></extra>",
    ))
    fig2.add_trace(go.Scatter(
        x=sev_data["Year"], y=sev_data["severe_food_insecurity_pct"],
        mode="lines+markers", name="Severe Only",
        line=dict(color=DANGER, width=3), marker=dict(size=8),
        hovertemplate="<b>Year %{x}</b><br>Severe: %{y:.1f}%<extra></extra>",
    ))
    fig2.add_hline(y=40, line_dash="dash", line_color=WARNING, annotation_text="40% warning", annotation_font_color=WARNING)
    fig2.add_hline(y=60, line_dash="dash", line_color=DANGER, annotation_text="60% critical", annotation_font_color=DANGER)
    fig2.update_layout(
        title="Food Insecurity Rates - Kenya",
        xaxis_title="Year", yaxis_title="% of population",
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="white",
        legend_font_color="white",
        xaxis=dict(gridcolor="#262730"), yaxis=dict(gridcolor="#262730"),
        height=500,
    )
    st.plot(fig2, use_container_width=True) if False else st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div class="danger-box">
    {insight_text("moderate_or_severe_food_insecurity_pct", mod_data["moderate_or_severe_food_insecurity_pct"].iloc[-1], int(mod_data["Year"].iloc[-1]))}
    <br><br>
    {insight_text("severe_food_insecurity_pct", sev_data["severe_food_insecurity_pct"].iloc[-1], int(sev_data["Year"].iloc[-1]))}
    </div>
    """, unsafe_allow_html=True)

    st.subheader("The Affordability Crisis")
    st.markdown("""
    A **healthy diet** includes fruits, vegetables, protein, and whole grains, not just staple calories.
    In Kenya, this costs ~$3.20/day (international dollars). The charts below show how cost and
    unaffordability have worsened over time.
    """)

    fig3 = make_subplots(rows=1, cols=3, subplot_titles=("Cost of Healthy Diet (Int$/day)", "% Cannot Afford", "People Unable (millions)"))

    afford_data = [
        ("healthy_diet_cost_ppp_per_day", 3.5, 5.0),
        ("healthy_diet_unaffordable_pct", 50, 70),
        ("people_unable_afford_healthy_diet_million", 20, 35),
    ]
    for i, (ind, warn_val, danger_val) in enumerate(afford_data):
        d = analysis_df[["Year", ind]].dropna()
        d["Color"] = d[ind].apply(lambda v: status_color(v, ind))
        fig3.add_trace(
            go.Bar(x=d["Year"], y=d[ind], marker_color=d["Color"],
                   text=d[ind].round(1), textposition="outside", textfont_color="white",
                   hovertemplate=f"<b>Year %{{x}}</b><br>{INDICATOR_META[ind]['label']}: %{{y:.1f}} {INDICATOR_META[ind]['unit']}<extra></extra>"),
            row=1, col=i+1
        )
        fig3.add_hline(y=warn_val, line_dash="dash", line_color=WARNING, line_width=1, row=1, col=i+1)
        fig3.add_hline(y=danger_val, line_dash="dash", line_color=DANGER, line_width=1, row=1, col=i+1)

    fig3.update_layout(
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
        font_color="white", showlegend=False, height=450,
    )
    fig3.update_xaxes(gridcolor="#262730")
    fig3.update_yaxes(gridcolor="#262730")
    st.plotly_chart(fig3, use_container_width=True)

    val = analysis_df.dropna(subset=["healthy_diet_unaffordable_pct"]).sort_values("Year").tail(1)["healthy_diet_unaffordable_pct"].iloc[0]
    year = int(analysis_df.dropna(subset=["healthy_diet_unaffordable_pct"]).sort_values("Year").tail(1)["Year"].iloc[0])
    st.markdown(f"""
    <div class="danger-box">
    {insight_text("healthy_diet_unaffordable_pct", val, year)}
    <br><br>
    <b>The bottom line:</b> 43+ million Kenyans (76% of the population) cannot afford a healthy diet.
    They rely on cheap, nutrient-poor staples like maize and ugali, which explains why child stunting
    remains high despite adequate calorie supply. <b>Availability without access is not food security.</b>
    </div>
    """, unsafe_allow_html=True)

# TAB 4: Child Nutrition
with tab4:
    st.header("Child Nutrition - The Human Cost")
    st.markdown("""
    <div class="story-box">
    <b>What this measures:</b> The impact of food insecurity on children under 5 years old.
    <b>Stunting</b> (too short for age) indicates chronic malnutrition, long-term nutrient deficiency.
    <b>Wasting</b> (dangerously thin) indicates acute malnutrition, recent severe food shortage.
    Both cause irreversible physical and cognitive damage.<br><br>
    <b>Why this matters:</b> Malnourished children do not grow to their full height or cognitive potential.
    This limits their education, earning capacity, and health for the rest of their lives, perpetuating the cycle of poverty.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Child Stunting and Wasting Trends")
    st.markdown("""
    **WHO thresholds:**
    - Stunting: <20% = acceptable, 20-30% = warning, >30% = very high (critical)
    - Wasting: <5% = acceptable, 5-15% = warning, >15% = critical
    """)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Child Stunting (Under-5)", "Child Wasting (Under-5)"))

    st_data = analysis_df[["Year", "under5_stunting_pct"]].dropna()
    st_data["Color"] = st_data["under5_stunting_pct"].apply(lambda v: status_color(v, "under5_stunting_pct"))
    fig.add_trace(
        go.Bar(x=st_data["Year"], y=st_data["under5_stunting_pct"], marker_color=st_data["Color"],
               text=st_data["under5_stunting_pct"].round(1), textposition="outside", textfont_color="white",
               hovertemplate="<b>Year %{x}</b><br>Stunting: %{y:.1f}%<extra></extra>"),
        row=1, col=1
    )
    fig.add_hline(y=20, line_dash="dash", line_color=WARNING, annotation_text="20% warning", annotation_font_color=WARNING, row=1, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color=DANGER, annotation_text="30% critical", annotation_font_color=DANGER, row=1, col=1)

    wa_data = analysis_df[["Year", "under5_wasting_pct"]].dropna()
    wa_data["Color"] = wa_data["under5_wasting_pct"].apply(lambda v: status_color(v, "under5_wasting_pct"))
    fig.add_trace(
        go.Bar(x=wa_data["Year"], y=wa_data["under5_wasting_pct"], marker_color=wa_data["Color"],
               text=wa_data["under5_wasting_pct"].round(1), textposition="outside", textfont_color="white",
               hovertemplate="<b>Year %{x}</b><br>Wasting: %{y:.1f}%<extra></extra>"),
        row=1, col=2
    )
    fig.add_hline(y=5, line_dash="dash", line_color=WARNING, annotation_text="5% warning", annotation_font_color=WARNING, row=1, col=2)
    fig.add_hline(y=15, line_dash="dash", line_color=DANGER, annotation_text="15% critical", annotation_font_color=DANGER, row=1, col=2)

    fig.update_layout(
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
        font_color="white", showlegend=False, height=500,
    )
    fig.update_xaxes(gridcolor="#262730")
    fig.update_yaxes(gridcolor="#262730")
    st.plotly_chart(fig, use_container_width=True)

    st_val = st_data["under5_stunting_pct"].iloc[-1]
    st_year = int(st_data["Year"].iloc[-1])
    wa_val = wa_data["under5_wasting_pct"].iloc[-1] if not wa_data.empty else None
    wa_year = int(wa_data["Year"].iloc[-1]) if not wa_data.empty else "N/A"

    st.markdown(f"""
    <div class="danger-box">
    {insight_text("under5_stunting_pct", st_val, st_year)}
    <br><br>
    {insight_text("under5_wasting_pct", wa_val, wa_year) if wa_val else ""}
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Economic Context - GDP per Capita")
    st.markdown("""
    Economic growth should theoretically improve food access. Kenya GDP per capita (PPP) has grown
    from ~$3,700 (2000) to ~$5,800 (2024), but food insecurity has worsened, showing that
    <b>growth alone does not solve food insecurity</b> without equitable distribution.
    """)

    gdp_data = analysis_df[["Year", "gdp_per_capita_ppp"]].dropna()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=gdp_data["Year"], y=gdp_data["gdp_per_capita_ppp"],
        mode="lines+markers", fill="tozeroy",
        line=dict(color=NEUTRAL, width=3),
        marker=dict(size=8, color=NEUTRAL),
        fillcolor="rgba(52,152,219,0.1)",
        hovertemplate="<b>Year %{x}</b><br>GDP per capita: $%{y:,.0f}<extra></extra>",
    ))
    fig2.add_hline(y=3000, line_dash="dash", line_color=WARNING, annotation_text="$3,000 warning", annotation_font_color=WARNING)
    fig2.update_layout(
        title="GDP per Capita (PPP, constant 2021 Int$) - Kenya",
        xaxis_title="Year", yaxis_title="GDP per capita (Int$)",
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="white",
        xaxis=dict(gridcolor="#262730"), yaxis=dict(gridcolor="#262730"),
        height=450,
    )
    st.plotly_chart(fig2, use_container_width=True)

# TAB 5: County Risk Map
with tab5:
    st.header("County Risk Map - Where Is the Crisis Worst?")
    st.markdown(f"""
    <div class="story-box">
    The World Bank Joint Monitoring Report (JMR) tracks food security risk at the sub-county level
    across 7 indicators: Conflict, Drought (NDVI), Drought (rainfall), Exchange rates, Food prices,
    and volatility in exchange rates and food prices.<br><br>
    <b>Latest data: {latest_alert_date.date()}</b> - showing the maximum alert level reached in any sub-county
    within each county. Hover over bars and cells for detailed values.
    </div>
    """, unsafe_allow_html=True)

    # County choropleth maps
    st.subheader("County Risk Choropleth Maps")
    st.markdown("""
    These maps show the food security risk level for each of Kenya 47 counties.
    Darker red indicates higher risk. Hover over a county for its name and risk level.
    """)

    map_choice = st.selectbox(
        "Select map to display:",
        ["Overall Alert Level", "Critical Alert Count"],
    )

    if map_choice == "Overall Alert Level":
        # Match notebook: column="overall_max_alert", cmap YlOrRd equivalent
        geo_json = county_geo_df.__geo_interface__
        fig_map = px.choropleth(
            county_geo_df,
            geojson=geo_json,
            locations=county_geo_df.index,
            color="overall_max_alert",
            color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
            range_color=[0, 2],
            labels={"overall_max_alert": "Alert Level"},
            title=f"Kenya County Food Security Risk - Overall Alert ({latest_alert_date.date()})",
        )
    else:
        geo_json = county_geo_df.__geo_interface__
        fig_map = px.choropleth(
            county_geo_df,
            geojson=geo_json,
            locations=county_geo_df.index,
            color="total_critical_flags",
            color_continuous_scale="Reds",
            labels={"total_critical_flags": "Critical Flags"},
            title=f"Critical Admin-2 Indicator Flags by County ({latest_alert_date.date()})",
        )

    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
        font_color="white",
        coloraxis_colorbar=dict(title="Alert"),
        height=600,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")
    st.subheader("County Risk Ranking")
    st.markdown("Alert levels: **Typical** (0) | **Heightened** (1) | **Critical** (2)")

    col1, col2 = st.columns([2, 1])

    with col1:
        top = county_risk_summary.head(15)
        top = top.iloc[::-1]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=top["adm1_name"], x=top["total_critical_flags"],
            orientation="h", name="Critical flags",
            marker_color=DANGER,
            text=top["total_critical_flags"], textposition="outside", textfont_color="white",
            hovertemplate="<b>%{y}</b><br>Critical flags: %{x}<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            y=top["adm1_name"], x=top["total_heightened_flags"],
            orientation="h", name="Heightened flags",
            marker_color=WARNING,
            text=top["total_heightened_flags"], textposition="outside", textfont_color="white",
            hovertemplate="<b>%{y}</b><br>Heightened flags: %{x}<extra></extra>",
        ))
        fig.update_layout(
            title=f"Top 15 Highest-Risk Counties ({latest_alert_date.date()})",
            xaxis_title="Number of sub-county alerts", yaxis_title="County",
            barmode="stack",
            plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
            font_color="white", legend_font_color="white",
            xaxis=dict(gridcolor="#262730"), yaxis=dict(gridcolor="#262730"),
            height=600,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Alert Summary")
        alert_counts = county_risk_summary["overall_alert_label"].value_counts()
        for label, color in [("Critical", DANGER), ("Heightened", WARNING), ("Typical", SAFE)]:
            count = alert_counts.get(label, 0)
            pct = count / len(county_risk_summary) * 100
            st.markdown(f"<div style=\"color:{color}; font-size:1.1em;\"><b>{label}:</b> {count} counties ({pct:.0f}%)</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Most Affected")
        for _, row in county_risk_summary.head(5).iterrows():
            c = ALERT_COLORS.get(row["overall_max_alert"], NEUTRAL)
            st.markdown(f"<span style=\"color:{c};\">*</span> <b>{row['adm1_name']}</b> - {row['overall_alert_label']}", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Least Affected")
        for _, row in county_risk_summary.tail(5).iterrows():
            c = ALERT_COLORS.get(row["overall_max_alert"], NEUTRAL)
            st.markdown(f"<span style=\"color:{c};\">*</span> <b>{row['adm1_name']}</b> - {row['overall_alert_label']}", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("County x Indicator Heatmap")
    st.markdown("""
    This heatmap shows the **maximum alert level** for each county across all JMR indicators.
    Red = at least one sub-county in that county reached critical level for that indicator.
    """)

    # Match notebook exactly: pivot latest_county_alerts with adm1_pcode, adm1_name as index
    latest_for_heatmap = county_alerts[county_alerts["date"] == latest_alert_date].copy()
    county_indicator_matrix = latest_for_heatmap.pivot_table(
        index=["adm1_pcode", "adm1_name"],
        columns="indicator",
        values="max_alert_level",
        aggfunc="max",
    ).reset_index()
    county_indicator_matrix.columns.name = None

    hm_data = county_indicator_matrix.set_index("adm1_name").drop(columns="adm1_pcode")
    hm_data = hm_data.loc[county_risk_summary["adm1_name"]]
    hm_data = hm_data.astype(float)

    fig_hm = go.Figure(data=go.Heatmap(
        z=hm_data.values,
        x=hm_data.columns.tolist(),
        y=hm_data.index.tolist(),
        colorscale=[[0, SAFE], [0.5, WARNING], [1, DANGER]],
        zmin=0, zmax=2,
        hovertemplate="<b>%{y}</b><br>%{x}<br>Alert: %{z:.0f}<extra></extra>",
        colorbar=dict(title="Alert", tickvals=[0, 1, 2], ticktext=["Typical", "Heightened", "Critical"]),
    ))
    fig_hm.update_layout(
        title=f"JMR Alert Levels by County ({latest_alert_date.date()})",
        xaxis_title="Indicator", yaxis_title="County",
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
        font_color="white",
        height=700,
    )
    st.plotly_chart(fig_hm, use_container_width=True)

    st.markdown(f"""
    <div style="display:flex; gap:24px; justify-content:center; flex-wrap:wrap;">
        <span style="color:{SAFE};">Typical (0)</span>
        <span style="color:{WARNING};">Heightened (1)</span>
        <span style="color:{DANGER};">Critical (2)</span>
    </div>
    """, unsafe_allow_html=True)
