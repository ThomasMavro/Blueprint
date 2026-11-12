-- Blueprint warehouse schema (Phase 0).
-- "IF NOT EXISTS" means running the build twice is safe: it never wipes existing data.
--
-- Every data table carries source_id, source_url and snapshot_date, so any figure can be
-- traced back to the raw page it came from and the day it was collected.
-- No foreign keys: DuckDB makes reloading parent tables awkward when they are used, so
-- links between tables (fixture -> club, fixture -> venue) are checked by the data rules
-- in checks.py instead, which report problems rather than silently blocking a load.

CREATE TABLE IF NOT EXISTS club (
    club_id        VARCHAR PRIMARY KEY,   -- short stable id, e.g. 'chelsea'
    name           VARCHAR NOT NULL,
    league         VARCHAR NOT NULL,
    country        VARCHAR NOT NULL,
    peer_groups    VARCHAR[],             -- e.g. ['wsl', 'european_elite']
    source_id      VARCHAR NOT NULL,
    source_url     VARCHAR NOT NULL,
    snapshot_date  DATE    NOT NULL
);

CREATE TABLE IF NOT EXISTS venue (
    venue_id       VARCHAR PRIMARY KEY,   -- e.g. 'stamford_bridge'
    name           VARCHAR NOT NULL,
    city           VARCHAR NOT NULL,
    country        VARCHAR NOT NULL,
    capacity       INTEGER CHECK (capacity > 0),
    source_id      VARCHAR NOT NULL,
    source_url     VARCHAR NOT NULL,      -- where the capacity figure comes from
    snapshot_date  DATE    NOT NULL
);

CREATE TABLE IF NOT EXISTS fixture (
    fixture_id     VARCHAR PRIMARY KEY,
    season         VARCHAR NOT NULL,      -- e.g. '2026/27'
    competition    VARCHAR NOT NULL,      -- e.g. 'WSL', 'UWCL', 'FA Cup'
    match_date     DATE    NOT NULL,
    kickoff        TIME,                  -- local UK time; unknown for some old games
    home_club_id   VARCHAR NOT NULL,
    away_club_id   VARCHAR NOT NULL,
    venue_id       VARCHAR,
    attendance     INTEGER CHECK (attendance >= 0),  -- NULL = not reported, never 0
    tv_broadcaster VARCHAR,
    source_id      VARCHAR NOT NULL,
    source_url     VARCHAR NOT NULL,
    snapshot_date  DATE    NOT NULL,
    CHECK (home_club_id <> away_club_id)
);

-- Machine-readable copy of docs/sources.md (loaded by build.py).
CREATE TABLE IF NOT EXISTS source (
    source_id         VARCHAR PRIMARY KEY,
    name              VARCHAR NOT NULL,
    url               VARCHAR,
    robots_ok         BOOLEAN,            -- NULL = not checked yet
    terms_checked_on  DATE,
    history_depth     VARCHAR,
    polite_rate       VARCHAR,
    verdict           VARCHAR NOT NULL
        CHECK (verdict IN ('use', 'use with limits', 'don''t use', 'not checked')),
    notes             VARCHAR
);

-- One row per scraper run, including failures. Feeds the data health page later.
CREATE TABLE IF NOT EXISTS collection_log (
    run_id          VARCHAR PRIMARY KEY,
    source_id       VARCHAR NOT NULL,
    started_at_utc  TIMESTAMP NOT NULL,
    finished_at_utc TIMESTAMP,
    rows_expected   INTEGER,
    rows_collected  INTEGER NOT NULL DEFAULT 0,
    status          VARCHAR NOT NULL
        CHECK (status IN ('running', 'ok', 'partial', 'blocked', 'failed')),
    errors          VARCHAR
);
