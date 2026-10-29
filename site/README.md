# site

The Astro website for this project. See the main README one folder up for the full workflow.

- `src/project.config.ts`: title and summary
- `src/pages/index.astro`: the page text
- `src/components/LineChart.astro`: interactive chart
- `src/components/PointMap.astro`: interactive map
- `scripts/sync-data.mjs`: copies `../data/processed` into `public/data` before each run or build

```
npm install
npm run dev      # live preview at http://localhost:4321
npm run build    # builds into dist/
```
