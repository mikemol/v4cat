"""
Branch-coverage tests — v4cat-core residue branches outside the
ISA and self-hosting test files.

Background: kquery on the per-test-file branch sets identified 27
branches in the (00) cell — neither the ISA-track nor the MCP-track
exercised them. This file closes that cell for the v4cat core. See
cotype/snap_report.md and the kquery analysis in the session of
2026-05-02. The MCP-side branch-coverage tests live in the
v4cat-mcp distribution.

Each test names the branch(es) it covers in its docstring so future
RFS fires can re-run the analysis and recognise these as orbit
positions of the kquery-on-coverage primitive.

Run as a script::

    python -m v4cat.tests.test_branch_coverage
"""
from __future__ import annotations

import sqlite3
import sys
import tempfile
import traceback
from pathlib import Path

from v4cat import SymmetryCatalogue, consistency
from v4cat.cells import Cell, Kind
from v4cat.bootstrap import (
    RiscDisciplineViolation,
    check_risc_discipline,
    enumerate_supported_cells,
    supported_kinds,
)
from v4cat.curry import (
    AxisCutReferent,
    CellReferent,
    EdgeReferent,
    KqueryNode,
    LiteralReferent,
    Param,
    Tension,
    evaluate_tension,
    resolve,
)
from v4cat.theory import SIGNATURE, by_kind


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


# =============================================================================
# (β) RISC reframe — branches in catalogue.py, bootstrap.py, curry.py
# added by S₁–S₄ that test_risc.py doesn't fully exercise.
# =============================================================================

def test_introduce_node_default_branch_records_attributes():
    """introduce_node default branch (non-break, non-tension) writes
    type-attribute and any extra attrs to spec_attributes."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node(
        'my-edge-kind', 'My edge kind', 'edge-kind',
        attrs={'source-type': 'spec', 'target-type': 'break'},
    )
    rows = cat.query(
        "SELECT name, value FROM spec_attributes "
        "WHERE spec_id = 'my-edge-kind' ORDER BY name",
    )
    attrs = {r['name']: r['value'] for r in rows}
    assert attrs.get('type') == 'edge-kind'
    assert attrs.get('source-type') == 'spec'
    assert attrs.get('target-type') == 'break'


def test_introduce_node_default_branch_with_explicit_catalogue_order():
    """introduce_node default branch when catalogue_order is provided
    in attrs skips the auto-assign path."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node(
        'foo', 'Foo', 'spec',
        attrs={'catalogue_order': 99, 'year': 2000},
    )
    rows = cat.query(
        "SELECT catalogue_order FROM specs WHERE id = 'foo'",
    )
    assert rows[0]['catalogue_order'] == 99


def test_edge_unsupported_target_type_raises():
    """edge() raises ValueError when kind's target-type is neither
    'break' nor 'spec'."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('weird-kind', 'Weird', 'edge-kind',
                       attrs={'source-type': 'spec',
                              'target-type': 'unknown-type'})
    cat.introduce_node('a', 'A', 'spec', attrs={'year': 2000})
    cat.introduce_node('b', 'B', 'spec', attrs={'year': 2001})
    try:
        cat.edge('a', 'b', 'weird-kind')
    except ValueError as e:
        assert 'unsupported target-type' in str(e)
    else:
        raise AssertionError('expected ValueError for unsupported target-type')


def test_edge_lineage_kind_with_notes():
    """edge() with target-type=spec writes notes to lineages."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    cat.introduce_node('beta', 'Beta', 'spec', attrs={'year': 2010})
    cat.edge('beta', 'alpha', 'descended-from', notes='direct descent')
    rows = cat.query(
        "SELECT notes FROM lineages "
        "WHERE descendant_id='beta' AND ancestor_id='alpha'",
    )
    assert rows[0]['notes'] == 'direct descent'


def test_attr_key_for_break_returns_none_for_non_kattr():
    """_attr_key_for_break returns None when the break id doesn't
    start with K-ATTR-."""
    assert SymmetryCatalogue._attr_key_for_break('Q-introduce_node') is None
    assert SymmetryCatalogue._attr_key_for_break('plain-break') is None


def test_attr_key_for_break_handles_dashes():
    """_attr_key_for_break converts dashes to underscores."""
    assert SymmetryCatalogue._attr_key_for_break(
        'K-ATTR-CATALOGUE-ORDER') == 'catalogue_order'
    assert SymmetryCatalogue._attr_key_for_break(
        'K-ATTR-SHORT-DESC') == 'short_desc'


