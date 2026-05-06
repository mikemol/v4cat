"""
Tests for the four HF-GeometricCurrying closure recognizers
(T-* tensions) catalogued in framework_seed.sql.

Closes v4cat#8 (gc-v4cat-closure-recognizers). Verifies:
  - all four T-* tensions are catalogued
  - each is a 'diagnostic' tension
  - each has a non-empty parameters_json + shape_json
  - the shape_json deserialises to valid JSON with the expected
    structural shape (type='kquery'; a, b, universe present;
    diagnostic_cell named)
  - tension_breaks links each to the umbrella break
"""
from __future__ import annotations

import json

import pytest

from v4cat.catalogue import SymmetryCatalogue


T_TENSIONS = [
    'T-edge-boundary-closure',
    'T-edge-projection-backed-by-cell',
    'T-path-advance-only-through-closed-cells',
    'T-path-presentation-closure',
]


@pytest.fixture
def cat() -> SymmetryCatalogue:
    with SymmetryCatalogue(':memory:', check_self_hosting=True) as c:
        yield c


def test_all_four_T_tensions_loaded(cat):
    for tid in T_TENSIONS:
        row = cat.conn.execute(
            "SELECT id, disposition FROM tensions WHERE id = ?",
            (tid,),
        ).fetchone()
        assert row is not None, f"tension {tid!r} missing"
        assert row[1] == 'diagnostic'


def test_T_tension_shape_json_is_well_formed(cat):
    for tid in T_TENSIONS:
        row = cat.conn.execute(
            "SELECT shape_json FROM tensions WHERE id = ?", (tid,)
        ).fetchone()
        assert row is not None
        shape = json.loads(row[0])
        assert shape.get('type') == 'kquery', (
            f"tension {tid!r} shape_json must be a kquery node"
        )
        assert 'a' in shape
        assert 'b' in shape
        assert 'universe' in shape
        assert 'diagnostic_cell' in shape
        assert shape['diagnostic_cell'] in ('00', '01', '10', '11')


def test_T_tension_parameters_json_is_list(cat):
    for tid in T_TENSIONS:
        row = cat.conn.execute(
            "SELECT parameters_json FROM tensions WHERE id = ?", (tid,)
        ).fetchone()
        params = json.loads(row[0])
        assert isinstance(params, list)


def test_T_tensions_linked_to_umbrella_break(cat):
    for tid in T_TENSIONS:
        row = cat.conn.execute(
            "SELECT break_number FROM tension_breaks WHERE tension_id = ?",
            (tid,),
        ).fetchone()
        assert row is not None and row[0] == 'Q-geometric-currying-vocabulary'


def test_T_edge_boundary_closure_diagnostic_cell_is_01(cat):
    """Per the central shadow's boundary-closure cover, c01 ⟺ open boundary."""
    row = cat.conn.execute(
        "SELECT shape_json FROM tensions WHERE id = 'T-edge-boundary-closure'"
    ).fetchone()
    shape = json.loads(row[0])
    assert shape['diagnostic_cell'] == '01'
