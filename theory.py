"""
v4cat.theory — the framework's signature, declared as data.

Per theory.md § 14.5.2: this module is *data*, not code. Each
entry declares one primitive operation or break the framework
implements. ``bootstrap.py`` reads :data:`SIGNATURE` at runtime as
the witness referent for the IMPL predicate.

Adding a primitive to the framework is a four-step move:
  1. Implement it (in ``catalogue.py`` / ``views.py`` / ``mcp_server.py``).
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
    # -----------------------------------------------------------------
    # Object-introduction operations (kind O)
    # -----------------------------------------------------------------
    Cell('introduce_object',  Kind.O,
         'Add a witness-object to the catalogue'),
    Cell('introduce_tension', Kind.O,
         'Add a structural tension'),

    # -----------------------------------------------------------------
    # Break-introduction (kind B)
    # -----------------------------------------------------------------
    Cell('introduce_break',   Kind.B,
         'Introduce a new symmetry break'),

    # -----------------------------------------------------------------
    # Witness operations (kind W)
    # -----------------------------------------------------------------
    Cell('witness',           Kind.W,
         'Record a typed (subject, break, kind) edge'),
    Cell('defer',             Kind.W,
         'Witness shorthand for kind=deferred-candidate'),
    Cell('promote',           Kind.W,
         'Witness shorthand for kind=confirms (promotion)'),
    Cell('boundary',          Kind.W,
         'Witness shorthand for kind=sibling-boundary'),

    # -----------------------------------------------------------------
    # Refinement (kind R)
    # -----------------------------------------------------------------
    Cell('refine',            Kind.R,
         'Annotate a (break, spec) edge with a named refinement'),

    # -----------------------------------------------------------------
    # Schema extension (kind E)
    # -----------------------------------------------------------------
    Cell('load_extension',    Kind.E,
         'Load a domain-specific schema/data extension'),

    # -----------------------------------------------------------------
    # Read primitives (kind K)
    # -----------------------------------------------------------------
    Cell('kquery',            Kind.K,
         'Klein-four read classifier (the universal read primitive)'),
    Cell('tropical_min',      Kind.K,
         'Generic tropical-MIN over an ordered column'),
    Cell('tropical_max',      Kind.K,
         'Generic tropical-MAX over an ordered column'),

    # -----------------------------------------------------------------
    # Closure check (kind X)
    # -----------------------------------------------------------------
    Cell('check_closure',     Kind.X,
         'Self-hosting closure check (Theorem 14.5)'),

    # -----------------------------------------------------------------
    # Bootstrap breaks (kind B; recursion clauses 2 and 3 of Def 14.7)
    # -----------------------------------------------------------------
    Cell('Q-supported-claims',  Kind.B,
         'Scope declaration for the closure check'),
    Cell('Q-bootstrap-closure', Kind.B,
         'Preservation theorem of Theorem 14.5'),
]


def by_id() -> dict[str, Cell]:
    """Index :data:`SIGNATURE` by cell id for O(1) lookup."""
    return {c.id: c for c in SIGNATURE}


def by_kind(kind: Kind) -> list[Cell]:
    """Filter :data:`SIGNATURE` to cells of a given kind."""
    return [c for c in SIGNATURE if c.kind == kind]


__all__ = ['SIGNATURE', 'by_id', 'by_kind']
