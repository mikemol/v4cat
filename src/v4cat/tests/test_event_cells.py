"""
Tests for v4cat.event_cells — the geometric-currying RISC primitives.

Closes v4cat#6 (gc-v4cat-cells-module). Verifies:
  - the five primitives behave as documented in
    cotype/shadow_geometric_currying.md
  - public introduce_node + edge redirects route through the cell
    layer (every node has a NodeCell, every edge has an EdgeCell)
  - legacy witnesses + lineages projections still land for
    backwards-compatible consumers
"""
from __future__ import annotations

import pytest

from v4cat import event_cells
from v4cat.catalogue import SymmetryCatalogue


# ---------------------------------------------------------------------------
# Primitives in isolation (don't need a full catalogue)
# ---------------------------------------------------------------------------

@pytest.fixture
def cat() -> SymmetryCatalogue:
    """A bootstrapped catalogue (so the cells / role_bindings tables exist)."""
    with SymmetryCatalogue(':memory:', check_self_hosting=True) as c:
        yield c


def test_introduce_cell_idempotent(cat):
    event_cells.introduce_cell(cat.conn, 'cell:test', 'EdgeCell')
    event_cells.introduce_cell(cat.conn, 'cell:test', 'EdgeCell')
    rows = list(cat.conn.execute("SELECT * FROM cells WHERE id = 'cell:test'"))
    assert len(rows) == 1


