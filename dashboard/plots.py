import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dashboard.config import (
    SAFE, WARNING, DANGER, NEUTRAL, BG, GRID, CHART_HEIGHT,
    INDICATOR_META, ALERT_LABELS, ALERT_COLORS,
)
from dashboard.insights import status_color, alert_color, insight_text, story_box, danger_box


def _style(fig, height=CHART_HEIGHT, legend=False):
    fig.update_layout(
        plot_bgcolor=BG, paper_bgcolor=BG,
        font_color="white",
        xaxis=dict(gridcolor=GRID), yaxis=dict(gridcolor=GRID),
        height=height,
        legend_font_color="white" if legend else None,
    )
    return fig


# ---------------------------------------------------------------- T1
def top_indicators_chart(analysis_df):
    df_melted = analysis_df.melt(
        id_vars="Year",
        value_vars=["undernourished_people_million", "moderate_or_severe_food_insecurity_pct", "dietary_energy_adequacy_pct"],
        var_name="Indicator", value_name="Value"
    ).dropna()
    df_melted["Indicator"] = df_melted["Indicator"].map({
        "undernourished_people_million": "Undernourished (million)",
        "moderate_or_severe_food_insecurity_pct": "Food Insecurity (%)",
        "dietary_energy_adequacy_pct": "Energy Adequacy (%)",
    })

    fig = go.Figure()
    color_map = {"Undernourished (million)": DANGER, "Food Insecurity (%)": WARNING, "Energy Adequacy (%)": SAFE}
    for indicator_name, group in df_melted.groupby("Indicator"):
        fig.add_trace(go.Scatter(
            x=group["Year"], y=group["Value"],
            mode="lines+markers",
            name=indicator_name,
            line=dict(color=color_map.get(indicator_name, NEUTRAL), width=2.5),
            marker=dict(size=7),
            hovertemplate=f"<b>Year %{{x}}</b><br>{indicator_name}: %{{y:.1f}}<extra></extra>",
        ))
    fig.update_layout(
        title="Key Food Security Indicators Over Time (2000-2025)",
        xaxis_title="Year", yaxis_title="Value",
        legend_font_color="white",
    )
    return _style(fig, height=600)


def top_indicators_insight(analysis_df):
    latest = analysis_df.sort_values("Year").tail(1)
    year = int(latest["Year"].iloc[0])
    return danger_box(
        f"<b>The big picture:</b> In {year}, "
        f"<b>{latest['moderate_or_severe_food_insecurity_pct'].iloc[0]:.0f}% of Kenyans</b> experienced some form of food insecurity while "
        f"<b>{latest['undernourishment_pct'].iloc[0]:.1f}% were chronically undernourished</b>, equivalent to roughly "
        f"<b>{latest['undernourished_people_million'].iloc[0]:.0f} million people</b>. The number of undernourished Kenyans has doubled "
        f"from ~10 million (2002) to ~{latest['undernourished_people_million'].iloc[0]:.0f} million ({year}), driven by population growth "
        f"that has outpaced improvements in food production and distribution.<br><br>"
        f"<b>Bottom line:</b> Despite economic growth, food insecurity has worsened. "
        "<b>Economic growth alone has not solved Kenya's food crisis.</b>"
    )


def correlation_chart(analysis_df):
    corr_df = analysis_df[["Year", "gdp_per_capita_ppp", "moderate_or_severe_food_insecurity_pct"]].dropna()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=corr_df["gdp_per_capita_ppp"],
        y=corr_df["moderate_or_severe_food_insecurity_pct"],
        mode="markers+text",
        marker=dict(
            size=12,
            color=corr_df["Year"],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Year"),
            line=dict(width=1, color="white"),
        ),
        text=corr_df["Year"],
        textposition="top center",
        textfont=dict(color="white", size=9),
        hovertemplate="<b>Year %{text}</b><br>GDP per capita: $%{x:,.0f}<br>Food Insecurity: %{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title="GDP per Capita vs Food Insecurity Rate",
        xaxis_title="GDP per Capita (PPP, Int$)",
        yaxis_title="Food Insecurity (%)",
    )
    return _style(fig, height=600)


