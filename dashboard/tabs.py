import streamlit as st

from dashboard.config import INDICATOR_META, BIG_IDEA
from dashboard.insights import status_label
from dashboard import plots


def act_banner(act, title, body):
    st.markdown(f"### {act} · {title}")
    st.markdown(body)


def story_roadmap():
    st.markdown("""
**The story in three acts** — each act is a tab, and each chart answers one question:

- **Act 1 · The Setup** — *Is there enough food?* (Availability tab)
- **Act 2 · The Conflict** — *Can people afford what exists, and who pays the price?* (Access and Child Nutrition)
- **Act 3 · The Resolution** — *Where is the crisis worst, and what should we do?* (County Risk, County Comparisons, Conclusion)
    """)


def section(title, body):
    st.markdown(f"**{title}**\n\n{body}")


def problem_statement():
    st.subheader("Problem Statement")
    st.markdown(
        "Kenya has grown steadily richer for two decades, yet hunger has not fallen with it: roughly 70% of Kenyans "
        "are moderately or severely food insecure, about 31% are undernourished, and 1 in 5 children under five are "
        "stunted. This is not a scarcity crisis - the country produces about 93% of its own calorie needs - but an "
        "affordability crisis. A nutritious diet costs around $3.20 per person per day, more than most people can "
        "pay, so households fall back on cheap staples that fill stomachs but not nutrient needs. The burden is also "
        "uneven: county-level alerts driven by drought, food prices, exchange-rate shocks, and conflict show that "
        "some regions and children are far more exposed than others, and national averages hide these hotspots."
    )
    st.markdown(
        "This project uses national trend data (FAOSTAT, 2000-2025) and sub-national risk maps (World Bank JMR, "
        "2010-2026) to answer why economic growth has not translated into food security and where the crisis is "
        "worst. It compares counties on measured outcomes such as child stunting and wasting, and it closes with "
        "evidence-based recommendations in the final tab."
    )


