"""Shared test setup. pytest loads this file automatically.

A "fixture" in pytest is a ready-made thing a test can ask for by naming it as an
argument (not to be confused with a football fixture).
"""

import duckdb
import pytest

from blueprint.models.build import create_schema, load_sources, parse_sources_md


@pytest.fixture
def con(tmp_path):
    """A fresh warehouse in a temporary folder, with the schema and source register loaded."""
    connection = duckdb.connect(str(tmp_path / "test.duckdb"))
    create_schema(connection)
    load_sources(connection, parse_sources_md())
    yield connection
    connection.close()