def correlation_insight(analysis_df):
    corr_df = analysis_df[["Year", "gdp_per_capita_ppp", "moderate_or_severe_food_insecurity_pct"]].dropna()
    gdp_start, gdp_end = corr_df["gdp_per_capita_ppp"].iloc[0], corr_df["gdp_per_capita_ppp"].iloc[-1]
    ins_start, ins_end = corr_df["moderate_or_severe_food_insecurity_pct"].iloc[0], corr_df["moderate_or_severe_food_insecurity_pct"].iloc[-1]
    corr = corr_df["gdp_per_capita_ppp"].corr(corr_df["moderate_or_severe_food_insecurity_pct"])
    return danger_box(
        f"<b>Correlation insight:</b> GDP per capita grew from ~${gdp_start:,.0f} to ~${gdp_end:,.0f} over two decades, yet "
        f"food insecurity actually <b>rose from {ins_start:.0f}% to {ins_end:.0f}%</b>. The correlation coefficient is "
        f"<b>{corr:+.2f}</b>, confirming that <b>higher GDP is NOT associated with lower food insecurity</b>.\n"
        "<br><br><b>Why?</b> The benefits of economic growth have not reached the poorest Kenyans. Rising food prices, "
        "income inequality, and unequal access to resources mean growth alone is insufficient.\n"
        "<br><br><b>Policy implication:</b> Targeted social protection, affordable-nutrition programs, and agricultural "
        "investment are essential, not just GDP growth."
    )