def about():
    st.header("Learn: Food Security and This Project")
    st.markdown(BIG_IDEA)
    story_roadmap()
    st.markdown("**Welcome!** This tab explains the key concepts, the main research questions this project answers, "
                "and the terms used throughout the dashboard. Read it first (or come back anytime) to get the most "
                "out of the charts.")

    st.subheader("What Is Food Security?")
    st.markdown("Food security exists when all people, at all times, have physical, social, and economic access to "
                "sufficient, safe, and nourishing food that meets their dietary needs for an active and healthy life.")
    st.markdown("It is built on four pillars, and a country can fail on any one of them even when the others look fine:")
    st.markdown("""
- **Availability** — Is there enough food produced or supplied? We track calories, protein, and fat per person per day.
- **Access** — Can people afford and physically reach food? We track undernourishment, food insecurity, and healthy-diet affordability.
- **Utilization** — Is the food nutritious and safely prepared? We track child stunting and wasting as outcomes.
- **Stability** — Is access reliable over time, or disrupted by drought, price shocks, and conflict? The county risk maps assess this.
    """)
    st.markdown("**Why this matters for Kenya:** Kenya can grow enough calories (Availability ~93%) yet most people are "
                "food insecure. That is the Access pillar failing - the crisis is not scarcity, it is poverty and "
                "affordability.")

    st.markdown("---")
    st.subheader("Primary Research Question")
    st.markdown("**Primary research question:** Why does economic growth in Kenya not translate into improved food?")

    st.markdown("### Research Questions and the Visualizations That Answer Them")
    st.markdown("Each tab in this dashboard exists to answer one or more specific questions:")
    st.markdown("""
        - What national food-security and healthy-diet trends are visible in the data?
        - Does economic growth reduce food insecurity?
        - Is healthy diet affordability improving or worsening?
        - What is the human cost, especially for children?
        - Which counties are at the highest risk and why?
        - Do the risk alerts match what is actually measured in each county?
    """)

    st.markdown("---")
    st.subheader("Glossary of Key Terms")

    st.markdown("""
        - **Dietary Energy Adequacy (%)** — The % of the population's daily calorie needs that the domestic food supply meets. Below 100% means Kenya relies on imports or aid.
        - **Prevalence of Undernourishment (%)** — The % of people who consistently fail to meet their daily calorie requirements. WHO: below 15% acceptable, 15-25% warning, above 25% critical.
        - **Food Insecurity - Moderate or Severe (%)** — The % of people who worry about food, are forced to eat less, or skip meals due to lack of affordable food.
        - **Severe Food Insecurity (%)** — The % of people who literally go entire days without eating.
        - **Healthy Diet Cost (Int$/day)** — The cost of a nutritious diet (fruits, vegetables, protein, whole grains) per person per day in international dollars.
        - **Prevalence of Unaffordability (%)** — The % of the population that cannot afford that healthy diet.
        - **Child Stunting (Under-5, %)** — Children too short for their age - a sign of chronic, largely irreversible malnutrition.
        - **Child Wasting (Under-5, %)** — Children dangerously thin - a sign of acute, recent food shortage that can be reversed with timely help.
        - **GDP per Capita (PPP, Int$)** — Economic output per person, adjusted for local prices. A rough proxy for average purchasing power.
        - **FAOSTAT** — The UN Food and Agriculture Organization's statistical database - the source of all national-level indicators used here.
        - **JMR - Joint Monitoring Report** — The World Bank's framework tracking food-security risk at sub-national (county/sub-county) level for climate, prices, exchange rates, and conflict.
        - **Alert Levels (Typical/Heightened/Critical)** — JMR risk ratings: 0 = Typical, 1 = Heightened, 2 = Critical. Applied per sub-county per indicator.
    """)

    st.markdown("**Tips for exploring:** Hover over any chart for exact values. Every chart carries a text insight "
                "explaining what the data means and why it matters. The sidebar always shows the status legend so you "
                "can decode colors instantly.")


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
        status = status_label(val, ind)
        unit = INDICATOR_META[ind]["unit"]
        with cols[idx % 3]:
            st.markdown(f"**{title}**")
            st.markdown(f"### {val:.1f} {unit}")
            st.markdown(f"{status} · {year}")


def executive_summary(analysis_df, county_risk_summary, latest_alert_date):
    st.header("Executive Summary - The Kenya Food Security Crisis at a Glance")
    act_banner(
        "",
        "The Paradox: Growth Without Food Security",
        "Kenya has grown richer for two decades and its farms produce nearly enough calories for everyone - yet the "
        "majority still cannot afford a healthy diet, about 1 in 3 are undernourished, and the burden falls hardest "
        "on children and on specific counties. This tab is the preview of that story.",
    )
    st.markdown(BIG_IDEA)
    story_roadmap()

    problem_statement()

    st.markdown("---")
    st.markdown("**How to read this dashboard:** Every chart uses one color system: green = acceptable, "
                "yellow = warning, and red = critical. Follow the tabs in order and you will move from the national "
                "picture down to the counties that need help most.")

    metric_cards(analysis_df)

    st.markdown("---")
    st.subheader("The Big Picture: Two Decades of Food Security")
    st.markdown("These three lines tell the core story of Kenya's food security: dietary energy supply has stayed "
                "flat, undernourishment has stubbornly persisted, and child stunting has slowly declined. The gap "
                "between energy adequacy (which is high) and undernourishment (which is also high) is the heart "
                "of the paradox - enough calories on paper, but not enough people actually getting them.")
    st.plotly_chart(plots.top_indicators_chart(analysis_df), use_container_width=True, key="chart_top_indicators")
    st.markdown(plots.top_indicators_insight(analysis_df))

    st.markdown("---")
    st.subheader("Correlation: GDP per Capita vs Food Insecurity")
    st.markdown("This scatter plot explores whether economic growth (GDP per capita) is associated with lower food "
                "insecurity. Each point represents one year. If growth helped, we would see a downward trend "
                "(higher GDP = lower insecurity). Hover over points for details.")
    st.plotly_chart(plots.correlation_chart(analysis_df), use_container_width=True, key="chart_correlation")
    st.markdown(plots.correlation_insight(analysis_df))

    st.markdown("---")
    st.subheader("The Crisis on a Map of Counties")
    st.markdown("National averages hide the geography of hunger. Here is the same story told county by county: "
                "which parts of Kenya are most affected, and which are least.")

    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(plots.county_alert_pie_chart(county_risk_summary, latest_alert_date), use_container_width=True, key="chart_county_pie")
        st.markdown(plots.county_pie_insight(county_risk_summary))
    with col_right:
        ml_n = st.slider("Counties to show (most affected):", min_value=3, max_value=20, value=5, step=1,
                         key="slider_most_affected")
        st.plotly_chart(plots.most_affected_chart(county_risk_summary, top_n=ml_n), use_container_width=True, key="chart_most_affected")
    st.markdown(plots.county_snapshot_insight(county_risk_summary, latest_alert_date))


