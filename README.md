# Food Security in Kenya — A Data Story

Welcome to the Food Security in Kenya End-to-End Analysis Project. This project uses data analysis and interactive visualization to examine Kenya's food security crisis — tracking national trends, identifying high-risk counties, and mapping risk patterns to inform policy and intervention strategies.

It pairs two complementary artifacts:

- **`app.py`** — an interactive **Streamlit dashboard** that tells the full data story in five tabs.
- **`notebooks/Food_Security.ipynb`** — a reproducible **Jupyter notebook** that mirrors the exact same visualizations and order as the app.

## Table of Contents
- [Project Objectives](#project-objectives)
- [Repository Structure](#repository-structure)
- [Project Overview](#project-overview)
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
├── app.py                     # Streamlit entry point (thin orchestration layer)
├── dashboard/                 # Modular Python package imported by app.py
│   ├── __init__.py
│   ├── config.py              # Colors, thresholds, indicator metadata, CSS
│   ├── data.py                # Data loading, cleaning, and building
│   ├── insights.py            # Status logic and narrative insight text
│   ├── plots.py               # All chart-building functions (one per chart)
│   └── tabs.py                # Tab renderers (Executive, Availability, Access,
│                              #   Child Nutrition, County Risk Map)
├── notebooks/
│   └── Food_Security.ipynb    # Full analysis, mirroring the app's charts
├── data/
│   ├── ken_faostat_*.csv      # National-level FAOSTAT data
│   ├── world_bank_jmr/        # County/sub-county JMR risk data (zip)
│   └── shapefiles/            # Kenya county boundaries (GeoJSON)
├── requirements.txt           # Pinned Python dependencies
└── README.md
```

**Why modular?** Each major concern lives in its own file inside `dashboard/`, so
`app.py` stays short and each chart / insight is easy to find, test, and extend:

| Module | Responsibility |
|---|---|
| `config.py` | Single source of truth for colors, thresholds, and labels |
| `data.py` | Cached loading + cleaning + building of `analysis_df` and county data |
| `insights.py` | Threshold → status color/label mapping and narrative insights |
| `plots.py` | Pure functions that return a Plotly figure (one per chart) |
| `tabs.py` | Composes charts + insights into the five dashboard tabs |

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
- **Undernourishment at ~30+%** — roughly 1 in 3 Kenyans doesn't get enough calories regularly.
- **Food insecurity at ~70%** — 7 out of 10 Kenyans experience some level of food anxiety or meal-skipping.
- **~43 million Kenyans cannot afford a healthy diet** — more than half the population.
- **Stunting at ~18%** — nearly 1 in 5 children suffer permanent growth impairment from chronic malnutrition.

---

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

Both the app and the notebook present the same charts in the same order:

### Tab 1 — Executive Summary
- **Key Food Security Indicators Over Time** — line chart combining undernourishment, food insecurity, and energy adequacy
- **GDP per Capita vs Food Insecurity** — scatter plot showing the paradox of growth without food security

### Tab 2 — Availability
- **Dietary Energy Supply Adequacy** — line chart vs 100% target, 95% warning, 90% critical lines
- **Food Supply Breakdown** — calories, protein, and fat per person per day (line charts with thresholds)

### Tab 3 — Access & Affordability
- **Prevalence of Undernourishment** — line chart vs 15% / 25% WHO thresholds
- **Food Insecurity Severity** — moderate/severe vs severe line chart
- **The Affordability Crisis** — cost of healthy diet, % cannot afford, people unable (all line charts, since they are trends)

### Tab 4 — Child Nutrition
- **Child Stunting and Wasting** — two-panel line chart with WHO thresholds
- **GDP per Capita** — line chart providing economic context

### Tab 5 — County Risk Map
- **County Risk Choropleth Maps** — overall alert level + critical alert count
- **County Risk Ranking** — top 15 highest-risk counties (stacked bar)
- **County × Indicator Heatmap** — alert level per indicator per county

Every trend chart uses a consistent color system: **green** = acceptable, **yellow** = warning, **red** = critical. Each chart is followed by a narrative insight box explaining what the data means.

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

## Running the Dashboard

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Launch the Streamlit app from the project root:

   ```bash
   streamlit run app.py
   ```

3. (Optional) Re-run the notebook, which mirrors the same analysis:

   ```bash
   jupyter notebook notebooks/Food_Security.ipynb
   ```

> **Note on data paths:** The notebook lives in `notebooks/` and references its data via
> `../data`, so both the app and the notebook resolve the same datasets.

---

## Future Enhancements

- Deploy the Streamlit dashboard to the cloud (Streamlit Community Cloud / Hugging Face Spaces).
- Add a conversational AI agent to answer questions about food security in Kenya.
- Integrate real-time climate data (rainfall, NDVI) for predictive modeling.
- Automate daily/weekly data pipeline updates.
- Add county-level time-series forecasting for risk prediction.
- Partner with NGOs for data validation and ground-truthing.