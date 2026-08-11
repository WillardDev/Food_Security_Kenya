import streamlit as st

from dashboard.config import (
    SAFE, WARNING, DANGER, NEUTRAL, ALERT_LABELS, ALERT_COLORS, INDICATOR_META,
)
from dashboard.insights import status_color, status_label
from dashboard import plots


def metric_cards(analysis_df):
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


def tab1(analysis_df):
    st.header("Kenya Food Security Crisis - At a Glance")
    st.markdown("""
    <div class="story-box">
    Kenya faces a <b>persistent, multi-dimensional food security crisis</b>. Despite steady economic growth over two decades,
    the majority of Kenyans cannot afford a healthy diet, and nearly 1 in 3 are undernourished. This dashboard tells the story
    through interactive national trends, county risk maps, and diet affordability data.<br><br>
    <b>How to read this dashboard:</b> Every chart uses a consistent color system:
    <span style="color:#2ecc71">green for acceptable</span>,
    <span style="color:#f39c12">yellow for warning</span>, and
    <span style="color:#e74c3c">red for critical</span>.
    Hover over any data point for detailed values and insights.
    </div>
    """, unsafe_allow_html=True)

    metric_cards(analysis_df)

    st.markdown("---")
    st.subheader("The Big Picture: Two Decades of Food Security")
    st.plotly_chart(plots.top_indicators_chart(analysis_df), use_container_width=True)
    st.markdown(plots.top_indicators_insight(analysis_df), unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Correlation: GDP per Capita vs Food Insecurity")
    st.markdown("""
    This scatter plot explores whether economic growth (GDP per capita) is associated with
    lower food insecurity. Each point represents one year. If growth helped, we would see
    a downward trend (higher GDP = lower insecurity). Hover over points for details.
    """)
    st.plotly_chart(plots.correlation_chart(analysis_df), use_container_width=True)
    st.markdown(plots.correlation_insight(analysis_df), unsafe_allow_html=True)


def tab2(analysis_df):
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
    st.plotly_chart(plots.energy_adequacy_chart(analysis_df), use_container_width=True)
    st.markdown(plots.energy_adequacy_insight(analysis_df), unsafe_allow_html=True)

    st.subheader("Food Supply Breakdown (per person per day)")
    st.markdown("""
    These three metrics show the actual nutritional content available per Kenyan per day.
    Recommended minimums: **2,100 kcal**, **50g protein**, **40g fat**.
    """)
    st.plotly_chart(plots.supply_breakdown_chart(analysis_df), use_container_width=True)
    st.markdown(plots.supply_breakdown_insight(analysis_df), unsafe_allow_html=True)


def tab3(analysis_df):
    st.header("Access and Affordability - Can People Afford Food?")
    st.markdown("""
    <div class="story-box">
    <b>What this measures:</b> Whether Kenyans can physically and economically access the food they need.
    This is the most critical dimension. Even when food is available, poverty prevents people from affording it.
    Kenya healthy diet costs ~$3.20/day (international dollars), but the majority of the population cannot afford it.<br><br>
    <b>The paradox:</b> Kenya has adequate calorie supply (~93% of needs met) yet most people are food insecure.
    The problem is not scarcity, it is poverty and affordability.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Prevalence of Undernourishment")
    st.markdown("""
    The percentage of Kenya population that **consistently fails to meet their daily calorie requirements**.
    WHO thresholds: <15% = acceptable, 15-25% = warning, >25% = critical.
    """)
    st.plotly_chart(plots.undernourishment_chart(analysis_df), use_container_width=True)
    st.markdown(plots.undernourishment_insight(analysis_df), unsafe_allow_html=True)

    st.subheader("Food Insecurity Severity")
    st.markdown("""
    Food insecurity exists on a spectrum:
    - **Moderate/Severe**: People who worry about food, are forced to eat less, or skip meals
    - **Severe**: People who go entire days without eating
    """)
    st.plotly_chart(plots.food_insecurity_chart(analysis_df), use_container_width=True)
    st.markdown(plots.food_insecurity_insight(analysis_df), unsafe_allow_html=True)

    st.subheader("The Affordability Crisis")
    st.markdown("""
    A **healthy diet** includes fruits, vegetables, protein, and whole grains, not just staple calories.
    In Kenya, this costs ~$3.20/day (international dollars). The charts below are line charts because they
    track how cost and unaffordability have changed over time.
    """)
    st.plotly_chart(plots.affordability_chart(analysis_df), use_container_width=True)
    st.markdown(plots.affordability_insight(analysis_df), unsafe_allow_html=True)


def tab4(analysis_df):
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
    st.plotly_chart(plots.child_nutrition_chart(analysis_df), use_container_width=True)
    st.markdown(plots.child_nutrition_insight(analysis_df), unsafe_allow_html=True)

    st.subheader("Economic Context - GDP per Capita")
    st.markdown("""
    Economic growth should theoretically improve food access. Kenya GDP per capita (PPP) has grown
    from ~$3,700 (2000) to ~$5,800 (2024), but food insecurity has worsened, showing that
    <b>growth alone does not solve food insecurity</b> without equitable distribution.
    """)
    st.plotly_chart(plots.gdp_chart(analysis_df), use_container_width=True)
    st.markdown(plots.gdp_insight(analysis_df), unsafe_allow_html=True)


def tab5(county_alerts, county_risk_summary, county_geo_df, latest_alert_date):
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

    st.subheader("County Risk Choropleth Maps")
    st.markdown("""
    These maps show the food security risk level for each of Kenya's 47 counties.
    Darker red indicates higher risk. Hover over a county for its name and risk level.
    """)

    map_choice = st.selectbox(
        "Select map to display:",
        ["Overall Alert Level", "Critical Alert Count"],
    )
    fig_map = plots.choropleth_chart(county_geo_df, latest_alert_date, map_choice)
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown(plots.county_map_insight(county_risk_summary, latest_alert_date), unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("County Risk Ranking")
    st.markdown("Alert levels: **Typical** (0) | **Heightened** (1) | **Critical** (2)")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(plots.county_ranking_chart(county_risk_summary, latest_alert_date), use_container_width=True)
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
    st.subheader("Top 10 Counties: Critical vs Heightened Alerts")
    st.markdown("""
    This bar chart compares the number of critical and heightened food security alerts
    across the 10 most affected counties. Unlike the trend charts above, this is a
    snapshot comparison, not a time series.
    """)
    st.plotly_chart(plots.top10_chart(county_risk_summary, latest_alert_date), use_container_width=True)

    st.markdown("---")
    st.subheader("County x Indicator Heatmap")
    st.markdown("""
    This heatmap shows the **maximum alert level** for each county across all JMR indicators.
    Red = at least one sub-county in that county reached critical level for that indicator.
    """)
    latest_for_heatmap = county_alerts[county_alerts["date"] == latest_alert_date].copy()
    county_indicator_matrix = latest_for_heatmap.pivot_table(
        index=["adm1_pcode", "adm1_name"],
        columns="indicator",
        values="max_alert_level",
        aggfunc="max",
    ).reset_index()
    county_indicator_matrix.columns.name = None

    st.plotly_chart(plots.heatmap_chart(county_indicator_matrix, county_risk_summary, latest_alert_date), use_container_width=True)
    st.markdown(plots.heatmap_insight(county_risk_summary), unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:flex; gap:24px; justify-content:center; flex-wrap:wrap;">
        <span style="color:{SAFE};">Typical (0)</span>
        <span style="color:{WARNING};">Heightened (1)</span>
        <span style="color:{DANGER};">Critical (2)</span>
    </div>
    """, unsafe_allow_html=True)