def act1_availability(analysis_df):
    st.header("Act 1 · Availability - Is There Enough Food?")
    act_banner(
        "",
        "The Setup: Kenya Produces Enough Calories",
        "This is where the story begins. On paper, Kenya should be food secure: the domestic food supply meets "
        "roughly 93% of calorie needs. Hold on to that fact - it makes the next acts harder to believe.",
    )
    st.markdown("**What this measures:** Whether Kenya produces or imports enough food to meet its population "
                "nutritional needs. We track calories, protein, and fat available per person per day, plus the "
                "overall dietary energy adequacy - the percentage of calorie needs met by the food supply.")
    st.markdown("**Why this matters:** If a country cannot produce enough food, it must import the rest. Import "
                "dependence creates vulnerability to global price shocks, currency fluctuations, and supply chain "
                "disruptions.")

    st.subheader("Dietary Energy Supply Adequacy")
    st.markdown("This is the percentage of the population daily calorie needs that are met by the domestic food "
                "supply. A value of 100% means supply exactly meets demand. Below 100% means Kenya relies on imports "
                "or aid.")
    st.plotly_chart(plots.energy_adequacy_chart(analysis_df), use_container_width=True, key="chart_energy_adequacy")
    st.markdown(plots.energy_adequacy_insight(analysis_df))

    st.subheader("Food Supply Breakdown (per person per day)")
    st.markdown("These three metrics show the actual nutritional content available per Kenyan per day. Recommended "
                "minimums: **2,100 kcal**, **50 g protein**, **40 g fat**.")
    st.plotly_chart(plots.supply_breakdown_chart(analysis_df), use_container_width=True, key="chart_supply_breakdown")
    st.markdown(plots.supply_breakdown_insight(analysis_df))


