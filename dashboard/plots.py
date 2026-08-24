import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dashboard.config import (
    SAFE, WARNING, DANGER, NEUTRAL, BG, GRID_SOFT, CHART_HEIGHT,
    INDICATOR_META, ALERT_LABELS, ALERT_COLORS,
)
from dashboard.insights import status_color, alert_color, insight_text


def _style(fig, height=CHART_HEIGHT, legend=False):
    fig.update_layout(
        plot_bgcolor=BG, paper_bgcolor=BG,
        font_color="white",
        height=height,
        margin=dict(l=30, r=30, t=70, b=40),
        legend_font_color="white" if legend else None,
        legend_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=False, showline=False, zeroline=False)
    fig.update_yaxes(gridcolor=GRID_SOFT, gridwidth=1, showline=False, zeroline=False)
    return fig


def _threshold_line(fig, y, label, color, row=None, col=None):
    kwargs = dict(
        y=y, line_dash="dash", line_color=color, line_width=1.5,
        annotation_text=label, annotation_position="top left",
        annotation_font_color=color, annotation_font_size=11,
    )
    if row is not None:
        kwargs.update(row=row, col=col)
    fig.add_hline(**kwargs)


def _critical_zone(fig, y0, y1, row=None, col=None):
    kwargs = dict(y0=y0, y1=y1, fillcolor="rgba(231,76,60,0.08)", line_width=0)
    if row is not None:
        kwargs.update(row=row, col=col)
    fig.add_hrect(**kwargs)


def _end_label(fig, x, y, text, color, xshift=10):
    fig.add_annotation(
        x=x, y=y, text=text, showarrow=False, xanchor="left",
        xshift=xshift, yanchor="middle",
        font=dict(color=color, size=12, family="Arial"),
    )


# ---------------------------------------------------------------- Executive Summary
def top_indicators_chart(analysis_df):
    series = [
        ("dietary_energy_adequacy_pct", "Dietary Energy Supply Adequacy", NEUTRAL),
        ("undernourishment_pct", "Undernourishment", WARNING),
        ("under5_stunting_pct", "Child Stunting", DANGER),
    ]
    fig = go.Figure()
    for ind, label, color in series:
        d = analysis_df[["Year", ind]].dropna()
        fig.add_trace(go.Scatter(
            x=d["Year"], y=d[ind], mode="lines+markers",
            name=label,
            line=dict(color=color, width=2.5), marker=dict(size=6),
            hovertemplate=f"<b>{label}</b><br>Year %{{x}}<br>%{{y:.1f}}%<extra></extra>",
        ))
    fig.update_layout(
        title="Key Food Security Indicators Over Time (2000-2025)",
        xaxis_title="Year", yaxis_title="Percent of population (%)",
        legend_font_color="white",
    )
    return _style(fig, height=520, legend=True)


def top_indicators_insight(analysis_df):
    dea = analysis_df.dropna(subset=["dietary_energy_adequacy_pct"]).sort_values("Year")
    unn = analysis_df.dropna(subset=["undernourishment_pct"]).sort_values("Year")
    stun = analysis_df.dropna(subset=["under5_stunting_pct"]).sort_values("Year")
    unn0, unn0y = unn["undernourishment_pct"].iloc[0], int(unn["Year"].iloc[0])
    stun0 = stun["under5_stunting_pct"].iloc[0]
    unn_v, unn_y = unn["undernourishment_pct"].iloc[-1], int(unn["Year"].iloc[-1])
    stun_v, stun_y = stun["under5_stunting_pct"].iloc[-1], int(stun["Year"].iloc[-1])
    dea_v, dea_y = dea["dietary_energy_adequacy_pct"].iloc[-1], int(dea["Year"].iloc[-1])
    return (
        f"Since {unn0y}, undernourishment has fallen from {unn0:.0f}% to {unn_v:.0f}% ({unn_y}) and child stunting "
        f"from {stun0:.0f}% to {stun_v:.0f}% ({stun_y}), while energy supply adequacy holds near {dea_v:.0f}% "
        f"({dea_y}). These are real long-run gains, yet hunger has not ended: the affordability data in later tabs "
        "shows that eating well remains out of reach for the majority of Kenyans. Kenya's survey-based food "
        "insecurity series only begins in 2016, so the long-run hunger line here uses the FAO undernourishment "
        "measure, which extends back to 2000."
    )


