"""
v4cat.bootstrap — the self-hosting closure check.

Per theory.md § 14.5.4: implements

    ClosureKQ(K, ◇C) := kquery(IMPL, CAT; ◇C)

where IMPL reads from :mod:`v4cat.theory`'s SIGNATURE and CAT
queries the catalogue's own tables. The check passes iff
``gap = ∅`` (Theorem 14.5).

When the check fails, :class:`SelfHostingViolation` carries the
constructive content of Corollary 14.5.1:

  * ``implicit`` (gap.10) — cells in IMPL but not CAT, the
    *implicit structure* (in code, not catalogued).
  * ``promissory`` (gap.01) — cells in CAT but not IMPL, the
    *promissory notes* (catalogued, not implemented).

These two sets are the precise to-do list for restoring
self-hosting.
"""
from __future__ import annotations

import sqlite3
from typing import Optional, Tuple

from .cells import Cell, Kind
from .theory import SIGNATURE, by_id


# -----------------------------------------------------------------------------
# Exceptions
# -----------------------------------------------------------------------------

class SelfHostingViolation(Exception):
    """Raised when ``check_closure``'s gap is non-empty.

    The exception's payload is ``(implicit, promissory)`` —
    Corollary 14.5.1's to-do list. ``implicit`` lists cells the
    framework's code implements but the catalogue doesn't record;
    ``promissory`` lists cells the catalogue records but the code
    doesn't implement.
    """

    def __init__(self, implicit: list[str], promissory: list[str]):
        self.implicit = list(implicit)
        self.promissory = list(promissory)
        super().__init__(
            f"Self-hosting violated:\n"
            f"  implicit (in IMPL, not in CAT): {sorted(self.implicit)!r}\n"
            f"  promissory (in CAT, not in IMPL): {sorted(self.promissory)!r}\n"
            f"See theory.md § 14.5 and Corollary 14.5.1."
        )


# -----------------------------------------------------------------------------
# IMPL and CAT predicates
# -----------------------------------------------------------------------------

def _catalogue_id_for(cell: Cell) -> str:
    """The catalogue's break-number convention for a signature cell.

    Cells whose id already starts with ``Q-`` (e.g.,
    ``Q-supported-claims``, ``Q-bootstrap-closure``) catalogue
    under that exact id. Other cells (e.g., ``kquery``, ``witness``)
    catalogue under ``Q-{cell.id}``.
    """
    return cell.id if cell.id.startswith('Q-') else f'Q-{cell.id}'


def IMPL(cell: Cell) -> bool:
    """Implementation predicate (Definition 14.4).

    Returns True iff ``cell.id`` appears in the framework's
    signature — i.e., the framework declares this cell as
    implemented.
    """
    return cell.id in by_id()


def CAT(cell: Cell, cat) -> bool:
    """Catalogue predicate (Definition 14.5).

    Returns True iff there exists a Q-numbered break in the
    catalogue with ``number = _catalogue_id_for(cell)`` AND at
    least one witness from any spec.

    "Sufficient witnesses" per Def 14.5 is currently relaxed to
    "at least one witness." A stricter form — requiring a witness
    from the ``framework`` spec specifically, or a refinement
    encoding the preservation theorem — is a future tightening
    recorded in ``Q-bootstrap-closure``'s refinement.
    """
    break_id = _catalogue_id_for(cell)
    rows = cat.query(
        "SELECT 1 FROM breaks b "
        "WHERE b.number = ? "
        "  AND EXISTS (SELECT 1 FROM witnesses w "
        "              WHERE w.break_number = b.number)",
        break_id,
    )
    return len(rows) > 0


# -----------------------------------------------------------------------------
# Scope enumeration
# -----------------------------------------------------------------------------

