"""Population & Language — tract / community-area heatmaps and language detail."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.constants import AANHPI_PALETTE, FOCAL_COMMUNITY_AREAS, SOURCES
from utils.data_loader import (
    load_acs_by_community_area,
    load_community_areas_geojson,
    load_detailed_aanhpi_chicago,
    load_detailed_aanhpi_cook,
    load_languages_by_community_area,
)
from utils.viz import community_choropleth, subgroup_bar

st.set_page_config(page_title="Population & Language", layout="wide")
st.title("Population & Language")
st.caption("Where Chicago's AANHPI communities live — and the languages they speak at home.")

acs = load_acs_by_community_area()
geo = load_community_areas_geojson()
lang = load_languages_by_community_area()
chi_det = load_detailed_aanhpi_chicago()
cook_det = load_detailed_aanhpi_cook()

# =============================================================================
# Section 1: Heatmap of Asian + NHPI population by Community Area
# =============================================================================
st.subheader("1. Chicago Community Area heatmap")

mode = st.radio(
    "Heatmap indicator",
    options=[
        "AANHPI residents (count)",
        "AANHPI share of population (%)",
        "Households earning under $50,000 (%)",
    ],
    horizontal=True,
)

display = acs.copy()
display["aanhpi_count"] = display["asian"] + display["native_hawaiin_or_pacific"]
display["aanhpi_share_pct"] = 100 * display["aanhpi_count"] / display["total_population"]

if mode.startswith("AANHPI residents"):
    fig = community_choropleth(
        display, geo,
        value_col="aanhpi_count",
        label="AANHPI residents",
        colorscale="Reds",
    )
elif mode.startswith("AANHPI share"):
    fig = community_choropleth(
        display, geo,
        value_col="aanhpi_share_pct",
        label="AANHPI share (%)",
        colorscale="Reds",
    )
else:
    fig = community_choropleth(
        display, geo,
        value_col="under_50k_share_pct",
        label="Households <$50K (%)",
        colorscale="Oranges",
    )

st.plotly_chart(fig, use_container_width=True)
st.caption(
    f"Source: [{SOURCES['acs_ca']['label']}]({SOURCES['acs_ca']['url']}). "
    "Note: Chicago open data currently reports **Asian** as a single aggregate; "
    "detailed subgroup breakdowns below come from the 2020 Census DHC-A."
)

# =============================================================================
# Section 2: Top community areas for AANHPI residents
# =============================================================================
st.subheader("2. Where AANHPI residents are concentrated")
left, right = st.columns([0.6, 0.4])

top = (
    display.sort_values("aanhpi_count", ascending=False)
    .head(15)[["community_area", "aanhpi_count", "aanhpi_share_pct", "total_population"]]
    .rename(columns={
        "community_area": "Community Area",
        "aanhpi_count": "AANHPI residents",
        "aanhpi_share_pct": "AANHPI share (%)",
        "total_population": "Total population",
    })
)

with left:
    fig_bar = go.Figure(go.Bar(
        x=top["AANHPI residents"], y=top["Community Area"],
        orientation="h", marker_color="#B31B1B",
        text=[f"{v:,.0f}" for v in top["AANHPI residents"]],
        textposition="outside",
        hovertemplate="%{y}<br>%{x:,.0f} AANHPI residents<extra></extra>",
    ))
    fig_bar.update_layout(
        yaxis=dict(autorange="reversed"),
        margin=dict(l=160, r=40, t=10, b=40), height=520,
        xaxis_title="AANHPI residents",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with right:
    st.markdown("**Focal neighborhoods**")
    st.markdown(
        "\n".join(
            [
                "- **Armour Square / Bridgeport / McKinley Park** — Chinatown core and its South Loop / Near South expansion.",
                "- **West Ridge** — Devon Avenue: largest South Asian commercial corridor in the Midwest.",
                "- **Albany Park / North Park / Irving Park** — Korean and Filipino concentration; Southeast Asian mix.",
                "- **Uptown / Edgewater / Rogers Park** — Vietnamese and Southeast Asian refugee-resettlement legacy neighborhoods.",
            ]
        )
    )
    st.dataframe(
        top.style.format({"AANHPI residents": "{:,.0f}", "AANHPI share (%)": "{:.1f}",
                          "Total population": "{:,.0f}"}),
        height=360, use_container_width=True,
    )

# =============================================================================
# Section 3: Detailed subgroup breakdown (Chicago city, 2020)
# =============================================================================
st.subheader("3. The detail the aggregate hides — Chicago city, 2020 Census")

lc, rc = st.columns([0.55, 0.45])

with lc:
    bar = subgroup_bar(
        chi_det, group_col="subgroup", value_col="population_2020",
        x_label="Population (Chicago city, 2020)",
    )
    st.plotly_chart(bar, use_container_width=True)

with rc:
    st.markdown(
        """
