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


class RiscDisciplineViolation(Exception):
    """Raised when a SIGNATURE cell's ``derives_from`` chain is invalid.

    Per cotype/shadow_risc_core.md, the (β) discipline requires:

    - RISC cells (introduce_node, edge, kquery, plus closure-check
      meta-cells) have ``derives_from=None``
    - CISC / DERIVED cells have ``derives_from`` referencing other
      SIGNATURE cells, with chains that terminate in RISC cells

    The exception payload distinguishes:

    - ``dangling`` (cell_id, missing_ref) — derives_from points at a
      cell id that's not in SIGNATURE
    - ``cyclic`` (cell_id) — derives_from chain contains a cycle, so
      it doesn't terminate in RISC
    """

    def __init__(
        self,
        dangling: list[tuple[str, str]],
        cyclic: list[str],
    ):
        self.dangling = list(dangling)
        self.cyclic = list(cyclic)
        super().__init__(
            f"RISC discipline violated (S₄ strengthening):\n"
            f"  dangling refs (cell, missing-id): {sorted(self.dangling)!r}\n"
            f"  cyclic chains (cell ids): {sorted(self.cyclic)!r}\n"
            f"See cotype/shadow_risc_core.md § 'Closure-check strengthening'."
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

def check_risc_discipline() -> None:
    """S₄ strengthening: verify every SIGNATURE cell's
    ``derives_from`` chain terminates in RISC cells.

    Per cotype/shadow_risc_core.md, the (β) RISC discipline holds
    iff:

    - RISC cells have ``derives_from=None`` and act as roots
    - Every CISC / DERIVED cell's ``derives_from`` references
      cells present in SIGNATURE (no dangling refs)
    - Every chain terminates (no cycles)

    Raises :class:`RiscDisciplineViolation` if any chain is
    invalid. Substrate-independent — operates only on
    :data:`SIGNATURE` (Python data); does not consult the
    catalogue.
    """
    sig_index = by_id()
    dangling: list[tuple[str, str]] = []
    cyclic: list[str] = []

    for cell in SIGNATURE:
        if cell.derives_from is None:
            continue
        # BFS/DFS the chain; detect dangling refs and cycles
        visited: set[str] = {cell.id}
        frontier = list(cell.derives_from)
        while frontier:
            ref_id = frontier.pop()
            if ref_id not in sig_index:
                dangling.append((cell.id, ref_id))
                continue
            if ref_id in visited:
                if cell.id not in cyclic:
                    cyclic.append(cell.id)
                continue
            visited.add(ref_id)
            ref_cell = sig_index[ref_id]
            if ref_cell.derives_from is not None:
                frontier.extend(ref_cell.derives_from)

    if dangling or cyclic:
        raise RiscDisciplineViolation(dangling=dangling, cyclic=cyclic)


def check_closure(cat) -> Optional[dict]:
    """Run the self-hosting closure check (Theorem 14.5, S₄-strengthened).

    Two checks now run:

    1. **RISC discipline** (S₄): every SIGNATURE cell's
       ``derives_from`` chain terminates in RISC cells. Raises
       :class:`RiscDisciplineViolation` if violated.
    2. **IMPL ↔ CAT closure** (Theorem 14.5 original): the
       closure kquery's gap is empty. Raises
       :class:`SelfHostingViolation` if ``gap.10`` or ``gap.01``
       is non-empty.

    Reads ``Q-supported-claims`` from the catalogue. If absent,
    returns None (the catalogue isn't framework-bootstrapped; no
    check applies). On pass, returns the kquery result dict
    ``{'00': [...], '01': [...], '10': [...], '11': [...]}``.
    """
    # S₄ strengthening — RISC discipline check (substrate-independent)
    check_risc_discipline()
    # Original Theorem 14.5 closure check
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
    'SelfHostingViolation', 'RiscDisciplineViolation',
    'IMPL', 'CAT',
    'supported_kinds', 'enumerate_supported_cells',
    'check_risc_discipline', 'check_closure', 'closure_status',
]
