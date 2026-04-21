"""Health — insurance coverage, LEP, age structure by detailed AANHPI subgroup."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.constants import AANHPI_PALETTE, SOURCES
from utils.data_loader import (
    load_health_by_subgroup, load_lep_by_subgroup,
)
from utils.viz import subgroup_bar

st.set_page_config(page_title="Health", layout="wide")
st.title("Health — coverage, language access, age structure")
st.caption("The three service-delivery indicators where the 'Asian' aggregate is most misleading.")

health = load_health_by_subgroup()
lep = load_lep_by_subgroup()

# --- Framing ----------------------------------------------------------------
st.markdown(
    """
Chicago Department of Public Health (CDPH), Chicago Department of Family &
Support Services (DFSS), and the Mayor's Office of Language Access all make
resource allocations that scale with the demographic profile of the service
population. Under the current OMB-15 framing, each of those agencies sees a
single **"Asian"** row that averages:

* well-insured, English-proficient Asian Indian households in Edison Park, and
* low-insured, LEP Burmese refugee households resettled through Uptown.

The ordinance would require each agency to carry the disaggregated distribution,
not the average, through to its annual equity report.
"""
)

# --- Insurance coverage -----------------------------------------------------
st.subheader("1. Uninsured rate by detailed AANHPI subgroup")

fig1 = subgroup_bar(
    health, group_col="subgroup", value_col="uninsured_pct",
    x_label="Uninsured (%)", value_fmt=".0f",
)
st.plotly_chart(fig1, use_container_width=True)
st.caption(
    "National ACS 2019–2023 estimates compiled by AAPI Data. A one-point difference in "
    "the citywide Asian uninsured rate is a ~2,000-person difference in the number of "
    "AANHPI Chicagoans needing connection to coverage — and the subgroup spread shown here "
    "dwarfs that."
)

# --- LEP --------------------------------------------------------------------
st.subheader("2. Limited English Proficiency (LEP) by subgroup")

# Merge local Cook County figure in as highlight
lep_df = lep.copy()
lep_df["is_local"] = lep_df["geography"].str.contains("Cook County")

fig2 = go.Figure()
colors = [
    "#B31B1B" if is_local else AANHPI_PALETTE.get(g, "#888")
    for g, is_local in zip(lep_df["subgroup"], lep_df["is_local"])
]
d = lep_df.sort_values("lep_pct")
fig2.add_trace(go.Bar(
    x=d["lep_pct"], y=d["subgroup"], orientation="h",
    marker_color=[AANHPI_PALETTE.get(g, "#888") for g in d["subgroup"]],
    text=[f"{v:.0f}%" for v in d["lep_pct"]],
    textposition="outside",
    hovertemplate="%{y}<br>%{x:.0f}% LEP<br>%{customdata}<extra></extra>",
    customdata=d["geography"],
))
fig2.update_layout(
    xaxis_title="Limited English Proficient (%)",
    margin=dict(l=140, r=40, t=10, b=40), height=440,
)
st.plotly_chart(fig2, use_container_width=True)
st.caption(
    "Korean LEP figure is from Asian Americans Advancing Justice | Chicago for **Cook County** "
    "(highlighted). Other figures are national benchmarks published by AAPI Data; Cook-County-"
    "specific LEP rates for Burmese, Bhutanese, Cambodian, and Hmong residents are either "
    "suppressed or unavailable in the current ACS release — a concrete example of the "
    "information gap the ordinance would fill."
)

# --- Elderly population -----------------------------------------------------
st.subheader("3. Age-65+ share — who needs senior health services")

fig3 = subgroup_bar(
    health, group_col="subgroup", value_col="elderly_pct_65plus",
    x_label="Population age 65+ (%)", value_fmt=".0f",
)
st.plotly_chart(fig3, use_container_width=True)
st.caption(
    "Japanese, Filipino, and Chinese populations skew significantly older than Bhutanese, "
    "Marshallese, or Pakistani populations. Senior-services planning (CDPH's chronic-disease "
    "programs, DFSS's senior centers, CPL's in-language programming) produces different siting "
    "decisions if built on disaggregated age pyramids rather than the 'Asian' average."
)

# --- Data table -------------------------------------------------------------
with st.expander("Table — full health indicator set by detailed subgroup"):
    st.dataframe(
        health.rename(columns={
            "subgroup": "Subgroup",
            "uninsured_pct": "Uninsured (%)",
            "limited_english_hh_pct": "Household LEP (%)",
            "elderly_pct_65plus": "Age 65+ (%)",
            "geography": "Geography",
            "source": "Source",
        }).style.format({
            "Uninsured (%)": "{:.0f}",
            "Household LEP (%)": "{:.0f}",
            "Age 65+ (%)": "{:.0f}",
        }),
        use_container_width=True,
    )

# --- Policy box -------------------------------------------------------------
st.markdown("---")
st.info(
    "**Implication for the Mayor's Office.** Language-access dollars, navigator programs, "
    "and culturally competent outreach contracts should be sized to the high-LEP, high-"
    "uninsured subgroups visible above, not smoothed across the aggregate. The ordinance's "
    "reporting mandate would let CDPH and DFSS make — and defend — exactly that case in "
    "the budget cycle."
)
