"""
Tests for the curry.py rename + new geometric-currying referents.

Closes v4cat#9 (gc-v4cat-curry-rename). Verifies:
  - CellReferent is a deprecated alias for KqueryCellReferent
  - EventCellReferent resolves to occupants of one role given another
  - RoleHornReferent resolves to the open horn of a partial cell
  - BoundaryClosureReferent filters EdgeCells by closure_state
"""
from __future__ import annotations

import pytest

from v4cat import event_cells
from v4cat.catalogue import SymmetryCatalogue
from v4cat.curry import (
    BoundaryClosureReferent,
    CellReferent,
    EventCellReferent,
    KqueryCellReferent,
    RoleHornReferent,
    resolve,
)


@pytest.fixture
def cat() -> SymmetryCatalogue:
    with SymmetryCatalogue(':memory:', check_self_hosting=True) as c:
        yield c


def test_cell_referent_alias_is_kquery_cell_referent():
    """The deprecated CellReferent name must be the KqueryCellReferent class."""
    assert CellReferent is KqueryCellReferent


def test_event_cell_referent_resolves(cat):
    # Build a closed EdgeCell manually via the cell layer.
    event_cells.introduce_cell(cat.conn, 'cell:e1', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:e1', 'source', 'a')
    event_cells.bind_role(cat.conn, 'cell:e1', 'kind',   'k')
    event_cells.bind_role(cat.conn, 'cell:e1', 'target', 'b')
    event_cells.close_boundary(cat.conn, 'cell:e1')
    event_cells.close_cell(cat.conn, 'cell:e1')

    # Build another closed EdgeCell sharing the target.
    event_cells.introduce_cell(cat.conn, 'cell:e2', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:e2', 'source', 'c')
    event_cells.bind_role(cat.conn, 'cell:e2', 'kind',   'k2')
    event_cells.bind_role(cat.conn, 'cell:e2', 'target', 'b')
    event_cells.close_boundary(cat.conn, 'cell:e2')
    event_cells.close_cell(cat.conn, 'cell:e2')

    # Sources of edges with target=b: should yield {a, c}.
    ref = EventCellReferent(
        pivot_role='target', pivot_id='b', return_role='source',
    )
    result = sorted(resolve(ref, cat, bindings={}))
    assert result == ['a', 'c']


def test_event_cell_referent_filters_by_closure_state(cat):
    """An open cell must NOT contribute occupants."""
    event_cells.introduce_cell(cat.conn, 'cell:open', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:open', 'source', 'x')
    event_cells.bind_role(cat.conn, 'cell:open', 'kind',   'k')
    # target unbound — boundary stays open
    ref = EventCellReferent(
        pivot_role='source', pivot_id='x', return_role='kind',
    )
    assert resolve(ref, cat, bindings={}) == []


def test_role_horn_referent_returns_unbound_roles(cat):
    event_cells.introduce_cell(cat.conn, 'cell:partial', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:partial', 'source', 'a')
    event_cells.bind_role(cat.conn, 'cell:partial', 'kind',   'k')
    # target unbound

    ref = RoleHornReferent(cell_id='cell:partial')
    assert sorted(resolve(ref, cat, bindings={})) == ['target']


def test_role_horn_referent_empty_when_fully_closed(cat):
    event_cells.introduce_cell(cat.conn, 'cell:full', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:full', 'source', 'a')
    event_cells.bind_role(cat.conn, 'cell:full', 'kind',   'k')
    event_cells.bind_role(cat.conn, 'cell:full', 'target', 'b')

    ref = RoleHornReferent(cell_id='cell:full')
    assert resolve(ref, cat, bindings={}) == []


def test_boundary_closure_referent_filters_by_state(cat):
    event_cells.introduce_cell(cat.conn, 'cell:o1', 'EdgeCell')  # open
    event_cells.introduce_cell(cat.conn, 'cell:o2', 'EdgeCell')  # open

    event_cells.introduce_cell(cat.conn, 'cell:c1', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:c1', 'source', 'a')
    event_cells.bind_role(cat.conn, 'cell:c1', 'kind',   'k')
    event_cells.bind_role(cat.conn, 'cell:c1', 'target', 'b')
    event_cells.close_boundary(cat.conn, 'cell:c1')
    event_cells.close_cell(cat.conn, 'cell:c1')

    open_cells = sorted(resolve(
        BoundaryClosureReferent(closure_state='open'), cat, bindings={},
    ))
    closed_cells = sorted(resolve(
        BoundaryClosureReferent(closure_state='closed'), cat, bindings={},
    ))
    # Cells from prior introduce_node tests may also be present;
    # filter to the test-prefixed ones.
    open_test = [c for c in open_cells if c.startswith('cell:o')]
    closed_test = [c for c in closed_cells if c.startswith('cell:c')]
    assert open_test == ['cell:o1', 'cell:o2']
    assert closed_test == ['cell:c1']
