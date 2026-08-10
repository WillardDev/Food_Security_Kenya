# Food Security Analysis in Kenya

A data analysis and visualization project examining food security trends, malnutrition patterns, and acute food insecurity across Kenya's 47 counties.

---

## 📊 Dataset Overview

The project leverages multiple publicly available datasets to analyze food security in Kenya:

| Dataset | Source | Key Variables | Time Period |
|---------|--------|---------------|-------------|
| Suite of Food Security Indicators | FAOSTAT / HDX | Food availability, access, utilization, stability metrics across 4 dimensions | 2000–2024   |
| IPC Acute Food Insecurity Data | IPC / ReliefWeb | Food insecurity phases, population affected, projections | 2025–2026   |
| Food Prices Database | WFP / FAOSTAT | Prices for maize, rice, beans, fish, sugar | Ongoing   |
| FEWS NET Staple Food Price Data | FEWS NET | Monthly staple food price data | 2005–present   |
| Kenya Agricultural Census | KNBS | Household farming data (6.3M households), crop/livestock patterns | 2025 Census   |
| NDMA Drought Early Warning Bulletin | NDMA | Child malnutrition (MUAC), drought phases by county | Monthly   |

**Dataset Size:** 2,278+ price records, 6.3M households covered, 47 counties  
**Geographic Coverage:** All 47 counties, with focus on 23 ASAL counties

---

## 🎯 Project Objective

Analyze and visualize the drivers and patterns of food insecurity in Kenya, identifying high-risk counties and quantifying the scale of malnutrition and acute food insecurity to inform evidence-based interventions.

---

## 🔍 Key Research Questions

1. **What is the current scale and geographic distribution of food insecurity in Kenya?** An estimated **3.3 million people** are in IPC Phase 3 (Crisis) or above as of early 2026, a **52% increase** from 2.15 million in early 2025. Of these, **400,000 people** are in IPC Phase 4 (Emergency) requiring immediate, life-saving assistance. Refugee settlements in Dadaab, Kakuma, and Kalobeyei have approximately **429,000 people** in Phase 4 (Emergency). Projections indicate **3.7 million people** will face crisis-level hunger by April–June 2026.  

2. **Which counties face the highest malnutrition burden, and what are the key drivers?** Nearly **810,900 children under five** require treatment for acute malnutrition in 2026, up from 760,488 in 2025. Over **202,000 children** suffer from the most severe form. The proportion of children at risk has climbed from 13.1% to 16%. An additional **116,800 pregnant and breastfeeding women** need nutritional support.   Most affected: Turkana (nearly 96,000 children needing treatment), Mandera (over 86,000), and three areas at IPC Phase 5—Mandera, North Horr (Marsabit), and Turkana South/East—where at least 1 in 3 children is acutely malnourished.  

3. **What are the primary drivers of food insecurity and malnutrition?** Below-average and erratic October–December 2025 rains caused widespread crop failure, poor pasture regeneration, and inadequate water source recovery. Severe drought conditions have led to livestock collapse—in Mandera, daily household milk consumption plummeted from 0.9 litres (October 2025) to just 0.1 litres (January 2026), directly pushing children into acute malnutrition. Poor health-seeking behavior, high disease burden, and suboptimal infant/young child feeding practices continue to undermine nutrition outcomes.  

4. **How have food price dynamics affected food access?** Food price volatility in staple foods (maize, potatoes, sorghum) makes it difficult to plan interventions and manage supply chains. An existing ML system processing 2,278+ monthly price records has demonstrated the feasibility of classifying volatility into Low, Medium, High, and Extreme categories.  

5. **How does agricultural dependence correlate with food security?** With 60.7% of 6.3M Kenyan households depending heavily on agriculture (primarily maize, beans, cattle, poultry), disruptions in agricultural production directly translate to food insecurity. Average household size is 4.51 persons, indicating both high labor availability and high dependency.  

---

## 🛠️ Technologies Used

- **Python** - Programming language
- **Pandas** - Data manipulation and merging of multiple datasets
- **Geopandas** - Geospatial mapping of county-level food security data
- **Seaborn** - Statistical visualizations and heatmaps
- **Matplotlib** - Custom visualizations
- **Scikit-learn** - Predictive modeling for food insecurity classification 
- **XGBoost** - Advanced machine learning for price volatility prediction 
- **Jupyter Notebook** - Development environment

