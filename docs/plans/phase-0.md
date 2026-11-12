# Phase 0 plan: Foundations

Status: **draft, waiting for Thomas's approval.** No code until approved.

## Goal

Phase 0 sets up the base that every later phase builds on: a working Python project, an empty
but tested warehouse, a checked list of data sources, and automatic quality checks.
Nothing shows on screen yet. When Phase 0 is done, Phase 1 (Matchday) can start collecting
real data straight away.

Note: the spec's roadmap diagram is an embedded image that didn't come through in
`docs/spec.md`, so I can't see the exact Phase 0 scope or hours. This plan is based on the
spec text. If the roadmap lists other Phase 0 items, tell me and I'll add them.

## 1. Repo structure

```
blueprint/
├── pyproject.toml           project name, Python version, dependencies, ruff + pytest settings
├── README.md                what it is, "independent project" label, how to run it
├── CLAUDE.md                instructions for Claude (exists)
├── .gitignore               keeps data, caches and secrets out of Git
├── .github/workflows/ci.yml runs ruff + pytest on every push
├── docs/
│   ├── spec.md              (exists)
│   ├── sources.md           source register: URL, terms checked, date, verdict
│   └── plans/phase-0.md     this file
├── src/blueprint/
│   ├── config.py            paths (data folder, warehouse file) in one place
│   ├── ingest/              one file per source (empty in Phase 0, apart from shared helpers)
│   │   └── _common.py       polite HTTP client, raw-snapshot writer, collection log
│   ├── models/schema.sql    CREATE TABLE statements for the warehouse
│   ├── analytics/  insights/  app/   empty folders with __init__.py, filled later
├── data/                    not in Git (see below)
│   ├── raw/<source>/<date>/ raw snapshots, never edited
│   └── warehouse.duckdb
└── tests/
    ├── fixtures/            small saved sample pages, so tests never hit the internet
    └── test_*.py
```

**Why this shape:**
- **`src/` layout.** The code lives in `src/blueprint/`, not loose at the top level. This
  makes Python import the *installed* package, the same way the app and GitHub Actions will,
  so "it works on my machine" problems show up early.
- **`pyproject.toml`.** This is the modern single file for a Python project. It replaces
  `requirements.txt` + `setup.py` + separate config files. We install with
  `pip install -e ".[dev]"`. The `-e` (editable) means your code changes apply without
  reinstalling.
- **A plain `venv` and `pip`.** Python's built-in tools, so you don't have to learn a new
  tool on top of everything else. We can switch to `uv` later if installs feel slow.
- **Data is not in Git.** Git is built for text you edit, not for growing data files.
  Raw snapshots go to a free Hugging Face dataset or a GitHub release later (spec, Hosting).
  For now they stay local. `.gitignore` enforces this.
- **Install only what Phase 0 needs:** httpx, BeautifulSoup, DuckDB, pandas, pyarrow
  (for Parquet), pytest and ruff. Dash, Playwright, statsmodels and the rest get added in
  the phase that first uses them. Fewer packages means fewer things to break.

## 2. The first tables

Phase 1 is Matchday, so Phase 0 creates the tables it needs, plus two tables that support
the "never fail silently" and "trace every figure" rules. Every table is created empty from
`schema.sql`.

| Table | One row per | Key fields | Why now |
| --- | --- | --- | --- |
| `club` | Club | club_id, name, league, country, peer_groups | Every metric is benchmarked against peers, so clubs come first |
| `venue` | Stadium | venue_id, name, city, capacity, capacity_source_url | Chelsea plays at the Bridge, Plough Lane and (in the past) Kingsmeadow. Occupancy needs each venue's capacity. A separate table avoids repeating capacity on every match |
| `fixture` | Match | fixture_id, date, kickoff, competition, season, home_club_id, away_club_id, venue_id, attendance, tv_broadcaster | Core of Matchday |
| `source` | Data source | source_id, url, terms_checked_on, robots_ok, verdict | Machine-readable copy of `docs/sources.md`, so every row can point back to its source |
| `collection_log` | Scraper run | run_id, source_id, started_at, rows_expected, rows_collected, status, errors | Records every run, including failures and shortfalls. This later feeds the data health page |

Every data table also gets `source_id`, `source_url` and `snapshot_date` columns. That's how
any figure traces back to a raw page and the date it was collected (CLAUDE.md rule).

