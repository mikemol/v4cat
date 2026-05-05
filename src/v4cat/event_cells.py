"""
v4cat.event_cells — geometric-currying RISC primitives.

Per ``cotype/shadow_geometric_currying.md``, the new semantic
substrate beneath the existing RISC projection: edges are not
typed relation rows but **closed event-cells whose boundary
contains three role obligations** (source / kind / target).

This module exposes five primitive functions over an open SQLite
connection. They operate on three new tables (``cells``,
``role_bindings``, ``path_steps``) added in ``schema.sql`` § S13.

**Naming caveat**. ``v4cat.cells`` already exists for a different
concept — the 8-way kind partition (Definition 14.1, ``Kind`` enum
with values O / B / W / R / E / A / K / X). The geometric event-cells
named here are a *third* meaning of "cell" alongside (1) the kquery
cell (``KqueryCellReferent``) and (2) the kind-stratification cell
(``v4cat.cells.Cell``). The disambiguation is recorded in
``shadow_geometric_currying.md`` § "Disambiguation: cell".

This module is named ``event_cells`` to avoid the filename collision.
The shadow refers to the new module as "the cells layer"; in code
the import is ``from v4cat import event_cells``.
"""
from __future__ import annotations

import hashlib
import sqlite3
from typing import Optional


# ---------------------------------------------------------------------------
# Cell-id derivation
# ---------------------------------------------------------------------------

def edge_cell_id(src: str, kind: str, tgt: str) -> str:
    """Content-addressed id for an edge-cell over (src, kind, tgt).

    SHA1-12 keeps cell IDs short and deterministic; collision risk is
    negligible for workspace scales (<1M edges). The shadow flags this
    as a workspace-level open sub-decision.
    """
    digest = hashlib.sha1(f"{src}|{kind}|{tgt}".encode("utf-8")).hexdigest()
    return f"cell:edge:{digest[:12]}"


def node_cell_id(node_id: str) -> str:
    """Content-addressed id for the trivial 0-cell over a node id.

    Used for the ``introduce_node`` redirect path so every node has a
    corresponding NodeCell that closes immediately on introduction.
    """
    digest = hashlib.sha1(f"node|{node_id}".encode("utf-8")).hexdigest()
    return f"cell:node:{digest[:12]}"


# ---------------------------------------------------------------------------
# RISC primitives
# ---------------------------------------------------------------------------

def introduce_cell(conn: sqlite3.Connection, cell_id: str, cell_kind: str) -> None:
    """Introduce a cell of stated kind. Idempotent on repeat."""
    conn.execute(
        "INSERT OR IGNORE INTO cells (id, cell_kind, closure_state) "
        "VALUES (?, ?, 'open')",
        (cell_id, cell_kind),
    )


def bind_role(
    conn: sqlite3.Connection,
    cell_id: str,
    role: str,
    occupant_id: str,
) -> None:
    """Record a role-binding ``ρ_r(e, x)`` for cell ``e``, role ``r``,
    occupant ``x``.

    Idempotent on repeat with the same occupant. Raises ValueError if
    a different occupant is already bound to the same (cell, role)
    position — role-bindings are functional in the saturating mode.
    """
    cur = conn.execute(
        "SELECT occupant_id FROM role_bindings "
        "WHERE cell_id = ? AND role = ?",
        (cell_id, role),
    )
    row = cur.fetchone()
    if row is not None:
        existing = row[0] if not hasattr(row, "keys") else row["occupant_id"]
        if existing != occupant_id:
            raise ValueError(
                f"role-binding conflict: cell {cell_id!r} role {role!r} "
                f"already bound to {existing!r}, refusing to re-bind to "
                f"{occupant_id!r}"
            )
        return  # idempotent

    conn.execute(
        "INSERT INTO role_bindings "
        "(cell_id, role, occupant_id, closure_state) "
        "VALUES (?, ?, ?, 'closed')",
        (cell_id, role, occupant_id),
    )


