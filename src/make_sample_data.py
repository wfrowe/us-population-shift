"""Make the example data for this template.

Shows the data flow every project follows:

    data/raw/        <- what you download or export. Stays on your computer.
    src/*.py         <- this script: clean it up, check it, reshape it.
    data/processed/  <- the small, clean files the website reads. Committed.

The numbers here are MADE UP so the template has something to draw.
Replace this script with your own once you have a real question.

Run from the project root:  uv run python src/make_sample_data.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

# Real city coordinates, made-up values.
CITIES = {
    "Seattle": (47.61, -122.33),
    "Denver": (39.74, -104.99),
    "Chicago": (41.88, -87.63),
    "Atlanta": (33.75, -84.39),
    "Boston": (42.36, -71.06),
    "Austin": (30.27, -97.74),
}


def make_raw() -> pd.DataFrame:
    """Pretend this is a messy download: one row per city per month."""
    rng = np.random.default_rng(seed=42)
    months = pd.date_range("2019-01-01", "2024-12-01", freq="MS")
    rows = []
    for i, (city, (lat, lon)) in enumerate(CITIES.items()):
        trend = np.linspace(100, 100 + 8 * (i + 1), len(months))
        noise = rng.normal(0, 2.5, len(months))
        for month, value in zip(months, trend + noise):
            rows.append({"city": city, "lat": lat, "lon": lon, "month": month, "value": value})
    return pd.DataFrame(rows)


def clean(raw: pd.DataFrame) -> pd.DataFrame:
    """Round, sort, and check. Fail loudly if something looks wrong."""
    df = raw.copy()
    df["value"] = df["value"].round(1)
    df = df.sort_values(["city", "month"]).reset_index(drop=True)
    assert df["value"].notna().all(), "missing values"
    assert not df.duplicated(["city", "month"]).any(), "duplicate city-month rows"
    return df


def to_geojson(df: pd.DataFrame) -> dict:
    """One point per city, with its latest value and change since the first month."""
    features = []
    for city, g in df.groupby("city"):
        first, last = g.iloc[0], g.iloc[-1]
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [float(last["lon"]), float(last["lat"])]},
                "properties": {
                    "city": city,
                    "latest": float(last["value"]),
                    "change": round(float(last["value"] - first["value"]), 1),
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    raw = make_raw()
    raw.to_csv(RAW / "example_raw.csv", index=False)  # git-ignored

    df = clean(raw)
    df[["city", "month", "value"]].to_csv(PROCESSED / "series.csv", index=False)
    (PROCESSED / "points.geojson").write_text(json.dumps(to_geojson(df), indent=2), encoding="utf-8")

    print(f"raw:       {RAW / 'example_raw.csv'} ({len(raw)} rows, not committed)")
    print(f"processed: {PROCESSED / 'series.csv'} ({len(df)} rows)")
    print(f"processed: {PROCESSED / 'points.geojson'} ({len(CITIES)} points)")


if __name__ == "__main__":
    main()