def test_node_type_attrs_skips_non_kattr_break():
    """_node_type_attrs ignores witnesses whose break_number isn't a
    K-ATTR-* break (the _attr_key_for_break returns None branch)."""
    cat = SymmetryCatalogue(':memory:')
    # Add a non-K-ATTR break and witness it from 'break' with kind='requires-attr'
    cat.conn.execute(
        "INSERT INTO breaks (number, name, short_desc) VALUES (?, ?, ?)",
        ('Q-something-not-attr', 'Something', 'desc'),
    )
    cat.conn.execute(
        "INSERT INTO witnesses (spec_id, break_number, kind, scope) "
        "VALUES (?, ?, ?, 'spec')",
        ('break', 'Q-something-not-attr', 'requires-attr'),
    )
    required, admitted = cat._node_type_attrs('break')
    # Q-something-not-attr is skipped (returns None from _attr_key_for_break)
    assert 'something' not in required
    # The legitimate K-ATTR-* attrs still come through
    assert 'name' in required


def test_kind_source_type_returns_none_for_uncatalogued_kind():
    """_kind_source_type returns None when the kind isn't catalogued."""
    cat = SymmetryCatalogue(':memory:')
    assert cat._kind_source_type('mythical-kind-xyz') is None


def test_witness_with_agent_scope_writes_directly():
    """witness(scope='agent') bypasses edge() to preserve the S8
    agent-level scope distinction."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('B1', 'B1', 'break')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    cat.witness('alpha', 'B1', 'origin', scope='agent')
    rows = cat.query(
        "SELECT scope FROM witnesses "
        "WHERE spec_id='alpha' AND break_number='B1'",
    )
    assert rows[0]['scope'] == 'agent'


def test_lineage_witness_without_seed_falls_back():
    """lineage_witness() with check_self_hosting=False writes directly
    to lineages (legacy path)."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    cat.introduce_object('alpha', 'Alpha')
    cat.introduce_object('beta', 'Beta')
    cat.lineage_witness('beta', 'alpha', 'descended-from',
                        notes='legacy path')
    rows = cat.query(
        "SELECT notes FROM lineages "
        "WHERE descendant_id='beta' AND ancestor_id='alpha'",
    )
    assert rows[0]['notes'] == 'legacy path'


def test_introduce_break_without_seed_falls_back():
    """introduce_break() with check_self_hosting=False writes directly
    to breaks; axes still write to break_axes."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    cat.introduce_break('B-legacy', 'B-legacy', short_desc='via legacy path',
                        axes=['spatial'])
    rows = cat.query("SELECT short_desc FROM breaks WHERE number='B-legacy'")
    assert rows[0]['short_desc'] == 'via legacy path'
    axis_rows = cat.query(
        "SELECT axis FROM break_axes WHERE break_number='B-legacy'",
    )
    assert axis_rows[0]['axis'] == 'spatial'


def test_introduce_object_with_lineage_via_seed():
    """introduce_object() with seed loaded delegates to introduce_node
    + edge() per lineage entry."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_object('alpha', 'Alpha', year=2000)
    cat.introduce_object(
        'beta', 'Beta', year=2010,
        lineage=[('alpha', 'descended-from')],
        attrs={'vendor': 'Acme'},
    )
    rows = cat.query(
        "SELECT * FROM lineages "
        "WHERE descendant_id='beta' AND ancestor_id='alpha'",
    )
    assert len(rows) == 1
    attr_rows = cat.query(
        "SELECT name, value FROM spec_attributes WHERE spec_id='beta'",
    )
    attrs = {r['name']: r['value'] for r in attr_rows}
    assert attrs.get('vendor') == 'Acme'


def test_introduce_tension_with_seed_and_breaks_involved():
    """introduce_tension() with seed loaded delegates to introduce_node
    plus tension_breaks for each break."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('B1', 'B1', 'break')
    cat.introduce_node('B2', 'B2', 'break')
    cat.introduce_tension('T-x', 'tension', description='d',
                          breaks_involved=['B1', 'B2'])
    rows = cat.query(
        "SELECT break_number FROM tension_breaks WHERE tension_id='T-x' "
        "ORDER BY break_number",
    )
    assert [r['break_number'] for r in rows] == ['B1', 'B2']


def test_refine_without_seed_legacy_only():
    """refine() with check_self_hosting=False writes only to refinements;
    no introduce_node delegation."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    cat.introduce_break('B1', 'B1')
    cat.introduce_object('alpha', 'Alpha')
    cat.refine('B1', 'alpha', 'r1', description='desc')
    rows = cat.query(
        "SELECT name, description FROM refinements WHERE name='r1'",
    )
    assert len(rows) == 1
    # No new break created from refinement-name (legacy path)
    breaks = cat.query("SELECT number FROM breaks WHERE number='r1'")
    assert breaks == []