---

## 📁 Project Structure

```
kenya-food-security-analysis/
├── data/
│   ├── faostat_food_security_indicators.csv
│   ├── ipc_acute_food_insecurity_2026.csv
│   ├── food_prices_kenya.csv
│   ├── ndma_malnutrition_data.csv
│   ├── agricultural_census_kenya.csv
│   └── kenya_counties_shapefile/
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_food_insecurity_mapping.ipynb
│   ├── 03_malnutrition_analysis.ipynb
│   ├── 04_food_price_volatility.ipynb
│   └── 05_risk_prediction_model.ipynb
├── src/
│   ├── data_preprocessing.py
│   ├── county_analysis.py
│   └── visualization.py
├── results/
│   ├── maps/
│   │   ├── food_insecurity_phase_map.png
│   │   ├── malnutrition_burden_map.png
│   │   └── vulnerability_index_map.png
│   ├── charts/
│   │   ├── malnutrition_trends.png
│   │   ├── food_prices_trends.png
│   │   ├── county_comparison.png
│   │   └── ipc_phase_distribution.png
│   └── model_results/
│       └── feature_importance.png
├── requirements.txt
└── README.md
```

---

## 📊 Analysis Components

### 1. Food Security Indicators Analysis
- Four dimensions of food security: availability, access, utilization, stability 
- Time-series analysis of food security trends (2000–2024) 
- County-level comparison using FAOSTAT Suite of Food Security Indicators

### 2. Acute Food Insecurity Mapping (IPC)
- Classification of counties by IPC Phase (1–5) 
- 3.3M in Crisis or worse (Phase 3+), 400,000 in Emergency (Phase 4) 
- **23 ASAL counties** most affected 
- 3.7M projected in Crisis or worse by April–June 2026 
- Refugee settlements: 429,000 in Phase 4 (Emergency) 

### 3. Malnutrition Crisis Analysis
- **810,900 children under five** needing acute malnutrition treatment 
- **202,000+ children** suffering from severe acute malnutrition 
- **16% of children at risk** (up from 13.1%) 
- **116,800 pregnant/breastfeeding women** needing nutritional support 
- Three areas at **IPC Phase 5 (most critical)**: Mandera, North Horr (Marsabit), Turkana South/East 
- County-level distribution: Turkana (96,000+ children needing treatment), Mandera (86,000+) 

### 4. Food Price Volatility Analysis
- Staple foods: maize, potatoes, sorghum 
- 2,278+ monthly price records 
- Volatility classification: Low, Medium, High, Extreme 
- Engineering of 21 features including lagged price changes, rolling volatility metrics 

### 5. Agricultural Dependence & Food Security Linkage
- 60.7% of 6.3M households depend on agriculture 
- Dominant crops: maize, beans 
- Dominant livestock: cattle, poultry 
- Average household size: 4.51 persons 
- Link to drought impacts: crop failure, livestock collapse, reduced milk consumption (0.9L to 0.1L in Mandera) 

---

## 📈 Key Findings Summary

### Current Crisis
| Metric | Value | Source |
|--------|-------|--------|
| People in IPC Phase 3+ (Jan–Mar 2026) | 3.3 million |  |
| People in IPC Phase 4 (Emergency) | 400,000 |  |
| Projected in Phase 3+ (Apr–Jun 2026) | 3.7 million |  |
| Children requiring malnutrition treatment | 810,900 |  |
| Children with severe acute malnutrition | 202,000+ |  |
| Pregnant/breastfeeding women needing support | 116,800 |  |
| Refugee settlement population in Phase 4 | 429,000 |  |

### Most Affected Counties
- **Turkana**: 96,000+ children needing treatment, multiple areas in IPC Phase 5 
- **Mandera**: 86,000+ children needing treatment, IPC Phase 5 
- **North Horr (Marsabit)**: IPC Phase 5 
- **Turkana South/East**: IPC Phase 5 
- **Garissa, Isiolo, Wajir, Embu, Kilifi, Narok, Tharaka Nithi**: Critical malnutrition 
- Other high-burden: Kwale, Lamu, Meru, Kitui 

