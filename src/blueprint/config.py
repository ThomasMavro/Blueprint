"""All file paths in one place, so no other module hard-codes where data lives."""

import os
from pathlib import Path

# The repo root is three levels up from this file: src/blueprint/config.py -> repo/
REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCES_MD = REPO_ROOT / "docs" / "sources.md"


def data_dir() -> Path:
    """Where data lives. Set BLUEPRINT_DATA_DIR to move it (tests use a temp folder)."""
    return Path(os.environ.get("BLUEPRINT_DATA_DIR", REPO_ROOT / "data"))


def raw_dir() -> Path:
    return data_dir() / "raw"


def warehouse_path() -> Path:
    return data_dir() / "warehouse.duckdb"
