"""Tests for the polite client, snapshot writers and collection log.

httpx.MockTransport plays the part of a website, so these tests never touch the internet.
"""

from datetime import date

import httpx
import pandas as pd
import pytest

from blueprint.ingest._common import (
    PoliteClient,
    RobotsDisallowed,
    collection_run,
    save_raw_page,
    save_raw_table,
)


class FakeTime:
    """A clock that only moves when the code 'sleeps', so tests run instantly."""

    def __init__(self):
        self.now = 0.0
        self.slept: list[float] = []

    def clock(self):
        return self.now

    def sleep(self, seconds):
        self.slept.append(seconds)
        self.now += seconds


def fake_site(robots_txt="User-agent: *\nDisallow: /private\n", robots_status=200):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(robots_status, text=robots_txt)
        if request.url.path == "/missing":
            return httpx.Response(404)
        return httpx.Response(200, text="<html>ok</html>")

    return httpx.MockTransport(handler)


def make_client(t, **site):
    return PoliteClient(min_delay=5, transport=fake_site(**site), clock=t.clock, sleep=t.sleep)


def test_respects_robots_disallow():
    with make_client(FakeTime()) as client, pytest.raises(RobotsDisallowed):
        client.get("https://example.org/private/page")


def test_allowed_page_is_fetched():
    with make_client(FakeTime()) as client:
        assert client.get("https://example.org/public").text == "<html>ok</html>"


def test_waits_between_requests_to_same_site():
    t = FakeTime()
    with make_client(t) as client:
        client.get("https://example.org/a")
        client.get("https://example.org/b")
    # robots.txt -> /a -> /b: two gaps of 5 seconds each
    assert t.slept == [5, 5]


def test_obeys_longer_crawl_delay():
    t = FakeTime()
    with make_client(t, robots_txt="User-agent: *\nCrawl-delay: 12\n") as client:
        client.get("https://example.org/a")
        client.get("https://example.org/b")
    assert t.slept[-1] == 12


def test_server_error_on_robots_means_blocked():
    with make_client(FakeTime(), robots_status=503) as client, pytest.raises(RobotsDisallowed):
        client.get("https://example.org/public")


def test_http_error_is_raised_not_hidden():
    with make_client(FakeTime()) as client, pytest.raises(httpx.HTTPStatusError):
        client.get("https://example.org/missing")


def test_raw_page_is_never_overwritten(tmp_path):
    day = date(2026, 11, 12)
    path = save_raw_page("wikipedia", "page.html", b"first", day, root=tmp_path)
    assert path == tmp_path / "wikipedia" / "2026-11-12" / "page.html"
    with pytest.raises(FileExistsError):
        save_raw_page("wikipedia", "page.html", b"second", day, root=tmp_path)
    assert path.read_bytes() == b"first"


def test_raw_table_is_never_overwritten(tmp_path):
    df = pd.DataFrame({"a": [1]})
    save_raw_table("wikipedia", "rows.parquet", df, date(2026, 11, 12), root=tmp_path)
    with pytest.raises(FileExistsError):
        save_raw_table("wikipedia", "rows.parquet", df, date(2026, 11, 12), root=tmp_path)


def logged(con):
    return con.execute(
        "SELECT status, rows_collected, errors FROM collection_log"
    ).fetchone()


def test_successful_run_is_logged_ok(con):
    with collection_run(con, "wikipedia", rows_expected=3) as run:
        run.rows_collected = 3
    assert logged(con) == ("ok", 3, None)


def test_short_run_is_logged_partial(con):
    with collection_run(con, "wikipedia", rows_expected=10) as run:
        run.rows_collected = 7
    assert logged(con)[0] == "partial"


def test_blocked_run_is_logged_blocked(con):
    with collection_run(con, "wikipedia") as run:
        run.blocked = True
    assert logged(con)[0] == "blocked"


def test_crash_is_logged_failed_and_still_raised(con):
    with pytest.raises(ValueError), collection_run(con, "wikipedia", rows_expected=5):
        raise ValueError("page layout changed")
    status, _, errors = logged(con)
    assert status == "failed"
    assert "page layout changed" in errors
