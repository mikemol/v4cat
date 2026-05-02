"""
Branch-coverage tests — exercises the residue branches outside the
ISA, MCP, sandbox, and self-hosting test files.

Background: kquery on the per-test-file branch sets identified 27
branches in the (00) cell — neither the ISA-track nor the MCP-track
exercised them. This file closes that cell. See
cotype/snap_report.md and the kquery analysis in the session of
2026-05-02.

Each test names the branch(es) it covers in its docstring so future
RFS fires can re-run the analysis and recognise these as orbit
positions of the kquery-on-coverage primitive.

Run as a script::

    python -m v4cat.tests.test_branch_coverage
"""
from __future__ import annotations

import asyncio
import json
import runpy
import sqlite3
import sys
import tempfile
import traceback
from pathlib import Path
from unittest.mock import patch

from v4cat import SymmetryCatalogue, consistency
from v4cat.cells import Cell, Kind
from v4cat.bootstrap import (
    enumerate_supported_cells,
    supported_kinds,
)
from v4cat.theory import SIGNATURE, by_kind
import v4cat.mcp_server as srv
from v4cat.mcp_server import server, set_catalogue


# =============================================================================
# Synchronous tests — catalogue / views / cells / theory / bootstrap
# =============================================================================

def test_catalogue_bootstrap_false_skips_schema():
    """catalogue.py:75->87 — bootstrap=False does NOT load schema."""
    cat = SymmetryCatalogue(
        ':memory:', bootstrap=False, check_self_hosting=False,
    )
    try:
        cat.query("SELECT * FROM specs")
        assert False, "expected sqlite3.OperationalError"
    except sqlite3.OperationalError:
        pass


def test_catalogue_bootstrap_false_with_check_self_hosting():
    """catalogue.py:87-93 — bootstrap=False + check_self_hosting=True
    is a no-op (closure_status returns None when Q-supported-claims
    is absent)."""
    cat = SymmetryCatalogue(
        ':memory:', bootstrap=False, check_self_hosting=True,
    )
    # No exception; the catalogue exists but has no schema
    assert cat is not None


def test_context_manager_enter_returns_self():
    """catalogue.py:114 — __enter__ returns the catalogue."""
    db = tempfile.NamedTemporaryFile(suffix='.db', delete=False).name
    try:
        with SymmetryCatalogue(db) as cat:
            assert cat is not None
            assert isinstance(cat, SymmetryCatalogue)
    finally:
        Path(db).unlink(missing_ok=True)


def test_context_manager_normal_exit_commits():
    """catalogue.py:117->118 — __exit__ commits on normal exit."""
    db = tempfile.NamedTemporaryFile(suffix='.db', delete=False).name
    try:
        with SymmetryCatalogue(db) as cat:
            cat.introduce_break('CTX', 'Context test')
        with SymmetryCatalogue(db) as cat2:
            assert any(b['number'] == 'CTX' for b in cat2.all_breaks())
    finally:
        Path(db).unlink(missing_ok=True)


def test_context_manager_exception_rolls_back():
    """catalogue.py:117->120 — __exit__ rolls back on exception."""
    db = tempfile.NamedTemporaryFile(suffix='.db', delete=False).name
    try:
        try:
            with SymmetryCatalogue(db) as cat:
                cat.introduce_break('RB', 'Rollback test')
                raise RuntimeError('expected for rollback test')
        except RuntimeError:
            pass
        with SymmetryCatalogue(db) as cat2:
            assert not any(b['number'] == 'RB' for b in cat2.all_breaks())
    finally:
        Path(db).unlink(missing_ok=True)


def test_introduce_tension_without_breaks_involved():
    """catalogue.py:374->exit — introduce_tension with no breaks_involved."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_tension('T1', 'Tension one', description='no breaks')
    rows = cat.query("SELECT * FROM tensions WHERE id = 'T1'")
    assert len(rows) == 1
    assert rows[0]['name'] == 'Tension one'


def test_introduce_tension_with_breaks_involved():
    """catalogue.py:374->375 — introduce_tension WITH breaks_involved."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_break('F1', 'Break one')
    cat.introduce_break('F2', 'Break two')
    cat.introduce_tension(
        'T2', 'Tension two', breaks_involved=['F1', 'F2'],
    )
    rows = cat.query(
        "SELECT * FROM tension_breaks WHERE tension_id = 'T2'"
    )
    assert {r['break_number'] for r in rows} == {'F1', 'F2'}


