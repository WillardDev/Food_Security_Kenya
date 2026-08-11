from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
JMR_DIR = DATA_DIR / "world_bank_jmr"
SHAPEFILE_DIR = DATA_DIR / "shapefiles"

KEYS = ["Iso3", "Area", "Year"]

SAFE = "#2ecc71"
WARNING = "#f39c12"
DANGER = "#e74c3c"
NEUTRAL = "#3498db"

ALERT_COLORS = {0: SAFE, 1: WARNING, 2: DANGER}
ALERT_LABELS = {0: "Typical", 1: "Heightened", 2: "Critical"}

THRESHOLDS = {
    "dietary_energy_adequacy_pct":      (95,  90,  "higher_is_better"),
    "food_supply_kcal_capita_day":      (2100, 1800, "higher_is_better"),
    "protein_supply_g_capita_day":      (50,  40,  "higher_is_better"),
    "fat_supply_g_capita_day":          (40,  30,  "higher_is_better"),
    "undernourishment_pct":             (15,  25,  "lower_is_better"),
    "undernourished_people_million":    (10,  15,  "lower_is_better"),
    "severe_food_insecurity_pct":       (10,  20,  "lower_is_better"),
    "moderate_or_severe_food_insecurity_pct": (40, 60, "lower_is_better"),
    "under5_stunting_pct":              (20,  30,  "lower_is_better"),
    "under5_wasting_pct":               (5,   15,  "lower_is_better"),
    "healthy_diet_cost_ppp_per_day":    (3.5, 5.0, "lower_is_better"),
    "healthy_diet_unaffordable_pct":    (50,  70,  "lower_is_better"),
    "people_unable_afford_healthy_diet_million": (20, 35, "lower_is_better"),
    "gdp_per_capita_ppp":               (3000, 2000, "higher_is_better"),
}

INDICATOR_META = {
    "dietary_energy_adequacy_pct":      {"label": "Dietary Energy Supply Adequacy", "unit": "%", "tip": "% of population calorie needs met by domestic supply"},
    "food_supply_kcal_capita_day":      {"label": "Food Supply", "unit": "kcal/day", "tip": "Average calories available per person per day"},
    "protein_supply_g_capita_day":      {"label": "Protein Supply", "unit": "g/day", "tip": "Average protein available per person per day"},
    "fat_supply_g_capita_day":          {"label": "Fat Supply", "unit": "g/day", "tip": "Average fat available per person per day"},
    "undernourishment_pct":             {"label": "Prevalence of Undernourishment", "unit": "%", "tip": "% of population consistently unable to meet calorie needs"},
    "undernourished_people_million":    {"label": "People Undernourished", "unit": "million", "tip": "Total number of undernourished people"},
    "severe_food_insecurity_pct":       {"label": "Severe Food Insecurity", "unit": "%", "tip": "% of population who went entire days without eating"},
    "moderate_or_severe_food_insecurity_pct": {"label": "Moderate/Severe Food Insecurity", "unit": "%", "tip": "% of population experiencing food anxiety or meal-skipping"},
    "under5_stunting_pct":              {"label": "Child Stunting (Under-5)", "unit": "%", "tip": "% of children too short for their age (chronic malnutrition)"},
    "under5_wasting_pct":               {"label": "Child Wasting (Under-5)", "unit": "%", "tip": "% of children dangerously thin (acute malnutrition)"},
    "healthy_diet_cost_ppp_per_day":    {"label": "Healthy Diet Cost", "unit": "Int$/day", "tip": "Cost of a nutritious diet per person per day"},
    "healthy_diet_unaffordable_pct":    {"label": "Cannot Afford Healthy Diet", "unit": "%", "tip": "% of population who cannot afford a healthy diet"},
    "people_unable_afford_healthy_diet_million": {"label": "People Unable to Afford", "unit": "million", "tip": "Total people who cannot afford a healthy diet"},
    "gdp_per_capita_ppp":               {"label": "GDP per Capita", "unit": "Int$", "tip": "Economic output per person, adjusted for local prices"},
}

CHART_HEIGHT = 550
BG = "#0e1117"
GRID = "#262730"

CSS = """
<style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #262730; color: white; border-radius: 4px 4px 0 0;
        padding: 8px 16px; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #e74c3c; color: white; }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px; padding: 20px; margin: 8px 0; border-left: 4px solid;
    }
    .story-box {
        background: #1a1a2e; border-radius: 8px; padding: 16px 20px;
        margin: 12px 0; border-left: 3px solid #3498db; color: #ddd; line-height: 1.6;
    }
    .danger-box {
        background: #2e1a1a; border-radius: 8px; padding: 16px 20px;
        margin: 12px 0; border-left: 3px solid #e74c3c; color: #ddd; line-height: 1.6;
    }
    .success-box {
        background: #1a2e1a; border-radius: 8px; padding: 16px 20px;
        margin: 12px 0; border-left: 3px solid #2ecc71; color: #ddd; line-height: 1.6;
    }
</style>
"""