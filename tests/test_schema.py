import duckdb

from blueprint.models.build import build_warehouse, create_schema

EXPECTED_COLUMNS = {
    "club": {"club_id", "name", "league", "country", "peer_groups"},
    "venue": {"venue_id", "name", "city", "country", "capacity"},
    "fixture": {
        "fixture_id", "season", "competition", "match_date", "kickoff",
        "home_club_id", "away_club_id", "venue_id", "attendance", "tv_broadcaster",
    },
    "source": {"source_id", "name", "url", "robots_ok", "terms_checked_on", "verdict"},
    "collection_log": {
        "run_id", "source_id", "started_at_utc", "finished_at_utc",
        "rows_expected", "rows_collected", "status", "errors",
    },
}
TRACE_COLUMNS = {"source_id", "source_url", "snapshot_date"}


def columns(con, table):
    return {r[0] for r in con.execute(f"DESCRIBE {table}").fetchall()}


def test_all_tables_and_columns_exist(con):
    for table, expected in EXPECTED_COLUMNS.items():
        assert expected <= columns(con, table), table


def test_data_tables_are_traceable(con):
    for table in ("club", "venue", "fixture"):
        assert TRACE_COLUMNS <= columns(con, table), table


def test_schema_can_run_twice_without_losing_data(con):
    con.execute(
        "INSERT INTO club VALUES ('chelsea', 'Chelsea', 'WSL', 'England', ['wsl'],"
        " 'wikipedia', 'https://en.wikipedia.org/x', DATE '2026-11-01')"
    )
    create_schema(con)
    assert con.execute("SELECT count(*) FROM club").fetchone()[0] == 1


def test_build_warehouse_creates_file(tmp_path):
    path = build_warehouse(tmp_path / "w.duckdb")
    with duckdb.connect(str(path)) as c:
        assert c.execute("SELECT count(*) FROM source").fetchone()[0] > 0
