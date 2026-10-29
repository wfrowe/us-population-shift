# Project template

Starter for a small data project: Python prepares the data, an Astro page shows it, and GitHub publishes it at `https://wfrowe.github.io/<repo-name>/`.

The page you get out of the box has a made-up example: an interactive line chart and a zoomable map. Replace the example with your own question.

Live example: https://wfrowe.github.io/project-template/

## How the pieces connect

```
data/raw/  --(src/*.py)-->  data/processed/  --(site/scripts/sync-data.mjs)-->  site/public/data/
 local only                  committed                                              copy, git-ignored
                                                                                         |
                                       push to main --> GitHub Actions builds site/ --> live page
```

- Python reads raw data and writes small, clean files to `data/processed/`.
- Astro copies those files into the site, and charts and maps load them in the visitor's browser.
- Every push to `main` rebuilds and publishes the page.

## Start a new project

1. On GitHub, click **Use this template** (or run `gh repo create wfrowe/<name> --template wfrowe/project-template --public --clone`).
2. In the new repo, turn on Pages with the GitHub Actions source:
   `gh api -X POST repos/wfrowe/<name>/pages -f build_type=workflow`
3. Set the title and summary in `site/src/project.config.ts`.
4. Replace `README.md` with `README.template.md`, filled in.
5. Replace `src/make_sample_data.py` with your own script. Put downloads in `data/raw/`, write clean files to `data/processed/`.
6. Edit `site/src/pages/index.astro` and the two components to match your data.
7. Commit and push. The page is live about a minute later.

## Run it on your computer

```
uv sync                                   # install Python packages
uv run python src/make_sample_data.py     # make the example data
cd site
npm install                               # first time only
npm run dev                               # preview at http://localhost:4321
```

For notebooks: `uv run jupyter lab`, and once per clone run `uv run nbstripout --install` so saved outputs are not committed.

## Rules baked in

- `data/raw/` is git-ignored. Only `data/processed/` is committed.
- `.gitignore` also blocks `.env` files, keys, and files with "secret" or "credentials" in the name.
- Before you push: check `data/processed/` and any notebook for keys or personal data. The repo and site are public.
- Free only. The map uses OpenFreeMap, which needs no key.