def test_tropical_min_rejects_invalid_direction():
    """catalogue.py:291->292 — invalid direction raises ValueError."""
    cat = SymmetryCatalogue(':memory:')
    try:
        cat.tropical_min(
            axis_column='year', witness_kinds=('origin',),
            direction='bogus',
        )
        assert False, "expected ValueError"
    except ValueError as e:
        assert 'direction' in str(e)


def test_tropical_min_rejects_empty_witness_kinds():
    """catalogue.py:302->303 — empty witness_kinds raises ValueError."""
    cat = SymmetryCatalogue(':memory:')
    try:
        cat.tropical_min(axis_column='year', witness_kinds=())
        assert False, "expected ValueError"
    except ValueError as e:
        assert 'witness_kinds' in str(e)


def test_cell_eq_with_non_cell_returns_notimplemented():
    """cells.py:59->60 — __eq__ returns NotImplemented for non-Cell."""
    c = Cell('test', Kind.O, 'd')
    # Python's __eq__ NotImplemented falls back to identity → False
    assert c != 'string'
    assert c != 42
    assert c != None
    # Direct invocation surfaces the sentinel
    assert c.__eq__('string') is NotImplemented


def test_origin_returns_none_for_unknown_break():
    """catalogue.py origin() — no rows -> return None."""
    cat = SymmetryCatalogue(':memory:')
    assert cat.origin('F-nonexistent') is None


def test_retroactive_gap_none_when_origin_missing():
    """catalogue.py retroactive_gap() — origin returns None
    (no origin/catalogue-introduces witness)."""
    cat = SymmetryCatalogue(':memory:')
    assert cat.retroactive_gap('F-nonexistent') is None


def test_retroactive_gap_none_when_origin_filters_to_nothing():
    """catalogue.py retroactive_gap() — every candidate spec has a
    null axis value (tropical_min's NULL filter excludes all)."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_object('only', 'Only', year=None, catalogue_order=1)
    cat.introduce_break('F', 'F', axes=['spatial'])
    cat.witness('only', 'F', 'origin')
    cat.witness('only', 'F', 'catalogue-introduces')
    # No spec has a non-null year for this break — origin returns None
    assert cat.origin('F') is None
    # retroactive_gap therefore returns None
    assert cat.retroactive_gap('F') is None


def test_retroactive_gap_none_when_first_seen_missing():
    """catalogue.py retroactive_gap() — origin OK, but no
    catalogue-introduces witness so first_seen is None."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_object('a', 'A', year=1990, catalogue_order=1)
    cat.introduce_break('F', 'F', axes=['spatial'])
    cat.witness('a', 'F', 'origin')
    # No catalogue-introduces witness — first_seen() returns None
    # But origin() will still pick a (origin witness, year=1990)
    assert cat.origin('F') is not None
    assert cat.first_seen('F') is None
    assert cat.retroactive_gap('F') is None


def test_retroactive_gap_none_when_first_seen_axis_value_is_null():
    """catalogue.py retroactive_gap() — first_seen's spec has a null
    value on the chosen axis_column."""
    cat = SymmetryCatalogue(':memory:')
    cat.conn.execute("ALTER TABLE specs ADD COLUMN version INTEGER")
    cat.introduce_object('older', 'Older', year=1990, catalogue_order=2)
    cat.introduce_object('newer', 'Newer', year=2000, catalogue_order=1)
    cat.conn.execute(
        "UPDATE specs SET version = ? WHERE id = ?", (5, 'older'))
    # newer.version intentionally null
    cat.introduce_break('F', 'F', axes=['spatial'])
    cat.witness('older', 'F', 'origin')
    cat.witness('newer', 'F', 'catalogue-introduces')
    # On 'version' axis: origin uses MIN(version) over origin/CI edges
    # → only older has non-null version, so origin = older, value = 5.
    # first_seen uses MIN(catalogue_order) → newer (CO=1).
    # newer.version is null → retroactive_gap returns None.
    assert cat.retroactive_gap('F', axis_column='version') is None


