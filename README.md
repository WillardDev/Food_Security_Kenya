# Food Security in Kenya

This project explores Kenya food security data from the FAOSTAT dataset published on the Humanitarian Data Exchange (HDX).

Data source: https://data.humdata.org/dataset/ken-faostat-food-security-indicators

## Dataset Overview

The project uses FAOSTAT Kenya food security files downloaded from HDX:

| File | Description |
| --- | --- |
| `data/ken_faostat_food_security_indicators.csv` | Food security indicator values for Kenya, including measures related to availability, access, utilization, and stability. |
| `data/ken_faostat_food_balances.csv` | Kenya food balance data, including population and food supply-related records. |
| `data/ken_faostat_cost_affordability_healthy_diet.csv` | Cost and affordability of a healthy diet data for Kenya. |

## Project Objective

The goal of this project is to examine Kenya food security trends using FAOSTAT indicators and supporting food balance and healthy diet affordability data.

## Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook

## Project Structure

```text
food_securtiy/
├── data/
│   ├── ken_faostat_cost_affordability_healthy_diet.csv
│   ├── ken_faostat_food_balances.csv
│   └── ken_faostat_food_security_indicators.csv
├── Food_Secuirty.ipynb
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
jupyter notebook Food_Secuirty.ipynb
```

## Data Source

All data used in this project comes from the HDX FAOSTAT Kenya food security indicators dataset:

https://data.humdata.org/dataset/ken-faostat-food-security-indicators