**What's in "Other Asian."** The residual category on the chart at left
includes Cambodian, Hmong, Laotian, Burmese, Thai, Nepalese, Bangladeshi,
Bhutanese, Sri Lankan, Indonesian, Malaysian, Taiwanese, and more.

Several of these communities are themselves sizable, but the Census only
publishes them separately at county-or-larger geographies — and City
departments do not collect them at all on intake forms. The ordinance
would close that gap.
        """
    )
    st.markdown("**Cook County \u201calone-or-in-any-combination\u201d comparator**")
    cook_show = cook_det[["subgroup", "population_alone_2020"]].rename(
        columns={"subgroup": "Detailed group", "population_alone_2020": "Cook County (alone)"}
    )
    st.dataframe(
        cook_show.style.format({"Cook County (alone)": "{:,.0f}"}),
        height=310, use_container_width=True,
    )

# =============================================================================
# Section 4: Non-English languages by Community Area
# =============================================================================
st.subheader("4. Asian-origin languages spoken at home, by Community Area")

lang_cols = {
    "chinese": "Chinese",
    "korean": "Korean",
    "vietnamese": "Vietnamese",
    "japanese": "Japanese",
    "tagalog": "Tagalog",
    "hindi": "Hindi",
    "gujarati": "Gujarati",
    "urdu": "Urdu",
    "cambodian_mon_khmer_": "Cambodian / Mon-Khmer",
    "hmong": "Hmong",
    "laotian": "Laotian",
    "thai": "Thai",
    "other_asian": "Other Asian language",
}
available = [k for k in lang_cols if k in lang.columns]
sel = st.selectbox(
    "Language",
    options=available,
    format_func=lambda k: lang_cols[k],
    index=0,
)

lang_df = (
    lang.drop(columns=[c for c in ("community_area",) if c in lang.columns])
        .rename(columns={"community_area_name": "community_area"})
        .copy()
)
lang_df[sel] = pd.to_numeric(lang_df[sel], errors="coerce").fillna(0)

fig_lang = community_choropleth(
    lang_df, geo,
    value_col=sel, label=f"{lang_cols[sel]} speakers (age 5+)",
    colorscale="PuBuGn", hover_fmt=":,.0f",
)
st.plotly_chart(fig_lang, use_container_width=True)
st.caption(
    f"Source: [{SOURCES['languages_ca']['label']}]({SOURCES['languages_ca']['url']}). "
    "The Census Bureau last published Community-Area-level language-at-home counts in the "
    "2008–2012 ACS 5-year release. Refreshing this at a usable geography is one of the "
    "most concrete benefits of a local data-disaggregation ordinance paired with the "
    "Language Access Ordinance."
)

# =============================================================================
# Section 5: Policy implication box
# =============================================================================
st.markdown("---")
st.info(
    "**Implication for the Mayor's Office.** Chicago's AANHPI residents are geographically "
    "concentrated but ethnolinguistically heterogeneous. Department-level service design, "
    "translation budgeting, and outreach targeting based on the single \"Asian\" field cannot "
    "respond to this heterogeneity. The ordinance standardizes the intake categories the "
    "City needs to plan against the real map above, not the average."
)
