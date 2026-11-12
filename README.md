# Blueprint

**An independent portfolio project. Not affiliated with, endorsed by or connected to
Chelsea FC, Chelsea FC Women or any other club.** It uses public data only.

Blueprint turns public data into plain-English insights for commercial decisions in
women's football: partnerships, partner value, matchday, fanbase and player commercial
value. See [docs/spec.md](docs/spec.md) for the full spec and
[docs/sources.md](docs/sources.md) for every data source and its terms.

## Status

Phase 0 (Foundations): project skeleton, empty warehouse, source register, tests.

## Run it

```bash
python3.12 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -e ".[dev]"
```

```bash
python -m blueprint.models.build
```

```bash
ruff check . && pytest
```

The build command creates `data/warehouse.duckdb` with the empty tables and loads the
source register.
