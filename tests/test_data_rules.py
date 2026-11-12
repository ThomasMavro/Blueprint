"""Data rules, tested on small made-up sample rows. These rows exist only inside the tests;
they are never written to the real warehouse."""

import duckdb
import pytest

from blueprint.models.checks import run_checks

SRC = "'wikipedia', 'https://en.wikipedia.org/x', DATE '2026-11-01'"


def add_sample_rows(con, attendance=30000, away="arsenal", source="wikipedia"):
    con.execute(f"INSERT INTO club VALUES ('chelsea', 'Chelsea', 'WSL', 'England', ['wsl'], {SRC})")
    con.execute(f"INSERT INTO club VALUES ('arsenal', 'Arsenal', 'WSL', 'England', ['wsl'], {SRC})")
    con.execute(
        f"INSERT INTO venue VALUES ('bridge', 'Stamford Bridge', 'London', 'England', 40000, {SRC})"
    )
    con.execute(
        "INSERT INTO fixture VALUES ('f1', '2026/27', 'WSL', DATE '2026-10-01', TIME '12:30',"
        f" 'chelsea', '{away}', 'bridge', {attendance}, NULL,"
        f" '{source}', 'https://en.wikipedia.org/x', DATE '2026-11-01')"
    )


def rules_broken(con):
    return {v.rule for v in run_checks(con)}


def test_clean_data_passes(con):
    add_sample_rows(con)
    assert run_checks(con) == []


def test_attendance_above_capacity_is_flagged(con):
    add_sample_rows(con, attendance=45000)
    assert "attendance_within_capacity" in rules_broken(con)


def test_unknown_club_is_flagged(con):
    add_sample_rows(con, away="nobody")
    assert "fixture_away_club_exists" in rules_broken(con)


def test_unregistered_source_is_flagged(con):
    add_sample_rows(con, source="made_up_source")
    assert "data_rows_have_registered_source" in rules_broken(con)


def test_negative_attendance_is_rejected(con):
    with pytest.raises(duckdb.ConstraintException):
        add_sample_rows(con, attendance=-1)


def test_row_without_source_url_is_rejected(con):
    with pytest.raises(duckdb.ConstraintException):
        con.execute(
            "INSERT INTO club VALUES ('x', 'X', 'WSL', 'England', NULL,"
            " 'wikipedia', NULL, DATE '2026-11-01')"
        )


def test_duplicate_fixture_id_is_rejected(con):
    add_sample_rows(con)
    with pytest.raises(duckdb.ConstraintException):
        con.execute(
            "INSERT INTO fixture SELECT * FROM fixture WHERE fixture_id = 'f1'"
        )
