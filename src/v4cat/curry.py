"""
v4cat.curry — the curry-spec algebra for tensions.

A *tension* is a named curry-spec AST over kquery. The algebra has
exactly three productions: atomic referent, kquery composition (via
cell projection), and parameter (free variable bound at evaluation
time). The output type embeds in the input type — each cell of a
kquery's klein-four partition is itself a referent — which makes the
algebra fixpoint-closed.

See cotype/shadow_risc_core.md (Curry-spec AST section) for the
formal framing.

Usage::

    from v4cat.curry import (
        Tension, KqueryNode, EdgeReferent, AxisCutReferent, Param,
    )
    t = Tension(
        id='Q-break-origin',
        name='Originator',
        description='Earliest origin-class witness on B (axis t)',
        disposition='utility',
        parameters=('B', 'axis_column', 't'),
        shape=KqueryNode(
            a=EdgeReferent(
                pivot=Param('B'),
                kinds=('origin', 'catalogue-introduces'),
                pivot_role='target', return_role='source',
            ),
            b=AxisCutReferent(
                axis_column=Param('axis_column'),
                op='<=', threshold=Param('t'),
            ),
        ),
    )
    cells = evaluate_tension(t, cat, B='F1', axis_column='year', t=1985)
    # cells is a klein-four partition: {'00':[...],'01':...,'10':...,'11':...}
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, Union

if TYPE_CHECKING:
    from .catalogue import SymmetryCatalogue


# =====================================================================
# Parameters (bound at evaluation time)
# =====================================================================

@dataclass(frozen=True)
class Param:
    """Free variable; bound when the tension is evaluated."""
    name: str


# =====================================================================
# Atomic referents (leaves of the AST)
# =====================================================================

@dataclass(frozen=True)
class EdgeReferent:
    """Nodes at one end of edges matching the kind filter, pivoted
    on ``pivot``.

    Under the (β) RISC reframe this single referent type covers both
    spec→break and spec→spec edges; the kind catalogue makes the
    namespace implicit (kinds with catalogued target-type 'break'
    are stored in the witnesses table; target-type 'spec' kinds are
    stored in the lineages table).

    pivot_role / return_role ∈ {'source','target'} pick which end of
    the matched edges to pivot on and which to return.
    """
    pivot:        Union[str, 'Param']
    kinds:        tuple[str, ...]
    pivot_role:   Literal['source', 'target']
    return_role:  Literal['source', 'target']


@dataclass(frozen=True)
class AxisCutReferent:
    """Nodes whose ``axis_column`` value satisfies ``op threshold``.
    ``axis_column`` must be a real column on the specs table.
    """
    axis_column:  Union[str, 'Param']
    op:           Literal['<', '<=', '>', '>=', '=']
    threshold:    Union[int, float, str, 'Param']


@dataclass(frozen=True)
class LiteralReferent:
    """Literal set of node ids — escape hatch for fully-specified
    populations."""
    ids: tuple[str, ...]


# =====================================================================
# Composition (internal AST node)
# =====================================================================

@dataclass(frozen=True)
class CellReferent:
    """Project a cell of a sub-kquery. The composition operator that
    makes the algebra fixpoint-closed: a kquery's output cell becomes
    a referent input to another kquery."""
    sub:  'KqueryNode'
    cell: Literal['00', '01', '10', '11']


# =====================================================================
# Kquery node (the composition operator)
# =====================================================================

Referent = Union[
    EdgeReferent, AxisCutReferent, LiteralReferent,
    CellReferent, Param,
]


@dataclass(frozen=True)
class KqueryNode:
    """A kquery application: ``(a, b, universe?) → KleinFour``.

    ``a`` and ``b`` are referents (possibly themselves CellReferents
    projecting from other KqueryNodes — fixpoint closure). The
    optional ``universe`` referent, when present, bounds the 00 cell
    for shared-blindness reads.
    """
    a:        'Referent'
    b:        'Referent'
    universe: Union['Referent', None] = None


# =====================================================================
# Tension (a named, parameterised KqueryNode)
# =====================================================================

@dataclass(frozen=True)
class Tension:
    """A named curry-spec AST. Tensions span a disposition spectrum:

    - ``concern``    — something to resolve (the original framing)
    - ``utility``    — a regularly-read view (origin, first_seen, status)
    - ``diagnostic`` — a detector for a structural condition
    - ``audit``      — a verification-mode read
    """
    id:           str
    name:         str
    description:  Union[str, None]
    disposition:  Literal['concern', 'utility', 'diagnostic', 'audit']
    parameters:   tuple[str, ...]
    shape:        KqueryNode


# =====================================================================
# Evaluator
# =====================================================================

# Physical-table → (source-column, target-column) mapping for the
# witness and lineage graphs the framework currently maintains. The
# evaluator queries both tables and unions the results; each catalogued
# edge-kind belongs to exactly one graph (by its source-type/target-type
# witnesses), so the other table contributes zero rows for that kind.
_TABLE_SCHEMAS = {
    'witnesses': {'source': 'spec_id',       'target': 'break_number'},
    'lineages':  {'source': 'descendant_id', 'target': 'ancestor_id'},
}


def evaluate_tension(
    tension: 'Tension',
    cat: 'SymmetryCatalogue',
    **bindings: Any,
) -> dict[str, list[str]]:
    """Walk a tension's AST and return its klein-four partition.

    ``bindings`` must cover every name in ``tension.parameters``;
    excess bindings are ignored. Returns
    ``{'00': [...], '01': [...], '10': [...], '11': [...]}``.
    """
    missing = set(tension.parameters) - set(bindings)
    if missing:
        raise ValueError(
            f"missing parameter bindings: {sorted(missing)}; "
            f"required: {sorted(tension.parameters)}"
        )
    return evaluate_node(tension.shape, cat, bindings)


def evaluate_node(
    node: 'KqueryNode',
    cat: 'SymmetryCatalogue',
    bindings: dict[str, Any],
) -> dict[str, list[str]]:
    """Evaluate a KqueryNode against the catalogue and return the
    klein-four partition (all four cells)."""
    a = resolve(node.a, cat, bindings)
    b = resolve(node.b, cat, bindings)
    universe = (
        resolve(node.universe, cat, bindings)
        if node.universe is not None else None
    )
    # Lazy import to avoid circularity (views imports nothing
    # catalogue-related, but this keeps the dependency direction one-way).
    from .views import kquery as _kquery
    return _kquery(a, b, universe=universe)


def resolve(
    referent: 'Referent',
    cat: 'SymmetryCatalogue',
    bindings: dict[str, Any],
) -> list[str]:
    """Resolve a referent to a flat population (list of node ids)."""
    if isinstance(referent, Param):
        val = bindings[referent.name]
        if isinstance(val, list):
            return list(val)
        return [str(val)]
    if isinstance(referent, EdgeReferent):
        return _resolve_edge(referent, cat, bindings)
    if isinstance(referent, AxisCutReferent):
        return _resolve_axis_cut(referent, cat, bindings)
    if isinstance(referent, LiteralReferent):
        return list(referent.ids)
    if isinstance(referent, CellReferent):
        sub_result = evaluate_node(referent.sub, cat, bindings)
        return list(sub_result[referent.cell])
    raise TypeError(
        f"unknown Referent type: {type(referent).__name__!r}"
    )


def _resolve_edge(
    referent: 'EdgeReferent',
    cat: 'SymmetryCatalogue',
    bindings: dict[str, Any],
) -> list[str]:
    """Resolve an EdgeReferent against both witness/lineage tables."""
    pivot = referent.pivot
    if isinstance(pivot, Param):
        pivot = bindings[pivot.name]
    if not referent.kinds:
        return []

    placeholders = ','.join('?' for _ in referent.kinds)
    results: set[str] = set()
    for table, schema in _TABLE_SCHEMAS.items():
        col_pivot = schema[referent.pivot_role]
        col_return = schema[referent.return_role]
        sql = (
            f"SELECT DISTINCT {col_return} FROM {table} "
            f"WHERE {col_pivot} = ? AND kind IN ({placeholders})"
        )
        params = [pivot, *referent.kinds]
        cur = cat.conn.execute(sql, params)
        for row in cur.fetchall():
            # witnesses.{spec_id, break_number} and lineages.{descendant_id,
            # ancestor_id} are all schema-NOT-NULL, so row[col_return] is
            # never NULL. No defensive None-check.
            results.add(row[col_return])
    return sorted(results)


def _resolve_axis_cut(
    referent: 'AxisCutReferent',
    cat: 'SymmetryCatalogue',
    bindings: dict[str, Any],
) -> list[str]:
    """Resolve an AxisCutReferent: specs where axis_column op threshold."""
    axis_column = referent.axis_column
    if isinstance(axis_column, Param):
        axis_column = bindings[axis_column.name]
    threshold = referent.threshold
    if isinstance(threshold, Param):
        threshold = bindings[threshold.name]

    valid_ops = {'<', '<=', '>', '>=', '='}
    if referent.op not in valid_ops:
        raise ValueError(
            f"AxisCutReferent.op must be one of {sorted(valid_ops)}, "
            f"got {referent.op!r}"
        )

    valid_cols = cat._spec_columns()
    if axis_column not in valid_cols:
        raise ValueError(
            f"axis_column {axis_column!r} not found on specs; "
            f"available: {sorted(valid_cols)}"
        )

    # axis_column whitelisted via _spec_columns; op whitelisted above —
    # safe substitution into the SQL.
    sql = (
        f"SELECT id FROM specs "
        f"WHERE {axis_column} IS NOT NULL AND {axis_column} {referent.op} ?"
    )
    cur = cat.conn.execute(sql, (threshold,))
    return sorted(row['id'] for row in cur.fetchall())


__all__ = [
    'Param',
    'EdgeReferent', 'AxisCutReferent', 'LiteralReferent', 'CellReferent',
    'Referent', 'KqueryNode', 'Tension',
    'evaluate_tension', 'evaluate_node', 'resolve',
]
