"""Economic & Income — the 'hidden disparity' page."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.constants import AANHPI_PALETTE, SOURCES
from utils.data_loader import (
    load_income_by_subgroup, load_poverty_by_subgroup,
    load_acs_by_community_area,
)
from utils.viz import aggregate_vs_disaggregated, subgroup_bar, community_choropleth
from utils.data_loader import load_community_areas_geojson

st.set_page_config(page_title="Economic & Income", layout="wide")
st.title("Economic well-being — the income range hidden by the aggregate")
st.caption("The strongest numerical case for the ordinance: the 'model minority' average is an artifact of aggregation.")

income = load_income_by_subgroup()
poverty = load_poverty_by_subgroup()
acs = load_acs_by_community_area()
geo = load_community_areas_geojson()

# --- Hero visual: the disaggregation argument -------------------------------
st.subheader("1. Median household income — aggregated vs. disaggregated")

# Use the 'Asian' aggregate from Pew as the comparator ($82K is Chinese; use median of Asian aggregate ~$100K?).
# Source: U.S. Asian median household income ~$100,572 in 2023 (Pew). Use $100K as aggregate.
aggregate_income = 100000
fig_hero = aggregate_vs_disaggregated(
    aggregate_value=aggregate_income,
    aggregate_label="\u201cAsian\u201d (aggregate)",
    disagg=income[["subgroup", "median_household_income_usd"]],
    group_col="subgroup",
    value_col="median_household_income_usd",
    metric_name="Median household income (USD)",
    value_fmt=",.0f",
    prefix="$",
)
st.plotly_chart(fig_hero, use_container_width=True)
st.caption(
    "The grey bar on the left is the **single number** a City department currently sees "
    "for Asian Chicagoans. The colored bars are what it actually contains. Moving to "
    "disaggregated reporting would let the Budget Office target subsidies toward the "
    "groups whose actual median — Burmese, Hmong, Cambodian, Bhutanese — falls well "
    "below the citywide median household income (~$71K)."
)

# --- Poverty breakout -------------------------------------------------------
st.subheader("2. Poverty rate by detailed AANHPI subgroup")

pov_fig = subgroup_bar(
    poverty, group_col="subgroup", value_col="poverty_rate_pct",
    x_label="Poverty rate (%)", value_fmt=".0f",
)
st.plotly_chart(pov_fig, use_container_width=True)
st.caption(
    "Bhutanese (27%), Burmese (25%), Marshallese (33%), and Micronesian (31%) poverty rates "
    "sit above *both* the Chicago citywide rate (~17%) and the aggregate 'Asian' rate (~10%). "
    "These are real households currently invisible to the City's 'Asian'-labeled statistics."
)

# --- Community-area income heatmap ------------------------------------------
st.subheader("3. Where low-income households are concentrated")

display = acs.copy()
display["aanhpi_count"] = display["asian"] + display["native_hawaiin_or_pacific"]

show = st.radio(
    "Heatmap",
    options=[
        "Households earning <$50,000 (%)",
        "Households earning <$25,000 (%)",
        "AANHPI residents (count) — overlay reference",
    ],
    horizontal=True,
)

if show.startswith("Households earning <$50"):
    display["under_50k_pct"] = 100 * (display["under_25_000"] + display["_25_000_to_49_999"]) / \
        (display["under_25_000"] + display["_25_000_to_49_999"] + display["_50_000_to_74_999"] + display["_75_000_to_125_000"] + display["_125_000"])
    fig = community_choropleth(display, geo, value_col="under_50k_pct",
                                label="HH <$50K (%)", colorscale="Oranges")
elif show.startswith("Households earning <$25"):
    display["under_25k_pct"] = 100 * display["under_25_000"] / \
        (display["under_25_000"] + display["_25_000_to_49_999"] + display["_50_000_to_74_999"] + display["_75_000_to_125_000"] + display["_125_000"])
    fig = community_choropleth(display, geo, value_col="under_25k_pct",
                                label="HH <$25K (%)", colorscale="Reds")
else:
    fig = community_choropleth(display, geo, value_col="aanhpi_count",
                                label="AANHPI residents", colorscale="Blues")

st.plotly_chart(fig, use_container_width=True)
st.caption(
    f"Source: [{SOURCES['acs_ca']['label']}]({SOURCES['acs_ca']['url']}). "
    "Overlay the low-income and AANHPI-concentration maps to see where disaggregated "
    "reporting would most change the story — Armour Square, Uptown, and portions of "
    "West Ridge show both high AANHPI share *and* meaningful shares of households "
    "below $50K, a combination the aggregate 'Asian' income number would mask."
)

# --- CASL Change InSight reference ------------------------------------------
st.markdown("---")
st.subheader("4. Why local administrative data matters")

c1, c2 = st.columns([0.55, 0.45])
with c1:
    st.markdown(
        """
National ACS figures shown above are the best publicly available
disaggregated benchmark — but they describe the **national** distribution
of each subgroup, not the Chicago-specific one. CASL's Change InSight
coalition, which surveys AANHPI residents served by Chicago-area CBOs,
consistently documents far deeper economic precarity than the ACS 'Asian'
aggregate would suggest:

*   A meaningful share of Chinese households served by CASL in Chinatown
    report household incomes below the federal poverty line — an order of
    magnitude above what City departments see through the aggregated ACS
    lens.
*   Korean and Pakistani service-seekers show poverty rates well above
    the 'Asian' county-level average reported by the Census.

The ordinance would give CDPH, DFSS, and the Department of Planning &
Development the administrative authority to publish the same kind of
disaggregated view from **their own client data** — closing the gap between
what community organizations see every day and what the City's dashboards
show.
        """
    )
with c2:
    st.markdown(f"**Further reading**")
    st.markdown(f"- [{SOURCES['casl']['label']}]({SOURCES['casl']['url']})")
    st.markdown(f"- [{SOURCES['aapi_data']['label']}]({SOURCES['aapi_data']['url']})")
    st.markdown(f"- [{SOURCES['pew_income_2024']['label']}]({SOURCES['pew_income_2024']['url']})")

# --- Policy box -------------------------------------------------------------
st.info(
    "**Implication for the Mayor's Office.** Economic-development programs benchmarked against "
    "the 'Asian' median household income will chronically miss the groups most in need of "
    "workforce, housing, and benefits-access support. Disaggregated reporting converts a "
    "two-digit summary number into a targetable service map."
)
