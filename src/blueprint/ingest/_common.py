"""Shared tools every scraper uses: a polite HTTP client, raw-snapshot writers, and a
collection log that records every run, including the ones that fail."""

import logging
import time
import uuid
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

import duckdb
import httpx
import pandas as pd

from blueprint import config

log = logging.getLogger(__name__)

# Identifies us honestly to websites. No personal contact details in here.
USER_AGENT = "BlueprintBot/0.1 (independent portfolio research project; public data only)"
DEFAULT_MIN_DELAY = 5.0  # seconds between requests to the same site

# Documented public APIs whose robots.txt blocks all bots. An API is built for programs to
# call, so its robots.txt is aimed at search-engine crawlers. Thomas approved skipping the
# robots check for these hosts only (2026-11-12). Each entry points to the terms we follow
# instead, and the polite delay still applies. Add a host only with Thomas's approval.
DOCUMENTED_APIS: dict[str, str] = {
    "archive-api.open-meteo.com": "https://open-meteo.com/en/terms",
}


class RobotsDisallowed(Exception):
    """The site's robots.txt asks bots not to fetch this URL, so we don't."""


class PoliteClient:
    """An HTTP client that obeys robots.txt and waits between requests to each site.

    `clock` and `sleep` can be swapped for fakes in tests, so the tests don't actually
    wait five seconds.
    """

    def __init__(
        self,
        min_delay: float = DEFAULT_MIN_DELAY,
        transport: httpx.BaseTransport | None = None,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        timeout: float = 30.0,
    ) -> None:
        self.min_delay = min_delay
        self._clock = clock
        self._sleep = sleep
        self._http = httpx.Client(
            headers={"User-Agent": USER_AGENT},
            transport=transport,
            timeout=timeout,
            follow_redirects=True,
        )
        self._robots: dict[str, RobotFileParser] = {}
        self._last_request: dict[str, float] = {}

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "PoliteClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def _site(self, url: str) -> str:
        parts = urlsplit(url)
        return f"{parts.scheme}://{parts.netloc}"

    def _wait_turn(self, site: str, delay: float) -> None:
        last = self._last_request.get(site)
        if last is not None:
            remaining = delay - (self._clock() - last)
            if remaining > 0:
                self._sleep(remaining)
        self._last_request[site] = self._clock()

    def _robots_for(self, site: str) -> RobotFileParser:
        if urlsplit(site).hostname in DOCUMENTED_APIS:
            # Approved API (see DOCUMENTED_APIS): don't read robots.txt, allow every path.
            parser = RobotFileParser()
            parser.parse([])
            self._robots[site] = parser
            return parser
        if site in self._robots:
            return self._robots[site]
        parser = RobotFileParser()
        self._wait_turn(site, self.min_delay)
        try:
            resp = self._http.get(f"{site}/robots.txt")
        except httpx.HTTPError:
            resp = None
        # Standard robots.txt rules (RFC 9309): a 4xx means "no robots file", so allowed;
        # a server error or no answer means we can't know, so treat everything as blocked.
        if resp is not None and resp.status_code < 400:
            parser.parse(resp.text.splitlines())
        elif resp is not None and resp.status_code < 500:
            parser.parse([])
        else:
            parser.parse(["User-agent: *", "Disallow: /"])
        self._robots[site] = parser
        return parser

    def get(self, url: str) -> httpx.Response:
        site = self._site(url)
        robots = self._robots_for(site)
        if not robots.can_fetch(USER_AGENT, url):
            raise RobotsDisallowed(url)
        # If the site asks for a longer gap (Crawl-delay), use that instead.
        delay = max(self.min_delay, float(robots.crawl_delay(USER_AGENT) or 0))
        self._wait_turn(site, delay)
        resp = self._http.get(url)
        resp.raise_for_status()  # a 404 or 500 raises an error instead of passing quietly
        return resp


def snapshot_dir(source_id: str, snapshot_date: date | None = None, root: Path | None = None):
    snapshot_date = snapshot_date or date.today()
    return (root or config.raw_dir()) / source_id / snapshot_date.isoformat()


def save_raw_page(
    source_id: str,
    filename: str,
    content: bytes,
    snapshot_date: date | None = None,
    root: Path | None = None,
) -> Path:
    """Save a fetched page exactly as received. Refuses to overwrite: raw data is never edited."""
    path = snapshot_dir(source_id, snapshot_date, root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    # Mode "xb" = create a new file for writing bytes, and fail if it already exists.
    with path.open("xb") as f:
        f.write(content)
    return path


def save_raw_table(
    source_id: str,
    filename: str,
    df: pd.DataFrame,
    snapshot_date: date | None = None,
    root: Path | None = None,
) -> Path:
    """Save parsed rows as Parquet next to the raw page. Also refuses to overwrite."""
    path = snapshot_dir(source_id, snapshot_date, root) / filename
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    return path


def _utc_now() -> datetime:
    # Stored as plain UTC time (no timezone attached) to keep DuckDB types simple.
    return datetime.now(UTC).replace(tzinfo=None)


@dataclass
class Run:
    """What a scraper reports about one run. The scraper updates it as it goes."""

    run_id: str
    source_id: str
    rows_expected: int | None
    rows_collected: int = 0
    blocked: bool = False
    errors: list[str] = field(default_factory=list)

    def status(self) -> str:
        if self.blocked:
            return "blocked"
        if self.rows_expected and self.rows_collected == 0:
            return "failed"
        if self.errors or (self.rows_expected and self.rows_collected < self.rows_expected):
            return "partial"
        return "ok"


@contextmanager
def collection_run(
    con: duckdb.DuckDBPyConnection, source_id: str, rows_expected: int | None = None
) -> Iterator[Run]:
    """Wrap a scraper run so it is always logged.

    Usage:
        with collection_run(con, "wikipedia", rows_expected=132) as run:
            ...
            run.rows_collected += len(rows)

    If the code inside crashes, the run is logged as 'failed' and the error is raised
    again, so it can't disappear quietly.
    """
    run = Run(uuid.uuid4().hex, source_id, rows_expected)
    con.execute(
        "INSERT INTO collection_log (run_id, source_id, started_at_utc, rows_expected, status)"
        " VALUES (?, ?, ?, ?, 'running')",
        [run.run_id, source_id, _utc_now(), rows_expected],
    )
    try:
        yield run
    except Exception as exc:
        run.errors.append(f"{type(exc).__name__}: {exc}")
        _finish(con, run, "failed")
        raise
    else:
        _finish(con, run, run.status())


def _finish(con: duckdb.DuckDBPyConnection, run: Run, status: str) -> None:
    con.execute(
        "UPDATE collection_log SET finished_at_utc = ?, rows_collected = ?, status = ?,"
        " errors = ? WHERE run_id = ?",
        [_utc_now(), run.rows_collected, status, "\n".join(run.errors) or None, run.run_id],
    )
    if status != "ok":
        log.warning(
            "Collection %s for %s: %s of %s rows. Errors: %s",
            status,
            run.source_id,
            run.rows_collected,
            run.rows_expected,
            run.errors or "none",
        )
