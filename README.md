# Where US population has grown since 2010

The US added 32.5 million people from 2010 to 2025. About half of that net gain went to five states: Texas, Florida, California, North Carolina and Georgia.

**Live page:** https://wfrowe.github.io/us-population-shift/

Interactive: a year slider, a state map, a ranking for any year, and a trend chart for states you pick.

## The question
Which US states gained or lost population between 2010 and 2025, and by how much?

## The short answer
- The US grew 10.5%, from 309.3 million to 341.8 million.
- Fastest: Idaho +29.2%, Utah +27.5%, Texas +25.6%, Florida +24.5%.
- Only three states shrank: West Virginia, Illinois, Mississippi.

## Data
| Dataset | Source | Date retrieved |
|---|---|---|
| State population estimates, 2010-2019 | US Census Bureau, `nst-est2019-alldata.csv` | 2026-10-29 |
| State population estimates, 2020-2025 | US Census Bureau, `NST-EST2025-ALLDATA.csv` | 2026-10-29 |
| State outlines, 1:20,000,000 | US Census Bureau, `cb_2024_us_state_20m.zip` | 2026-10-29 |

Download URLs are in `src/build_data.py` and on the live page. Raw files go in `data/raw/` (not committed). Terms: I did not find an explicit license statement on the Census download pages. The Census Bureau's open-data page asks for citation, which this project does.

## Method
1. Keep the 50 states and DC. Drop Puerto Rico (not in the Census US total).
2. Use the 2010-2019 release for 2010-2019 and the 2020-2025 release for 2020-2025 (July 1 estimates).
3. Growth = population / 2010 population - 1.
4. Check: the 51 state values add up to the Census US total in all 16 years (the script stops if not).

## Limits
- The two releases do not line up at 2020. The newer one starts from the 2020 Census count, 1.0% above the older 2019 estimate for the US, and from +4.6% (New Jersey) to -2.3% (DC) for states. `data/processed/seam.csv` has every state.
- Estimates, not head counts. They are revised with each release.
- Totals only. No births, deaths or migration.
- Map outlines are simplified. Alaska's Aleutian Islands are shifted to keep the state in one piece.

## Run it yourself
```
uv sync
uv run python src/build_data.py      # raw -> data/processed
cd site
npm install
npm run dev                          # preview at http://localhost:4321
```

Raw downloads go in `data/raw/`:
`nst-est2019-alldata.csv`, `NST-EST2025-ALLDATA.csv`, `cb_2024_us_state_20m.zip`.

## How it is built
Started from [wfrowe/project-template](https://github.com/wfrowe/project-template). Python (`src/build_data.py`) writes `population.csv`, `states.geojson` and `seam.csv`. The Astro page in `site/` reads them in the browser: Observable Plot for charts, MapLibre for the map.