# ---------------------------------------------------------------- T2
def energy_adequacy_chart(analysis_df):
    data = analysis_df[["Year", "dietary_energy_adequacy_pct"]].dropna()
    data["Color"] = data["dietary_energy_adequacy_pct"].apply(lambda v: status_color(v, "dietary_energy_adequacy_pct"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Year"], y=data["dietary_energy_adequacy_pct"],
        mode="lines+markers",
        line=dict(color=NEUTRAL, width=2.5),
        marker=dict(color=data["Color"], size=8),
        text=data["dietary_energy_adequacy_pct"].round(1),
        textposition="top center",
        textfont_color="white",
        hovertemplate="<b>Year %{x}</b><br>Energy Adequacy: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=100, line_dash="solid", line_color=SAFE, line_width=2, annotation_text="100% target", annotation_position="top left", annotation_font_color=SAFE)
    fig.add_hline(y=95, line_dash="dash", line_color=WARNING, line_width=1.5, annotation_text="95% warning", annotation_position="top left", annotation_font_color=WARNING)
    fig.add_hline(y=90, line_dash="dash", line_color=DANGER, line_width=1.5, annotation_text="90% critical", annotation_position="top left", annotation_font_color=DANGER)
    fig.update_layout(
        title="Dietary Energy Supply Adequacy - Kenya",
        xaxis_title="Year", yaxis_title="% of calorie needs met",
        yaxis_range=[85, 105],
    )
    return _style(fig, height=600)


def energy_adequacy_insight(analysis_df):
    data = analysis_df[["Year", "dietary_energy_adequacy_pct"]].dropna()
    val = data["dietary_energy_adequacy_pct"].iloc[-1]
    year = int(data["Year"].iloc[-1])
    return danger_box(
        f"{insight_text('dietary_energy_adequacy_pct', val, year)}"
        "<br><br><b>Why this matters:</b> A value below 100% means Kenya cannot produce enough food for its population "
        "and must rely on imports and aid. This creates vulnerability to global price shocks and supply disruptions. "
        "When global food prices spike, as they did in 2008 and 2022, Kenya experiences immediate food crises."
    )


def supply_breakdown_chart(analysis_df):
    fig = make_subplots(rows=1, cols=3, subplot_titles=("Calories (kcal/day)", "Protein (g/day)", "Fat (g/day)"))
    supply_data = [
        ("food_supply_kcal_capita_day", 2100, 1800),
        ("protein_supply_g_capita_day", 50, 40),
        ("fat_supply_g_capita_day", 40, 30),
    ]
    for i, (ind, warn_val, danger_val) in enumerate(supply_data):
        d = analysis_df[["Year", ind]].dropna()
        d["Color"] = d[ind].apply(lambda v, k=ind: status_color(v, k))
        fig.add_trace(
            go.Scatter(x=d["Year"], y=d[ind], mode="lines+markers",
                       marker=dict(color=d["Color"], size=8),
                       line=dict(color=NEUTRAL, width=2),
                       name=INDICATOR_META[ind]["label"],
                       hovertemplate=f"<b>Year %{{x}}</b><br>{INDICATOR_META[ind]['label']}: %{{y:.1f}} {INDICATOR_META[ind]['unit']}<extra></extra>"),
            row=1, col=i + 1
        )
        fig.add_hline(y=warn_val, line_dash="dash", line_color=WARNING, line_width=1, row=1, col=i + 1)
        fig.add_hline(y=danger_val, line_dash="dash", line_color=DANGER, line_width=1, row=1, col=i + 1)
    fig.update_layout(showlegend=False)
    _style(fig, height=CHART_HEIGHT)
    fig.update_xaxes(gridcolor=GRID)
    fig.update_yaxes(gridcolor=GRID)
    return fig


def supply_breakdown_insight(analysis_df):
    parts = []
    for ind, target in [("food_supply_kcal_capita_day", 2100), ("protein_supply_g_capita_day", 50), ("fat_supply_g_capita_day", 40)]:
        latest = analysis_df.dropna(subset=[ind]).sort_values("Year").tail(1)
        if latest.empty:
            continue
        v, y = latest[ind].iloc[0], int(latest["Year"].iloc[0])
        pct = v / target * 100 if target else 0
        parts.append(
            f"<b>{INDICATOR_META[ind]['label']}</b>: {v:.0f} {INDICATOR_META[ind]['unit']} in {y}, "
            f"{pct:.0f}% of the {target} recommended minimum."
        )
    return danger_box(
        "<b>Supply breakdown insight:</b><br>" + "<br>".join(parts) +
        "<br><br>Offering <b>enough calories is necessary but not sufficient</b>. Even where calorie targets are met, "
        "a diet short on protein and fat leaves people malnourished. Kenya's supply profile has stayed broadly flat for "
        "two decades while the population grew, so per-person availability has not improved."
    )


# ---------------------------------------------------------------- T3
def undernourishment_chart(analysis_df):
    data = analysis_df[["Year", "undernourishment_pct"]].dropna()
    data["Color"] = data["undernourishment_pct"].apply(lambda v: status_color(v, "undernourishment_pct"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Year"], y=data["undernourishment_pct"],
        mode="lines+markers",
        line=dict(color=DANGER, width=2.5),
        marker=dict(color=data["Color"], size=8),
        text=data["undernourishment_pct"].round(1),
        textposition="top center",
        textfont_color="white",
        hovertemplate="<b>Year %{x}</b><br>Undernourishment: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=15, line_dash="dash", line_color=WARNING, annotation_text="15% warning", annotation_position="top left", annotation_font_color=WARNING)
    fig.add_hline(y=25, line_dash="dash", line_color=DANGER, annotation_text="25% critical", annotation_position="top left", annotation_font_color=DANGER)
    fig.update_layout(
        title="Undernourishment Rate - Kenya",
        xaxis_title="Year", yaxis_title="% of population",
    )
    return _style(fig, height=600)


def undernourishment_insight(analysis_df):
    data = analysis_df[["Year", "undernourishment_pct"]].dropna()
    val = data["undernourishment_pct"].iloc[-1]
    year = int(data["Year"].iloc[-1])
    return danger_box(insight_text("undernourishment_pct", val, year))


def food_insecurity_chart(analysis_df):
    mod_data = analysis_df[["Year", "moderate_or_severe_food_insecurity_pct"]].dropna()
    sev_data = analysis_df[["Year", "severe_food_insecurity_pct"]].dropna()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mod_data["Year"], y=mod_data["moderate_or_severe_food_insecurity_pct"],
        mode="lines+markers", name="Moderate or Severe",
        line=dict(color=WARNING, width=3), marker=dict(size=8),
        fill="tozeroy", fillcolor="rgba(243,156,18,0.1)",
        hovertemplate="<b>Year %{x}</b><br>Moderate/Severe: %{y:.1f}%<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=sev_data["Year"], y=sev_data["severe_food_insecurity_pct"],
        mode="lines+markers", name="Severe Only",
        line=dict(color=DANGER, width=3), marker=dict(size=8),
        hovertemplate="<b>Year %{x}</b><br>Severe: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=40, line_dash="dash", line_color=WARNING, annotation_text="40% warning", annotation_font_color=WARNING)
    fig.add_hline(y=60, line_dash="dash", line_color=DANGER, annotation_text="60% critical", annotation_font_color=DANGER)
    fig.update_layout(
        title="Food Insecurity Rates - Kenya",
        xaxis_title="Year", yaxis_title="% of population",
        legend_font_color="white",
    )
    return _style(fig, height=600)


def food_insecurity_insight(analysis_df):
    mod_data = analysis_df[["Year", "moderate_or_severe_food_insecurity_pct"]].dropna()
    sev_data = analysis_df[["Year", "severe_food_insecurity_pct"]].dropna()
    mod_val = mod_data["moderate_or_severe_food_insecurity_pct"].iloc[-1]
    sev_val = sev_data["severe_food_insecurity_pct"].iloc[-1]
    mod_year = int(mod_data["Year"].iloc[-1])
    sev_year = int(sev_data["Year"].iloc[-1])
    return danger_box(
        f"{insight_text('moderate_or_severe_food_insecurity_pct', mod_val, mod_year)}"
        f"<br><br>{insight_text('severe_food_insecurity_pct', sev_val, sev_year)}"
        "<br><br><b>The spectrum of food insecurity:</b> Food insecurity exists on a spectrum from mild anxiety "
        f"about food availability to extreme deprivation. The gap between moderate/severe ({mod_val:.0f}%) and severe ({sev_val:.0f}%) "
        "represents people who worry about food or skip meals but do not go entire days without eating.<br><br>"
        "Both measures have worsened significantly since 2016, reflecting drought, economic shocks, and the COVID-19 pandemic. "
        "The narrowing gap means more people are sliding from moderate into severe food insecurity."
    )


def affordability_chart(analysis_df):
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Cost of Healthy Diet (Int$/day)", "% Cannot Afford", "People Unable (millions)"),
    )
    afford_data = [
        ("healthy_diet_cost_ppp_per_day", 3.5, 5.0),
        ("healthy_diet_unaffordable_pct", 50, 70),
        ("people_unable_afford_healthy_diet_million", 20, 35),
    ]
    for i, (ind, warn_val, danger_val) in enumerate(afford_data):
        d = analysis_df[["Year", ind]].dropna()
        d["Color"] = d[ind].apply(lambda v, k=ind: status_color(v, k))
        fig.add_trace(
            go.Scatter(x=d["Year"], y=d[ind], mode="lines+markers",
                       marker=dict(color=d["Color"], size=8),
                       line=dict(color=NEUTRAL, width=2),
                       name=INDICATOR_META[ind]["label"],
                       hovertemplate=f"<b>Year %{{x}}</b><br>{INDICATOR_META[ind]['label']}: %{{y:.1f}} {INDICATOR_META[ind]['unit']}<extra></extra>"),
            row=1, col=i + 1
        )
        fig.add_hline(y=warn_val, line_dash="dash", line_color=WARNING, line_width=1, row=1, col=i + 1)
        fig.add_hline(y=danger_val, line_dash="dash", line_color=DANGER, line_width=1, row=1, col=i + 1)
    fig.update_layout(showlegend=False)
    _style(fig, height=CHART_HEIGHT)
    fig.update_xaxes(gridcolor=GRID)
    fig.update_yaxes(gridcolor=GRID)
    return fig


def affordability_insight(analysis_df):
    val = analysis_df.dropna(subset=["healthy_diet_unaffordable_pct"]).sort_values("Year").tail(1)["healthy_diet_unaffordable_pct"].iloc[0]
    year = int(analysis_df.dropna(subset=["healthy_diet_unaffordable_pct"]).sort_values("Year").tail(1)["Year"].iloc[0])
    people_unafford = analysis_df.dropna(subset=["people_unable_afford_healthy_diet_million"]).sort_values("Year").tail(1)["people_unable_afford_healthy_diet_million"].iloc[0]
    return danger_box(
        f"{insight_text('healthy_diet_unaffordable_pct', val, year)}"
        "<br><br><b>The affordability crisis in numbers:</b> A healthy diet costs approximately $3.20 per person per day "
        f"(international dollars). With <b>{people_unafford:.0f} million Kenyans</b> unable to afford this, the majority of "
        "the population relies on cheap, nutrient-poor staples like maize, ugali, and porridge.<br><br>"
        "This explains the paradox of high calorie adequacy but high stunting rates: people get enough calories but not "
        "enough nutrients. <b>Availability without access is not food security.</b>"
    )


# ---------------------------------------------------------------- T4
def child_nutrition_chart(analysis_df):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Child Stunting (Under-5)", "Child Wasting (Under-5)"))
    st_data = analysis_df[["Year", "under5_stunting_pct"]].dropna()
    st_data["Color"] = st_data["under5_stunting_pct"].apply(lambda v: status_color(v, "under5_stunting_pct"))
    fig.add_trace(
        go.Scatter(x=st_data["Year"], y=st_data["under5_stunting_pct"], mode="lines+markers",
                   line=dict(color=WARNING, width=2.5),
                   marker=dict(color=st_data["Color"], size=8),
                   text=st_data["under5_stunting_pct"].round(1), textposition="top center", textfont_color="white",
                   hovertemplate="<b>Year %{x}</b><br>Stunting: %{y:.1f}%<extra></extra>"),
        row=1, col=1
    )
    fig.add_hline(y=20, line_dash="dash", line_color=WARNING, annotation_text="20% warning", annotation_font_color=WARNING, row=1, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color=DANGER, annotation_text="30% critical", annotation_font_color=DANGER, row=1, col=1)

    wa_data = analysis_df[["Year", "under5_wasting_pct"]].dropna()
    if not wa_data.empty:
        wa_data["Color"] = wa_data["under5_wasting_pct"].apply(lambda v: status_color(v, "under5_wasting_pct"))
        fig.add_trace(
            go.Scatter(x=wa_data["Year"], y=wa_data["under5_wasting_pct"], mode="lines+markers",
                       line=dict(color=DANGER, width=2.5),
                       marker=dict(color=wa_data["Color"], size=8),
                       text=wa_data["under5_wasting_pct"].round(1), textposition="top center", textfont_color="white",
                       hovertemplate="<b>Year %{x}</b><br>Wasting: %{y:.1f}%<extra></extra>"),
            row=1, col=2
        )
        fig.add_hline(y=5, line_dash="dash", line_color=WARNING, annotation_text="5% warning", annotation_font_color=WARNING, row=1, col=2)
        fig.add_hline(y=15, line_dash="dash", line_color=DANGER, annotation_text="15% critical", annotation_font_color=DANGER, row=1, col=2)

    fig.update_layout(showlegend=False, height=600)
    fig.update_xaxes(gridcolor=GRID)
    fig.update_yaxes(gridcolor=GRID)
    _style(fig)
    return fig


def child_nutrition_insight(analysis_df):
    st_data = analysis_df[["Year", "under5_stunting_pct"]].dropna()
    st_val = st_data["under5_stunting_pct"].iloc[-1]
    st_year = int(st_data["Year"].iloc[-1])
    parts = [insight_text("under5_stunting_pct", st_val, st_year)]
    wa_data = analysis_df[["Year", "under5_wasting_pct"]].dropna()
    if not wa_data.empty:
        wa_val = wa_data["under5_wasting_pct"].iloc[-1]
        wa_year = int(wa_data["Year"].iloc[-1])
        parts.append(insight_text("under5_wasting_pct", wa_val, wa_year))
    parts.append(
        "<br><b>Understanding the difference:</b> Stunting reflects chronic, long-term malnutrition that develops "
        "over months or years and causes permanent physical and cognitive damage. Wasting reflects acute, recent food "
        "shortage and can often be reversed with proper nutrition.<br><br>"
        "<b>Progress and challenges:</b> Stunting has improved dramatically from ~38% (2000) to ~18% (2024), yet the "
        "remaining children still face lifelong limits. Wasting fluctuates with drought cycles and remains a persistent threat."
    )
    return danger_box("".join(parts))


# ---------------------------------------------------------------- T5
def choropleth_chart(county_geo_df, latest_alert_date, map_choice):
    geo_json = county_geo_df.__geo_interface__
    county_names = county_geo_df[["county_name"]].to_numpy()
    if map_choice == "Overall Alert Level":
        fig = px.choropleth(
            county_geo_df,
            geojson=geo_json,
            locations=county_geo_df.index,
            color="overall_max_alert",
            color_continuous_scale=[SAFE, WARNING, DANGER],
            range_color=[0, 2],
            labels={"overall_max_alert": "Alert Level"},
            title=f"Kenya County Food Security Risk - Overall Alert ({latest_alert_date.date()})",
        )
        fig.update_traces(
            customdata=county_names,
            hovertemplate="<b>%{customdata[0]}</b><br>Overall Alert Level: %{z}<extra></extra>",
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Alert"))
    else:
        fig = px.choropleth(
            county_geo_df,
            geojson=geo_json,
            locations=county_geo_df.index,
            color="total_critical_flags",
            color_continuous_scale="Reds",
            labels={"total_critical_flags": "Critical Flags"},
            title=f"Critical Admin-2 Indicator Flags by County ({latest_alert_date.date()})",
        )
        fig.update_traces(
            customdata=county_names,
            hovertemplate="<b>%{customdata[0]}</b><br>Critical flags: %{z}<extra></extra>",
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Critical Flags"))
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        plot_bgcolor=BG, paper_bgcolor=BG, font_color="white",
        height=600, margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig


def county_ranking_chart(county_risk_summary, latest_alert_date, top_n=15):
    col1 = county_risk_summary.head(top_n).iloc[::-1]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=col1["adm1_name"], x=col1["total_critical_flags"],
        orientation="h", name="Critical flags",
        marker_color=DANGER,
        text=col1["total_critical_flags"], textposition="outside", textfont_color="white",
        hovertemplate="<b>%{y}</b><br>Critical flags: %{x}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=col1["adm1_name"], x=col1["total_heightened_flags"],
        orientation="h", name="Heightened flags",
        marker_color=WARNING,
        text=col1["total_heightened_flags"], textposition="outside", textfont_color="white",
        hovertemplate="<b>%{y}</b><br>Heightened flags: %{x}<extra></extra>",
    ))
    fig.update_layout(
        title=f"Top {top_n} Highest-Risk Counties ({latest_alert_date.date()})",
        xaxis_title="Number of sub-county alerts", yaxis_title="County",
        barmode="stack",
        legend_font_color="white",
    )
    return _style(fig, height=max(320, 22 * len(col1) + 120))


def heatmap_chart(county_indicator_matrix, county_risk_summary, latest_alert_date):
    hm_data = county_indicator_matrix.set_index("adm1_name").drop(columns="adm1_pcode")
    hm_data = hm_data.loc[county_risk_summary["adm1_name"]]
    hm_data = hm_data.astype(float)

    fig = go.Figure(data=go.Heatmap(
        z=hm_data.values,
        x=hm_data.columns.tolist(),
        y=hm_data.index.tolist(),
        colorscale=[[0, SAFE], [0.5, WARNING], [1, DANGER]],
        zmin=0, zmax=2,
        hovertemplate="<b>%{y}</b><br>%{x}<br>Alert: %{z:.0f}<extra></extra>",
        colorbar=dict(title="Alert", tickvals=[0, 1, 2], ticktext=["Typical", "Heightened", "Critical"]),
        xgap=2, ygap=2,
    ))
    fig.update_layout(
        title=f"JMR Alert Levels by County ({latest_alert_date.date()})",
        xaxis_title="Indicator", yaxis_title="County",
        height=700,
    )
    return _style(fig, height=700)


def county_map_insight(county_risk_summary, latest_alert_date):
    top = county_risk_summary.head(5)["adm1_name"].tolist()
    n_crit = int((county_risk_summary["overall_max_alert"] == 2).sum())
    n_high = int((county_risk_summary["overall_max_alert"] == 1).sum())
    n_typ = int((county_risk_summary["overall_max_alert"] == 0).sum())
    return danger_box(
        f"<b>County risk insight ({latest_alert_date.date()}):</b> "
        f"<b>{n_crit} counties</b> are at <b>critical</b> risk and <b>{n_high}</b> are at <b>heightened</b> risk "
        f"across the alert indicators, while {n_typ} remain typical. The most affected counties are "
        f"<b>{', '.join(top)}</b>.<br><br>"
        "These are the areas where climate shocks, conflict, food-price spikes, and exchange-rate volatility are "
        "currently combining to push sub-counties past the critical threshold. Priority food assistance and early-warning "
        "response should target these counties first."
    )


# ---------------------------------------------------------------- County snapshot (T1/T5)
def county_alert_pie_chart(county_risk_summary, latest_alert_date):
    counts = county_risk_summary["overall_alert_label"].value_counts()
    labels = ["Critical", "Heightened", "Typical"]
    values = [counts.get(label, 0) for label in labels]
    colors = [DANGER, WARNING, SAFE]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        sort=False,
        marker=dict(colors=colors, line=dict(color=BG, width=2)),
        textinfo="label+value",
        textfont=dict(color="white", size=13),
        hovertemplate="<b>%{label}</b><br>%{value} of 47 counties (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        title=f"Share of Counties by Risk Level ({latest_alert_date.date()})",
        showlegend=True,
        legend=dict(font=dict(color="white"), orientation="h", y=-0.15),
        annotations=[dict(
            text=f"{len(county_risk_summary)}<br>counties",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="white", size=18),
        )],
    )
    return _style(fig, height=480, legend=True)


def most_least_affected_chart(county_risk_summary, top_n=5):
    summary = county_risk_summary.copy()
    summary["flags"] = summary["total_critical_flags"] + summary["total_heightened_flags"]

    top = summary.head(top_n).iloc[::-1]
    bottom = summary.tail(top_n).iloc[::-1]

    def bar_color(row):
        return ALERT_COLORS.get(row["overall_max_alert"], NEUTRAL)

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Most Affected (top 5)", "Least Affected (bottom 5)"),
        column_widths=[0.6, 0.4],
    )
    fig.add_trace(go.Bar(
        y=top["adm1_name"], x=top["flags"], orientation="h",
        marker_color=[bar_color(r) for _, r in top.iterrows()],
        text=top["flags"], textposition="outside", textfont_color="white",
        hovertemplate="<b>%{y}</b><br>Alert flags: %{x}<extra></extra>",
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        y=bottom["adm1_name"], x=bottom["flags"], orientation="h",
        marker_color=[bar_color(r) for _, r in bottom.iterrows()],
        text=bottom["flags"], textposition="outside", textfont_color="white",
        hovertemplate="<b>%{y}</b><br>Alert flags: %{x}<extra></extra>",
    ), row=1, col=2)
    fig.update_layout(
        title=f"Counties Most and Least Affected by Food-Security Alerts (top {top_n})",
        showlegend=False,
        barmode="overlay",
    )
    _style(fig, height=max(320, 28 * len(top) + 140))
    fig.update_xaxes(gridcolor=GRID)
    fig.update_yaxes(gridcolor=GRID)
    return fig