def close_boundary(conn: sqlite3.Connection, cell_id: str) -> bool:
    """Check whether a cell's boundary is closed (all required role-
    bindings present). If so, advance the cell's closure_state from
    ``'open'`` to ``'boundary-closed'``. Return True iff the boundary
    is now closed.

    A cell is *boundary-closed* iff it has all required role-bindings.
    For an EdgeCell this means all three of source / kind / target.
    For a NodeCell this means the single ``self`` role.

    Idempotent: calling on an already-boundary-closed-or-closed cell
    returns True without further writes.
    """
    cur = conn.execute(
        "SELECT cell_kind, closure_state FROM cells WHERE id = ?",
        (cell_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"unknown cell {cell_id!r}")
    cell_kind = row[0] if not hasattr(row, "keys") else row["cell_kind"]
    closure_state = row[1] if not hasattr(row, "keys") else row["closure_state"]

    if closure_state in ("boundary-closed", "closed"):
        return True

    required_roles = _required_roles_for(cell_kind)
    cur = conn.execute(
        "SELECT role FROM role_bindings WHERE cell_id = ?",
        (cell_id,),
    )
    bound_roles = {
        (r[0] if not hasattr(r, "keys") else r["role"])
        for r in cur.fetchall()
    }
    if not required_roles.issubset(bound_roles):
        return False

    conn.execute(
        "UPDATE cells SET closure_state = 'boundary-closed' WHERE id = ?",
        (cell_id,),
    )
    return True


def close_cell(conn: sqlite3.Connection, cell_id: str) -> None:
    """Mark a cell as ``'closed'`` if its boundary is closed.

    No-op if the boundary isn't closed — the saturating-mode public
    API can call this speculatively after ``edge()`` writes.
    """
    cur = conn.execute(
        "SELECT closure_state FROM cells WHERE id = ?",
        (cell_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"unknown cell {cell_id!r}")
    state = row[0] if not hasattr(row, "keys") else row["closure_state"]

    if state == "closed":
        return  # idempotent
    if state != "boundary-closed":
        return  # boundary not yet closed; cell stays open
    conn.execute(
        "UPDATE cells SET closure_state = 'closed' WHERE id = ?",
        (cell_id,),
    )


def advance_path(
    conn: sqlite3.Connection,
    path_id: str,
    cell_id: str,
) -> int:
    """Append a step to a path. Precondition: the cell is closed
    (per the boundary-closure-before-traversal law from
    ``shadow_geometric_currying.md``). Returns the new step_index.
    """
    cur = conn.execute(
        "SELECT closure_state FROM cells WHERE id = ?",
        (cell_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"unknown cell {cell_id!r}")
    state = row[0] if not hasattr(row, "keys") else row["closure_state"]
    if state != "closed":
        raise ValueError(
            f"cannot advance path {path_id!r} through cell {cell_id!r}: "
            f"closure_state={state!r}; per the boundary-closure-before-"
            f"traversal law, only closed cells admit path advancement"
        )

    cur = conn.execute(
        "SELECT COALESCE(MAX(step_index), -1) + 1 FROM path_steps "
        "WHERE path_id = ?",
        (path_id,),
    )
    next_index = cur.fetchone()[0]

    conn.execute(
        "INSERT INTO path_steps (path_id, step_index, cell_id) "
        "VALUES (?, ?, ?)",
        (path_id, int(next_index), cell_id),
    )
    return int(next_index)


# ---------------------------------------------------------------------------
# Role schemas per cell-kind
# ---------------------------------------------------------------------------

def _required_roles_for(cell_kind: str) -> set[str]:
    """Required role-set per cell-kind, used by close_boundary."""
    if cell_kind == "EdgeCell":
        return {"source", "kind", "target"}
    if cell_kind == "NodeCell":
        return {"self"}
    # Other cell-kinds (Boundary, Path, PathStep, …) don't have a
    # tri-fold role schema in v0.1; their boundary is structurally
    # vacuous (nothing required → empty set ⊆ any set → True).
    return set()