def supported_kinds(cat) -> set[str]:
    """Read the supported-kinds list from ``Q-supported-claims``.

    Returns the set of single-letter kind codes the catalogue
    claims scope over. Returns an empty set if any of:

      * The catalogue's framework tables (refinements, breaks)
        haven't been bootstrapped (``bootstrap=False``).
      * ``Q-supported-claims`` exists but has no
        ``supported_kinds`` refinement.
      * The break isn't present (non-self-hosting catalogue).

    Empty-set return makes :func:`check_closure` a clean no-op
    in all three cases, which is the right behaviour for
    domain-extension catalogues that aren't claiming framework
    self-hosting.
    """
    try:
        rows = cat.query(
            "SELECT description FROM refinements "
            "WHERE break_number = 'Q-supported-claims' "
            "  AND name = 'supported_kinds'"
        )
    except sqlite3.OperationalError:
        # `refinements` table doesn't exist (bootstrap=False catalogue
        # without the framework schema loaded). Treat as no-scope.
        return set()
    if not rows:
        return set()
    desc = rows[0]['description'] or ''
    return {k.strip() for k in desc.split(',') if k.strip()}


def enumerate_supported_cells(cat) -> Tuple[set[str], set[str]]:
    """Compute the IMPL and CAT cell-id sets at the catalogue's
    declared scope.

    Returns ``(impl_ids, cat_ids)``:

    * ``impl_ids`` — cell ids from :data:`SIGNATURE` whose kind is
      in ``supported_kinds(cat)``.
    * ``cat_ids`` — distinct break-numbers in the catalogue
      witnessed by the ``framework`` spec (i.e., framework-level
      cataloguings).

    The closure check kquery operates on the union of these two
    sets as its universe.
    """
    kinds = supported_kinds(cat)

    impl_ids: set[str] = set()
    for cell in SIGNATURE:
        if cell.kind.value in kinds:
            impl_ids.add(_catalogue_id_for(cell))

    try:
        rows = cat.query(
            "SELECT DISTINCT break_number FROM witnesses "
            "WHERE spec_id = 'framework'"
        )
    except sqlite3.OperationalError:
        # `witnesses` table absent — same no-op condition as in
        # supported_kinds(). Caller already returned via the
        # `if not kinds` branch in check_closure(); this is defensive.
        rows = []
    cat_ids: set[str] = {r['break_number'] for r in rows}

    return impl_ids, cat_ids


# -----------------------------------------------------------------------------
# The closure check
# -----------------------------------------------------------------------------

def check_closure(cat) -> Optional[dict]:
    """Run the self-hosting closure check (Theorem 14.5).

    Reads ``Q-supported-claims`` from the catalogue. If absent,
    returns None (the catalogue isn't framework-bootstrapped; no
    check applies). Otherwise computes the closure kquery; if
    ``gap`` is non-empty, raises :class:`SelfHostingViolation`.

    On pass, returns the kquery result dict
    ``{'00': [...], '01': [...], '10': [...], '11': [...]}``.
    """
    result = closure_status(cat)
    if result is None:
        return None
    if result['10'] or result['01']:
        raise SelfHostingViolation(
            implicit=result['10'],
            promissory=result['01'],
        )
    return result


def closure_status(cat) -> Optional[dict]:
    """Compute the closure kquery without raising on gap.

    Same signature as :func:`check_closure` but never raises:
    returns the kquery result dict (with possibly non-empty
    ``10`` / ``01`` cells) for callers that want to *inspect* the
    self-hosting state rather than enforce it. Used by the MCP
    server's ``catalogue://self_hosting`` resource.

    Returns None when ``Q-supported-claims`` is absent (catalogue
    isn't claiming framework self-hosting).
    """
    kinds = supported_kinds(cat)
    if not kinds:
        return None

    impl_ids, cat_ids = enumerate_supported_cells(cat)

    # Lazy import to avoid circularity.
    from .views import kquery
    universe = impl_ids | cat_ids
    return kquery(impl_ids, cat_ids, universe=universe)


__all__ = [
    'SelfHostingViolation',
    'IMPL', 'CAT',
    'supported_kinds', 'enumerate_supported_cells',
    'check_closure', 'closure_status',
]