**One small change from the spec:** the spec has `stadiums` as a field inside `club`. I've
moved it into its own `venue` table, because one club uses several grounds and capacity
belongs to the ground, not the club. Tell me if you'd rather keep the spec's version.

Left for later phases: `ticket_price` (Phase 1), `partner_deal` and `brand` (Partnerships),
and the social, logo, player, trend and finding tables.

## 3. Sources to check

For each source I'll record five things in `docs/sources.md`: whether it's available,
whether `robots.txt` allows it, what the terms of use say about automated access, how many
seasons of history it has, and the polite rate we'd use. Each source gets one of three
verdicts: **use**, **use with limits**, or **don't use**. In Phase 0 I only read
`robots.txt` and terms pages and fetch a sample page or two. No bulk collection.

**Priority A: Matchday (needed for Phase 1)**
- WSL official site (fixtures, results, attendances)
- FBref (women's match logs, attendances): known to have strict bot rate limits
- Wikipedia WSL season pages (attendances, long history; open licence)
- Transfermarkt (attendances): terms may forbid scraping, to be checked
- Chelsea FC fixtures and ticketing pages (prices, venues)
- Open-Meteo historical weather API (free, no key)
- Men's Premier League fixture list (clash dates)
- BBC / Sky TV pick listings

**Priority B: later modules (quick check now, so we know the risks early)**
- Club partner pages (WSL + European elite)
- Trade press RSS: SportBusiness, SportsPro, FC Business
- YouTube Data API (free quota)
- Instagram, TikTok, X public profiles (the spec's biggest risk)
- Google Trends via pytrends
- Companies House API (free; annual accounts)

**Priority C: hosting free tiers.** The spec asks for these checks in Phase 0: Hugging Face
Spaces and the Render free plan (memory, sleep rules, storage), and Hugging Face datasets /
GitHub releases for the data files.

**Network access needed.** The `blueprint` environment can currently only reach package
registries. Before the source checks I'll ask you to approve the exact hosts above, one
priority group at a time.

## 4. Tests

| Test | What it catches |
| --- | --- |
| `test_schema.py` | Builds the warehouse in a temporary file, then checks every table and column exists with the right type |
| `test_data_rules.py` | Data tests run against sample rows: unique IDs, no missing keys, attendance ≥ 0 and ≤ venue capacity, every row has a `source_url` and `snapshot_date` |
| `test_common.py` | The polite HTTP client waits between requests and obeys `robots.txt`. The snapshot writer never overwrites an existing raw file. A failed fetch writes a `collection_log` row with status `failed` instead of disappearing |
| `test_sources.py` | Every source in `docs/sources.md` is in the `source` table, and every ingest module names a registered source |

**Why tests look like this:**
- **No live internet in tests.** Tests use small saved pages in `tests/fixtures/`. That keeps
  them fast and repeatable, and they don't hammer real sites. A website changing breaks the
  scraper's *collection log*, not the test suite.
- **Data tests are separate from code tests.** Later, the same rules run on real data after
  every scheduled refresh, so bad data is stopped before it reaches the app.
- **CI.** GitHub Actions runs `ruff` (style and common bugs) and `pytest` on every push, for
  free. A red cross on GitHub means something broke.

## 5. Git workflow

- Work on a branch called `phase-0`, not `main`. `main` only gets work that is finished and
  approved, merged through a pull request you review.
- Small commits, one idea each (for example "add schema and schema test"). `ruff` and
  `pytest` run before each commit, as CLAUDE.md requires.
- **Blocker:** this session can read the repo but GitHub currently refuses pushes from it.
  Before I can push, you need to reconnect GitHub in claude.ai settings (Connectors) and give
  the Claude GitHub App access to `Blueprint`.

## 6. Done when

- `pip install -e ".[dev]"`, `ruff check .` and `pytest` all pass locally and in CI
- `warehouse.duckdb` builds from `schema.sql` with the five tables
- `docs/sources.md` has a verdict for every Priority A, B and C item, and any red flags are
  reported to you with options
- The README carries the "independent project, not affiliated with Chelsea FC" label

## Questions for you

1. Do you approve the separate `venue` table?
2. Plain `venv` + `pip` (simpler) or `uv` (faster)? I suggest venv + pip.
3. Is anything in the roadmap diagram for Phase 0 missing from this plan?
