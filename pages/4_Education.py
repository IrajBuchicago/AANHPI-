"""Education — attainment and school-age population by detailed AANHPI subgroup."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.constants import AANHPI_PALETTE, SOURCES
from utils.data_loader import load_education_by_subgroup, load_acs_by_community_area
from utils.viz import subgroup_bar

st.set_page_config(page_title="Education", layout="wide")
st.title("Educational attainment by detailed AANHPI subgroup")
st.caption("The starkest illustration of within-'Asian' variation — and a clear equity case for CPS and the College-to-Careers pipeline.")

edu = load_education_by_subgroup()
acs = load_acs_by_community_area()

# --- Framing ----------------------------------------------------------------
st.markdown(
    """
The attainment distribution across AANHPI subgroups is arguably the widest
of any OMB-15 racial category. A single "Asian" bachelor's-attainment rate
compresses a range that runs from **79 % (Asian Indian)** to **6 % (Marshallese)**
— a spread that shapes everything from CPS ESL programming to the City Colleges
pipeline and workforce development strategy.
    """
)

# --- Bachelor's-or-higher ---------------------------------------------------
st.subheader("1. Bachelor's degree or higher (%) — adults age 25+")

fig_b = subgroup_bar(
    edu, group_col="subgroup", value_col="bachelors_or_higher_pct",
    x_label="Bachelor's or higher (%)", value_fmt=".0f",
)
st.plotly_chart(fig_b, use_container_width=True)
st.caption(
    f"Source: [{SOURCES['aapi_data']['label']}]({SOURCES['aapi_data']['url']}); "
    f"[{SOURCES['pew_income_2024']['label']}]({SOURCES['pew_income_2024']['url']}). "
    "National ACS 2019–2023 estimates; local-scale disaggregation is suppressed or "
    "unavailable for most subgroups below in current Chicago releases."
)

# --- Less than HS -----------------------------------------------------------
st.subheader("2. Less than high school diploma (%) — adults age 25+")

fig_h = subgroup_bar(
    edu, group_col="subgroup", value_col="less_than_hs_pct",
    x_label="Less than high school (%)", value_fmt=".0f",
)
st.plotly_chart(fig_h, use_container_width=True)
st.caption(
    "Note the mirror-image of the bachelor's chart: the groups furthest below "
    "the 'Asian' median attainment are the same ones most often missed by CPS "
    "and adult-education outreach that is designed against the aggregate profile."
)

# --- Side-by-side delta chart -----------------------------------------------
st.subheader("3. Educational polarization within the 'Asian' category")

d = edu.sort_values("bachelors_or_higher_pct", ascending=True)
fig_d = go.Figure()
fig_d.add_trace(go.Bar(
    x=d["subgroup"], y=d["bachelors_or_higher_pct"],
    name="Bachelor's+",
    marker_color="#1E7A5F",
    text=[f"{v:.0f}%" for v in d["bachelors_or_higher_pct"]],
    textposition="outside",
))
fig_d.add_trace(go.Bar(
    x=d["subgroup"], y=d["less_than_hs_pct"],
    name="Less than HS",
    marker_color="#B31B1B",
    text=[f"{v:.0f}%" for v in d["less_than_hs_pct"]],
    textposition="outside",
))
fig_d.update_layout(
    barmode="group", yaxis_title="%",
    margin=dict(l=40, r=20, t=10, b=100),
    height=480,
    xaxis={"tickangle": -35},
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_d, use_container_width=True)
st.caption(
    "Reading left-to-right: bachelor's-attainment subgroups ascend, but the less-than-HS "
    "bar does not monotonically descend. Marshallese, Bhutanese, Laotian, Cambodian, and "
    "Hmong communities carry **both** low bachelor's-attainment and elevated less-than-HS "
    "shares — the policy-relevant extreme tail the aggregate 'Asian' category averages away."
)

# --- Companion: school-age population by community area ---------------------
st.subheader("4. School-age residents (0–17) in Community Areas with high AANHPI share")

top = (
    acs.assign(aanhpi_count=acs["asian"] + acs["native_hawaiin_or_pacific"])
    .sort_values("aanhpi_count", ascending=False)
    .head(10)
)
top["school_age"] = top["male_0_to_17"].fillna(0) + top["female_0_to_17"].fillna(0)
top_show = top[["community_area", "school_age", "aanhpi_count"]].rename(
    columns={
        "community_area": "Community Area",
        "school_age": "Residents age 0–17",
        "aanhpi_count": "AANHPI residents",
    }
)
st.dataframe(
    top_show.style.format({"Residents age 0–17": "{:,.0f}", "AANHPI residents": "{:,.0f}"}),
    use_container_width=True, height=380,
)
st.caption(
    "CPS enrollment patterns in these Community Areas already show meaningfully different "
    "English-learner profiles by home language. The ordinance would let CPS (and the Mayor's "
    "Office of Education) cross-tabulate those ELL shares against detailed AANHPI subgroup "
    "rather than the single 'Asian' dropdown, which is currently the only category CPS "
    "reports publicly for AANHPI students."
)

# --- Policy box -------------------------------------------------------------
st.markdown("---")
st.info(
    "**Implication for the Mayor's Office.** Education and workforce-development programs "
    "targeted at the 'Asian' aggregate over-serve already-advantaged subgroups and under-serve "
    "communities with the greatest equity need. Disaggregated data is the prerequisite for "
    "designing — and defending — AANHPI-targeted programs that actually reach those communities."
)
