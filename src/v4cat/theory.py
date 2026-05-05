"""
v4cat.theory — the framework's signature, declared as data.

Per theory.md § 14.5.2: this module is *data*, not code. Each
entry declares one primitive operation or break the framework
implements. ``bootstrap.py`` reads :data:`SIGNATURE` at runtime as
the witness referent for the IMPL predicate.

Adding a primitive to the framework is a four-step move:
  1. Implement it (in ``catalogue.py`` / ``views.py``; or, for an
     MCP-side primitive, in ``v4cat_mcp.server`` in the v4cat-mcp
     distribution).
  2. Add a Cell for it here.
  3. Catalogue it (a Q-numbered break + witness in ``framework_seed.sql``).
  4. Run the closure check; if green, the move is honest.

Step 1 alone makes the cell *implicit* (gap.10). Step 3 alone
makes it *promissory* (gap.01). Both together, plus this entry,
make it self-hosted (gap = ∅).

Note on the filename: deliberately named ``theory.py`` per
theory.md § 14.5.2 — the file is the runtime referent for IMPL,
distinct from theory.md the design doc. The two coexist.
"""
from __future__ import annotations

from .cells import Cell, Kind


SIGNATURE: list[Cell] = [
    # =================================================================
    # RISC core (β) — derives_from=None
    #
    # Three primitives, irreducible at the framework level.
    # Everything else in this SIGNATURE has a derives_from chain
    # that terminates here. See cotype/shadow_risc_core.md.
    # =================================================================

    Cell('introduce_node',    Kind.O,
         'Universal node introduction (the RISC primitive); '
         'dispatches over catalogued node-type.'),
    Cell('edge',              Kind.W,
         'Universal typed-edge introduction (the RISC primitive); '
         'dispatches over catalogued edge-kind to witnesses or lineages.'),
    Cell('kquery',            Kind.K,
         'Klein-four read classifier (the universal read primitive)'),

    # =================================================================
    # CISC sugar — derives_from references the RISC reductions
    # =================================================================

    # Object-introduction (kind O) sugar
    Cell('introduce_object',  Kind.O,
         'CISC sugar: introduce_node(type=spec) + edge(...) for lineage',
         derives_from=('introduce_node', 'edge')),
    Cell('introduce_tension', Kind.O,
         'CISC sugar: introduce_node(type=tension) with disposition=concern',
         derives_from=('introduce_node',)),

    # Break-introduction (kind B) sugar
    Cell('introduce_break',   Kind.B,
         'CISC sugar: introduce_node(type=break)',
         derives_from=('introduce_node',)),

    # Witness operations (kind W) sugar
    Cell('witness',           Kind.W,
         'CISC sugar: edge(...) with default scope=spec',
         derives_from=('edge',)),
    Cell('lineage_witness',   Kind.W,
         'CISC sugar: edge(...) for spec-spec graph (lineage edges)',
         derives_from=('edge',)),
    Cell('defer',             Kind.W,
         'Orbit-element of witness with kind=deferred-candidate',
         derives_from=('witness',)),
    Cell('promote',           Kind.W,
         'Orbit-element of witness with kind=confirms (promotion)',
         derives_from=('witness',)),
    Cell('boundary',          Kind.W,
         'Orbit-element of witness with kind=sibling-boundary',
         derives_from=('witness',)),

    # Refinement (kind R) sugar — the principal RISC composition
    Cell('refine',            Kind.R,
         'CISC sugar: introduce_node(child-break) + edge(origin) + edge(refines)',
         derives_from=('introduce_node', 'edge')),

    # Schema extension (kind E) — substrate-coupled, not RISC-reducible
    Cell('load_extension',    Kind.E,
         'Load a domain-specific schema/data extension'),

    # Read sugar (kind K) — orbit-elements of kquery sweeps
    Cell('tropical_min',      Kind.K,
         'Orbit-element of kquery: sweep over ordered axis (MIN direction)',
         derives_from=('kquery',)),
    Cell('tropical_max',      Kind.K,
         'Orbit-element of kquery: sweep over ordered axis (MAX direction)',
         derives_from=('kquery',)),

    # =================================================================
    # Closure check (kind X)
    # =================================================================

    Cell('check_closure',     Kind.X,
         'Self-hosting closure check (Theorem 14.5) — strengthened in S₄ '
         'to also verify derives_from chains terminate in RISC cells'),

    # =================================================================
    # Bootstrap breaks (kind B; recursion clauses 2 and 3 of Def 14.7)
    # =================================================================

    Cell('Q-supported-claims',  Kind.B,
         'Scope declaration for the closure check'),
    Cell('Q-bootstrap-closure', Kind.B,
         'Preservation theorem of Theorem 14.5'),

    # =================================================================
    # HF-GeometricCurrying vocabulary (kind B; landed at fire #14)
    # =================================================================

    Cell('Q-geometric-currying-vocabulary', Kind.B,
         'Umbrella break: framework introduces 11 node-kinds + 17 '
         'edge-kinds for the geometric-currying substrate per '
         'cotype/shadow_geometric_currying.md'),
]


def by_id() -> dict[str, Cell]:
    """Index :data:`SIGNATURE` by cell id for O(1) lookup."""
    return {c.id: c for c in SIGNATURE}


def by_kind(kind: Kind) -> list[Cell]:
    """Filter :data:`SIGNATURE` to cells of a given kind."""
    return [c for c in SIGNATURE if c.kind == kind]


__all__ = ['SIGNATURE', 'by_id', 'by_kind']
