import streamlit as st
import warnings

warnings.filterwarnings("ignore")

from dashboard.config import SAFE, WARNING, DANGER, CSS
from dashboard.data import load_all, build_analysis_df, build_county_data
from dashboard import tabs

st.set_page_config(
    page_title="Food Security in Kenya",
    page_icon=":bar_chart:",
    layout="wide",
)

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

with st.sidebar:
    st.header("Dashboard Controls")
    st.markdown("---")
    st.markdown("### Status Legend")
    st.markdown(f"<span style=\"color:{SAFE}\">Acceptable</span> - Within safe range", unsafe_allow_html=True)
    st.markdown(f"<span style=\"color:{WARNING}\">Warning</span> - Needs attention", unsafe_allow_html=True)
    st.markdown(f"<span style=\"color:{DANGER}\">Critical</span> - Immediate action required", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### About the Data")
    st.markdown("- **FAOSTAT**: UN FAO national statistics")
    st.markdown("- **World Bank JMR**: County-level risk monitoring")
    st.markdown("- **Coverage**: 2000-2025 (national), 2010-2026 (county)")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Summary", "Availability", "Access and Affordability",
    "Child Nutrition", "County Risk Map",
])

with tab1:
    tabs.tab1(analysis_df)

with tab2:
    tabs.tab2(analysis_df)

with tab3:
    tabs.tab3(analysis_df)

with tab4:
    tabs.tab4(analysis_df)

with tab5:
    tabs.tab5(county_alerts, county_risk_summary, county_geo_df, latest_alert_date)