def test_consistency_with_valid_rule_reads_violations_view():
    """views.consistency — parametric over rule name; reads the
    `<rule>_violations` view that a domain extension defines."""
    cat = SymmetryCatalogue(':memory:')
    with tempfile.NamedTemporaryFile('w', suffix='.sql', delete=False) as f:
        f.write(
            "CREATE VIEW IF NOT EXISTS demo_violations AS "
            "SELECT 'sentinel' AS spec_id WHERE 1 = 0;"
        )
        f.flush()
        cat.load_extension(f.name)
    rows = consistency(cat, 'demo')
    assert rows == []


def test_consistency_rejects_invalid_rule_name():
    """views.consistency — invalid identifier raises ValueError before
    any SQL runs (defends against injection at the resource boundary)."""
    cat = SymmetryCatalogue(':memory:')
    for bad in ('1bad', 'has-dash', 'has space', "drop'", '', 'with;semi'):
        try:
            consistency(cat, bad)
            assert False, f"expected ValueError for {bad!r}"
        except ValueError as e:
            assert 'identifier' in str(e)


def test_spec_axis_summary_callable():
    """views.py:212 — spec_axis_summary executes against the schema."""
    from v4cat.views import spec_axis_summary
    cat = SymmetryCatalogue(':memory:')
    result = spec_axis_summary(cat)
    assert isinstance(result, list)


def test_theory_by_kind_filters_signature():
    """theory.py:100 — by_kind filters SIGNATURE to one kind."""
    o_cells = by_kind(Kind.O)
    assert all(c.kind == Kind.O for c in o_cells)
    assert len(o_cells) >= 1
    # And it filters: K-cells aren't included in the O list
    k_cells = by_kind(Kind.K)
    o_ids = {c.id for c in o_cells}
    k_ids = {c.id for c in k_cells}
    assert o_ids.isdisjoint(k_ids)


def test_supported_kinds_handles_missing_table():
    """bootstrap.py:133-136 — supported_kinds returns empty set when
    refinements table is absent."""
    cat = SymmetryCatalogue(
        ':memory:', bootstrap=False, check_self_hosting=False,
    )
    kinds = supported_kinds(cat)
    assert kinds == set()


def test_enumerate_supported_cells_filters_out_of_scope_kinds():
    """bootstrap.py:162->161 — cells with kind not in scope are skipped."""
    cat = SymmetryCatalogue(':memory:')
    # Restrict scope to {O, B} only — drops W, R, E, K, X cells
    cat.conn.execute(
        "UPDATE refinements SET description='O,B' "
        "WHERE break_number='Q-supported-claims' AND name='supported_kinds'"
    )
    cat.commit()
    impl_ids, _ = enumerate_supported_cells(cat)
    # SIGNATURE has 2 O-cells (introduce_object, introduce_tension)
    # and 3 B-cells (introduce_break + 2 bootstrap breaks)
    o_cells = [c for c in SIGNATURE if c.kind == Kind.O]
    b_cells = [c for c in SIGNATURE if c.kind == Kind.B]
    assert len(impl_ids) == len(o_cells) + len(b_cells)


def test_enumerate_supported_cells_handles_missing_witness_table():
    """bootstrap.py:170-174 — defensive OperationalError handler when
    witnesses table is missing."""
    cat = SymmetryCatalogue(':memory:')
    # Add a refinement so supported_kinds is non-empty, then drop the
    # witnesses table to trigger the except branch.
    cat.conn.execute("DROP TABLE witnesses")
    cat.commit()
    impl_ids, cat_ids = enumerate_supported_cells(cat)
    assert cat_ids == set()  # except branch fired; rows = []


# =============================================================================
# Asynchronous tests — MCP server resources, tools, error paths, CLI
# =============================================================================

async def call_tool(tool_name, /, **kwargs):
    result = await server.call_tool(tool_name, kwargs)
    if isinstance(result, tuple) and len(result) == 2:
        _, structured = result
        if isinstance(structured, dict) and set(structured.keys()) == {'result'}:
            return structured['result']
        return structured
    if isinstance(result, list) and result and hasattr(result[0], 'text'):
        text = result[0].text
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    return result


async def read_resource(uri: str):
    result = await server.read_resource(uri)
    items = list(result)
    if items and hasattr(items[0], 'content'):
        text = items[0].content
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    return items


