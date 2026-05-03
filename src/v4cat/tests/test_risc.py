"""
Tests for the (β) RISC primitives — introduce_node, edge,
evaluate_tension — and the curry-spec algebra.

Per cotype/shadow_migration_02_risc_dispatch.md (S₂ green-light
criterion), the RISC primitives must:

  * introduce_node dispatches to the right physical table by type
  * introduce_node validates type is catalogued and attrs satisfy
    the catalogued attribute-schema
  * edge dispatches to witnesses or lineages by the kind's
    catalogued target-type
  * edge validates kind is catalogued
  * Both raise RuntimeError when the type-system seed isn't loaded
  * evaluate_tension correctly walks the curry-spec AST and runs
    kquery against the catalogue's witness graph

These tests exercise each invariant directly.
"""
from __future__ import annotations

import sys
import traceback

from v4cat import SymmetryCatalogue
from v4cat.curry import (
    AxisCutReferent, CellReferent, EdgeReferent,
    KqueryNode, LiteralReferent, Param, Tension,
    evaluate_tension,
)


# ============================================================
# introduce_node — dispatch + validation
# ============================================================

def test_introduce_node_break_writes_to_breaks_table():
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('F1', 'Break one', 'break',
                       attrs={'short_desc': 'foo'})
    rows = cat.query("SELECT * FROM breaks WHERE number = 'F1'")
    assert len(rows) == 1
    assert rows[0]['name'] == 'Break one'
    assert rows[0]['short_desc'] == 'foo'


def test_introduce_node_spec_writes_to_specs_table():
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('alpha', 'Alpha', 'spec',
                       attrs={'year': 2020})
    rows = cat.query("SELECT * FROM specs WHERE id = 'alpha'")
    assert len(rows) == 1
    assert rows[0]['name'] == 'Alpha'
    assert rows[0]['year'] == 2020


def test_introduce_node_spec_auto_assigns_catalogue_order():
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('a', 'A', 'spec', attrs={'year': 2000})
    cat.introduce_node('b', 'B', 'spec', attrs={'year': 2001})
    rows = {r['id']: r for r in cat.query(
        "SELECT id, catalogue_order FROM specs WHERE id IN ('a','b')"
    )}
    # Both get assigned non-NULL catalogue_orders, monotonically
    assert rows['a']['catalogue_order'] is not None
    assert rows['b']['catalogue_order'] is not None
    assert rows['b']['catalogue_order'] > rows['a']['catalogue_order']


def test_introduce_node_rejects_unknown_type():
    cat = SymmetryCatalogue(':memory:')
    try:
        cat.introduce_node('x', 'X', 'mythical-type-not-in-seed')
    except ValueError as e:
        assert 'unknown node-type' in str(e)
    else:
        raise AssertionError('expected ValueError')


def test_introduce_node_rejects_missing_required_attr():
    """'tension' type requires 'disposition' and 'shape'.
    'id' / 'name' are top-level params; missing them isn't a ValueError
    in the introduce_node API (they're positional). But required attrs
    in the attrs dict are validated.
    """
    cat = SymmetryCatalogue(':memory:')
    try:
        # 'tension' requires shape and disposition; we provide neither
        cat.introduce_node('T1', 'Tension one', 'tension', attrs={})
    except ValueError as e:
        msg = str(e)
        # Either 'shape' or 'disposition' (whichever is missing first)
        assert 'requires attrs' in msg
    else:
        raise AssertionError('expected ValueError for missing required attrs')


def test_introduce_node_rejects_unknown_attrs_for_closed_types():
    """Closed-schema types ('break', 'tension') reject unknown attrs.
    Spec-style types ('spec', 'node-type', 'edge-kind', domain types)
    accept extras — they flow to spec_attributes."""
    cat = SymmetryCatalogue(':memory:')
    # 'break' is closed — unknown attr rejected
    try:
        cat.introduce_node('F1', 'Break', 'break',
                           attrs={'wibble': 'wobble'})
    except ValueError as e:
        assert "doesn't admit attrs" in str(e)
    else:
        raise AssertionError('expected ValueError for unknown attrs on break')

    # 'spec' is open — unknown attr accepted, lands in spec_attributes
    cat.introduce_node('alpha', 'Alpha', 'spec',
                       attrs={'wibble': 'wobble', 'year': 2000})
    rows = cat.query(
        "SELECT name, value FROM spec_attributes WHERE spec_id = 'alpha'"
    )
    attrs = {r['name']: r['value'] for r in rows}
    assert attrs.get('wibble') == 'wobble'


