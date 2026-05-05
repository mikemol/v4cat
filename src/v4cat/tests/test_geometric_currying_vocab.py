"""
Tests for the HF-GeometricCurrying vocabulary additions in
framework_seed.sql.

Closes v4cat#7 (gc-v4cat-vocabulary-seed). Verifies:
  - all 11 new node-kinds are catalogued as type='node-type'
  - all 17 new edge-kinds are catalogued with source-type and
    target-type schema-witnesses
  - introduce_node + edge accept the new kinds
  - the umbrella break 'Q-geometric-currying-vocabulary' is
    catalogued + witnessed
"""
from __future__ import annotations

import pytest

from v4cat.catalogue import SymmetryCatalogue


NODE_KINDS_11 = [
    'Cell', 'NodeCell', 'EdgeCell', 'RoleBinding', 'Boundary',
    'Path', 'PathStep', 'PathPresentation', 'PathSnapshot',
    'ClosureObligation', 'RoleHorn',
]

EDGE_KINDS_17 = [
    'has-cell-kind', 'has-boundary', 'has-role-binding',
    'role-of-cell', 'role-name', 'role-occupant',
    'source-role', 'kind-role', 'target-role',
    'boundary-of', 'closes-role', 'closes-cell',
    'path-advances-through', 'blocked-by-boundary',
    'presents-path', 'snapshot-of', 'projects-as-edge',
]


@pytest.fixture
def cat() -> SymmetryCatalogue:
    with SymmetryCatalogue(':memory:', check_self_hosting=True) as c:
        yield c


def test_all_11_node_kinds_loaded(cat):
    for name in NODE_KINDS_11:
        row = cat.conn.execute(
            "SELECT s.id FROM specs s "
            "JOIN spec_attributes sa ON sa.spec_id = s.id "
            "WHERE s.id = ? AND sa.name = 'type' AND sa.value = 'node-type'",
            (name,),
        ).fetchone()
        assert row is not None, f"node-kind {name!r} missing or wrong type"


def test_all_17_edge_kinds_loaded(cat):
    for name in EDGE_KINDS_17:
        row = cat.conn.execute(
            "SELECT s.id FROM specs s "
            "JOIN spec_attributes sa ON sa.spec_id = s.id "
            "WHERE s.id = ? AND sa.name = 'type' AND sa.value = 'edge-kind'",
            (name,),
        ).fetchone()
        assert row is not None, f"edge-kind {name!r} missing or wrong type"


def test_edge_kinds_have_source_target_types(cat):
    for name in EDGE_KINDS_17:
        attrs = {
            r[0]: r[1]
            for r in cat.conn.execute(
                "SELECT name, value FROM spec_attributes WHERE spec_id = ?",
                (name,),
            )
        }
        assert 'source-type' in attrs, f"{name!r} missing source-type"
        assert 'target-type' in attrs, f"{name!r} missing target-type"


def test_introduce_node_with_new_node_kinds_works(cat):
    # Introduce a node typed as one of the new node-kinds.
    cat.introduce_node('test:cellinst', 'test cell instance', 'EdgeCell')
    row = cat.conn.execute(
        "SELECT value FROM spec_attributes WHERE spec_id = 'test:cellinst' "
        "AND name = 'type'"
    ).fetchone()
    assert row is not None and row[0] == 'EdgeCell'


def test_edge_with_new_edge_kinds_works(cat):
    # The new edge-kinds have spec→spec dispatch (lineages table).
    cat.introduce_node('test:c1', 'cell 1', 'spec')
    cat.introduce_node('test:b1', 'boundary 1', 'spec')
    cat.edge('test:c1', 'test:b1', 'has-boundary')
    row = cat.conn.execute(
        "SELECT descendant_id, ancestor_id, kind FROM lineages "
        "WHERE descendant_id = 'test:c1'"
    ).fetchone()
    assert row is not None
    assert tuple(row) == ('test:c1', 'test:b1', 'has-boundary')


def test_umbrella_break_catalogued_and_witnessed(cat):
    row = cat.conn.execute(
        "SELECT name FROM breaks WHERE number = 'Q-geometric-currying-vocabulary'"
    ).fetchone()
    assert row is not None

    wit = cat.conn.execute(
        "SELECT spec_id FROM witnesses "
        "WHERE break_number = 'Q-geometric-currying-vocabulary' "
        "AND kind = 'catalogue-introduces'"
    ).fetchone()
    assert wit is not None and wit[0] == 'framework'
