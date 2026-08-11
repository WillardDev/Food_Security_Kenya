import pandas as pd

from dashboard.config import THRESHOLDS, SAFE, WARNING, DANGER, NEUTRAL, BG, GRID


def status_color(value, indicator):
    if indicator not in THRESHOLDS or pd.isna(value):
        return NEUTRAL
    warn, danger, direction = THRESHOLDS[indicator]
    if direction == "lower_is_better":
        if value >= danger: return DANGER
        elif value >= warn: return WARNING
        else: return SAFE
    else:
        if value <= danger: return DANGER
        elif value <= warn: return WARNING
        else: return SAFE


def status_label(value, indicator):
    if indicator not in THRESHOLDS or pd.isna(value):
        return "No data"
    warn, danger, direction = THRESHOLDS[indicator]
    if direction == "lower_is_better":
        if value >= danger: return "Critical"
        elif value >= warn: return "Warning"
        else: return "Acceptable"
    else:
        if value <= danger: return "Critical"
        elif value <= warn: return "Warning"
        else: return "Acceptable"


def alert_color(level):
    return {0: SAFE, 1: WARNING, 2: DANGER}.get(level, NEUTRAL)


def insight_text(indicator, value, year):
    if indicator not in THRESHOLDS or pd.isna(value):
        return "No data available."
    warn, danger, direction = THRESHOLDS[indicator]
    if direction == "lower_is_better":
        severity = "critical" if value >= danger else ("warning" if value >= warn else "acceptable")
    else:
        severity = "critical" if value <= danger else ("warning" if value <= warn else "acceptable")

    texts = {
        "dietary_energy_adequacy_pct": {
            "critical": f"In {year}, Kenya domestic food supply met only {value:.1f}% of calorie needs. The country depends on imports and aid, making it highly vulnerable to global price shocks and supply chain disruptions.",
            "warning": f"At {value:.1f}%, energy adequacy is below the 100% target. Kenya consistently fails to produce enough food for its population and relies on imports to fill the gap.",
            "acceptable": f"At {value:.1f}%, food supply adequately meets population needs.",
        },
        "undernourishment_pct": {
            "critical": f"{value:.1f}% of Kenyans, roughly 1 in {int(100/value)}, are chronically undernourished in {year}. This is a persistent humanitarian crisis requiring systemic intervention in food production, distribution, and affordability.",
            "warning": f"At {value:.1f}%, undernourishment remains in the warning zone. Millions of Kenyans experience chronic hunger that impairs health, productivity, and child development.",
            "acceptable": f"At {value:.1f}%, undernourishment is within manageable levels but still affects vulnerable populations.",
        },
        "moderate_or_severe_food_insecurity_pct": {
            "critical": f"Over {value:.0f}% of Kenyans experienced food insecurity in {year}. The majority of the population regularly worries about food or skips meals. This is a societal crisis affecting more than 3 in 4 people.",
            "warning": f"At {value:.0f}%, food insecurity affects a staggering portion of the population. Food anxiety and meal-skipping have become normalized experiences for most Kenyan households.",
            "acceptable": f"At {value:.0f}%, food insecurity affects a portion of the population but is not yet widespread.",
        },
        "severe_food_insecurity_pct": {
            "critical": f"{value:.1f}% of Kenyans went entire days without eating in {year}. This is extreme deprivation, people experiencing 24+ hours of zero food intake. Immediate food assistance is required.",
            "warning": f"At {value:.1f}%, severe food deprivation affects millions. Going a full day without food causes acute physical and psychological harm.",
            "acceptable": f"At {value:.1f}%, severe food deprivation is relatively contained.",
        },
        "under5_stunting_pct": {
            "critical": f"{value:.1f}% of Kenyan children under 5 are stunted, too short for their age due to chronic malnutrition. Stunting causes irreversible brain and body damage that limits these children potential for life.",
            "warning": f"At {value:.1f}%, nearly 1 in 5 children suffer chronic malnutrition with lifelong consequences for health and cognitive development.",
            "acceptable": f"At {value:.1f}%, stunting has improved significantly but remains a concern for vulnerable communities.",
        },
        "under5_wasting_pct": {
            "critical": f"{value:.1f}% of Kenyan children under 5 are dangerously thin (wasted) from acute malnutrition. These children have recently lost weight and face immediate risk of illness and death. Life-saving therapeutic feeding is urgently needed.",
            "warning": f"At {value:.1f}%, child wasting indicates acute food shortage. Children are losing weight now and require urgent nutritional support to prevent long-term harm.",
            "acceptable": f"At {value:.1f}%, child wasting is within WHO acceptable range, but drought years can reverse this progress quickly.",
        },
        "healthy_diet_unaffordable_pct": {
            "critical": f"{value:.0f}% of Kenyans cannot afford a healthy diet. They rely on cheap, nutrient-poor staples like maize and ugali, which explains high stunting despite adequate calorie supply.",
            "warning": f"At {value:.0f}%, the majority cannot afford nutritious food. Cheap staples dominate, leading to hidden hunger and micronutrient deficiencies.",
            "acceptable": f"At {value:.0f}%, a significant portion still struggles to afford nutritious food.",
        },
    }
    return texts.get(indicator, {}).get(severity, f"Value: {value:.1f} ({severity})")


def story_box(body):
    return f'<div class="story-box">{body}</div>'


def danger_box(body):
    return f'<div class="danger-box">{body}</div>'


def success_box(body):
    return f'<div class="success-box">{body}</div>'