### Key Drivers
- Below-average October–December 2025 rains 
- Widespread crop failure 
- Poor pasture regeneration 
- Inadequate water source recovery 
- Livestock collapse (milk consumption dropped 89% in Mandera) 
- Poor health-seeking behavior 
- High disease burden (cholera, measles, kala-azar) 
- Suboptimal infant/young child feeding practices 

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install pandas geopandas numpy scikit-learn matplotlib seaborn jupyter xgboost
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/kenya-food-security-analysis.git
cd kenya-food-security-analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download Kenya county shapefile from Humanitarian Data Exchange

4. Run the Jupyter notebooks:
```bash
jupyter notebook notebooks/01_exploratory_analysis.ipynb
```

---

## 🔮 Usage Example

```python
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
faostat = pd.read_csv('data/faostat_food_security_indicators.csv')
ipc_data = pd.read_csv('data/ipc_acute_food_insecurity_2026.csv')
ndma = pd.read_csv('data/ndma_malnutrition_data.csv')

# Load Kenya counties shapefile
kenya = gpd.read_file('data/kenya_counties_shapefile/kenya_counties.shp')

# Merge data with spatial data
food_insecurity_map = kenya.merge(ipc_data, on='county')

# Create IPC phase map
fig, ax = plt.subplots(1, 1, figsize=(12, 15))
food_insecurity_map.plot(column='ipc_phase', 
                         cmap='RdYlGn_r', 
                         legend=True,
                         ax=ax)
ax.set_title('IPC Acute Food Insecurity Phase by County, Jan-Mar 2026', fontsize=16)
plt.savefig('results/maps/food_insecurity_phase_map.png')

# Create malnutrition analysis
malnutrition = ndma.groupby('county')['children_needing_treatment'].sum().sort_values(ascending=False)
plt.figure(figsize=(12, 8))
malnutrition.head(10).plot(kind='barh')
plt.title('Top 10 Counties by Children Needing Acute Malnutrition Treatment')
plt.savefig('results/charts/malnutrition_burden.png')
```

---

## 📊 Visualizations Created

1. **IPC Acute Food Insecurity Phase Map** - 23 ASAL counties showing Phase 3+ classifications 
2. **Children Needing Malnutrition Treatment by County** - County-level burden ranking 
3. **Food Price Volatility Dashboard** - Classification of staple food volatility trends 
4. **Drought Phase Map** - NDMA drought classifications (Alarm, Alert, Pre-Alert, Normal) 
5. **Malnutrition Trends Dashboard** - 13.1% → 16% children at risk 
6. **Food Security Indicators Time-Series** - 2000–2024 trends 

---

## 🌍 Data Sources

| Source | Description |
|--------|-------------|
| **FAOSTAT / HDX** | Suite of Food Security Indicators (2000–2024), 4 dimensions of food security  |
| **IPC / ReliefWeb** | Acute Food Insecurity classifications, projections 2025–2026  |
| **WFP Price Database** | Food prices for Kenya (maize, rice, beans, fish, sugar)  |
| **FEWS NET** | Staple food price data (2005–present), acute food insecure population estimates  |
| **NDMA** | Drought Early Warning Bulletins, child malnutrition data (MUAC)  |
| **KNBS** | Agricultural Census 2025, 6.3M households data  |

---

## 💡 Policy & Humanitarian Applications

- **Early Warning Systems**: Identify counties at risk before shocks hit 
- **Resource Allocation**: Target high-burden counties (Turkana, Mandera, Marsabit) 
- **Nutrition Interventions**: Prioritize treatment commodities for counties with >86,000 children needing treatment 
- **Drought Response**: Direct interventions to counties in Alarm phase (Mandera, Wajir, Kilifi, Kwale) 
- **Food Price Monitoring**: Early warning for price instability to guide market interventions 
- **Optima Nutrition Modeling**: Scale up evidence-based nutrition interventions (IFA fortification, vitamin A, cash transfers) in 24 high-risk counties 

---

## 📝 Data Availability Summary

All datasets identified are **publicly available**:

| Dataset | Access |
|---------|--------|
| FAOSTAT Food Security Indicators | HDX download  |
| IPC AFI Country Data | ReliefWeb / ipcinfo.org  |
| WFP Food Prices | ReliefWeb / WFP Price Database  |
| NDMA Bulletins | NDMA website  |
| FEWS NET Data | ReliefWeb  |

---

## 🙏 Acknowledgments

- IPC for acute food insecurity classification data 
- FAOSTAT for food security indicator data 
- NDMA for drought early warning and malnutrition data 
- WFP for food price database 
- KNBS for agricultural census data 