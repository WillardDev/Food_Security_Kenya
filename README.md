# Food Security in Kenya — A Data Analysis (2016–2025)

Welcome to the Food Security in Kenya End-to-End Analysis Project. This project uses data analysis and visualization to examine Kenya's food security crisis — tracking national trends, identifying high-risk counties, and mapping risk patterns to inform policy and intervention strategies.

## Table of Contents
- [ Project Objectives](#project-objectives)
- [ Project Overview](#project-overview)
- [ Key Findings](#key-findings)
- [ Tools & Technologies](#tools--technologies)
- [ Visualizations](#visualizations)
- [ Dataset](#dataset)
- [ Future Enhancements](#future-enhancements)

---

##  Project Objectives

The primary goals of this project were to:

- Analyze Kenya's national food security trends using FAOSTAT (Food and Agriculture Organization Corporate Statistical Database) indicators from 2016–2025.
- Map county-level food security risk using the World Bank Joint Monitoring Report (JMR) data.
- Identify hotspot regions most vulnerable to food insecurity.
- Visualize trends in food availability, access, utilization, and stability.
- Provide actionable insights for policymakers, NGOs, and aid organizations.

---

## Project Overview

**What is Food Security?**

Food Security exists when all people, at all times, have physical, social, and economic access to sufficient, safe, and nourishing food that meets their dietary needs for an active and healthy life. It is measured across four key dimensions:

- **Availability:** Is there enough food produced or supplied?
- **Access:** Can people afford and physically reach food?
- **Utilization:** Is the food nutritious and safely prepared?
- **Stability:** Is access to food consistent over time, or disrupted by shocks?

## Food Security Indicators Explained

Think of food security as a four-legged stool: **Availability, Access, Utilization, and Stability**. This project tracks each through concrete metrics:

### Availability (Is there enough food?)

| Indicator | What it means | Good value |
|---|---|---|
| **Dietary Energy Supply Adequacy %** | How much of the population's daily calorie needs are met by domestic food supply | Higher is better (~100%) |
| **Food Supply (kcal/person/day)** | Average calories available per person per day | ~2,100–2,400 is typical; Kenya: ~2,100–2,200 |
| **Protein Supply (g/person/day)** | Average protein available per person per day | ~50–60g is adequate |
| **Fat Supply (g/person/day)** | Average fat available per person per day | ~40–60g is adequate |

### Access (Can people afford food?)

| Indicator | What it means | Good value |
|---|---|---|
| **Prevalence of Undernourishment %** | % of population consistently unable to meet calorie needs | Lower is better |
| **Number of People Undernourished (millions)** | Total people who are undernourished | Lower is better |
| **Moderate or Severe Food Insecurity %** | % of population experiencing anxiety about food or forced to skip meals | Lower is better |
| **Severe Food Insecurity %** | % of population who went entire days without eating | Lower is better |
| **Healthy Diet Cost (Int$/day)** | Cost of a nutritious diet per person per day in international dollars | Lower is better |
| **Prevalence of Unaffordability %** | % of population who cannot afford a healthy diet | Lower is better |
| **GDP per Capita (PPP)** | Economic output per person, adjusted for local prices — a proxy for purchasing power | Higher is better |

### Utilization (Is the food nutritious and safely used?)

| Indicator | What it means | Good value |
|---|---|---|
| **Under-5 Stunting %** | % of children under 5 too short for age (chronic malnutrition) | Lower is better; Kenya: ~18–19% |
| **Under-5 Wasting %** | % of children under 5 dangerously thin (acute malnutrition) | Lower is better; below 5% is good |

### In Plain English

- **Dietary energy adequacy at ~93%** — Kenya's food supply meets about 93% of what people need, leaving a 7% gap.
- **Undernourishment at ~30–35%** — roughly 1 in 3 Kenyans doesn't get enough calories regularly.
- **Food insecurity at ~70%** — 7 out of 10 Kenyans experience some level of food anxiety or meal-skipping.
- **~43 million Kenyans cannot afford a healthy diet** — more than half the population.
- **Stunting at ~18%** — nearly 1 in 5 children suffer permanent growth impairment from chronic malnutrition.

---

##  Problem Statement

Kenya faces persistent food insecurity due to climate variability (droughts, floods), economic shocks, displacement, and regional inequalities — particularly in arid and semi-arid lands (ASALs). This project applies data analysis to quantify and visualize these challenges.

### 1. Exploratory Data Analysis (EDA)

EDA is the process of summarizing and visually exploring a dataset to understand its structure, patterns, and anomalies before formal modeling.

**Data Cleaning:**
- Removed duplicate records and standardized column names across FAOSTAT and JMR datasets.
- Handled missing values through contextual imputation or exclusion.
- Merged JMR risk data with county boundary geometries for spatial analysis.

**Key Metrics Explored:**
- Yearly national food security indicator trends (2016–2025).
- County-level food security risk distribution.
- Cost and affordability of a healthy diet across regions.
- Food supply quantity and population trends.

### 2. Key Questions Answered

- Which counties face the highest food security risk?
- How have national food indicators changed over time?
- Is healthy diet affordability improving or worsening?
- Which regions require the most urgent intervention?
- What is the relationship between climate events and food insecurity spikes?

---

## Key Findings

*(To be completed after analysis — placeholder examples below)*

- X of 47 counties classified as high-risk in the most recent JMR report.
- [Specific indicator] has worsened by X% since 2016.
- Cost of a healthy diet exceeds the daily income of X% of households in ASAL counties.
- [Region] shows the strongest correlation between drought events and food insecurity spikes.

---

## Tools & Technologies

| Tool | Purpose |
| --- | --- |
| Python | Data collection, cleaning, analysis |
| Pandas | DataFrame manipulation and transformation |
| GeoPandas | Spatial data handling and county boundary joins |
| Matplotlib | Static visualizations and charts |
| Seaborn | Statistical visualizations and heatmaps |
| Plotly | Interactive charts and dashboards |
| Scikit-learn | Statistical modeling and correlation analysis |
| Jupyter Notebook | Documentation and reproducible analysis |

---

## Visualizations

Visualizations were developed using GeoPandas, Matplotlib, Seaborn, and Plotly:

- **County Risk Choropleth Map** — Color-coded map showing food security risk by county.
- **National Trend Lines** — Time-series plots of food security indicators over 2016–2025.
- **Diet Affordability Bar Charts** — Regional comparison of healthy diet costs.
- **Food Supply vs. Population** — Dual-axis analysis of supply adequacy.
- **Correlation Heatmap** — Relationships between food security indicators.
- **Risk Distribution Histogram** — Spread of JMR risk scores across counties.

---

## Dataset

All datasets are stored in the `data/` directory:

| File | Description | Source |
| --- | --- | --- |
| `ken_faostat_food_security_indicators.csv` | National food security metrics (availability, access, utilization, stability) | [FAOSTAT / HDX](https://data.humdata.org/dataset/ken-faostat-food-security-indicators) |
| `ken_faostat_food_balances.csv` | Kenya food supply and population records | [FAOSTAT / HDX](https://data.humdata.org/dataset/ken-faostat-food-security-indicators) |
| `ken_faostat_cost_affordability_healthy_diet.csv` | Cost and affordability of a healthy diet | [FAOSTAT / HDX](https://data.humdata.org/dataset/ken-faostat-food-security-indicators) |
| `KEN_JMR_data.zip` | Monthly admin-level food security risk indicators | [World Bank JMR](https://microdata.worldbank.org/catalog/8115) |
| `KEN_JMR_pcodes.zip` | Admin-level geographic codes for joining JMR data to counties | [World Bank JMR](https://microdata.worldbank.org/catalog/8115) |
| `kenya_counties.geojson` | Kenya county boundary polygons for mapping | GeoPandas compatible |

**What is FAOSTAT?** The Food and Agriculture Organization Corporate Statistical Database — the UN's primary source for food and agriculture statistics across countries.

**What is JMR?** Joint Monitoring Report — the World Bank's framework for tracking food security risk at sub-national administrative levels.

---

## Future Enhancements

- Build an interactive web dashboard with Plotly Dash or Streamlit.
- Deploy a conversational AI agent to answer questions about food security in Kenya.
- Integrate real-time climate data (rainfall, NDVI) for predictive modeling.
- Automate daily/weekly data pipeline updates.
- Add county-level time-series forecasting for risk prediction.
- Partner with NGOs for data validation and ground-truthing.

---