def fresh_populated_catalogue():
    cat = SymmetryCatalogue(':memory:')
    set_catalogue(cat)
    cat.introduce_object('alpha', 'Alpha', year=1980, catalogue_order=1)
    cat.introduce_break('F1', 'Spatial test', axes=['spatial'])
    cat.witness('alpha', 'F1', 'origin')
    cat.witness('alpha', 'F1', 'catalogue-introduces')
    cat.commit()
    return cat


async def test_get_catalogue_lazy_init():
    """mcp_server.py:83-84 — get_catalogue() lazily creates _cat when None."""
    saved = srv._cat
    srv._cat = None
    try:
        # Use a temp file path so the lazy default doesn't write to /tmp/cat.db
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tf:
            tf_path = tf.name
        old_default = srv.DEFAULT_DB_PATH
        srv.DEFAULT_DB_PATH = tf_path
        try:
            cat = srv.get_catalogue()
            assert cat is not None
            assert srv._cat is cat
        finally:
            srv.DEFAULT_DB_PATH = old_default
            Path(tf_path).unlink(missing_ok=True)
    finally:
        srv._cat = saved


async def test_swap_active_swallows_close_error():
    """mcp_server.py:115->120 — _swap_active swallows close exception."""
    class BrokenCat:
        def close(self):
            raise RuntimeError('close failed')
    saved = srv._cat
    srv._cat = BrokenCat()
    try:
        new = SymmetryCatalogue(':memory:')
        srv._swap_active(new, 'test_slot')
        assert srv._cat is new
        assert srv._active_slot == 'test_slot'
    finally:
        srv._cat = saved
        srv._active_slot = None


async def test_swap_active_with_no_prior_catalogue():
    """mcp_server.py:115->120 (False side) — _swap_active when _cat is None."""
    saved = srv._cat
    saved_slot = srv._active_slot
    srv._cat = None
    srv._active_slot = None
    try:
        new = SymmetryCatalogue(':memory:')
        srv._swap_active(new, 'fresh_slot')
        assert srv._cat is new
        assert srv._active_slot == 'fresh_slot'
    finally:
        srv._cat = saved
        srv._active_slot = saved_slot


async def test_introduce_tension_tool():
    """mcp_server.py:270-277 — introduce_tension MCP tool body."""
    fresh_populated_catalogue()
    result = await call_tool(
        'introduce_tension',
        id='T_mcp', name='MCP-introduced tension',
        description='via MCP', breaks_involved=['F1'],
    )
    assert result['ok'] is True
    assert result['id'] == 'T_mcp'


async def test_query_first_seen_tool():
    """mcp_server.py:435 — query_first_seen tool returns None for unknown."""
    fresh_populated_catalogue()
    result = await call_tool('query_first_seen', break_number='F-unknown')
    assert result is None


async def test_query_inherited_breaks_tool():
    """mcp_server.py:455 — query_inherited_breaks tool body."""
    cat = fresh_populated_catalogue()
    cat.introduce_object(
        'beta', 'Beta', year=1990,
        lineage=[('alpha', 'descended-from')],
    )
    cat.commit()
    result = await call_tool('query_inherited_breaks', object_id='beta')
    assert isinstance(result, list)
    inherited = {r['break_number'] for r in result}
    assert 'F1' in inherited


async def test_get_break_404_for_missing():
    """mcp_server.py:567->568 — get_break returns error for unknown."""
    fresh_populated_catalogue()
    result = await read_resource('catalogue://breaks/Q-nonexistent')
    assert 'error' in result


async def test_list_objects_resource():
    """mcp_server.py:578 — list_objects resource body."""
    fresh_populated_catalogue()
    result = await read_resource('catalogue://objects')
    assert isinstance(result, list)
    assert any(o['id'] == 'alpha' for o in result)


async def test_get_object_404_for_missing():
    """mcp_server.py:586->587 — get_object returns error for unknown."""
    fresh_populated_catalogue()
    result = await read_resource('catalogue://objects/nonexistent')
    assert 'error' in result


async def test_tensions_resource():
    """mcp_server.py:606 — tensions resource body."""
    cat = fresh_populated_catalogue()
    cat.introduce_tension('T1', 'Sample tension')
    cat.commit()
    result = await read_resource('catalogue://tensions')
    assert isinstance(result, list)
    assert any(t['id'] == 'T1' for t in result)