def act2_access_nutrition(analysis_df, county_stats):
    st.header("Act 2 · Access and Child Nutrition - The Conflict")
    act_banner(
        "",
        "The Conflict: Food Exists, But People Cannot Afford It",
        "Here is the turn of the story. Kenya has the calories, yet most people cannot buy a nutritious diet. "
        "This is not scarcity - it is poverty. The affordability lines climb while the country grows richer, and "
        "the human cost shows up in stunted children.",
    )
    st.markdown("**What this measures:** Whether Kenyans can physically and economically access the food they need. "
                "Even when food is available, poverty prevents people from affording it. A healthy diet in Kenya "
                "costs roughly $3.20 per person per day, but the majority of the population cannot afford it.")
    st.markdown("**The paradox:** Kenya has adequate calorie supply (~93% of needs met) yet most people are food "
                "insecure. The problem is not scarcity, it is poverty and affordability.")

    st.subheader("Prevalence of Undernourishment")
    st.markdown("The percentage of the Kenyan population that consistently fails to meet their daily calorie "
                "requirements. WHO thresholds: below 15% = acceptable, 15-25% = warning, above 25% = critical.")
    st.plotly_chart(plots.undernourishment_chart(analysis_df), use_container_width=True, key="chart_undernourishment")
    st.markdown(plots.undernourishment_insight(analysis_df))

    st.markdown("---")
    st.subheader("Child Nutrition - The Human Cost")
    st.markdown("Food insecurity is not just a line on a chart - it is stunted children whose bodies and brains "
                "will never fully recover. This section shows the human cost that makes the affordability crisis urgent.")
    st.markdown("**What this measures:** The impact of food insecurity on children under 5. **Stunting** (too short "
                "for age) indicates chronic malnutrition; **wasting** (dangerously thin) indicates acute "
                "malnutrition. Both cause irreversible physical and cognitive damage.")
    st.markdown("**Why this matters:** Malnourished children do not grow to their full height or cognitive "
                "potential. This limits their education, earning capacity, and health for the rest of their lives, "
                "perpetuating the cycle of poverty.")
    st.markdown("**WHO thresholds:** Stunting: below 20% = acceptable, 20-30% = warning, above 30% = very high "
                "(critical). Wasting: below 5% = acceptable, 5-15% = warning, above 15% = critical.")
    st.plotly_chart(plots.child_nutrition_chart(analysis_df), use_container_width=True, key="chart_child_nutrition")
    st.markdown(plots.child_nutrition_insight(analysis_df))

    st.markdown("### Child Malnutrition by County")
    st.markdown("National trends hide the counties that are struggling. Select an indicator below - every county "
                "gets its own bar, and the insight updates to match your selection. Counties are ranked from worst "
                "to best using DHS 2022 data.")

    child_indicators = {k: plots.COUNTY_INDICATORS[k] for k in ["stunting_pct", "wasting_pct"]}
    ctl1, ctl2 = st.columns([2, 1])
    with ctl1:
        child_indicator = st.selectbox(
            "Choose an indicator to compare:",
            list(child_indicators.keys()),
            format_func=lambda k: child_indicators[k]["label"],
            key="select_child_indicator",
        )
    with ctl2:
        county_top_n = st.slider("Number of counties to show:", min_value=5, max_value=47, value=47, step=1,
                                 key="slider_county_top_n")
    st.plotly_chart(plots.county_indicator_bar_chart(county_stats, child_indicator, top_n=county_top_n),
                    use_container_width=True, key="chart_child_county")
    st.markdown(plots.county_indicator_insight(county_stats, child_indicator))