def correlation_chart(analysis_df):
    corr_df = analysis_df[["Year", "gdp_per_capita_ppp", "moderate_or_severe_food_insecurity_pct"]].dropna()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=corr_df["gdp_per_capita_ppp"],
        y=corr_df["moderate_or_severe_food_insecurity_pct"],
        mode="markers",
        customdata=corr_df["Year"],
        marker=dict(
            size=10,
            color="rgba(155,170,190,0.6)",
            line=dict(width=1, color="rgba(255,255,255,0.35)"),
        ),
        hovertemplate="<b>Year %{customdata}</b><br>GDP per capita: $%{x:,.0f}<br>Food Insecurity: %{y:.1f}%<extra></extra>",
    ))

    first = corr_df.iloc[0]
    fig.add_trace(go.Scatter(
        x=[first["gdp_per_capita_ppp"]], y=[first["moderate_or_severe_food_insecurity_pct"]],
        mode="markers+text",
        marker=dict(size=15, color=NEUTRAL, line=dict(width=2, color="white")),
        text=[f"{int(first['Year'])}: ${first['gdp_per_capita_ppp']:,.0f} &rarr; {first['moderate_or_severe_food_insecurity_pct']:.0f}%"],
        textposition="top left",
        textfont=dict(color=NEUTRAL, size=12),
        hovertemplate="<b>Start</b><br>GDP per capita: $%{x:,.0f}<br>Food Insecurity: %{y:.1f}%<extra></extra>",
    ))

    last = corr_df.iloc[-1]
    fig.add_trace(go.Scatter(
        x=[last["gdp_per_capita_ppp"]], y=[last["moderate_or_severe_food_insecurity_pct"]],
        mode="markers+text",
        marker=dict(size=18, color=DANGER, line=dict(width=2, color="white")),
        text=[f"{int(last['Year'])}: ${last['gdp_per_capita_ppp']:,.0f} &rarr; {last['moderate_or_severe_food_insecurity_pct']:.0f}%"],
        textposition="top left",
        textfont=dict(color=DANGER, size=13, family="Arial"),
        hovertemplate="<b>Latest year</b><br>GDP per capita: $%{x:,.0f}<br>Food Insecurity: %{y:.1f}%<extra></extra>",
    ))

    fig.add_annotation(
        xref="paper", yref="paper", x=0.5, y=1.02,
        text="GDP grew &rarr; food insecurity did not fall",
        showarrow=False,
        font=dict(color="white", size=13),
    )
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
    return (
        f"GDP per capita grew from roughly ${gdp_start:,.0f} to ${gdp_end:,.0f} over two decades, "
        f"yet food insecurity rose from {ins_start:.0f}% to {ins_end:.0f}%. "
        f"The correlation coefficient is {corr:+.2f}, confirming that higher GDP is not associated with lower "
        f"food insecurity. The benefits of economic growth have not reached the poorest Kenyans; rising food "
        f"prices, income inequality, and unequal access to resources mean growth alone is insufficient. "
        f"Targeted social protection, affordable-nutrition programs, and agricultural investment are essential."
    )