def test_introduce_node_requires_seed():
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    try:
        cat.introduce_node('F1', 'Break', 'break')
    except RuntimeError as e:
        assert 'type-system seed' in str(e)
    else:
        raise AssertionError('expected RuntimeError without seed')


# ============================================================
# edge — dispatch + validation
# ============================================================

def test_edge_witness_kind_writes_to_witnesses_table():
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('F1', 'Break one', 'break')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    cat.edge('alpha', 'F1', 'origin')
    rows = cat.query(
        "SELECT * FROM witnesses "
        "WHERE spec_id = 'alpha' AND break_number = 'F1'"
    )
    assert len(rows) == 1
    assert rows[0]['kind'] == 'origin'


def test_edge_lineage_kind_writes_to_lineages_table():
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    cat.introduce_node('beta',  'Beta',  'spec', attrs={'year': 2010})
    cat.edge('beta', 'alpha', 'descended-from')
    rows = cat.query(
        "SELECT * FROM lineages "
        "WHERE descendant_id = 'beta' AND ancestor_id = 'alpha'"
    )
    assert len(rows) == 1
    assert rows[0]['kind'] == 'descended-from'


def test_edge_rejects_uncatalogued_kind():
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_node('F1', 'Break', 'break')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    try:
        cat.edge('alpha', 'F1', 'mythical-kind-not-catalogued')
    except ValueError as e:
        assert 'not catalogued' in str(e)
    else:
        raise AssertionError('expected ValueError for unknown kind')


def test_edge_requires_seed():
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    try:
        cat.edge('a', 'b', 'origin')
    except RuntimeError as e:
        assert 'type-system seed' in str(e)
    else:
        raise AssertionError('expected RuntimeError without seed')


# ============================================================
# evaluate_tension — curry-spec evaluator
# ============================================================

def _populate(cat):
    """Populate a small catalogue for tension-evaluation tests."""
    cat.introduce_node('F1', 'Break one',  'break')
    cat.introduce_node('F2', 'Break two',  'break')
    cat.introduce_node('alpha', 'Alpha', 'spec', attrs={'year': 2000})
    cat.introduce_node('beta',  'Beta',  'spec', attrs={'year': 2010})
    cat.introduce_node('gamma', 'Gamma', 'spec', attrs={'year': 2020})
    cat.edge('alpha', 'F1', 'origin')
    cat.edge('beta',  'F1', 'confirms')
    cat.edge('gamma', 'F2', 'origin')
    cat.commit()


def test_evaluate_tension_simple_intersection():
    cat = SymmetryCatalogue(':memory:')
    _populate(cat)

    # Tension: (specs witnessing F1 with origin/confirms,
    #           specs witnessing F2 with origin)
    # 11 cell = both — should be empty (alpha and beta witness F1; gamma F2)
    # 10 cell = F1 only — alpha, beta
    # 01 cell = F2 only — gamma
    t = Tension(
        id='T-test',
        name='Test tension',
        description=None,
        disposition='diagnostic',
        parameters=(),
        shape=KqueryNode(
            a=EdgeReferent(
                pivot='F1', kinds=('origin', 'confirms'),
                pivot_role='target', return_role='source',
            ),
            b=EdgeReferent(
                pivot='F2', kinds=('origin',),
                pivot_role='target', return_role='source',
            ),
        ),
    )
    cells = evaluate_tension(t, cat)
    assert sorted(cells['10']) == ['alpha', 'beta']
    assert sorted(cells['01']) == ['gamma']
    assert cells['11'] == []