def county_trend_chart(county_alerts):
    daily = county_alerts.groupby(["date", "adm1_name"])["max_alert_level"].max().reset_index()
    crit = daily[daily["max_alert_level"] == 2].groupby("date")["adm1_name"].nunique()
    height = daily[daily["max_alert_level"] >= 1].groupby("date")["adm1_name"].nunique()
    df = pd.concat(
        [height.rename("At least heightened"), crit.rename("Critical")],
        axis=1,
    ).fillna(0).sort_index().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["At least heightened"],
        mode="lines+markers", name="Counties at heightened or worse",
        line=dict(color=WARNING, width=2.5), marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(243,156,18,0.08)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Counties: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["Critical"],
        mode="lines+markers", name="Counties at critical risk",
        line=dict(color=DANGER, width=3), marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(231,76,60,0.15)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Counties: %{y}<extra></extra>",
    ))
    fig.add_hline(
        y=47, line_dash="dot", line_color=NEUTRAL, line_width=1.5,
        annotation_text="47 counties total", annotation_position="top right",
        annotation_font_color=NEUTRAL,
    )
    fig.update_layout(
        title="How Many Kenyan Counties Are at Risk? (2010-2026)",
        xaxis_title="Date", yaxis_title="Number of counties",
        yaxis_range=[0, 50],
        legend_font_color="white",
    )
    return _style(fig, height=480, legend=True)


