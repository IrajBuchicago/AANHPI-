"""Shared constants for the AANHPI Data Disaggregation Dashboard."""

# --- Data provenance ----------------------------------------------------------
SOURCES = {
    "acs_ca": {
        "label": "City of Chicago · ACS 5-Year Estimates by Community Area (2019–2023)",
        "url": "https://data.cityofchicago.org/d/t68z-cikk",
    },
    "boundaries": {
        "label": "City of Chicago · Community Area Boundaries",
        "url": "https://data.cityofchicago.org/d/igwz-8jzy",
    },
    "languages_ca": {
        "label": "City of Chicago · Languages Spoken by Community Area (ACS 2008–2012)",
        "url": "https://data.cityofchicago.org/d/a2fk-ec6q",
    },
    "popcounts": {
        "label": "City of Chicago · Chicago Population Counts",
        "url": "https://data.cityofchicago.org/d/85cm-7uqa",
    },
    "dhc_a_2020": {
        "label": "U.S. Census Bureau · 2020 Census DHC-A (Detailed Demographic & Housing Characteristics)",
        "url": "https://www.census.gov/library/stories/2023/09/2020-census-dhc-a-asian-population.html",
    },
    "aapi_data": {
        "label": "AAPI Data · AANHPI Community Data Explorer",
        "url": "https://explore.aapidata.com/",
    },
    "casl": {
        "label": "Chinese American Service League · Change InSight coalition",
        "url": "https://casl.org/",
    },
    "pew_income_2024": {
        "label": "Pew Research · State of the Asian American Middle Class (2024)",
        "url": "https://www.pewresearch.org/race-and-ethnicity/2024/05/31/the-state-of-the-asian-american-middle-class/",
    },
}

# --- AANHPI detailed subgroup ordering & palette -----------------------------
DETAILED_ASIAN = [
    "Chinese",
    "Asian Indian",
    "Filipino",
    "Korean",
    "Pakistani",
    "Vietnamese",
    "Japanese",
    "Other Asian",
]

NHPI = [
    "Native Hawaiian",
    "Samoan",
    "Tongan",
    "Guamanian/Chamorro",
    "Marshallese",
    "Other NHPI",
]

# Categorical palette optimized for choropleth-adjacent bar charts
AANHPI_PALETTE = {
    "Chinese":            "#B31B1B",
    "Asian Indian":       "#C77B30",
    "Filipino":           "#1E7A5F",
    "Korean":             "#345995",
    "Pakistani":          "#7A4B8A",
    "Vietnamese":         "#D4A017",
    "Japanese":           "#6B7A8F",
    "Other Asian":        "#8E8E8E",
    "Native Hawaiian":    "#005B96",
    "Samoan":             "#4F6D7A",
    "Tongan":             "#A14A76",
    "Guamanian/Chamorro": "#7A9E7E",
    "Marshallese":        "#C2B280",
    "Other NHPI":         "#A0A0A0",
}

# --- Key community areas with concentrated AANHPI population -----------------
FOCAL_COMMUNITY_AREAS = [
    "ARMOUR SQUARE",       # Chinatown
    "BRIDGEPORT",          # Expanded Chinatown
    "MCKINLEY PARK",       # South-side Chinese growth
    "WEST RIDGE",          # South Asian / Devon Avenue
    "ALBANY PARK",         # Korean / Filipino / South Asian
    "IRVING PARK",         # Filipino / Korean
    "NORTH PARK",          # Korean
    "UPTOWN",              # Vietnamese / Southeast Asian
    "LINCOLN SQUARE",      # Mixed AANHPI
    "EDGEWATER",           # Mixed AANHPI
]