# ---------------------------------------------------------------- T2
def supply_breakdown_chart(analysis_df):
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Energy (kcal/day)", "Protein (g/day)", "Fat (g/day)"),
    )
    series = [
        ("food_supply_kcal_capita_day", 2100, 1800, NEUTRAL),
        ("protein_supply_g_capita_day", 50, 40, SAFE),
        ("fat_supply_g_capita_day", 40, 30, WARNING),
    ]
    for i, (ind, warn_val, danger_val, color) in enumerate(series):
        d = analysis_df[["Year", ind]].dropna()
        d["Color"] = d[ind].apply(lambda v, k=ind: status_color(v, k))
        fig.add_trace(
            go.Scatter(x=d["Year"], y=d[ind], mode="lines+markers",
                       line=dict(color=color, width=2.5),
                       marker=dict(color=d["Color"], size=8),
                       name=INDICATOR_META[ind]["label"],
                       hovertemplate=f"<b>Year %{{x}}</b><br>{INDICATOR_META[ind]['label']}: %{{y:.0f}} {INDICATOR_META[ind]['unit']}<extra></extra>"),
            row=1, col=i + 1,
        )
        fig.add_hline(y=warn_val, line_dash="dash", line_color=WARNING, line_width=1.5, row=1, col=i + 1,
                      annotation_text=f"{warn_val} min", annotation_position="top left",
                      annotation_font_color=WARNING, annotation_font_size=10)
        fig.add_hline(y=danger_val, line_dash="dash", line_color=DANGER, line_width=1.5, row=1, col=i + 1,
                      annotation_text=f"{danger_val} critical", annotation_position="top left",
                      annotation_font_color=DANGER, annotation_font_size=10)
        _critical_zone(fig, danger_val, warn_val, row=1, col=i + 1)
        last = d.iloc[-1]
        _end_label(fig, last["Year"], last[ind], f"{last[ind]:.0f}", status_color(last[ind], ind))
    fig.update_layout(showlegend=False)
    return _style(fig, height=CHART_HEIGHT)


