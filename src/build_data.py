"""Build the data files for the US population page.

    data/raw/        <- Census downloads (not committed)
    this script      <- joins the two estimate releases, checks totals, adds shapes
    data/processed/  <- population.csv, states.geojson, seam.csv (committed)

Run from the project root:  uv run python src/build_data.py

Sources (US Census Bureau, public domain):
  - Population estimates, 2010-2019 release: nst-est2019-alldata.csv
  - Population estimates, 2020-2025 release: NST-EST2025-ALLDATA.csv
  - State outlines, 1:20,000,000 cartographic boundary file: cb_2024_us_state_20m.zip
"""

import json
import zipfile
from pathlib import Path

import pandas as pd
import shapefile  # pyshp

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

FIRST_YEAR, LAST_YEAR = 2010, 2025
EXCLUDE = {"Puerto Rico"}  # in the files, but not part of the "United States" total


def states_only(df: pd.DataFrame) -> pd.DataFrame:
    """Keep the 50 states and DC. SUMLEV 040 = state-level rows."""
    df = df[df["SUMLEV"].astype(str).str.zfill(3) == "040"]
    df = df[~df["NAME"].isin(EXCLUDE)].copy()
    df["fips"] = df["STATE"].astype(int).astype(str).str.zfill(2)
    return df


def long_form(df: pd.DataFrame, years: range) -> pd.DataFrame:
    cols = [f"POPESTIMATE{y}" for y in years]
    out = df.melt(id_vars=["fips", "NAME"], value_vars=cols, var_name="col", value_name="population")
    out["year"] = out["col"].str[-4:].astype(int)
    return out.rename(columns={"NAME": "state"})[["fips", "state", "year", "population"]]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    old_raw = pd.read_csv(RAW / "nst-est2019-alldata.csv")
    new_raw = pd.read_csv(RAW / "NST-EST2025-ALLDATA.csv")
    old, new = states_only(old_raw), states_only(new_raw)

    # --- Population by state and year (July 1 estimates) ---
    # 2010-2019 come from the older release, 2020-2025 from the newer one.
    pop = pd.concat([long_form(old, range(2010, 2020)), long_form(new, range(2020, 2026))], ignore_index=True)
    pop = pop.sort_values(["fips", "year"]).reset_index(drop=True)

    # --- Checks: fail loudly if anything is off ---
    assert pop["fips"].nunique() == 51, "expected 50 states + DC"
    assert len(pop) == 51 * (LAST_YEAR - FIRST_YEAR + 1), "missing state-years"
    assert pop["population"].notna().all() and (pop["population"] > 0).all()
    # State totals must equal the national row for every year.
    us_old = old_raw[old_raw["NAME"] == "United States"].iloc[0]
    us_new = new_raw[new_raw["NAME"] == "United States"].iloc[0]
    for year, us_row in [*[(y, us_old) for y in range(2010, 2020)], *[(y, us_new) for y in range(2020, 2026)]]:
        total = int(pop.loc[pop["year"] == year, "population"].sum())
        assert total == int(us_row[f"POPESTIMATE{year}"]), f"{year}: states sum {total} != US row"

    # --- Derived columns ---
    base = pop[pop["year"] == FIRST_YEAR].set_index("fips")["population"]
    pop["growth_pct"] = ((pop["population"] / pop["fips"].map(base) - 1) * 100).round(2)
    pop["rank"] = pop.groupby("year")["population"].rank(ascending=False, method="min").astype(int)
    pop.to_csv(OUT / "population.csv", index=False)

    # --- The seam: how much the two releases disagree at the 2019/2020 boundary ---
    s19 = old.set_index("fips")["POPESTIMATE2019"]
    s20 = new.set_index("fips")["ESTIMATESBASE2020"]  # 2020 Census-based starting point
    seam = pd.DataFrame(
        {
            "state": new.set_index("fips")["NAME"],
            "estimate_2019_old_release": s19,
            "base_2020_new_release": s20,
        }
    )
    seam["difference"] = seam["base_2020_new_release"] - seam["estimate_2019_old_release"]
    seam["difference_pct"] = (seam["difference"] / seam["estimate_2019_old_release"] * 100).round(2)
    seam.reset_index().to_csv(OUT / "seam.csv", index=False)

    # --- State outlines -> GeoJSON ---
    with zipfile.ZipFile(RAW / "cb_2024_us_state_20m.zip") as z:
        z.extractall(RAW / "cb_2024_us_state_20m")
    reader = shapefile.Reader(str(RAW / "cb_2024_us_state_20m" / "cb_2024_us_state_20m.shp"))
    names = {f: n for f, n in pop[["fips", "state"]].drop_duplicates().itertuples(index=False)}
    features = []
    for sr in reader.shapeRecords():
        fips = sr.record["GEOID"]
        if fips not in names:
            continue  # Puerto Rico and other territories
        geom = sr.shape.__geo_interface__
        # Alaska's Aleutian Islands cross the 180th meridian. Shift those points so the shape stays in one piece.
        def fix(coords):
            if isinstance(coords[0], (int, float)):
                return [coords[0] - 360 if coords[0] > 0 and fips == "02" else coords[0], coords[1]]
            return [fix(c) for c in coords]
        geom = {"type": geom["type"], "coordinates": fix(geom["coordinates"])}
        features.append({"type": "Feature", "id": int(fips), "properties": {"fips": fips, "state": names[fips]}, "geometry": geom})
    assert len(features) == 51, f"expected 51 shapes, got {len(features)}"
    (OUT / "states.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": features}, separators=(",", ":")), encoding="utf-8")

    # --- Summary for the console ---
    last = pop[pop["year"] == LAST_YEAR].sort_values("growth_pct")
    print(f"rows: {len(pop)}  states: {pop['fips'].nunique()}  years: {FIRST_YEAR}-{LAST_YEAR}")
    print(f"US total {FIRST_YEAR}: {int(pop[pop.year == FIRST_YEAR].population.sum()):,}   {LAST_YEAR}: {int(pop[pop.year == LAST_YEAR].population.sum()):,}")
    print("Slowest growth since 2010:", ", ".join(f"{r.state} {r.growth_pct:+.1f}%" for r in last.head(3).itertuples()))
    print("Fastest growth since 2010:", ", ".join(f"{r.state} {r.growth_pct:+.1f}%" for r in last.tail(3).iloc[::-1].itertuples()))
    for f in ("population.csv", "seam.csv", "states.geojson"):
        print(f"{f}: {(OUT / f).stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
