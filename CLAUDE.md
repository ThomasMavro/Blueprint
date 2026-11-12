# Blueprint — Chelsea FC Women commercial intelligence

## What this is
An independent portfolio tool that turns public data into insights for commercial decisions at
Chelsea FC Women: partnerships, partner value, matchday (Stamford Bridge), fanbase,
player commercial value. Full spec: docs/spec.md. Read it before planning any phase.

## Who uses it
Commercial staff who are not data experts. Every screen opens with plain-English
findings (number + context: peer comparison, trend, confidence); charts sit
underneath as proof. It informs decisions; it never makes them.

## Owner
Thomas, MSc Sport Analytics & AI student, comfortable with Python but still learning.
Explain non-obvious code choices briefly in comments and in your replies.

## Stack
Python 3.12 · httpx, BeautifulSoup, Playwright · Parquet raw store · DuckDB warehouse
· pandas/polars, statsmodels, scikit-learn · Dash + Dash Mantine Components + Plotly
· Jinja2 + WeasyPrint · pytest, ruff · GitHub Actions for schedules.

## Repo layout
src/blueprint/ingest/<source>.py   one module per source, writes raw Parquet
src/blueprint/models/               SQL + Python that build warehouse tables
src/blueprint/analytics/            models, rankings, logo detection
src/blueprint/insights/             detectors and finding templates
src/blueprint/app/                  Dash pages, one per module
data/raw/<source>/<date>/           never edited by hand
docs/sources.md                     source register: URL, terms checked, date

## Rules
- Plan each phase in a short plan file before writing code; wait for approval.
- Order: data + tests first, analysis second, screens last.
- Never invent data. Every figure must trace to a raw snapshot and its source URL.
- Never fail silently: report any failed, blocked or partial collection to Thomas at
  once, with what broke and the options. Never skip, guess or back-fill without approval.
- When a source is missing or thin, say so and ask whether Thomas can help fill it.
- Scrape politely: respect robots.txt and rate limits; public data only; no personal
  data about fans.
- Estimates (media value, forecasts) always show a range and a method note.
- Benchmark every metric against the selected peer set (WSL, European elite, custom).
- No club crests or implied endorsement; label the app an independent project.
- Insights, not recommendations: no "you should" wording in findings or reports.
- Zero budget: free tiers and free APIs only. Flag any cost to Thomas before adding it.
- Run ruff and pytest before every commit.

## Skills to use when available
- frontend-design and dataviz: for any screen, chart, colour or layout work.
- tool-showcase: when a phase ships, for the GitHub, Substack and CV updates.
- lboro-ai-assignment-support: if any part becomes assessed MSc work.

## Current phase
Phase 0: Foundations (see docs/spec.md, Build roadmap).