def test_evaluate_tension_via_catalogue_method():
    """SymmetryCatalogue.evaluate_tension delegates to curry's evaluator."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('F1', 'F1', 'break')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    cat.edge('alpha', 'F1', 'origin')
    t = Tension(
        id='T-x', name='x', description=None, disposition='diagnostic',
        parameters=(),
        shape=KqueryNode(
            a=EdgeReferent(pivot='F1', kinds=('origin',),
                           pivot_role='target', return_role='source'),
            b=LiteralReferent(ids=('alpha',)),
        ),
    )
    cells = cat.evaluate_tension(t)
    assert cells['11'] == ['alpha']


def test_curry_param_resolves_string_to_singleton():
    """Param resolved with a string value yields a singleton list
    (the [str(val)] branch in resolve)."""
    cat = SymmetryCatalogue(':memory:')
    bindings = {'p': 'alpha'}
    result = resolve(Param('p'), cat, bindings)
    assert result == ['alpha']


def test_curry_param_resolves_int_to_singleton_str():
    """Param with non-string non-list value gets stringified."""
    cat = SymmetryCatalogue(':memory:')
    result = resolve(Param('p'), cat, {'p': 42})
    assert result == ['42']


def test_curry_edge_referent_empty_kinds_returns_empty():
    """EdgeReferent with empty kinds tuple short-circuits to []."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('F1', 'F1', 'break')
    er = EdgeReferent(pivot='F1', kinds=(), pivot_role='target',
                      return_role='source')
    assert resolve(er, cat, {}) == []


def test_curry_edge_referent_with_param_pivot():
    """EdgeReferent with Param pivot resolves the binding before query."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('F1', 'F1', 'break')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    cat.edge('alpha', 'F1', 'origin')
    er = EdgeReferent(pivot=Param('B'), kinds=('origin',),
                      pivot_role='target', return_role='source')
    assert resolve(er, cat, {'B': 'F1'}) == ['alpha']


def test_curry_axis_cut_with_param_threshold():
    """AxisCutReferent with Param threshold resolves the binding."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 1990})
    cat.introduce_node('beta', 'Beta', 'spec', attrs={'year': 2010})
    ac = AxisCutReferent(axis_column='year', op='<',
                         threshold=Param('t'))
    result = resolve(ac, cat, {'t': 2000})
    assert 'alpha' in result and 'beta' not in result


def test_curry_axis_cut_with_param_axis_column():
    """AxisCutReferent with Param axis_column resolves the binding."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 1990})
    ac = AxisCutReferent(axis_column=Param('col'), op='<',
                         threshold=2000)
    result = resolve(ac, cat, {'col': 'year'})
    assert 'alpha' in result


def test_curry_axis_cut_rejects_invalid_op():
    """AxisCutReferent.op outside the whitelist raises ValueError."""
    cat = SymmetryCatalogue(':memory:')
    ac = AxisCutReferent(axis_column='year', op='!!', threshold=2000)
    try:
        resolve(ac, cat, {})
    except ValueError as e:
        assert 'op must be one of' in str(e)
    else:
        raise AssertionError('expected ValueError for invalid op')


def test_curry_axis_cut_rejects_unknown_axis_column():
    """AxisCutReferent.axis_column not on specs raises ValueError."""
    cat = SymmetryCatalogue(':memory:')
    ac = AxisCutReferent(axis_column='not_a_col', op='<', threshold=1)
    try:
        resolve(ac, cat, {})
    except ValueError as e:
        assert 'not found on specs' in str(e)
    else:
        raise AssertionError('expected ValueError for unknown axis_column')


def test_curry_resolve_unknown_referent_type_raises():
    """resolve() with a type outside the Referent union raises TypeError."""
    cat = SymmetryCatalogue(':memory:')
    try:
        resolve("not a referent", cat, {})  # type: ignore[arg-type]
    except TypeError as e:
        assert 'unknown Referent type' in str(e)
    else:
        raise AssertionError('expected TypeError')


def test_curry_evaluate_node_with_universe_referent():
    """evaluate_node with a non-None universe referent passes it to kquery."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('F1', 'F1', 'break')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    cat.edge('alpha', 'F1', 'origin')
    node = KqueryNode(
        a=LiteralReferent(ids=('alpha',)),
        b=LiteralReferent(ids=('beta',)),
        universe=LiteralReferent(ids=('alpha', 'beta', 'gamma')),
    )
    t = Tension(id='T', name='T', description=None, disposition='diagnostic',
                parameters=(), shape=node)
    cells = cat.evaluate_tension(t)
    assert 'gamma' in cells['00']


def test_risc_violation_message_contains_payload():
    """RiscDisciplineViolation's str includes its dangling/cyclic
    payloads."""
    err = RiscDisciplineViolation(
        dangling=[('cell-x', 'missing-y')], cyclic=['cell-z'],
    )
    msg = str(err)
    assert 'cell-x' in msg
    assert 'missing-y' in msg
    assert 'cell-z' in msg


