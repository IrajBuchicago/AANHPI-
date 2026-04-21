"""
Refresh the City of Chicago open-data inputs used by the dashboard.

Run once to populate /data, and whenever the City publishes a new ACS
release. Does not touch the hand-curated detailed-subgroup CSVs.

    python fetch_data.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)


SOCRATA = "https://data.cityofchicago.org/resource"

DATASETS = {
    "acs_community_areas.csv": f"{SOCRATA}/t68z-cikk.json?$limit=5000",
    "languages_chicago.csv":   f"{SOCRATA}/a2fk-ec6q.json?$limit=5000",
    "chicago_pop_counts.csv":  f"{SOCRATA}/85cm-7uqa.json?$limit=50000",
}

BOUNDARIES = f"{SOCRATA}/igwz-8jzy.json?$select=the_geom,community,area_numbe&$limit=200"


def _download_json(url: str) -> list[dict]:
    r = requests.get(url, timeout=120, headers={"User-Agent": "aanhpi-dashboard/1.0"})
    r.raise_for_status()
    return r.json()


def _download_csv(path: Path, url: str) -> None:
    rows = _download_json(url)
    if not rows:
        print(f"  empty response → {path.name}")
        return
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"  wrote {path.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def _download_boundaries(path: Path) -> None:
    rows = _download_json(BOUNDARIES)
    features = []
    for row in rows:
        features.append({
            "type": "Feature",
            "geometry": row["the_geom"],
            "properties": {
                "community": row["community"],
                "area_number": int(row["area_numbe"]),
            },
        })
    gj = {"type": "FeatureCollection", "features": features}
    with open(path, "w") as f:
        json.dump(gj, f)
    print(f"  wrote {path.name}  ({len(features)} features)")


def main() -> None:
    print("Refreshing Chicago open-data inputs …")
    for fname, url in DATASETS.items():
        try:
            _download_csv(DATA / fname, url)
        except Exception as e:
            print(f"  FAILED {fname}: {e}")
    try:
        _download_boundaries(DATA / "community_areas.geojson")
    except Exception as e:
        print(f"  FAILED boundaries: {e}")
    print("Done.")


if __name__ == "__main__":
    main()