def act3_counties(county_alerts, county_risk_summary, county_geo_df, county_stats, latest_alert_date):
    st.header("Act 3 · County Risk and Comparisons")
    act_banner(
        "",
        "The Resolution: Finding the Hotspots",
        "National averages hide where the crisis actually bites. Act 3 zooms into Kenya's 47 counties to find who "
        "needs help first, maps the risk drivers (drought, prices, conflict), and compares counties on poverty "
        "and acute food insecurity to turn the story into a way forward in the final tab.",
    )

    st.subheader("Where Is the Crisis Worst? - County Risk Map")
    st.markdown(f"The national trend lines smooth away geography. This section zooms in on Kenya's 47 counties using "
                f"the World Bank Joint Monitoring Report (JMR), which tracks food-security risk at the sub-county "
                f"level across indicators including conflict, drought (NDVI and rainfall), exchange rates, and food "
                f"prices. **Latest data: {latest_alert_date.date()}**.")

    st.markdown("#### County Risk Choropleth Maps")
    st.markdown("These maps show the food-security risk level for each of Kenya's 47 counties. Darker red indicates "
                "higher risk. Hover over a county for its name and risk level.")
    map_choice = st.selectbox(
        "Select map to display:",
        ["Overall Alert Level", "Critical Alert Count"],
        key="select_map_choice",
    )
    st.plotly_chart(plots.choropleth_chart(county_geo_df, latest_alert_date, map_choice), use_container_width=True,
                    key="chart_choropleth")
    st.markdown(plots.county_map_insight(county_risk_summary, latest_alert_date))

    st.markdown("#### County Risk Ranking")
    st.markdown("Alert levels: **Typical** (0) | **Heightened** (1) | **Critical** (2)")

    col1, col2 = st.columns([2, 1])
    with col1:
        rank_n = st.slider("Number of counties in the ranking:", min_value=5, max_value=47, value=15, step=1,
                           key="slider_ranking")
        st.plotly_chart(plots.county_ranking_chart(county_risk_summary, latest_alert_date, top_n=rank_n),
                        use_container_width=True, key="chart_county_ranking")
        st.markdown(plots.county_ranking_insight(county_risk_summary, top_n=rank_n))
    with col2:
        st.markdown("##### Alert Summary")
        alert_counts = county_risk_summary["overall_alert_label"].value_counts()
        for label in ["Critical", "Heightened", "Typical"]:
            count = alert_counts.get(label, 0)
            pct = count / len(county_risk_summary) * 100
            st.markdown(f"**{label}:** {count} counties ({pct:.0f}%)")

        st.markdown("##### Most Affected")
        for _, row in county_risk_summary.head(5).iterrows():
            st.markdown(f"- **{row['adm1_name']}** - {row['overall_alert_label']}")

    st.markdown("#### County x Indicator Heatmap")
    st.markdown("This heatmap shows the maximum alert level for each county across all JMR indicators. Red means at "
                "least one sub-county in that county reached the critical level for that indicator.")
    latest_for_heatmap = county_alerts[county_alerts["date"] == latest_alert_date].copy()
    county_indicator_matrix = latest_for_heatmap.pivot_table(
        index=["adm1_pcode", "adm1_name"],
        columns="indicator",
        values="max_alert_level",
        aggfunc="max",
    ).reset_index()
    county_indicator_matrix.columns.name = None

    st.plotly_chart(plots.heatmap_chart(county_indicator_matrix, county_risk_summary, latest_alert_date),
                    use_container_width=True, key="chart_heatmap")
    st.markdown(plots.heatmap_insight(county_risk_summary))

    st.markdown("---")
    st.subheader("County Comparisons - Poverty by County")
    st.markdown("This section merges externally measured county poverty data with the JMR risk alerts so counties "
                "can be compared directly - no national averages, one bar per county. Poverty is the underlying "
                "driver that makes food unaffordable even when it is available.")

    st.markdown("#### Compare Counties on Poverty or Severe Poverty")
    st.markdown("Select an indicator below - every county gets its own bar, and the insight below the chart updates "
                "to match your selection.")

    poverty_indicators = {k: plots.COUNTY_INDICATORS[k] for k in ["poverty_pct", "severe_poverty_pct"]}
    pctl1, pctl2 = st.columns([2, 1])
    with pctl1:
        pov_indicator = st.selectbox(
            "Choose an indicator to compare:",
            list(poverty_indicators.keys()),
            format_func=lambda k: poverty_indicators[k]["label"],
            key="select_pov_indicator",
        )
    with pctl2:
        pov_top_n = st.slider("Number of counties to show:", min_value=5, max_value=47, value=47, step=1,
                              key="slider_pov_top_n")
    st.plotly_chart(plots.county_indicator_bar_chart(county_stats, pov_indicator, top_n=pov_top_n),
                    use_container_width=True, key="chart_pov_county")
    st.markdown(plots.county_indicator_insight(county_stats, pov_indicator))

    st.markdown("#### Share of Population in Acute Food Insecurity by County")
    st.markdown("The IPC analysis measures the share of each county's population in Phase 3+ (crisis) - the people "
                "who need help right now. Percentages make counties of very different sizes directly comparable.")
    st.plotly_chart(plots.county_crisis_chart(county_stats, top_n=pov_top_n), use_container_width=True,
                    key="chart_county_crisis")
    st.markdown(plots.county_crisis_insight(county_stats))