def county_snapshot_insight(county_risk_summary, latest_alert_date):
    n_crit = int((county_risk_summary["overall_max_alert"] == 2).sum())
    n_high = int((county_risk_summary["overall_max_alert"] == 1).sum())
    n_typ = int((county_risk_summary["overall_max_alert"] == 0).sum())
    top = county_risk_summary.head(5)["adm1_name"].tolist()
    bottom = county_risk_summary.tail(5)["adm1_name"].tolist()
    return danger_box(
        f"<b>County snapshot ({latest_alert_date.date()}):</b> of Kenya's 47 counties, "
        f"<b>{n_crit} are at critical risk</b> and <b>{n_high} are heightened</b>, while {n_typ} are currently typical. "
        f"The most affected counties are <b>{', '.join(top)}</b>; the least affected are "
        f"<b>{', '.join(bottom)}</b>.<br><br>"
        "The national line charts hide this reality: averages smooth away the counties where drought, "
        "food prices, exchange rates, and conflict are already pushing people past the critical threshold. "
        "The country risk map (Tab 6) shows exactly where."
    )


def county_trend_insight(county_alerts):
    daily = county_alerts.groupby(["date", "adm1_name"])["max_alert_level"].max().reset_index()
    crit = daily[daily["max_alert_level"] == 2].groupby("date")["adm1_name"].nunique()
    height = daily[daily["max_alert_level"] >= 1].groupby("date")["adm1_name"].nunique()
    crit_now = int(crit.iloc[-1])
    crit_min, crit_max = int(crit.min()), int(crit.max())
    peak_year = crit.idxmax().year
    first_year = int(daily["date"].dt.year.min())
    return story_box(
        f"<b>County risk over time:</b> since {first_year}, the number of counties in crisis has ranged from "
        f"{crit_min} to <b>{crit_max} at the worst point ({peak_year})</b>, and <b>{crit_now} counties are critical today</b>. "
        "The line chart shows the crisis is not static - it expands and contracts with drought cycles and "
        "price shocks, which is exactly why <b>early-warning systems that monitor counties month by month</b> "
        "matter more than national averages."
    )


