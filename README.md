# AANHPI Data Disaggregation Dashboard — Chicago

A Streamlit briefing tool supporting IMRR's evaluation of the CASL-proposed
Asian American, Native Hawaiian, and Pacific Islander (AANHPI) data
disaggregation ordinance. Designed as a Grade-A deliverable for the Office of
the Mayor and department heads.

## What's in it

- **`app.py`** — overview page: policy framing, top-line metrics, ordinance ask.
- **`pages/1_Population_and_Language.py`** — Community-Area heatmap of AANHPI
  residents, Chicago-city detailed subgroup population, language-at-home
  choropleth by Community Area.
- **`pages/2_Health.py`** — uninsured rate, LEP, and age-65+ share by
  detailed subgroup.
- **`pages/3_Economic_and_Income.py`** — the aggregate-vs-disaggregated
  median-income hero visual, poverty by subgroup, low-income-household
  heatmap.
- **`pages/4_Education.py`** — bachelor's and less-than-HS attainment by
  detailed subgroup; school-age population in AANHPI-concentrated Community
  Areas.

## Running

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will open at <http://localhost:8501>.

## Data

| File | Source | Vintage |
| --- | --- | --- |
| `data/community_areas.geojson` | Chicago Open Data (`igwz-8jzy`) | Current |
| `data/acs_community_areas.csv` | Chicago Open Data · ACS by Community Area (`t68z-cikk`) | ACS 2019–2023 |
| `data/languages_chicago.csv` | Chicago Open Data (`a2fk-ec6q`) | ACS 2008–2012 |
| `data/chicago_pop_counts.csv` | Chicago Open Data (`85cm-7uqa`) | 2000–2020+ |
| `data/detailed_aanhpi_chicago.csv` | 2020 Decennial Census (compiled) | 2020 |
| `data/detailed_aanhpi_cook.csv` | 2020 Census DHC-A | 2020 |
| `data/income_by_subgroup.csv` | Pew Research · State of the Asian American Middle Class | 2024 |
| `data/poverty_by_subgroup.csv` | AAPI Data · AANHPI Community Data Explorer | 2022–2023 |
| `data/education_by_subgroup.csv` | AAPI Data / Pew Research | 2023 |
| `data/health_by_subgroup.csv` | AAPI Data · ACS 2019–2023 | 2023 |
| `data/lep_by_subgroup.csv` | Asian Americans Advancing Justice · Chicago; AAPI Data | 2020–2023 |

Chicago-specific detailed subgroup data (beyond aggregated "Asian" at
Community-Area level) is not currently produced by the City's data pipelines.
That gap is the core rationale for the ordinance — and is annotated on every
relevant page of the dashboard.

## Refreshing the data

`fetch_data.py` pulls the latest community-area ACS and boundary data from
`data.cityofchicago.org`. It is *idempotent*; rerun it whenever the City's
open-data portal publishes a new ACS vintage:

```bash
python fetch_data.py
```

Detailed-subgroup CSVs are maintained by hand and should be refreshed on
each ACS 5-year release (approximately every December) and after every
Decennial Census DHC-A update.

## Design notes for the brief

1. Every page closes with a **blue info box** tying the visual evidence to a
   concrete implication for a Mayor's Office or department-level decision.
2. Every chart that uses national disaggregated data makes the local-data gap
   explicit in its caption — the absence of Chicago-level disaggregation is
   itself a talking point for the ordinance.
3. Neutral palette with Chicago-flag red (#B31B1B) as the accent;
   serif typography to match mayoral briefing documents rather than the
   default Streamlit sans-serif.

## Outstanding items before presentation

- Replace Pew / AAPI Data national proxies on Health, Economic, and Education
  pages with Cook County S0201 Selected Population Profile pulls once the
  Census API is reachable from the presentation environment.
- Wire in CPS student enrollment by home-language cross-tabulation once the
  CPS data-sharing MOU is finalized.
- Add a Community Area lookup panel for the Mayor to jump directly to the
  neighborhoods of greatest AANHPI concentration on each page.
