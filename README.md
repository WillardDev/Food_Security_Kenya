# Food Security in Kenya

This project explores Kenya food security trends and county-level risk patterns using FAOSTAT data from HDX and sub-national World Bank Joint Food Security Monitor data.

FAOSTAT / HDX source: https://data.humdata.org/dataset/ken-faostat-food-security-indicators

World Bank JMR source: https://microdata.worldbank.org/catalog/8115

## Dataset Overview

The project uses FAOSTAT Kenya food security files downloaded from HDX and World Bank JMR files for sub-national county analysis:

| File | Description |
| --- | --- |
| `data/ken_faostat_food_security_indicators.csv` | Food security indicator values for Kenya, including measures related to availability, access, utilization, and stability. |
| `data/ken_faostat_food_balances.csv` | Kenya food balance data, including population and food supply-related records. |
| `data/ken_faostat_cost_affordability_healthy_diet.csv` | Cost and affordability of a healthy diet data for Kenya. |
| `data/world_bank_jmr/KEN_JMR_data.zip` | Monthly World Bank JMR admin-2 food security risk indicators for Kenya. |
| `data/world_bank_jmr/KEN_JMR_pcodes.zip` | Admin-2 and county p-code lookup used to join JMR data to counties. |
| `data/shapefiles/kenya_counties.geojson` | Kenya county boundaries used for GeoPandas county maps. |

## Project Objective

The goal of this project is to examine national food security trends and map county-level food security risk using Python data analysis and GeoPandas.

## Technologies Used

- Python
- Pandas
- GeoPandas
- Matplotlib
- Seaborn
- Jupyter Notebook

## Project Structure

```text
food_securtiy/
├── data/
│   ├── shapefiles/
│   │   ├── .gitkeep
│   │   └── kenya_counties.geojson
│   ├── world_bank_jmr/
│   │   ├── KEN_JMR_data.zip
│   │   └── KEN_JMR_pcodes.zip
│   ├── ken_faostat_cost_affordability_healthy_diet.csv
│   ├── ken_faostat_food_balances.csv
│   └── ken_faostat_food_security_indicators.csv
├── Food_Security.ipynb
├── requirements.txt
└── README.md
```

## Getting Started

Install the required packages:

```bash
pip install -r requirements.txt
```

Open the notebook:

```bash
jupyter notebook Food_Security.ipynb
```

## Data Source

The national FAOSTAT food security data comes from the HDX FAOSTAT Kenya food security indicators dataset:

https://data.humdata.org/dataset/ken-faostat-food-security-indicators

The county/sub-county risk data comes from the World Bank Joint Food Security Monitor:

https://microdata.worldbank.org/catalog/8115

The county boundary GeoJSON is used only for GeoPandas map joins and visualization.
