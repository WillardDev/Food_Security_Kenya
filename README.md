# Food Security in Kenya — A Data Story

Welcome to the Food Security in Kenya End-to-End Analysis Project. This project uses data analysis and interactive visualization to examine Kenya's food security crisis — tracking national trends, identifying high-risk counties, and mapping risk patterns to inform policy and intervention strategies.

It pairs two complementary artifacts:

- **`app.py`** — an interactive **Streamlit dashboard** that tells the full data story in nine tabs.
- **`notebooks/Food_Security.ipynb`** — a reproducible **Jupyter notebook** that mirrors the exact same visualizations and order as the app.

## Table of Contents
- [Project Objectives](#project-objectives)
- [Repository Structure](#repository-structure)
- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Primary Research Question](#primary-research-question)
- [Key Findings](#key-findings)
- [Tools & Technologies](#tools--technologies)
- [Visualizations](#visualizations)
- [Dataset](#dataset)
- [Running the Dashboard](#running-the-dashboard)
- [Future Enhancements](#future-enhancements)

---

## Project Objectives

- Analyze Kenya's national food security trends using FAOSTAT (Food and Agriculture Organization Corporate Statistical Database) indicators.
- Map county-level food security risk using the World Bank Joint Monitoring Report (JMR) data.
- Identify hotspot regions most vulnerable to food insecurity.
- Visualize trends in food availability, access, utilization, and stability.
- Provide actionable insights for policymakers, NGOs, and aid organizations — through both an interactive dashboard and a reproducible notebook.

---

## Repository Structure

```
food_security/
├── app.py                     
├── dashboard/                 
│   ├── __init__.py
│   ├── config.py              
│   ├── data.py                
│   ├── insights.py            
│   ├── plots.py               
│   └── tabs.py                
│                            
├── notebooks/
│   └── Food_Security.ipynb    
├── data/
│   ├── ken_faostat_*.csv      
│   ├── kenya_dhs_nutrition_county.csv   
│   ├── kenya_poverty_rate_county.csv     
│   ├── kenya_ipc_area_long_latest.csv    
│   ├── world_bank_jmr/        
│   └── shapefiles/            
└── README.md
```
---

## Project Overview

**What is Food Security?**

Food Security exists when all people, at all times, have physical, social, and economic access to sufficient, safe, and nourishing food that meets their dietary needs for an active and healthy life. It is measured across four key dimensions:

- **Availability:** Is there enough food produced or supplied?
- **Access:** Can people afford and physically reach food?
- **Utilization:** Is the food nutritious and safely prepared?
- **Stability:** Is access to food consistent over time, or disrupted by shocks?

## Problem Statement

Kenya faces persistent food insecurity due to climate variability (droughts, floods), economic shocks, displacement, and regional inequalities — particularly in arid and semi-arid lands (ASALs). This project applies data analysis to quantify and visualize these challenges.

### 1. Exploratory Data Analysis (EDA)

**Data Cleaning:**
- Removed duplicate records and standardized column names across FAOSTAT and JMR datasets.
- Handled missing values through contextual imputation or exclusion.
- Merged JMR risk data with county boundary geometries for spatial analysis.

**Key Metrics Explored:**
- Yearly national food security indicator trends.
- County-level food security risk distribution.
- Cost and affordability of a healthy diet across regions.
- Food supply quantity and population trends.

### 2. Key Questions Answered

- Which counties face the highest food security risk?
- How have national food indicators changed over time?
- Is healthy diet affordability improving or worsening?
- Which regions require the most urgent intervention?
- What is the relationship between economic growth (GDP) and food insecurity?

---

## The Data Story

The dashboard is deliberately shaped as a narrative, following the principles of *Storytelling with Data*
(Cole Nussbaumer Knaflic): one **Big Idea**, repeated across every tab, told in **three acts**.

**The Big Idea:** Kenya grows enough food for everyone, yet two decades of economic growth have not ended
hunger — because the crisis is *affordability, not scarcity*, and its worst face is *children* and *specific counties*.

| Act | Story beat | Tabs | What the viewer learns |
|---|---|---|---|
| **Act 1 · The Setup** | "Kenya has enough food." | Availability | Energy adequacy ~93% — this is not a famine |
| **Act 2 · The Conflict** | "…but people can't afford it." | Executive Summary, Access, Child Nutrition | Affordability vs GDP; children bear the cost |
| **Act 3 · The Resolution** | "…and it's worst in these places." | County Risk, County Comparisons, Conclusion | Identify hotspots, verify the alerts, act |

Every tab opens with an act banner and a recurring Big Idea reminder ("tell 'em, tell 'em, tell 'em"); the
Executive Summary is the *Bing* (what you'll tell them) and the Conclusion is the *Bongo* (what you told them).
Charts use preattentive color (the story-critical series is red), direct labels instead of legend lookups,
threshold reference lines with shaded critical zones, and no chart border or vertical gridlines (clutter is the enemy).

## Primary Research Question

> **Why does economic growth in Kenya not translate into improved food security, and where is the crisis worst?**

The visualization that directly answers this is the **GDP per Capita vs Food Insecurity scatter plot** (Tab 1),
which shows that higher GDP was NOT associated with lower food insecurity. The **county choropleth maps**
(Tab 5) answer *where* the crisis is worst. See the **About** tab in the app for a full breakdown of
every research question and which chart answers it.

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

---

## Key Findings

- The number of undernourished Kenyans has grown from ~10 million (2002) to ~20 million (2025), driven by population growth outpacing food system improvements.
- Food insecurity (moderate or severe) affects the majority of Kenyans and has worsened significantly since 2016.
- Despite GDP per capita nearly doubling over two decades, food insecurity did not fall — **economic growth alone does not solve food insecurity**; income inequality and affordability gaps persist.
- Millions of Kenyans cannot afford a healthy diet, explaining why child stunting remains high despite adequate calorie supply ("hidden hunger").
- A subset of Kenya's 47 counties are at critical risk across multiple JMR indicators (drought, food prices, exchange rates, conflict) and should be prioritized for intervention.

---

## Tools & Technologies

| Tool | Purpose |
| --- | --- |
| Python | Data collection, cleaning, analysis |
| Pandas | DataFrame manipulation and transformation |
| GeoPandas | Spatial data handling and county boundary joins |
| Matplotlib | Static visualizations and charts (notebook) |
| Seaborn | Statistical visualizations and heatmaps |
| Plotly | Interactive charts and dashboards (app) |
| Streamlit | Interactive web dashboard |
| Jupyter Notebook | Documentation and reproducible analysis |

---

## Visualizations

Both the app and the notebook present the same charts in the same order. The dashboard opens with an educational first tab:

- **Primary Research Question** — *"Why does economic growth in Kenya not translate into improved food security, and where is the crisis worst?"*
- **Problem Statement**
- **Key Indicators Over Time**
- **GDP per Capita vs Food Insecurity**
- **County Risk Pie + Most/Least Affected**
- **Dietary Energy Supply Adequacy**
- **Food Supply Breakdown**
- **Prevalence of Undernourishment**
- **Food Insecurity Severity** 
- **The Affordability Crisis**
- **Child Stunting and Wasting**
- **Counties at Risk Over Time**
- **County Risk Choropleth Maps**
- **County Risk Ranking**
- **County × Indicator Heatmap**
- **County Comparisons (Tab 7)**
  - **Indicator bar charts**
  - **People in acute food insecurity**
  - **Cross-check scatter**

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
| `kenya_dhs_nutrition_county.csv` | County-level child stunting & wasting (DHS 2022) | [HDX / DHS](https://data.humdata.org/dataset/dhs-subnational-data-for-kenya) |
| `kenya_poverty_rate_county.csv` | County-level poverty rates, MPI & severe poverty (2022) | [HDX / HAPI](https://data.humdata.org/dataset/hdx-hapi-ken) |
| `kenya_ipc_area_long_latest.csv` | County-level IPC acute food insecurity (people in Phase 3+, Feb 2026) | [HDX / IPC](https://data.humdata.org/dataset/kenya-acute-food-insecurity-country-data) |

**What is FAOSTAT?** The Food and Agriculture Organization Corporate Statistical Database — the UN's primary source for food and agriculture statistics across countries.

**What is JMR?** Joint Monitoring Report — the World Bank's framework for tracking food security risk at sub-national administrative levels.

---

## Running the Dashboard

1. Install dependencies:

   ```bash
   pip install streamlit pandas numpy matplotlib seaborn geopandas plotly jupyter
   ```

2. Launch the Streamlit app from the project root:

   ```bash
   streamlit run app.py
   ```

3. (Optional) Re-run the notebook, which mirrors the same analysis:

   ```bash
   jupyter notebook notebooks/Food_Security.ipynb
   ```

---

## Future Enhancements

- Deploy the Streamlit dashboard to the cloud (Streamlit Community Cloud / Hugging Face Spaces) — note that deployment will require regenerating a `requirements.txt` (e.g. `pip freeze > requirements.txt`).
- Add a conversational AI agent to answer questions about food security in Kenya.
- Integrate real-time climate data (rainfall, NDVI) for predictive modeling.
- Automate daily/weekly data pipeline updates.
- Add county-level time-series forecasting for risk prediction.
- Partner with NGOs for data validation and ground-truthing.

---