# ---------------------------------------------------------------- County comparisons (external data)
COUNTY_INDICATORS = {
    "stunting_pct": {"label": "Child Stunting (DHS 2022)", "unit": "%", "thresholds": (20, 30)},
    "wasting_pct": {"label": "Child Wasting (DHS 2022)", "unit": "%", "thresholds": (5, 15)},
    "poverty_pct": {"label": "Overall Poverty Rate (HAPI 2022)", "unit": "%", "thresholds": (40, 60)},
    "severe_poverty_pct": {"label": "Severe Poverty Rate (HAPI 2022)", "unit": "%", "thresholds": (20, 40)},
    "mpi": {"label": "Multidimensional Poverty Index (2022)", "unit": "", "thresholds": (0.2, 0.4)},
    "ipc_crisis_population": {"label": "People in Acute Food Insecurity (IPC Feb 2026)", "unit": "people", "thresholds": (None, None)},
    "ipc_crisis_pct": {"label": "% Population in Acute Food Insecurity (IPC Feb 2026)", "unit": "%", "thresholds": (20, 35)},
    "total_critical_flags": {"label": "JMR Critical Alert Flags (risk map)", "unit": "flags", "thresholds": (None, None)},
}

def _county_bar_color(value, thresholds, direction="lower_is_better"):
    warn, danger = thresholds
    if warn is None or pd.isna(value):
        return NEUTRAL
    if direction == "lower_is_better":
        if value >= danger: return DANGER
        if value >= warn: return WARNING
        return SAFE
    if value <= danger: return DANGER
    if value <= warn: return WARNING
    return SAFE


