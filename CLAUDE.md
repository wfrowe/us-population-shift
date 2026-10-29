# Project instructions

Small data project: Python prepares the data, an Astro page in `site/` shows it, GitHub Actions publishes it at `https://wfrowe.github.io/<repo-name>/`.
Global rules in `~/.claude/CLAUDE.md` still apply (plain language, ask before destructive or public actions, explain the structure).

## Layout
- `data/raw/`: downloads and exports. Git-ignored. Never commit.
- `data/processed/`: clean files the site reads. Committed. Must be safe to publish.
- `src/`: Python scripts that turn raw into processed.
- `notebooks/`: exploration. Strip outputs before committing.
- `site/`: Astro site. Page text in `src/pages/index.astro`, title in `src/project.config.ts`.
- `README.md`: the project write-up (start from `README.template.md`).

## Commands
- `uv sync`: install Python packages (Python 3.14, native ARM64)
- `uv run python src/<script>.py`: run a script
- `uv run jupyter lab`: open notebooks
- `cd site; npm install`: install site packages (first time)
- `cd site; npm run dev`: live preview at http://localhost:4321
- `cd site; npm run build`: production build (copies data/processed into the site first)

## Rules for this project
- Public repo and public site. Before every push, scan changed files and `data/processed/` for keys, personal data, and anything not meant to be public.
- Everything free. No paid APIs or map services. Basemap is OpenFreeMap (no key).
- Every dataset gets its source, date retrieved, and terms of use written in the README.
- Lead the page with the question and the short answer. State the limits.
- Check key numbers a second way before they go on the page.
- No job-search language anywhere in the project.
- Use uv for Python. Do not use pip directly. Do not add packages that lack ARM64 builds without asking.
- Chart and map code: `site/src/components/LineChart.astro` and `PointMap.astro`. Copy and adapt them. They read `series.csv` and `points.geojson`.
- Do not hard-code the base path. `BASE_PATH` comes from the workflow.
