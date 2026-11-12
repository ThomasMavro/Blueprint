import importlib
import pkgutil

import blueprint.ingest
from blueprint.models.build import parse_sources_md


def test_register_has_unique_ids():
    ids = [r["source_id"] for r in parse_sources_md()]
    assert len(ids) == len(set(ids))


def test_every_register_row_is_in_source_table(con):
    in_md = {r["source_id"] for r in parse_sources_md()}
    in_db = {r[0] for r in con.execute("SELECT source_id FROM source").fetchall()}
    assert in_md == in_db


def test_every_ingest_module_names_a_registered_source():
    registered = {r["source_id"] for r in parse_sources_md()}
    for mod in pkgutil.iter_modules(blueprint.ingest.__path__):
        if mod.name.startswith("_"):
            continue  # shared helpers, not sources
        module = importlib.import_module(f"blueprint.ingest.{mod.name}")
        assert getattr(module, "SOURCE_ID", None) in registered, mod.name