def test_bind_role_idempotent_on_match(cat):
    event_cells.introduce_cell(cat.conn, 'cell:t', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:t', 'source', 'a')
    event_cells.bind_role(cat.conn, 'cell:t', 'source', 'a')  # no-op
    rows = list(cat.conn.execute(
        "SELECT * FROM role_bindings WHERE cell_id = 'cell:t'"
    ))
    assert len(rows) == 1


def test_bind_role_raises_on_conflict(cat):
    event_cells.introduce_cell(cat.conn, 'cell:t', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:t', 'source', 'a')
    with pytest.raises(ValueError, match='conflict'):
        event_cells.bind_role(cat.conn, 'cell:t', 'source', 'b')


def test_close_boundary_returns_true_when_all_three_roles_bound(cat):
    event_cells.introduce_cell(cat.conn, 'cell:e1', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:e1', 'source', 'a')
    event_cells.bind_role(cat.conn, 'cell:e1', 'kind',   'k')
    event_cells.bind_role(cat.conn, 'cell:e1', 'target', 'b')
    assert event_cells.close_boundary(cat.conn, 'cell:e1') is True
    state = cat.conn.execute(
        "SELECT closure_state FROM cells WHERE id = 'cell:e1'"
    ).fetchone()
    assert state[0] == 'boundary-closed'


def test_close_boundary_returns_false_when_role_missing(cat):
    event_cells.introduce_cell(cat.conn, 'cell:e2', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:e2', 'source', 'a')
    event_cells.bind_role(cat.conn, 'cell:e2', 'kind',   'k')
    # target unbound
    assert event_cells.close_boundary(cat.conn, 'cell:e2') is False


def test_close_cell_no_op_when_boundary_open(cat):
    event_cells.introduce_cell(cat.conn, 'cell:open', 'EdgeCell')
    event_cells.close_cell(cat.conn, 'cell:open')  # no-op
    state = cat.conn.execute(
        "SELECT closure_state FROM cells WHERE id = 'cell:open'"
    ).fetchone()[0]
    assert state == 'open'


def test_close_cell_advances_to_closed_when_boundary_closed(cat):
    event_cells.introduce_cell(cat.conn, 'cell:e3', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:e3', 'source', 'a')
    event_cells.bind_role(cat.conn, 'cell:e3', 'kind',   'k')
    event_cells.bind_role(cat.conn, 'cell:e3', 'target', 'b')
    event_cells.close_boundary(cat.conn, 'cell:e3')
    event_cells.close_cell(cat.conn, 'cell:e3')
    state = cat.conn.execute(
        "SELECT closure_state FROM cells WHERE id = 'cell:e3'"
    ).fetchone()[0]
    assert state == 'closed'


def test_advance_path_raises_when_cell_open(cat):
    event_cells.introduce_cell(cat.conn, 'cell:open2', 'EdgeCell')
    with pytest.raises(ValueError, match='boundary-closure-before-traversal'):
        event_cells.advance_path(cat.conn, 'path:p1', 'cell:open2')


def test_advance_path_succeeds_when_cell_closed(cat):
    event_cells.introduce_cell(cat.conn, 'cell:closed', 'EdgeCell')
    event_cells.bind_role(cat.conn, 'cell:closed', 'source', 'a')
    event_cells.bind_role(cat.conn, 'cell:closed', 'kind',   'k')
    event_cells.bind_role(cat.conn, 'cell:closed', 'target', 'b')
    event_cells.close_boundary(cat.conn, 'cell:closed')
    event_cells.close_cell(cat.conn, 'cell:closed')
    idx = event_cells.advance_path(cat.conn, 'path:p1', 'cell:closed')
    assert idx == 0
    idx2 = event_cells.advance_path(cat.conn, 'path:p1', 'cell:closed')
    assert idx2 == 1


def test_edge_cell_id_is_deterministic():
    a = event_cells.edge_cell_id('s', 'k', 't')
    b = event_cells.edge_cell_id('s', 'k', 't')
    assert a == b
    c = event_cells.edge_cell_id('s', 'k', 'u')
    assert a != c


# ---------------------------------------------------------------------------
# Public-API redirects
# ---------------------------------------------------------------------------

def test_introduce_node_public_api_creates_node_cell(cat):
    cat.introduce_node('test:foo', 'foo', 'spec')
    cell_id = event_cells.node_cell_id('test:foo')
    row = cat.conn.execute(
        "SELECT closure_state FROM cells WHERE id = ?", (cell_id,)
    ).fetchone()
    assert row is not None
    assert row[0] == 'closed'  # 0-cells close trivially

    rb = [tuple(r) for r in cat.conn.execute(
        "SELECT role, occupant_id FROM role_bindings WHERE cell_id = ?",
        (cell_id,),
    )]
    assert rb == [('self', 'test:foo')]


def test_edge_public_api_creates_edge_cell_with_three_role_bindings(cat):
    # Use a pre-catalogued spec→break edge-kind ('catalogue-introduces').
    cat.introduce_break('TEST-1', 'test break')
    cat.introduce_node('test:agent', 'test agent', 'spec')
    cat.edge('test:agent', 'TEST-1', 'catalogue-introduces')

    cell_id = event_cells.edge_cell_id(
        'test:agent', 'catalogue-introduces', 'TEST-1'
    )
    state = cat.conn.execute(
        "SELECT closure_state FROM cells WHERE id = ?", (cell_id,)
    ).fetchone()
    assert state is not None and state[0] == 'closed'

    bindings = sorted(tuple(r) for r in cat.conn.execute(
        "SELECT role, occupant_id FROM role_bindings WHERE cell_id = ?",
        (cell_id,),
    ))
    assert bindings == [
        ('kind',   'catalogue-introduces'),
        ('source', 'test:agent'),
        ('target', 'TEST-1'),
    ]


def test_legacy_witnesses_row_still_present(cat):
    """The geometric-currying landing must NOT remove legacy projections."""
    cat.introduce_break('TEST-2', 'test break 2')
    cat.introduce_node('test:agent2', 'test agent 2', 'spec')
    cat.edge('test:agent2', 'TEST-2', 'catalogue-introduces')

    rows = [tuple(r) for r in cat.conn.execute(
        "SELECT spec_id, break_number, kind FROM witnesses "
        "WHERE spec_id = 'test:agent2'"
    )]
    assert len(rows) == 1
    assert rows[0][0] == 'test:agent2'
    assert rows[0][1] == 'TEST-2'
    assert rows[0][2] == 'catalogue-introduces'