async def test_violations_resource_with_valid_rule():
    """mcp_server — catalogue://violations/{rule} parametric
    consistency-rule resource (success path)."""
    cat = fresh_populated_catalogue()
    with tempfile.NamedTemporaryFile('w', suffix='.sql', delete=False) as f:
        f.write(
            "CREATE VIEW IF NOT EXISTS demo_violations AS "
            "SELECT 'sentinel' AS spec_id WHERE 1 = 0;"
        )
        f.flush()
        cat.load_extension(f.name)
    cat.commit()
    result = await read_resource('catalogue://violations/demo')
    assert result == []


async def test_violations_resource_rejects_bad_rule_name():
    """mcp_server — catalogue://violations/{rule} returns an error
    object when the rule name is not a valid identifier."""
    fresh_populated_catalogue()
    result = await read_resource('catalogue://violations/1bad')
    assert isinstance(result, dict)
    assert 'error' in result
    assert 'identifier' in result['error']


async def test_axes_resource():
    """mcp_server.py:622 — axes resource body."""
    fresh_populated_catalogue()
    result = await read_resource('catalogue://axes')
    assert isinstance(result, dict)


async def test_mixed_breaks_resource():
    """mcp_server.py:628 — mixed_breaks resource body."""
    cat = fresh_populated_catalogue()
    cat.introduce_break(
        'F-mixed', 'Mixed-axis break',
        axes=['spatial', 'temporal'],
    )
    cat.commit()
    result = await read_resource('catalogue://mixed_breaks')
    assert isinstance(result, list)


async def test_agent_witnesses_resource():
    """mcp_server.py:634 — agent_witnesses resource body."""
    fresh_populated_catalogue()
    result = await read_resource('catalogue://agent_witnesses')
    assert isinstance(result, list)


async def test_spec_axes_resource():
    """mcp_server.py:640 — spec_axes resource body."""
    fresh_populated_catalogue()
    result = await read_resource('catalogue://spec_axes')
    assert isinstance(result, list)


async def test_top_originators_resource():
    """mcp_server.py:646 — top_originators resource body."""
    fresh_populated_catalogue()
    result = await read_resource('catalogue://top_originators')
    assert isinstance(result, list)


async def test_self_hosting_resource_when_self_hosting():
    """mcp_server.py:693-711 — self_hosting resource when supported."""
    fresh_populated_catalogue()
    result = await read_resource('catalogue://self_hosting')
    assert result['supported'] is True
    assert result['passing'] is True
    assert 'cells' in result


async def test_self_hosting_resource_when_not_self_hosting():
    """mcp_server.py:697->698 — self_hosting resource when not supported."""
    cat = SymmetryCatalogue(
        ':memory:', bootstrap=True, check_self_hosting=False,
    )
    set_catalogue(cat)
    result = await read_resource('catalogue://self_hosting')
    assert result['supported'] is False
    assert result['passing'] is None


# =============================================================================
# CLI / main() — covered by running mcp_server as a script with mocks
# =============================================================================

async def test_main_default_without_root_errors():
    """mcp_server.py:1021->1022 — --default without --root errors out."""
    with patch('sys.argv', ['v4cat-mcp', '--default', 'foo']):
        with patch.object(srv.server, 'run'):
            try:
                srv.main()
                assert False, "expected SystemExit"
            except SystemExit:
                pass


async def test_main_root_only():
    """mcp_server.py:1025->1032 — --root without --default."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('sys.argv', ['v4cat-mcp', '--root', tmpdir]):
            with patch.object(srv.server, 'run'):
                srv.main()


async def test_main_root_with_default_creates_slot():
    """mcp_server.py:1027->1028, 1027->1035 — --root + --default opens slot."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Pre-create the slot file so path_for() finds it
        Path(tmpdir, 'mydomain.db').touch()
        with patch('sys.argv', ['v4cat-mcp', '--root', tmpdir,
                                 '--default', 'mydomain']):
            with patch.object(srv.server, 'run'):
                srv.main()


async def test_main_db_path_only():
    """mcp_server.py:1032->1033, 1032->1035 — --db sets DEFAULT_DB_PATH."""
    saved_default = srv.DEFAULT_DB_PATH
    saved_cat = srv._cat
    try:
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tf:
            tf_path = tf.name
        with patch('sys.argv', ['v4cat-mcp', '--db', tf_path]):
            with patch.object(srv.server, 'run'):
                srv.main()
        assert srv.DEFAULT_DB_PATH == tf_path
        Path(tf_path).unlink(missing_ok=True)
    finally:
        srv.DEFAULT_DB_PATH = saved_default
        srv._cat = saved_cat


