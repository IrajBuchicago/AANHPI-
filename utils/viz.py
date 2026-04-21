"""Reusable Plotly figure builders."""
from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from .constants import AANHPI_PALETTE


CHICAGO_CENTER = {"lat": 41.8400, "lon": -87.6850}


def community_choropleth(
    df: pd.DataFrame,
    geojson: dict,
    value_col: str,
    name_col: str = "community_area",
    label: str = "Value",
    colorscale: str = "Reds",
    hover_fmt: str = ":,.0f",
) -> go.Figure:
    """Render a choropleth over Chicago's 77 community areas."""
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations=name_col,
        featureidkey="properties.community",
        color=value_col,
        color_continuous_scale=colorscale,
        mapbox_style="carto-positron",
        center=CHICAGO_CENTER,
        zoom=9.3,
        opacity=0.78,
        hover_name=name_col,
        hover_data={value_col: True, name_col: False},
        labels={value_col: label},
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar={"title": label, "thickness": 12, "len": 0.7},
        height=560,
    )
    fig.update_traces(marker_line_width=0.4, marker_line_color="#555")
    return fig


def subgroup_bar(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    x_label: str,
    y_label: str = "",
    sort: bool = True,
    horizontal: bool = True,
    value_fmt: str = ",.0f",
) -> go.Figure:
    """Colored bar chart keyed off AANHPI_PALETTE."""
    d = df.copy()
    if sort:
        d = d.sort_values(value_col, ascending=horizontal)
    colors = [AANHPI_PALETTE.get(g, "#888") for g in d[group_col]]

    if horizontal:
        fig = go.Figure(go.Bar(
            x=d[value_col], y=d[group_col], orientation="h",
            marker_color=colors,
            text=[f"{v:{value_fmt}}" for v in d[value_col]],
            textposition="outside",
            hovertemplate=f"%{{y}}<br>{x_label}: %{{x:{value_fmt}}}<extra></extra>",
        ))
        fig.update_layout(xaxis_title=x_label, yaxis_title=y_label,
                          margin=dict(l=130, r=40, t=10, b=40), height=420)
    else:
        fig = go.Figure(go.Bar(
            x=d[group_col], y=d[value_col],
            marker_color=colors,
            text=[f"{v:{value_fmt}}" for v in d[value_col]],
            textposition="outside",
            hovertemplate=f"%{{x}}<br>{y_label}: %{{y:{value_fmt}}}<extra></extra>",
        ))
        fig.update_layout(xaxis_title="", yaxis_title=y_label,
                          margin=dict(l=40, r=40, t=10, b=40), height=420)
    return fig


def aggregate_vs_disaggregated(
    aggregate_value: float,
    aggregate_label: str,
    disagg: pd.DataFrame,
    group_col: str,
    value_col: str,
    metric_name: str,
    value_fmt: str = ",.0f",
    prefix: str = "",
    suffix: str = "",
) -> go.Figure:
    """Side-by-side: the single 'Asian' number vs the scatter of subgroup values.
    This is the core visual argument for disaggregation."""
    d = disagg.sort_values(value_col)
    colors = [AANHPI_PALETTE.get(g, "#888") for g in d[group_col]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[aggregate_label], y=[aggregate_value],
        marker_color="#777777", width=[0.45],
        text=[f"{prefix}{aggregate_value:{value_fmt}}{suffix}"],
        textposition="outside",
        name="Aggregated",
        hovertemplate=f"{aggregate_label}<br>{metric_name}: {prefix}%{{y:{value_fmt}}}{suffix}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=d[group_col], y=d[value_col],
        marker_color=colors, width=[0.7]*len(d),
        text=[f"{prefix}{v:{value_fmt}}{suffix}" for v in d[value_col]],
        textposition="outside",
        name="Disaggregated",
        hovertemplate=f"%{{x}}<br>{metric_name}: {prefix}%{{y:{value_fmt}}}{suffix}<extra></extra>",
    ))
    fig.update_layout(
        showlegend=False, yaxis_title=metric_name,
        margin=dict(l=40, r=20, t=10, b=60), height=440,
        xaxis={"tickangle": -35},
    )
    return fig