def county_indicator_bar_chart(county_stats, indicator, top_n=47, latest_alert_date=None):
    meta = COUNTY_INDICATORS[indicator]
    df = county_stats.dropna(subset=[indicator]).copy()
    df = df.sort_values(indicator, ascending=False).head(top_n)
    title = meta["label"]
    if latest_alert_date is not None:
        title += f" by County"
    fig = go.Figure(go.Bar(
        y=df["adm1_name"], x=df[indicator], orientation="h",
        marker_color=[_county_bar_color(v, meta["thresholds"]) for v in df[indicator]],
        text=[f"{v:,.1f}" for v in df[indicator]],
        textposition="outside", textfont_color="white",
        hovertemplate="<b>%{y}</b><br>%{x:,.1f}" + ("%" if meta["unit"] == "%" else "") + "<extra></extra>",
    ))
    fig.update_layout(
        title=f"{title} - top {len(df)} counties",
        xaxis_title=f"{meta['label']} ({meta['unit']})" if meta["unit"] else meta["label"],
        yaxis_title="County",
        showlegend=False,
    )
    return _style(fig, height=max(320, 22 * len(df) + 120))


def county_crisis_chart(county_stats, top_n=47):
    df = county_stats.dropna(subset=["ipc_crisis_population"]).sort_values("ipc_crisis_population", ascending=False).head(top_n)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["adm1_name"], x=df["ipc_crisis_population"], orientation="h",
        marker_color=DANGER,
        text=[f"{v/1000:.0f}k" for v in df["ipc_crisis_population"]],
        textposition="outside", textfont_color="white",
        hovertemplate="<b>%{y}</b><br>People in crisis: %{x:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=df["adm1_name"], x=df["ipc_total_population"], orientation="h",
        marker_color="rgba(231,76,60,0.25)", name="Total population (IPC)",
        text=[f"{v/1000:.0f}k" for v in df["ipc_total_population"]],
        textposition="outside", textfont_color="white",
        hovertemplate="<b>%{y}</b><br>Total population: %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title=f"People in Acute Food Insecurity (IPC Phase 3+) by County - top {len(df)} (Feb 2026)",
        xaxis_title="Number of people", yaxis_title="County",
        barmode="overlay",
        legend_font_color="white",
    )
    return _style(fig, height=max(320, 22 * len(df) + 120))


