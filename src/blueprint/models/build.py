"""Build the warehouse: create the tables and load the source register.

Run with:  python -m blueprint.models.build
"""

from datetime import date
from pathlib import Path

import duckdb

from blueprint import config

SCHEMA_SQL = Path(__file__).with_name("schema.sql")
SOURCE_COLUMNS = [
    "source_id",
    "name",
    "url",
    "robots_ok",
    "terms_checked_on",
    "history_depth",
    "polite_rate",
    "verdict",
    "notes",
]


def create_schema(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(SCHEMA_SQL.read_text())


def parse_sources_md(path: Path = config.SOURCES_MD) -> list[dict]:
    """Read the source register table out of docs/sources.md.

    The register is kept in Markdown so it is easy to read and edit on GitHub; this
    turns the first table whose header starts with `source_id` into a list of dicts.
    """
    rows: list[dict] = []
    header: list[str] | None = None
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            if header is not None and rows:
                break  # the register table has ended
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if header is None:
            if cells[0] == "source_id":
                header = cells
            continue
        if set(cells[0]) <= {"-", ":", " "}:
            continue  # the |---|---| separator line
        rows.append(_clean_row(dict(zip(header, cells, strict=True))))
    if header != SOURCE_COLUMNS:
        raise ValueError(f"sources.md register header must be {SOURCE_COLUMNS}, got {header}")
    return rows


def _clean_row(row: dict) -> dict:
    """Turn Markdown text into proper values: blank -> None, yes/no -> True/False."""
    out = {k: (v if v else None) for k, v in row.items()}
    robots = (out["robots_ok"] or "").lower()
    out["robots_ok"] = {"yes": True, "no": False}.get(robots)
    if out["terms_checked_on"]:
        out["terms_checked_on"] = date.fromisoformat(out["terms_checked_on"])
    # Markdown shows code-formatted ids with backticks; strip them.
    out["source_id"] = out["source_id"].strip("`")
    return out


def load_sources(con: duckdb.DuckDBPyConnection, rows: list[dict]) -> None:
    """Replace the source table with the current register (the Markdown file is the master)."""
    con.execute("DELETE FROM source")
    placeholders = ", ".join("?" for _ in SOURCE_COLUMNS)
    con.executemany(
        f"INSERT INTO source ({', '.join(SOURCE_COLUMNS)}) VALUES ({placeholders})",
        [[r[c] for c in SOURCE_COLUMNS] for r in rows],
    )


def build_warehouse(path: Path | None = None) -> Path:
    path = path or config.warehouse_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(path)) as con:
        create_schema(con)
        load_sources(con, parse_sources_md())
    return path


if __name__ == "__main__":
    print(f"Warehouse built at {build_warehouse()}")