async def test_main_no_args_uses_defaults():
    """mcp_server.py:1032->1035 (False side) — no --root and no --db."""
    saved_default = srv.DEFAULT_DB_PATH
    saved_cat = srv._cat
    try:
        with patch('sys.argv', ['v4cat-mcp']):
            with patch.object(srv.server, 'run'):
                srv.main()
    finally:
        srv.DEFAULT_DB_PATH = saved_default
        srv._cat = saved_cat


async def test_module_main_guard():
    """mcp_server.py:1038->1039 — `if __name__ == '__main__': main()`.

    Run the module as a script via runpy. runpy re-imports the
    module under name '__main__', so we patch the FastMCP.run
    method at the *class* level so the freshly-instantiated server
    inherits the no-op.
    """
    from mcp.server.fastmcp import FastMCP
    saved_default = srv.DEFAULT_DB_PATH
    saved_cat = srv._cat
    try:
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tf:
            tf_path = tf.name
        with patch('sys.argv', ['v4cat-mcp', '--db', tf_path]):
            with patch.object(FastMCP, 'run', lambda self, *a, **kw: None):
                runpy.run_module(
                    'v4cat.mcp_server', run_name='__main__',
                )
        Path(tf_path).unlink(missing_ok=True)
    finally:
        srv.DEFAULT_DB_PATH = saved_default
        srv._cat = saved_cat


# =============================================================================
# Test harness
# =============================================================================

SYNC_TESTS = [
    test_catalogue_bootstrap_false_skips_schema,
    test_catalogue_bootstrap_false_with_check_self_hosting,
    test_context_manager_enter_returns_self,
    test_context_manager_normal_exit_commits,
    test_context_manager_exception_rolls_back,
    test_introduce_tension_without_breaks_involved,
    test_introduce_tension_with_breaks_involved,
    test_tropical_min_rejects_invalid_direction,
    test_tropical_min_rejects_empty_witness_kinds,
    test_cell_eq_with_non_cell_returns_notimplemented,
    test_origin_returns_none_for_unknown_break,
    test_retroactive_gap_none_when_origin_missing,
    test_retroactive_gap_none_when_origin_filters_to_nothing,
    test_retroactive_gap_none_when_first_seen_missing,
    test_retroactive_gap_none_when_first_seen_axis_value_is_null,
    test_consistency_with_valid_rule_reads_violations_view,
    test_consistency_rejects_invalid_rule_name,
    test_spec_axis_summary_callable,
    test_theory_by_kind_filters_signature,
    test_supported_kinds_handles_missing_table,
    test_enumerate_supported_cells_filters_out_of_scope_kinds,
    test_enumerate_supported_cells_handles_missing_witness_table,
]

ASYNC_TESTS = [
    test_get_catalogue_lazy_init,
    test_swap_active_swallows_close_error,
    test_swap_active_with_no_prior_catalogue,
    test_introduce_tension_tool,
    test_query_first_seen_tool,
    test_query_inherited_breaks_tool,
    test_get_break_404_for_missing,
    test_list_objects_resource,
    test_get_object_404_for_missing,
    test_tensions_resource,
    test_violations_resource_with_valid_rule,
    test_violations_resource_rejects_bad_rule_name,
    test_axes_resource,
    test_mixed_breaks_resource,
    test_agent_witnesses_resource,
    test_spec_axes_resource,
    test_top_originators_resource,
    test_self_hosting_resource_when_self_hosting,
    test_self_hosting_resource_when_not_self_hosting,
    test_main_default_without_root_errors,
    test_main_root_only,
    test_main_root_with_default_creates_slot,
    test_main_db_path_only,
    test_main_no_args_uses_defaults,
    test_module_main_guard,
]


async def run_async_all():
    passed = failed = 0
    for test in ASYNC_TESTS:
        try:
            await test()
            print(f"  ✓ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__}: {e}")
            traceback.print_exc()
            failed += 1
    return passed, failed


def main() -> int:
    passed = failed = 0
    for test in SYNC_TESTS:
        try:
            test()
            print(f"  ✓ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__}: {e}")
            traceback.print_exc()
            failed += 1
    a_passed, a_failed = asyncio.run(run_async_all())
    passed += a_passed
    failed += a_failed
    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