def county_comparison_scatter_chart(county_stats, x_key, y_key, latest_alert_date=None):
    df = county_stats.dropna(subset=[x_key, y_key]).copy()
    x_meta = COUNTY_INDICATORS[x_key]["label"]
    y_meta = COUNTY_INDICATORS[y_key]["label"]
    fig = go.Figure(go.Scatter(
        x=df[x_key], y=df[y_key],
        mode="markers+text",
        marker=dict(
            size=11,
            color=df["overall_max_alert"],
            colorscale=[SAFE, WARNING, DANGER],
            cmin=0, cmax=2,
            showscale=True,
            colorbar=dict(title="JMR Risk", tickvals=[0, 1, 2], ticktext=["Typical", "Heightened", "Critical"]),
            line=dict(width=1, color="white"),
        ),
        text=df["adm1_name"],
        textposition="top center",
        textfont=dict(color="white", size=8),
        hovertemplate="<b>%{text}</b><br>%{xaxis.title.text}: %{x:,.1f}<br>%{yaxis.title.text}: %{y:,.1f}<extra></extra>",
    ))
    fig.update_layout(
        title=f"{y_meta} vs {x_meta}",
        xaxis_title=x_meta, yaxis_title=y_meta,
    )
    return _style(fig, height=620)


def county_comparisons_insight(county_stats):
    top_poverty = county_stats.dropna(subset=["poverty_pct"]).sort_values("poverty_pct", ascending=False).head(3)["adm1_name"].tolist()
    top_stunt = county_stats.dropna(subset=["stunting_pct"]).sort_values("stunting_pct", ascending=False).head(3)["adm1_name"].tolist()
    crisis_total = int(county_stats["ipc_crisis_population"].sum())
    return danger_box(
        "<b>Merging external data changes the picture:</b> now that we compare counties directly, the "
        "<b>counties with the worst measured outcomes</b> (highest poverty and child stunting) are the arid and "
        "semi-arid north - "
        f"<b>{', '.join(top_poverty)}</b> for poverty and <b>{', '.join(top_stunt)}</b> for child nutrition.<br><br>"
        f"The IPC analysis (Feb 2026) puts roughly <b>{crisis_total:,} people in acute food insecurity</b> (IPC Phase 3+) "
        "across the affected counties. These externally-measured indicators line up closely with the JMR risk alerts - "
        "the same counties the risk map flags critical are the ones with the worst stunting and poverty, "
        "which cross-validates the JMR early-warning system."
    )


def heatmap_insight(county_risk_summary):
    critical_on = county_risk_summary["indicators_at_critical"] if "indicators_at_critical" in county_risk_summary else None
    note = ""
    return story_box(
        "<b>Reading the heatmap:</b> Each cell shows the maximum alert level (Typical 0 / Heightened 1 / Critical 2) "
        "reached by any sub-county for a given indicator. <b>Red</b> cells mean that indicator already triggered a "
        "critical alert somewhere in that county, so it warrants immediate action; <b>yellow</b> means elevated but "
        "not yet critical.<br><br>"
        "Indicators covering food prices, exchange rates, drought (NDVI and rainfall), and conflict move independently, "
        "so a county can be critical on one indicator while typical on another. Looking across the row shows which "
        "risk drivers are contributing most to each county's overall alert."
    )