def test_evaluate_tension_axis_cut():
    cat = SymmetryCatalogue(':memory:')
    _populate(cat)

    # Tension: (origin-witnesses on F1) ∩ (specs with year < 2005)
    # alpha (2000) is the only origin-witness on F1, and only one with year<2005
    t = Tension(
        id='T-axis',
        name='Axis-cut test',
        description=None,
        disposition='utility',
        parameters=('B', 't'),
        shape=KqueryNode(
            a=EdgeReferent(
                pivot=Param('B'),
                kinds=('origin', 'catalogue-introduces'),
                pivot_role='target', return_role='source',
            ),
            b=AxisCutReferent(
                axis_column='year', op='<', threshold=Param('t'),
            ),
        ),
    )
    cells = evaluate_tension(t, cat, B='F1', t=2005)
    assert cells['11'] == ['alpha']
    # 'beta' is NOT an origin-witness on F1 (it's confirms) so not in 10/11
    # 'beta' is in 01? Year 2010 is not < 2005, so not in 01 either
    # gamma year 2020 not < 2005


def test_evaluate_tension_cell_projection():
    """Composed tension: project one kquery's cell into another's input."""
    cat = SymmetryCatalogue(':memory:')
    _populate(cat)

    # Outer kquery: (F1-witnesses, year < 2015) ∩ literal {beta, gamma}
    # F1 witnesses (any kind): alpha, beta. With year<2015: alpha, beta both
    # Inner 11 cell = alpha, beta
    # Outer: cell('11', inner) ∩ literal {beta, gamma} = beta (intersection)
    inner = KqueryNode(
        a=EdgeReferent(
            pivot='F1', kinds=('origin', 'confirms'),
            pivot_role='target', return_role='source',
        ),
        b=AxisCutReferent(
            axis_column='year', op='<', threshold=2015,
        ),
    )
    outer = Tension(
        id='T-compose',
        name='Composed test',
        description=None,
        disposition='diagnostic',
        parameters=(),
        shape=KqueryNode(
            a=CellReferent(sub=inner, cell='11'),
            b=LiteralReferent(ids=('beta', 'gamma')),
        ),
    )
    cells = evaluate_tension(outer, cat)
    assert cells['11'] == ['beta']
    assert sorted(cells['10']) == ['alpha']
    assert cells['01'] == ['gamma']


def test_evaluate_tension_missing_param_raises():
    cat = SymmetryCatalogue(':memory:')
    _populate(cat)
    t = Tension(
        id='T-p', name='P', description=None, disposition='utility',
        parameters=('X',),
        shape=KqueryNode(
            a=EdgeReferent(
                pivot=Param('X'), kinds=('origin',),
                pivot_role='target', return_role='source',
            ),
            b=LiteralReferent(ids=()),
        ),
    )
    try:
        evaluate_tension(t, cat)  # missing X
    except ValueError as e:
        assert 'missing parameter bindings' in str(e)
    else:
        raise AssertionError('expected ValueError for missing param')


# ============================================================
# Test harness (matches existing convention)
# ============================================================

ALL_TESTS = [
    test_introduce_node_break_writes_to_breaks_table,
    test_introduce_node_spec_writes_to_specs_table,
    test_introduce_node_spec_auto_assigns_catalogue_order,
    test_introduce_node_rejects_unknown_type,
    test_introduce_node_rejects_missing_required_attr,
    test_introduce_node_rejects_unknown_attrs_for_closed_types,
    test_introduce_node_requires_seed,
    test_edge_witness_kind_writes_to_witnesses_table,
    test_edge_lineage_kind_writes_to_lineages_table,
    test_edge_rejects_uncatalogued_kind,
    test_edge_requires_seed,
    test_evaluate_tension_simple_intersection,
    test_evaluate_tension_axis_cut,
    test_evaluate_tension_cell_projection,
    test_evaluate_tension_missing_param_raises,
]


def main() -> int:
    passed = 0
    failed = 0
    for test in ALL_TESTS:
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
