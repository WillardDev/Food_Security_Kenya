import streamlit as st
import warnings

warnings.filterwarnings("ignore")

from dashboard.config import SAFE, WARNING, DANGER, CSS
from dashboard.data import load_all, build_analysis_df, build_county_data, load_county_external, build_county_stats
from dashboard import tabs

st.set_page_config(
    page_title="Food Security in Kenya",
    page_icon=":bar_chart:",
    layout="wide",
)

st.markdown('<a id="top" style="position:absolute;"></a>', unsafe_allow_html=True)

st.markdown(CSS, unsafe_allow_html=True)

st.title("Food Security in Kenya - A Data Story")
st.markdown("*An interactive analysis of national trends, county risk, and the affordability crisis threatening millions of Kenyans.*")
st.markdown("---")

with st.spinner("Loading data..."):
    food_security, food_balances, healthy_diet, jmr_data, jmr_pcodes, kenya_counties = load_all()
    analysis_df = build_analysis_df(food_security, food_balances, healthy_diet)
    county_alerts, county_risk_summary, county_geo_df, latest_alert_date = build_county_data(
        jmr_data, jmr_pcodes, kenya_counties
    )
    county_external = load_county_external()
    county_stats = build_county_stats(county_risk_summary, county_external)

with st.sidebar:
    st.header("Dashboard Controls")
    st.markdown("---")
    st.markdown("### Status Legend")
    st.markdown(f"<span style=\"color:{SAFE}\">Acceptable</span> - Within safe range", unsafe_allow_html=True)
    st.markdown(f"<span style=\"color:{WARNING}\">Warning</span> - Needs attention", unsafe_allow_html=True)
    st.markdown(f"<span style=\"color:{DANGER}\">Critical</span> - Immediate action required", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### About the Data")
    st.markdown("- **FAOSTAT**: UN FAO national statistics (2000-2025)")
    st.markdown("- **World Bank JMR**: County/sub-county risk (2010-2026)")
    st.markdown("- **Coverage**: 47 counties, 6+ risk indicators")
    st.markdown("- **Learn**: See the *About & Learn* tab for terms and research questions")

tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "About & Learn", "Problem Statement", "Executive Summary", "Availability",
    "Access and Affordability", "Child Nutrition", "County Risk Map",
    "County Comparisons", "Conclusion & Way Forward",
])

with tab0:
    tabs.about()

with tab1:
    tabs.problem_statement()

with tab2:
    tabs.tab1(analysis_df, county_risk_summary, latest_alert_date)

with tab3:
    tabs.tab2(analysis_df)

with tab4:
    tabs.tab3(analysis_df)

with tab5:
    tabs.tab4(analysis_df)

with tab6:
    tabs.tab5(county_alerts, county_risk_summary, county_geo_df, latest_alert_date)

with tab7:
    tabs.tab6(county_stats, latest_alert_date)

with tab8:
    tabs.tab7(analysis_df, county_risk_summary, latest_alert_date)

st.markdown('<a href="#top" class="back-to-top" title="Back to top">&#8593;</a>', unsafe_allow_html=True)