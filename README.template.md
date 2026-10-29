# Project title

One plain sentence: the question, and the answer.

**Live page:** https://wfrowe.github.io/REPO-NAME/

## The question
What are you trying to find out, and why does it matter?

## The short answer
The answer and the number behind it. Two or three sentences.

## Data
| Dataset | Source | Date retrieved | Terms / license |
|---|---|---|---|
| name | link | YYYY-MM-DD | e.g. public domain, CC BY |

Raw files live in `data/raw/` and are not committed. Processed files are in `data/processed/`.

## Method
1. What you did first.
2. What you did next.
3. How you checked the result a second way.

## Limits
- What the data misses.
- What could be wrong.
- What you would check next.

## Run it yourself
```
uv sync
uv run python src/<your_script>.py     # raw -> data/processed
cd site
npm install
npm run dev                            # preview at http://localhost:4321
```