def conclusion_tab(analysis_df, county_risk_summary, latest_alert_date):
    st.header("Conclusion and Way Forward")
    act_banner(
        "The Resolution",
        "What the Data Demands",
        "Everything you saw - the abundance, the affordability failure, the stunted children, the county hotspots - "
        "points to one conclusion and one call to action.",
    )

    latest = analysis_df.sort_values("Year").dropna(subset=["undernourishment_pct"]).tail(1)
    year = int(latest["Year"].iloc[0]) if not latest.empty else 2025
    und = latest["undernourishment_pct"].iloc[0] if not latest.empty else 31.4
    ins = latest["moderate_or_severe_food_insecurity_pct"].iloc[0] if not latest.empty else 69.9
    stun = latest["under5_stunting_pct"].iloc[0] if not latest.empty else 18.3
    gdp = latest["gdp_per_capita_ppp"].iloc[0] if not latest.empty else 5800

    st.markdown("### 1. Conclusion - What the Data Tells Us")
    conclusions = [
        ("Growth is not translating into food security",
         f"GDP per capita reached about ${gdp:,.0f} in {year}, yet {ins:.0f}% of Kenyans are food insecure. "
         "Higher income has not lowered hunger - the gains are not reaching the poorest."),
        ("Scarcity is not the problem; affordability is",
         "Energy adequacy sits near 93%, meaning Kenya grows most of its calories - but a nutritious diet costs "
         "about $3.20 per person per day and the majority cannot afford it. People fill up on cheap staples but "
         "stay malnourished (hidden hunger)."),
        ("The human cost is concentrated in children",
         f"About {stun:.0f}% of under-5s are stunted - permanent cognitive and physical damage that is largely "
         "irreversible. Progress has been made, but millions of children are still left behind."),
        ("The crisis is geographical and targeted responses are possible",
         f"The JMR data ({latest_alert_date.date()}) shows some counties at critical risk driven by drought, food "
         "prices, exchange rates, and conflict. These hotspots are identifiable and can be prioritized."),
    ]
    for title, body in conclusions:
        section(title, body)

    st.markdown("### 2. Way Forward - Recommendations")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Immediate (0-2 years)**\n"
                    "- **Cash and food transfers** to the counties flagged critical on the risk map.\n"
                    "- **Subsidize or fortify staples** so affordable calories also carry protein and micronutrients.\n"
                    "- **Expand school feeding** to reach malnourished children where the data shows the worst outcomes.\n"
                    "- **Social protection** (e.g. Hunger Safety Net Program) targeted by the JMR alerts.")
    with col2:
        st.markdown("**Medium & Long Term (3-10 years)**\n"
                    "- **Agricultural productivity** - irrigation, drought-tolerant crops, and climate-resilient farming in ASALs.\n"
                    "- **Redistributive growth** - invest in rural livelihoods so GDP growth reaches the poorest.\n"
                    "- **Resilient supply chains** to buffer global price shocks and the exchange-rate volatility JMR tracks.\n"
                    "- **Early-warning systems** that act on county alerts before a crisis peaks.")

    st.markdown("### 3. The Data Story")

    gdp_growth = gdp - 2000

    st.markdown(f"**Enough food. Unaffordable to most. Worst for children and the counties in the north.** "
                f"Two decades of GDP growth (average income rose by roughly ${gdp_growth:,.0f} per capita) did not "
                f"end hunger: Kenya's problem is not a shortage of food, it is that the poorest cannot afford a "
                f"nutritious diet, leaving {und:.0f}% undernourished and the majority food-insecure, with children "
                f"bearing permanent damage. The counties already flagged as critical in the JMR data are where "
                f"intervention must start.")

    st.markdown("**Data availability and limitations:** National indicators come from FAOSTAT estimates "
                "(2000-2025); county risk from the World Bank JMR (2010-2026). Values are point-in-time estimates "
                "and may be revised by source agencies. Cross-check any headline figure with the raw data tables in "
                "the data folder.")