def supply_breakdown_insight(analysis_df):
    kcal = analysis_df.dropna(subset=["food_supply_kcal_capita_day"]).sort_values("Year").iloc[-1]
    prot = analysis_df.dropna(subset=["protein_supply_g_capita_day"]).sort_values("Year").iloc[-1]
    fat = analysis_df.dropna(subset=["fat_supply_g_capita_day"]).sort_values("Year").iloc[-1]
    return (
        f"Kenya supplies about {kcal['food_supply_kcal_capita_day']:.0f} kcal, "
        f"{prot['protein_supply_g_capita_day']:.0f} g of protein, and {fat['fat_supply_g_capita_day']:.0f} g of fat "
        f"per person per day ({int(kcal['Year'])}), comfortably above the recommended minimums of 2,100 kcal, 50 g "
        "protein, and 40 g fat. In calorie terms Kenya has enough food for everyone - which sharpens the puzzle at "
        "the heart of this dashboard: enough food exists, yet millions go hungry because they cannot afford it. "
        "The next tabs examine who is left out and why."
    )


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
    _critical_zone(fig, 85, 90)
    last = data.iloc[-1]
    _end_label(fig, last["Year"], last["dietary_energy_adequacy_pct"], f"{last['dietary_energy_adequacy_pct']:.1f}%", status_color(last["dietary_energy_adequacy_pct"], "dietary_energy_adequacy_pct"))
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
    return (
        f"{insight_text('dietary_energy_adequacy_pct', val, year)} "
        "A value below 100% means Kenya cannot produce enough food for its population and must rely on "
        "imports and aid, which creates vulnerability to global price shocks and supply disruptions. "
        "When global food prices spike, as they did in 2008 and 2022, Kenya experiences immediate food crises."
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
    _critical_zone(fig, 25, 40)
    last = data.iloc[-1]
    _end_label(fig, last["Year"], last["undernourishment_pct"], f"{last['undernourishment_pct']:.1f}%", status_color(last["undernourishment_pct"], "undernourishment_pct"))
    fig.update_layout(
        title="Undernourishment Rate - Kenya",
        xaxis_title="Year", yaxis_title="% of population",
        yaxis_range=[0, 45],
    )
    return _style(fig, height=600)


def undernourishment_insight(analysis_df):
    data = analysis_df[["Year", "undernourishment_pct"]].dropna().sort_values("Year")
    val = data["undernourishment_pct"].iloc[-1]
    year = int(data["Year"].iloc[-1])
    base = insight_text("undernourishment_pct", val, year)
    if len(data) >= 2:
        old_year = int(data["Year"].iloc[0])
        old_val = data["undernourishment_pct"].iloc[0]
        delta = val - old_val
        direction = "declined" if delta < 0 else "increased"
        base += (
            f" Compared to {old_year}, when {old_val:.0f}% of the population was undernourished, the rate has "
            f"{direction} by {abs(delta):.1f} percentage points over {year - old_year} years."
        )
    return base


def food_insecurity_chart(analysis_df):
    mod_data = analysis_df[["Year", "moderate_or_severe_food_insecurity_pct"]].dropna()
    sev_data = analysis_df[["Year", "severe_food_insecurity_pct"]].dropna()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mod_data["Year"], y=mod_data["moderate_or_severe_food_insecurity_pct"],
        mode="lines+markers", name="Moderate or Severe",
        line=dict(color=DANGER, width=3.5), marker=dict(size=9),
        fill="tozeroy", fillcolor="rgba(231,76,60,0.10)",
        hovertemplate="<b>Year %{x}</b><br>Moderate/Severe: %{y:.1f}%<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=sev_data["Year"], y=sev_data["severe_food_insecurity_pct"],
        mode="lines+markers", name="Severe Only",
        line=dict(color=WARNING, width=2.5), marker=dict(size=7),
        hovertemplate="<b>Year %{x}</b><br>Severe: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=40, line_dash="dash", line_color=WARNING, annotation_text="40% warning", annotation_font_color=WARNING)
    fig.add_hline(y=60, line_dash="dash", line_color=DANGER, annotation_text="60% critical", annotation_font_color=DANGER)
    _critical_zone(fig, 60, 80)
    last_mod = mod_data.iloc[-1]
    _end_label(fig, last_mod["Year"], last_mod["moderate_or_severe_food_insecurity_pct"], f"{last_mod['moderate_or_severe_food_insecurity_pct']:.0f}%", DANGER)
    last_sev = sev_data.iloc[-1]
    _end_label(fig, last_sev["Year"], last_sev["severe_food_insecurity_pct"], f"{last_sev['severe_food_insecurity_pct']:.0f}%", WARNING)
    fig.update_layout(
        title="Food Insecurity Rates - Kenya",
        xaxis_title="Year", yaxis_title="% of population",
        yaxis_range=[0, 80],
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
    return (
        f"{insight_text('moderate_or_severe_food_insecurity_pct', mod_val, mod_year)} "
        f"{insight_text('severe_food_insecurity_pct', sev_val, sev_year)} "
        "Food insecurity exists on a spectrum from mild anxiety about food availability to extreme deprivation. "
        f"The gap between moderate or severe ({mod_val:.0f}%) and severe ({sev_val:.0f}%) represents people who "
        "worry about food or skip meals but do not go entire days without eating. Both measures have worsened "
        "significantly since 2016, reflecting drought, economic shocks, and the COVID-19 pandemic; the narrowing "
        "gap means more people are sliding from moderate into severe food insecurity."
    )


def affordability_chart(analysis_df):
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Cost of Healthy Diet (Int$/day)", "% Cannot Afford", "People Unable (millions)"),
    )
    afford_data = [
        ("healthy_diet_cost_ppp_per_day", 3.5, 5.0, NEUTRAL),
        ("healthy_diet_unaffordable_pct", 50, 70, DANGER),
        ("people_unable_afford_healthy_diet_million", 20, 35, WARNING),
    ]
    for i, (ind, warn_val, danger_val, color) in enumerate(afford_data):
        d = analysis_df[["Year", ind]].dropna()
        d["Color"] = d[ind].apply(lambda v, k=ind: status_color(v, k))
        fig.add_trace(
            go.Scatter(x=d["Year"], y=d[ind], mode="lines+markers",
                       marker=dict(color=d["Color"], size=8),
                       line=dict(color=color, width=2.5 if color == DANGER else 2),
                       name=INDICATOR_META[ind]["label"],
                       hovertemplate=f"<b>Year %{{x}}</b><br>{INDICATOR_META[ind]['label']}: %{{y:.1f}} {INDICATOR_META[ind]['unit']}<extra></extra>"),
            row=1, col=i + 1
        )
        fig.add_hline(y=warn_val, line_dash="dash", line_color=WARNING, line_width=1.5, row=1, col=i + 1,
                      annotation_text=f"{warn_val} warn", annotation_position="top left",
                      annotation_font_color=WARNING, annotation_font_size=10)
        fig.add_hline(y=danger_val, line_dash="dash", line_color=DANGER, line_width=1.5, row=1, col=i + 1,
                      annotation_text=f"{danger_val} critical", annotation_position="top left",
                      annotation_font_color=DANGER, annotation_font_size=10)
        _critical_zone(fig, danger_val, danger_val * 1.4, row=1, col=i + 1)
        last = d.iloc[-1]
        _end_label(fig, last["Year"], last[ind], f"{last[ind]:.1f}", status_color(last[ind], ind))
    fig.update_layout(showlegend=False)
    _style(fig, height=CHART_HEIGHT)
    return fig


def affordability_insight(analysis_df):
    val = analysis_df.dropna(subset=["healthy_diet_unaffordable_pct"]).sort_values("Year").tail(1)["healthy_diet_unaffordable_pct"].iloc[0]
    year = int(analysis_df.dropna(subset=["healthy_diet_unaffordable_pct"]).sort_values("Year").tail(1)["Year"].iloc[0])
    people_unafford = analysis_df.dropna(subset=["people_unable_afford_healthy_diet_million"]).sort_values("Year").tail(1)["people_unable_afford_healthy_diet_million"].iloc[0]
    return (
        f"{insight_text('healthy_diet_unaffordable_pct', val, year)} "
        f"A healthy diet costs approximately $3.20 per person per day. With {people_unafford:.0f} million Kenyans "
        "unable to afford it, the majority of the population relies on cheap, nutrient-poor staples such as maize, "
        "ugali, and porridge. This explains the paradox of high calorie adequacy but high stunting rates: people get "
        "enough calories but not enough nutrients. Availability without access is not food security."
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
    _critical_zone(fig, 30, 45, row=1, col=1)
    last_st = st_data.iloc[-1]
    _end_label(fig, last_st["Year"], last_st["under5_stunting_pct"], f"{last_st['under5_stunting_pct']:.1f}%", status_color(last_st["under5_stunting_pct"], "under5_stunting_pct"))

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
        _critical_zone(fig, 15, 30, row=1, col=2)
        last_wa = wa_data.iloc[-1]
        _end_label(fig, last_wa["Year"], last_wa["under5_wasting_pct"], f"{last_wa['under5_wasting_pct']:.1f}%", status_color(last_wa["under5_wasting_pct"], "under5_wasting_pct"))

    fig.update_layout(showlegend=False, height=600)
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
        "Stunting reflects chronic, long-term malnutrition that develops over months or years and causes "
        "permanent physical and cognitive damage; wasting reflects acute, recent food shortage and can often "
        "be reversed with proper nutrition. Stunting has improved dramatically, from roughly 38% in 2000 to "
        "about 18% in 2024, yet the remaining children still face lifelong limits, and wasting fluctuates with "
        "drought cycles and remains a persistent threat."
    )
    return " ".join(parts)


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


def county_ranking_insight(county_risk_summary, top_n=15):
    top = county_risk_summary.head(top_n)
    n_crit = int((top["total_critical_flags"] > 0).sum())
    top_name = top.iloc[0]["adm1_name"]
    top_flags = int(top.iloc[0]["total_critical_flags"] + top.iloc[0]["total_heightened_flags"])
    return (
        f"The top {top_n} highest-risk counties account for {n_crit} counties with at least one critical JMR alert. "
        f"{top_name} leads with {top_flags} combined alert flags. These stacked bars show both critical (red) and "
        "heightened (amber) flags, so a county with many yellow bars may be nearly as urgent as one with a few red "
        "ones. This ranking helps prioritise where limited humanitarian resources should go first."
    )


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
    return (
        f"On {latest_alert_date.date()}, {n_crit} counties are at critical risk and {n_high} at heightened risk "
        f"across the alert indicators, while {n_typ} remain typical. The most affected counties are {', '.join(top)}. "
        "These are the areas where climate shocks, conflict, food-price spikes, and exchange-rate volatility are "
        "currently combining to push sub-counties past the critical threshold, so priority food assistance and "
        "early-warning response should target them first."
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


def county_pie_insight(county_risk_summary):
    counts = county_risk_summary["overall_alert_label"].value_counts()
    n_crit = int(counts.get("Critical", 0))
    n_high = int(counts.get("Heightened", 0))
    n_typ = int(counts.get("Typical", 0))
    return (
        f"Of Kenya's 47 counties, {n_crit} are at critical risk, {n_high} at heightened risk, "
        f"and only {n_typ} are currently typical. More than a quarter of counties sit in the critical "
        "zone, meaning multiple food-security indicators have already triggered alerts. The crisis is "
        "not evenly spread: it clusters in the arid and semi-arid north, while the highlands remain "
        "comparatively stable."
    )


def most_affected_chart(county_risk_summary, top_n=5):
    summary = county_risk_summary.copy()
    summary["flags"] = summary["total_critical_flags"] + summary["total_heightened_flags"]

    def bar_color(row):
        return ALERT_COLORS.get(row["overall_max_alert"], NEUTRAL)

    top = summary.head(top_n).iloc[::-1]

    fig = go.Figure(go.Bar(
        y=top["adm1_name"], x=top["flags"], orientation="h",
        marker_color=[bar_color(r) for _, r in top.iterrows()],
        text=top["flags"], textposition="outside", textfont_color="white",
        hovertemplate="<b>%{y}</b><br>Alert flags: %{x}<extra></extra>",
    ))
    fig.update_layout(
        title=f"Counties Most Affected by Food-Security Alerts (top {top_n})",
        showlegend=False,
    )
    return _style(fig, height=max(320, 28 * len(top) + 140))


def county_snapshot_insight(county_risk_summary, latest_alert_date):
    n_crit = int((county_risk_summary["overall_max_alert"] == 2).sum())
    n_high = int((county_risk_summary["overall_max_alert"] == 1).sum())
    n_typ = int((county_risk_summary["overall_max_alert"] == 0).sum())
    top = county_risk_summary.head(5)["adm1_name"].tolist()
    return (
        f"On {latest_alert_date.date()}, {n_crit} of Kenya's 47 counties are at critical risk and {n_high} are "
        f"heightened, while {n_typ} are currently typical. The most affected counties are {', '.join(top)}. "
        "National averages smooth away these differences, hiding the counties where drought, food prices, exchange "
        "rates, and conflict are already pushing people past the critical threshold. The county analysis in Act 3 "
        "shows exactly where."
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
    df = df.sort_values(indicator).tail(top_n)
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


def county_indicator_insight(county_stats, indicator):
    meta = COUNTY_INDICATORS[indicator]
    df = county_stats.dropna(subset=[indicator]).sort_values(indicator, ascending=False)
    if df.empty:
        return "No county-level data available for this indicator."
    worst_name, worst = df["adm1_name"].iloc[0], df[indicator].iloc[0]
    best_name, best = df["adm1_name"].iloc[-1], df[indicator].iloc[-1]
    top3 = df.head(3)["adm1_name"].tolist()
    warn_thr, danger_thr = meta["thresholds"]
    n_above_danger = int((df[indicator] >= danger_thr).sum()) if danger_thr else 0
    n_above_warn = int((df[indicator] >= warn_thr).sum()) if warn_thr else 0
    notes = {
        "stunting_pct": (
            f"Under WHO classification, stunting above 30% is very high and 20-30% is high. "
            f"{n_above_danger} counties exceed the 30% very-high threshold and {n_above_warn} exceed 20%, "
            "meaning a generation of children in those areas faces lifelong physical and cognitive limitations."
        ),
        "wasting_pct": (
            f"Wasting is acute malnutrition that can be reversed with timely treatment. WHO treats "
            f"anything above 15% as critical and 5-15% as serious. "
            f"{n_above_danger} counties exceed the 15% critical threshold and need life-saving "
            "therapeutic feeding now."
        ),
        "poverty_pct": (
            f"Poverty is the root cause that makes food unaffordable even when it is available. "
            f"{n_above_danger} counties exceed the 60% poverty threshold and {n_above_warn} exceed 40%, "
            "concentrated in the same arid and semi-arid areas flagged by the JMR risk maps."
        ),
        "severe_poverty_pct": (
            f"Severe poverty indicates households that cannot meet basic needs. "
            f"{n_above_danger} counties exceed the 40% severe-poverty threshold, "
            "meaning nearly half the population in those counties lives in extreme deprivation."
        ),
    }
    note = notes.get(indicator, "")
    return (
        f"For {meta['label']}, the worst-affected county is {worst_name} at {worst:.1f}%, followed by "
        f"{', '.join(top3[1:])}; the county with the lowest rate is {best_name} at {best:.1f}%. {note} The wide "
        "spread between counties shows this is not a uniform national problem but a geographically "
        "concentrated one, which is exactly why county-level targeting matters."
    )


def county_crisis_chart(county_stats, top_n=47):
    df = county_stats.dropna(subset=["ipc_crisis_pct"]).sort_values("ipc_crisis_pct").tail(top_n)
    fig = go.Figure(go.Bar(
        y=df["adm1_name"], x=df["ipc_crisis_pct"], orientation="h",
        marker_color=DANGER,
        text=[f"{v:.1f}%" for v in df["ipc_crisis_pct"]],
        textposition="outside", textfont_color="white",
        hovertemplate="<b>%{y}</b><br>% in crisis: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title=f"Share of Population in Acute Food Insecurity (IPC Phase 3+) by County - top {len(df)} (Feb 2026)",
        xaxis_title="% of county population in crisis", yaxis_title="County",
        showlegend=False,
    )
    return _style(fig, height=max(320, 22 * len(df) + 120))


def county_crisis_insight(county_stats):
    df = county_stats.dropna(subset=["ipc_crisis_pct"]).sort_values("ipc_crisis_pct", ascending=False)
    if df.empty:
        return "No IPC crisis data available."
    worst_name = df["adm1_name"].iloc[0]
    worst = df["ipc_crisis_pct"].iloc[0]
    top3 = df.head(3)["adm1_name"].tolist()
    has_pop = "ipc_crisis_population" in df.columns and df["ipc_crisis_population"].notna().any()
    total_pop = int(df["ipc_crisis_population"].sum()) if has_pop else None
    n_above_20 = int((df["ipc_crisis_pct"] >= 20).sum())
    pop_text = (
        f" Across all counties with data, an estimated {total_pop:,} people face acute food insecurity (IPC Phase 3+). "
        if total_pop else ""
    )
    return (
        f"In the February 2026 IPC analysis, {worst_name} has the largest share of its population in acute food "
        f"insecurity at {worst:.0f}%, followed by {', '.join(top3[1:])}. "
        f"{n_above_20} of the {len(df)} counties exceed the 20% crisis threshold.{pop_text}"
        "Using percentages makes counties comparable regardless of size: they show how deeply each county is "
        "affected relative to its own population. The counties with the largest shares are the arid and semi-arid "
        "north, matching the counties the JMR risk maps flag as critical."
    )


def heatmap_insight(county_risk_summary):
    return (
        "Each cell shows the maximum alert level (Typical 0, Heightened 1, Critical 2) reached by any sub-county for "
        "a given indicator. A red cell means that indicator already triggered a critical alert somewhere in that county "
        "and warrants immediate action; yellow means elevated but not yet critical. The indicators - food prices, "
        "exchange rates, drought (NDVI and rainfall), and conflict - move independently, so a county can be critical "
        "on one indicator while typical on another. Reading across a row shows which risk drivers contribute most to "
        "each county's overall alert."
    )