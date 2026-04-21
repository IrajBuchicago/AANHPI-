"""Data loading helpers for the AANHPI Data Disaggregation Dashboard."""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data(show_spinner=False)
def load_community_areas_geojson() -> dict:
    """77 Chicago Community Area polygons (GeoJSON)."""
    path = DATA_DIR / "community_areas.geojson"
    with open(path) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_acs_by_community_area() -> pd.DataFrame:
    """ACS 5-year (2019–2023) aggregates by Community Area — Chicago open data."""
    df = pd.read_csv(DATA_DIR / "acs_community_areas.csv")
    df["community_area"] = df["community_area"].str.strip().str.upper()
    # Asian share as % of total population
    df["asian_share_pct"] = 100.0 * df["asian"] / df["total_population"]
    df["nhpi_share_pct"] = 100.0 * df["native_hawaiin_or_pacific"] / df["total_population"]
    # Helpful rollups
    df["under_50k_share_pct"] = 100.0 * (df["under_25_000"] + df["_25_000_to_49_999"]) / (
        df["under_25_000"] + df["_25_000_to_49_999"] + df["_50_000_to_74_999"] + df["_75_000_to_125_000"] + df["_125_000"]
    )
    return df


@st.cache_data(show_spinner=False)
def load_languages_by_community_area() -> pd.DataFrame:
    """Number of residents aged 5+ speaking each non-English language at home,
    by Chicago Community Area (ACS 2008–2012). Community-level language
    disaggregation is not released in later ACS cycles for tract/CA geographies,
    which is itself a data-gap argument for the ordinance."""
    df = pd.read_csv(DATA_DIR / "languages_chicago.csv")
    df["community_area_name"] = df["community_area_name"].str.strip().str.upper()
    return df


@st.cache_data(show_spinner=False)
def load_detailed_aanhpi_chicago() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "detailed_aanhpi_chicago.csv")


@st.cache_data(show_spinner=False)
def load_detailed_aanhpi_cook() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "detailed_aanhpi_cook.csv")


@st.cache_data(show_spinner=False)
def load_income_by_subgroup() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "income_by_subgroup.csv")


@st.cache_data(show_spinner=False)
def load_poverty_by_subgroup() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "poverty_by_subgroup.csv")


@st.cache_data(show_spinner=False)
def load_education_by_subgroup() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "education_by_subgroup.csv")


@st.cache_data(show_spinner=False)
def load_health_by_subgroup() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "health_by_subgroup.csv")


@st.cache_data(show_spinner=False)
def load_lep_by_subgroup() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "lep_by_subgroup.csv")