def test_check_risc_discipline_skips_self_chain():
    """check_risc_discipline correctly walks chains of length > 1
    (defer → witness → edge → None terminates cleanly)."""
    # The current SIGNATURE has exactly such chains — this test
    # exercises the recurse-into-non-None-derives_from branch.
    check_risc_discipline()  # no exception


def test_curry_param_resolves_list_value_returns_copy():
    """Param with a list binding returns a list copy (the
    `return list(val)` branch)."""
    cat = SymmetryCatalogue(':memory:')
    out = resolve(Param('p'), cat, {'p': ['alpha', 'beta']})
    assert out == ['alpha', 'beta']


def test_introduce_object_legacy_path_records_attrs():
    """introduce_object() with check_self_hosting=False writes attrs
    via the legacy direct INSERT to spec_attributes (line 239-240)."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    cat.introduce_object(
        'alpha', 'Alpha', year=2000,
        attrs={'vendor': 'Acme', 'paradigm': 'imperative'},
    )
    rows = cat.query(
        "SELECT name, value FROM spec_attributes WHERE spec_id='alpha' "
        "ORDER BY name",
    )
    attrs = {r['name']: r['value'] for r in rows}
    assert attrs.get('vendor') == 'Acme'
    assert attrs.get('paradigm') == 'imperative'


def test_lineage_witness_with_seed_delegates_to_edge():
    """lineage_witness() with check_self_hosting=True (default)
    delegates to edge (the if-loaded branch at catalogue.py:770)."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    cat.introduce_node('beta', 'Beta', 'spec', attrs={'year': 2010})
    cat.lineage_witness('beta', 'alpha', 'descended-from')
    rows = cat.query(
        "SELECT * FROM lineages "
        "WHERE descendant_id='beta' AND ancestor_id='alpha'",
    )
    assert len(rows) == 1


def test_check_risc_discipline_doesnt_double_record_cycle():
    """When a cell's derives_from has duplicate references that all
    lead into a cycle, check_risc_discipline records the cell as
    cyclic only once (the `if cell.id not in cyclic` else branch)."""
    # Construct a cell whose derives_from has TWO refs to the same
    # cyclic counterpart. The BFS visits the cycle from both refs;
    # cell.id should be appended to cyclic exactly once.
    a = Cell('cyc-dup-a', Kind.O, 'cyc dup a',
             derives_from=('cyc-dup-b', 'cyc-dup-b'))
    b = Cell('cyc-dup-b', Kind.O, 'cyc dup b',
             derives_from=('cyc-dup-a',))
    SIGNATURE.append(a)
    SIGNATURE.append(b)
    try:
        check_risc_discipline()
    except RiscDisciplineViolation as e:
        # 'cyc-dup-a' should appear exactly once in cyclic, not twice
        assert e.cyclic.count('cyc-dup-a') == 1
    else:
        raise AssertionError('expected RiscDisciplineViolation for cycle')
    finally:
        SIGNATURE.remove(a)
        SIGNATURE.remove(b)


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
    # (β) RISC reframe coverage
    test_introduce_node_default_branch_records_attributes,
    test_introduce_node_default_branch_with_explicit_catalogue_order,
    test_edge_unsupported_target_type_raises,
    test_edge_lineage_kind_with_notes,
    test_attr_key_for_break_returns_none_for_non_kattr,
    test_attr_key_for_break_handles_dashes,
    test_node_type_attrs_skips_non_kattr_break,
    test_kind_source_type_returns_none_for_uncatalogued_kind,
    test_witness_with_agent_scope_writes_directly,
    test_lineage_witness_without_seed_falls_back,
    test_introduce_break_without_seed_falls_back,
    test_introduce_object_with_lineage_via_seed,
    test_introduce_tension_with_seed_and_breaks_involved,
    test_refine_without_seed_legacy_only,
    test_evaluate_tension_via_catalogue_method,
    test_curry_param_resolves_string_to_singleton,
    test_curry_param_resolves_int_to_singleton_str,
    test_curry_edge_referent_empty_kinds_returns_empty,
    test_curry_edge_referent_with_param_pivot,
    test_curry_axis_cut_with_param_threshold,
    test_curry_axis_cut_with_param_axis_column,
    test_curry_axis_cut_rejects_invalid_op,
    test_curry_axis_cut_rejects_unknown_axis_column,
    test_curry_resolve_unknown_referent_type_raises,
    test_curry_evaluate_node_with_universe_referent,
    test_risc_violation_message_contains_payload,
    test_check_risc_discipline_skips_self_chain,
    test_curry_param_resolves_list_value_returns_copy,
    test_introduce_object_legacy_path_records_attrs,
    test_lineage_witness_with_seed_delegates_to_edge,
    test_check_risc_discipline_doesnt_double_record_cycle,
]

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
    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
