import streamlit as st

from dashboard.config import (
    SAFE, WARNING, DANGER, NEUTRAL, ALERT_LABELS, ALERT_COLORS, INDICATOR_META,
)
from dashboard.insights import status_color, status_label
from dashboard import plots


def section(label, title, body):
    st.markdown(f"""
    <div style="background:#1a1a2e; border-radius:8px; padding:16px 20px; margin:12px 0; border-left:3px solid {label}; color:#ddd; line-height:1.6;">
        <b style="color:{label};">{title}</b><br>{body}
    </div>
    """, unsafe_allow_html=True)


def problem_statement():
    st.header("Problem Statement")
    st.markdown("""
    <div class="story-box">
    <b>In one sentence:</b> Despite two decades of sustained economic growth, the majority of Kenyans still
    cannot afford a nutritious diet, and food insecurity - especially among children - remains persistently high.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Background")
    st.markdown("""
    <div class="story-box">
    Kenya is often described as an <b>emerging economy</b>. Over the last 20 years GDP per capita has grown
    steadily, yet national food-security indicators tell a very different story:
    roughly <b>70% of Kenyans</b> are moderately or severely food insecure, about <b>31% are undernourished</b>,
    and <b>1 in 5 children under five</b> are stunted. The country produces enough calories to feed itself
    (energy adequacy ~93%), so this is not a classic famine or scarcity crisis.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("The Core Problem")
    st.markdown("""
    <div class="story-box">
    The problem is one of <b>access and affordability, not availability</b>. A nutritious diet in Kenya costs
    roughly <b>$3.20 per person per day</b> - an amount a large share of the population simply cannot afford.
    People fall back on cheap staples that provide calories but not the vitamins, protein, and minerals needed
    for health, leaving a population that is <b>fed but still malnourished</b>.
    <br><br>
    Compounding this, the crisis is <b>unevenly spread</b>. County-level alerts flag severe risk driven by
    drought, volatile food prices, exchange-rate shocks, and conflict - meaning some regions and households
    are far more exposed than others, and national averages hide these hotspots.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Why This Matters")
    st.markdown("""
    <div class="story-box">
    The consequences are <b>economic and generational</b>. Malnourished children are more likely to grow into
    adults with lower earnings and poorer health, trapping families in poverty and dragging down the country's
    human capital. The economic growth that Kenya has achieved is therefore <b>not translating into improved
    wellbeing</b> - growth without food security is growth that leaves people behind.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("What This Project Addresses")
    st.markdown("""
    <div class="danger-box">
    <b>Research question:</b> "Why does economic growth in Kenya not translate into improved food security,
    and where is the crisis worst?"
    <br><br>
    This dashboard answers it with national trend data (FAOSTAT, 2000-2025) and sub-national risk maps
    (World Bank JMR, 2010-2026), and concludes with evidence-based recommendations in the final tab.
    </div>
    """, unsafe_allow_html=True)


def about():
    st.header("Learn: Food Security and This Project")
    st.markdown("""
    <div class="story-box">
    <b>Welcome!</b> This tab explains the key concepts, the main research questions this project answers,
    and the terms used throughout the dashboard. Read it first (or come back anytime) to get the most out
    of the charts.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("What Is Food Security?")
    st.markdown("""
    <div class="story-box">
    <b>Food security exists when all people, at all times, have physical, social, and economic access to
    sufficient, safe, and nourishing food that meets their dietary needs for an active and healthy life.</b>
    <br><br>
    It is built on <b>four pillars</b>, and a country can fail on any one of them even when the others look fine:
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    pillars = [
        ("Availability", "Is there enough food produced or supplied? We track calories, protein, and fat per person per day.", SAFE),
        ("Access", "Can people afford and physically reach food? We track undernourishment, food insecurity, and healthy-diet affordability.", WARNING),
        ("Utilization", "Is the food nutritious and safely prepared? We track child stunting and wasting as outcomes.", DANGER),
        ("Stability", "Is access reliable over time, or disrupted by drought, price shocks, and conflict? The county risk maps assess this.", NEUTRAL),
    ]
    for col, (name, desc, color) in zip(cols, pillars):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {color};">
                <h4 style="margin:0; color:{color};">{name}</h4>
                <p style="margin:0; color:#ccc; font-size:0.85em;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="story-box">
    <b>Why this matters for Kenya:</b> Kenya can grow enough calories (Availability ~93%) yet most people are
    food insecure. That is the <b>Access</b> pillar failing — the crisis is not scarcity, it is poverty and affordability.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Primary Research Question")
    st.markdown("""
    <div class="danger-box">
    <b>Primary research question:</b>
    "Why does economic growth in Kenya not translate into improved food security, and where is the crisis worst?"
    <br><br>
    In short: <b>Has Kenya's two decades of GDP growth made its people more food secure — and if not, why?</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Research Questions and the Visualizations That Answer Them
    Each tab in this dashboard exists to answer one or more specific questions:
    """)

    q_rows = {
        "What national food-security and healthy-diet trends are visible in the data?": 
            ("Tab 3 & Tab 4", "Key Indicators Over Time, Undernourishment, Food Insecurity Severity, and the Affordability Crisis charts show 2000-2025 trends."),
        "Does economic growth reduce food insecurity?": 
            ("Tab 3", "The GDP per Capita vs Food Insecurity scatter is THE chart answering this — it shows higher GDP did NOT lower food insecurity."),
        "Is healthy diet affordability improving or worsening?": 
            ("Tab 4", "The Affordability Crisis line charts show cost and the % unable to afford rising over time."),
        "What is the human cost, especially for children?": 
            ("Tab 5", "Child Stunting & Wasting charts show the irreversible impact of malnutrition on under-5s."),
        "Which counties are at the highest risk and why?": 
            ("Tab 6", "The choropleth maps rank counties by overall alert and critical flags; the heatmap shows WHICH indicator is driving each county's risk. The executive summary (Tab 2) adds a county-by-county snapshot and the pie chart showing how many counties are at risk."),
        "Do the risk alerts match what is actually measured in each county?": 
            ("Tab 7", "County Comparisons merges external data - DHS child stunting/wasting, poverty rates, and IPC crisis populations - with the JMR alerts. The bar charts rank all 47 counties; the cross-check scatter colors each county by its JMR alert to see whether measured outcomes line up with the early-warning system."),
    }
    for q, (where, viz) in q_rows.items():
        section(SAFE, "Question", f"<b>{q}</b><br><span style='color:#888;'><b>Where:</b> {where}</span><br>{viz}")

    st.markdown("---")
    st.subheader("Glossary of Key Terms")

    glossary = [
        ("Dietary Energy Adequacy (%)", "The % of the population's daily calorie needs that the domestic food supply meets. Below 100% means Kenya relies on imports or aid.", SAFE),
        ("Prevalence of Undernourishment (%)", "The % of people who consistently fail to meet their daily calorie requirements. WHO: <15% acceptable, 15-25% warning, >25% critical.", WARNING),
        ("Food Insecurity - Moderate or Severe (%)", "The % of people who worry about food, are forced to eat less, or skip meals due to lack of affordable food.", DANGER),
        ("Severe Food Insecurity (%)", "The % of people who literally go entire days without eating.", DANGER),
        ("Healthy Diet Cost (Int$/day)", "The cost of a nutritious diet (fruits, vegetables, protein, whole grains) per person per day in international dollars.", NEUTRAL),
        ("Prevalence of Unaffordability (%)", "The % of the population that cannot afford that healthy diet.", WARNING),
        ("Child Stunting (Under-5, %)", "Children too short for their age — a sign of chronic, largely irreversible malnutrition.", DANGER),
        ("Child Wasting (Under-5, %)", "Children dangerously thin — a sign of acute, recent food shortage that can be reversed with timely help.", DANGER),
        ("GDP per Capita (PPP, Int$)", "Economic output per person, adjusted for local prices. A rough proxy for average purchasing power.", NEUTRAL),
        ("FAOSTAT", "The UN Food and Agriculture Organization's statistical database — the source of all national-level indicators used here.", NEUTRAL),
        ("JMR - Joint Monitoring Report", "The World Bank's framework tracking food-security risk at sub-national (county/sub-county) level for climate, prices, exchange rates, and conflict.", NEUTRAL),
        ("Alert Levels (Typical/Heightened/Critical)", "JMR risk ratings: 0 = Typical, 1 = Heightened, 2 = Critical. Applied per sub-county per indicator.", WARNING),
    ]
    for term, desc, color in glossary:
        section(color, term, desc)

    st.markdown("""
    <div class="story-box">
    <b>Tips for exploring:</b> Hover over any chart for exact values. Every chart carries a colored insight box
    (green/yellow/red border) that explains what the data means and why it matters. The sidebar always shows the
    status legend so you can decode colors instantly.
    </div>
    """, unsafe_allow_html=True)


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


def tab1(analysis_df, county_risk_summary, latest_alert_date):
    st.header("Executive Summary - Kenya Food Security Crisis at a Glance")
    st.markdown("""
    <div class="story-box">
    <b>This is a story about a paradox.</b> Kenya has grown richer for two decades, and its farms produce nearly
    enough calories to feed everyone. Yet <b>the majority of Kenyans still cannot afford a healthy diet</b>, about
    <b>1 in 3 are undernourished</b>, and the crisis is concentrated in specific counties while others are barely touched.<br><br>
    <b>How to read this dashboard:</b> Every chart uses one color system:
    <span style="color:#2ecc71">green = acceptable</span>,
    <span style="color:#f39c12">yellow = warning</span>, and
    <span style="color:#e74c3c">red = critical</span>.
    Follow the tabs in order and you will move from the national picture down to the counties that need help most.
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

    st.markdown("---")
    st.subheader("The Crisis on a Map of Counties")
    st.markdown("""
    National averages hide the geography of hunger. Here is the same story told county by county:
    which parts of Kenya are most affected, and which are least.
    """)

    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(plots.county_alert_pie_chart(county_risk_summary, latest_alert_date), use_container_width=True)
    with col_right:
        ml_n = st.slider("Counties to show in most/least:", min_value=3, max_value=20, value=5, step=1)
        st.plotly_chart(plots.most_least_affected_chart(county_risk_summary, top_n=ml_n), use_container_width=True)
    st.markdown(plots.county_snapshot_insight(county_risk_summary, latest_alert_date), unsafe_allow_html=True)


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


def tab5(county_alerts, county_risk_summary, county_geo_df, latest_alert_date):
    st.header("County Risk Map - Where Is the Crisis Worst?")
    st.markdown(f"""
    <div class="story-box">
    The national trend lines in the earlier tabs smooth away geography. This tab zooms in on
    Kenya's <b>47 counties</b> using the World Bank Joint Monitoring Report (JMR), which tracks
    food security risk at the sub-county level across 7 indicators: Conflict, Drought (NDVI),
    Drought (rainfall), Exchange rates, Food prices, and volatility in exchange rates and food prices.<br><br>
    <b>Latest data: {latest_alert_date.date()}</b> - showing the maximum alert level reached in any sub-county
    within each county. Hover over bars and cells for detailed values.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("How Many Counties Are at Risk - Over Time")
    st.markdown("""
    Unlike national charts, this line chart is <b>county-specific</b>: it counts how many of Kenya's 47 counties
    were at heightened or critical risk each month from 2010 to today. Watch how the crisis expands and contracts
    with drought cycles and price shocks.
    """)
    st.plotly_chart(plots.county_trend_chart(county_alerts), use_container_width=True)
    st.markdown(plots.county_trend_insight(county_alerts), unsafe_allow_html=True)

    st.markdown("---")
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
        rank_n = st.slider("Number of counties in the ranking:", min_value=5, max_value=47, value=15, step=1)
        st.plotly_chart(plots.county_ranking_chart(county_risk_summary, latest_alert_date, top_n=rank_n), use_container_width=True)
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


def tab6(county_stats, latest_alert_date):
    st.header("County Comparisons - Measured Outcomes vs Risk Alerts")
    st.markdown("""
    <div class="story-box">
    This tab merges <b>externally-measured county data</b> with the JMR risk alerts so all 47 counties can be
    compared directly - no national averages, one bar per county:
    - <b>Child nutrition</b> - stunting & wasting (Kenya DHS 2022)
    - <b>Poverty</b> - overall & severe poverty rates and the Multidimensional Poverty Index (HAPI / World Bank 2022)
    - <b>Acute food insecurity</b> - people in IPC Phase 3+ crisis (IPC, Feb 2026)
    - <b>Population</b> - county populations from the JMR data
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Compare Counties on Any Indicator")
    st.markdown("""
    Select an indicator below - every county gets its own bar, so you can see the full spread from least
    to most affected instead of a single national line.
    """)

    ctl1, ctl2 = st.columns([2, 1])
    with ctl1:
        indicator = st.selectbox(
            "Choose an indicator to compare:",
            list(plots.COUNTY_INDICATORS.keys()),
            format_func=lambda k: plots.COUNTY_INDICATORS[k]["label"],
        )
    with ctl2:
        top_n = st.slider("Number of counties to show:", min_value=5, max_value=47, value=47, step=1)
    st.plotly_chart(plots.county_indicator_bar_chart(county_stats, indicator, top_n=top_n), use_container_width=True)

    st.markdown("---")
    st.subheader("People in Acute Food Insecurity by County")
    st.markdown("""
    The IPC analysis counts how many people in each county are in Phase 3+ (crisis) - the people who need help
    right now. The light bar is the county's total population; the red bar is the population in crisis.
    """)
    st.plotly_chart(plots.county_crisis_chart(county_stats, top_n=top_n), use_container_width=True)

    st.markdown("---")
    st.subheader("Cross-Check: Do the Measures Agree?")
    st.markdown("""
    Pick any two indicators and compare them county by county. Each point is a county, colored by its JMR risk
    alert (green = typical, yellow = heightened, red = critical). If the externally-measured outcomes line up
    with the risk alerts, the early-warning system is doing its job.
    """)
    col1, col2 = st.columns(2)
    with col1:
        x_key = st.selectbox(
            "X axis (lower = less affected):", list(plots.COUNTY_INDICATORS.keys()), index=2,
            format_func=lambda k: plots.COUNTY_INDICATORS[k]["label"],
        )
    with col2:
        y_key = st.selectbox(
            "Y axis (lower = less affected):", list(plots.COUNTY_INDICATORS.keys()), index=0,
            format_func=lambda k: plots.COUNTY_INDICATORS[k]["label"],
        )
    if x_key == y_key:
        st.info("Pick two different indicators to compare. Right now both axes are the same measure.")
    else:
        st.plotly_chart(plots.county_comparison_scatter_chart(county_stats, x_key, y_key), use_container_width=True)
        st.markdown(plots.county_comparisons_insight(county_stats), unsafe_allow_html=True)


def tab7(analysis_df, county_risk_summary, latest_alert_date):
    st.header("Conclusion and Way Forward")
    st.markdown("""
    <div class="story-box">
    <b>In one sentence:</b> Kenya can produce enough calories, yet the majority of its people cannot
    afford a nutritious diet, and economic growth over two decades has not reduced food insecurity.
    This final tab synthesizes what the data shows and sets out a path forward.
    </div>
    """, unsafe_allow_html=True)

    # --- Key takeaways from the data ---
    latest = analysis_df.sort_values("Year").dropna(subset=["undernourishment_pct"]).tail(1)
    year = int(latest["Year"].iloc[0]) if not latest.empty else 2025
    und = latest["undernourishment_pct"].iloc[0] if not latest.empty else 31.4
    ins = latest["moderate_or_severe_food_insecurity_pct"].iloc[0] if not latest.empty else 69.9
    stun = latest["under5_stunting_pct"].iloc[0] if not latest.empty else 18.3
    gdp = latest["gdp_per_capita_ppp"].iloc[0] if not latest.empty else 5800

    st.subheader("1. Conclusion - What the Data Tells Us")
    conclusions = [
        ("Growth is not translating into food security",
         f"GDP per capita reached ~${gdp:,.0f} in {year}, yet {ins:.0f}% of Kenyans are food insecure. "
         "The GDP vs Food Insecurity scatter proves higher income has NOT lowered hunger - the gains are not reaching the poorest."),
        ("Scarcity is not the problem; affordability is",
         "Energy adequacy sits near 93%, meaning Kenya grows most of its calories - but a nutritious diet costs ~$3.20/day "
         "and the majority cannot afford it. People fill up on cheap staples but stay malnourished ('hidden hunger')."),
        ("The human cost is concentrated in children",
         f"~{stun:.0f}% of under-5s are stunted - permanent cognitive and physical damage that is largely irreversible. "
         "Progress has been made, but millions of children are still left behind."),
        ("The crisis is geographical and targeted responses are possible",
         f"The JMR data ({latest_alert_date.date()}) shows some counties at critical risk driven by drought, food prices, "
         f"exchange rates, and conflict. These hotspots are identifiable and can be prioritized."),
    ]
    for title, body in conclusions:
        section(WARNING, title, body)

    st.markdown("---")
    st.subheader("2. Way Forward - Recommendations")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="story-box">
        <h4 style="color:#3498db; margin-top:0;">Immediate (0-2 years)</h4>
        - <b>Cash and food transfers</b> to the counties flagged critical on the risk map.<br>
        - <b>Subsidize or fortify staples</b> so affordable calories also carry protein and micronutrients.<br>
        - <b>Expand school feeding</b> to reach malnourished children where the data shows the worst outcomes.<br>
        - <b>Social protection</b> (e.g. Hunger Safety Net Program) targeted by the JMR alerts.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="story-box">
        <h4 style="color:#2ecc71; margin-top:0;">Medium & Long Term (3-10 years)</h4>
        - <b>Agricultural productivity</b> - irrigation, drought-tolerant crops, and climate-resilient farming in ASALs.<br>
        - <b>Redistributive growth</b> - invest in rural livelihoods so GDP growth reaches the poorest.<br>
        - <b>Resilient supply chains</b> to buffer global price shocks and the exchange-rate volatility JMR tracks.<br>
        - <b>Early-warning systems</b> that act on county alerts before a crisis peaks.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("3. The Data Story in 30 Seconds")

    gdp_growth = gdp - 2000

    st.markdown(f"""
    <div class="danger-box">
    <b>Two decades of GDP growth (average income rose by roughly ${gdp_growth:,.0f} per capita) did not end hunger.</b>
    Kenya's problem is not a shortage of food - it is that <b>the poorest cannot afford a nutritious diet</b>,
    leaving {und:.0f}% undernourished and the majority food-insecure, with children bearing permanent damage.
    The counties already flagged as critical in the JMR data are where intervention must start.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ---
    <div class="story-box">
    <b>Data availability & limitations:</b> National indicators come from FAOSTAT estimates (2000-2025);
    county risk from the World Bank JMR (2010-2026). Values are point-in-time estimates and may be revised
    by source agencies. Cross-check any headline figure with the raw data tables in <i>data/</i>.
    </div>
    """, unsafe_allow_html=True)