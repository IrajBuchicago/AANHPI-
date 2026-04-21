"""
AANHPI Data Disaggregation Dashboard — Chicago
==============================================

Entry page for a Streamlit multi-page app briefing mayoral leadership on the
case for a municipal AANHPI data-disaggregation ordinance proposed in
partnership with the Chinese American Service League (CASL) and the Change
InSight coalition.

Run:
    streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

from utils.constants import SOURCES
from utils.data_loader import (
    load_acs_by_community_area,
    load_detailed_aanhpi_chicago,
    load_detailed_aanhpi_cook,
)

st.set_page_config(
    page_title="AANHPI Data Disaggregation — Chicago",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Header ----------------------------------------------------------
st.title("AANHPI Data Disaggregation Dashboard")
st.caption(
    "Briefing for the Mayor's Office Policy Team  — March 2026"
)

st.markdown("---")

# ---------- Top-line framing ------------------------------------------------
c1, c2 = st.columns([0.6, 0.4])

with c1:
    st.subheader("The policy question")
    st.markdown(
        """
City departments currently report demographic outcomes using the single
**"Asian"** racial category established by OMB Directive 15. Consolidating
30+ distinct AANHPI origin groups into one field produces a statistical
average that does not describe any single community accurately — and it
systematically hides disparities in health, education, income, and access
to services.

CASL's proposed ordinance would require Chicago departments to:

1.  **Collect** disaggregated race, ethnicity, and language-spoken data on all
    client-facing intake forms, using at minimum the categories released in
    the 2020 Census DHC-A.
2.  **Publish** an annual equity report cross-tabulating service utilization
    and outcome measures by detailed AANHPI subgroup and Community Area.
3.  **Train** department staff on disaggregated intake practices and
    culturally competent data handling.

This dashboard presents the data the City **can** currently produce, and
makes visible the specific gaps the ordinance would close.
"""
    )

with c2:
    st.subheader("At-a-glance")
    try:
        acs = load_acs_by_community_area()
        chi = load_detailed_aanhpi_chicago()
        cook = load_detailed_aanhpi_cook()

        total_asian = int(acs["asian"].sum())
        total_nhpi = int(acs["native_hawaiin_or_pacific"].sum())
        total_pop = int(acs["total_population"].sum())
        asian_pct = 100 * total_asian / total_pop if total_pop else 0
        cas_with_asian_over_5pct = int((acs["asian_share_pct"] >= 5).sum())

        st.metric("AANHPI residents (Chicago, ACS 2019–2023)",
                  f"{total_asian + total_nhpi:,}",
                  f"{asian_pct:.1f}% of the city")
        st.metric("Detailed origin groups identified in 2020 Census DHC-A",
                  "30+",
                  "ordinance would require this granularity in City data")
        st.metric("Community Areas with AANHPI share ≥ 5%",
                  f"{cas_with_asian_over_5pct} of 77")
        st.metric("Largest AANHPI origin in Cook County",
                  "Asian Indian (~134K)",
                  "alone or in any combination, 2020 Census DHC-A")
    except Exception as e:
        st.warning(f"Metrics unavailable: {e}")

st.markdown("---")

# ---------- Why this matters ------------------------------------------------
st.subheader("Why the aggregate obscures policy-relevant disparities")

st.markdown(
    """
Consider three illustrations of how the single "Asian" label misleads the
policymaker relying on it:

* **Income.** National ACS estimates show Asian Indian median household income
  near $119K — while Burmese, Hmong, and Bhutanese households are concentrated
  in the $40–55K range. The "Asian median" of ~$82K describes neither
  community.
* **Limited English Proficiency.** Around 40% of Korean Cook County residents
  are LEP, versus roughly 11% of Filipino residents. Language access budgeting
  that treats "Asian" as one category underserves the high-LEP groups.
* **Poverty.** In Chinatown, CASL's Change InSight survey routinely finds
  Chinese-origin households facing poverty rates an order of magnitude above
  the ACS "Asian" county average — but those households are invisible in the
  aggregate number that drives City resource allocation.

The remaining pages of this dashboard show the geographic and subgroup
variation that the current aggregate hides, using Chicago open data and
published ACS / Census DHC-A estimates.
"""
)

# ---------- Navigation hint -------------------------------------------------
st.info(
    "Use the left sidebar to navigate:  "
    "**Population & Language** (community-area heatmaps) · "
    "**Health** (coverage & LEP) · "
    "**Economic & Income** (the income range hidden by the aggregate) · "
    "**Education** (attainment by detailed group).",
    icon=None,
)

# ---------- Sources footer --------------------------------------------------
with st.expander("Data provenance & methodology"):
    for _, s in SOURCES.items():
        st.markdown(f"- [{s['label']}]({s['url']})")
    st.markdown(
        """
**Geographic framing.** Chicago open data publishes ACS estimates at the
Community Area (n=77) level. Census-tract detail for small AANHPI subgroups
is frequently suppressed by the Census Bureau due to small-cell disclosure
rules — which is precisely why the ordinance also contemplates City-collected
administrative data as a supplement.

**Detailed-subgroup figures by detailed Asian / NHPI origin come
from the 2020 Census DHC-A release for Cook County and the City of Chicago;
outcome measures (income, education, health) by detailed origin come from
the 2019–2023 ACS 5-year Selected Population Profile tables as compiled by
AAPI Data and Pew Research. Values are national where Chicago-specific
disaggregation is suppressed — that suppression is itself part of the case
for the ordinance.
"""
    )
