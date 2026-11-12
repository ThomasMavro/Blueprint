"""Data rules that run on the warehouse.

Each rule is a SQL query that returns the rows breaking the rule. An empty result means
the rule passes. Rules report problems; they never delete or fix rows, because fixing
data without Thomas's approval is against the project rules.
"""

from dataclasses import dataclass

import duckdb

RULES: dict[str, str] = {
    "fixture_home_club_exists": """
        SELECT f.fixture_id FROM fixture f
        LEFT JOIN club c ON c.club_id = f.home_club_id WHERE c.club_id IS NULL
    """,
    "fixture_away_club_exists": """
        SELECT f.fixture_id FROM fixture f
        LEFT JOIN club c ON c.club_id = f.away_club_id WHERE c.club_id IS NULL
    """,
    "fixture_venue_exists": """
        SELECT f.fixture_id FROM fixture f
        LEFT JOIN venue v ON v.venue_id = f.venue_id
        WHERE f.venue_id IS NOT NULL AND v.venue_id IS NULL
    """,
    # Attendance above capacity is usually a typo or a wrong venue, so flag it for review.
    "attendance_within_capacity": """
        SELECT f.fixture_id FROM fixture f JOIN venue v USING (venue_id)
        WHERE f.attendance > v.capacity
    """,
    "data_rows_have_registered_source": """
        SELECT 'club:' || club_id FROM club WHERE source_id NOT IN (SELECT source_id FROM source)
        UNION ALL
        SELECT 'venue:' || venue_id FROM venue
            WHERE source_id NOT IN (SELECT source_id FROM source)
        UNION ALL
        SELECT 'fixture:' || fixture_id FROM fixture
            WHERE source_id NOT IN (SELECT source_id FROM source)
    """,
    "snapshot_not_in_future": """
        SELECT 'club:' || club_id FROM club WHERE snapshot_date > current_date
        UNION ALL
        SELECT 'venue:' || venue_id FROM venue WHERE snapshot_date > current_date
        UNION ALL
        SELECT 'fixture:' || fixture_id FROM fixture WHERE snapshot_date > current_date
    """,
}


@dataclass
class Violation:
    rule: str
    row_ids: list[str]


def run_checks(con: duckdb.DuckDBPyConnection) -> list[Violation]:
    """Run every rule; return only the ones that found problems."""
    violations = []
    for name, sql in RULES.items():
        bad = [str(r[0]) for r in con.execute(sql).fetchall()]
        if bad:
            violations.append(Violation(name, bad))
    return violations
