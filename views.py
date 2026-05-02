"""
Analytic queries — derived projections over the catalogue's witness
graph. None of these mutate state; they read views the schema defines.

These functions are exposed at the package level so that callers can
write::

    from v4cat import kquery, axis_distribution

without going through the SymmetryCatalogue class for read-only
operations.

The read primitive is :func:`kquery` — a Klein-four classifier that
labels every element of a bounded universe with its membership
signature ``(left ∈ A, right ∈ B) ∈ ℤ₂ × ℤ₂``. Every other read
(``wedge``, ``agree``, ``coverage``, ``blind``) is a named selection
from kquery's four cells. See methodology.md "The Klein-four read
core" for the algebraic argument.
"""
from __future__ import annotations

from typing import Callable, Hashable, Iterable, Optional, TypeAlias

from .catalogue import SymmetryCatalogue


# =============================================================================
# KQUERY — the Klein-four classifier (the only primitive read)
# =============================================================================

# Cell labels (the membership signature). Read as (left, right):
#   '00' — neither (in universe but absent from both A and B)
#   '01' — right-only (in B, not in A)
#   '10' — left-only  (in A, not in B)
#   '11' — both       (in A and in B; agreement)
Cell: TypeAlias = str  # one of '00' | '01' | '10' | '11'

ALL_CELLS: tuple[Cell, ...] = ('00', '01', '10', '11')


def kquery(
    a: Iterable[Hashable],
    b: Iterable[Hashable],
    *,
    universe: Optional[Iterable[Hashable]] = None,
    normalize: Callable[[Hashable], Hashable] = lambda x: x,
    emit: Iterable[Cell] = ALL_CELLS,
) -> dict[Cell, list[Hashable]]:
    """The Klein-four classifier: label every element of ``universe``
    with its ``(in A, in B)`` membership signature.

    Returns a mapping from cell label to the items in that cell.

    Arguments:
        a, b:        the two referents (sets / iterables of items)
        universe:    the bounded universe of discourse. Defaults to
                     ``set(a) | set(b)``, which collapses cell ``00``
                     to empty (you can't observe co-absence outside
                     the union without a universe).
        normalize:   pre-applied to each item before set membership;
                     gives an equivalence-class quotient (e.g. case-
                     folding, identifier canonicalisation).
        emit:        which cells to compute. Default returns all four.

    The four cells form ``ℤ₂ × ℤ₂`` (Klein four-group); every other
    read operation in the catalogue is a named selection from this
    classifier:

      * ``wedge(a, b)``     — emit ``{10, 01}`` (symmetric difference)
      * ``agree(a, b)``     — emit ``{11}``     (intersection)
      * ``coverage(a, b)``  — emit ``{10, 01, 11}`` (union)
      * ``blind(a, b, U)``  — emit ``{00}``     (shared absence)
      * unary ``query(A)``  — equivalent to ``kquery(A, U).11``

    The ``00`` cell is structurally significant: it surfaces the
    *shared blindness* between A and B relative to the universe —
    items the universe contains that neither representation accounts
    for. Most diff tools erase this cell; the methodology elevates
    it as a methodological object.
    """
    sa = {normalize(x) for x in a}
    sb = {normalize(x) for x in b}
    if universe is None:
        su = sa | sb
    else:
        su = {normalize(x) for x in universe}

    cells: dict[Cell, list[Hashable]] = {c: [] for c in emit}
    for x in su:
        sig = (1 if x in sa else 0, 1 if x in sb else 0)
        label = f'{sig[0]}{sig[1]}'
        if label in cells:
            cells[label].append(x)
    for c in cells:
        cells[c].sort(key=str)
    return cells


# -----------------------------------------------------------------------------
# Named selections (sugar over kquery)
# -----------------------------------------------------------------------------

def wedge(a: Iterable[Hashable], b: Iterable[Hashable]) -> dict:
    """Wedge-product audit: the symmetric residue between A and B.

    Equivalent to ``kquery(a, b, emit={'10', '01', '11'})`` reformatted
    to the legacy shape (``in_a_not_b`` / ``in_b_not_a`` / ``in_both``)
    used by older callers and tests.
    """
    cells = kquery(a, b, emit=('10', '01', '11'))
    return {
        'in_a_not_b': cells['10'],
        'in_b_not_a': cells['01'],
        'in_both':    cells['11'],
    }


def agree(a: Iterable[Hashable], b: Iterable[Hashable]) -> list:
    """Items in both A and B (cell 11)."""
    return kquery(a, b, emit=('11',))['11']


def left_residue(a: Iterable[Hashable], b: Iterable[Hashable]) -> list:
    """Items in A but not in B (cell 10)."""
    return kquery(a, b, emit=('10',))['10']


def right_residue(a: Iterable[Hashable], b: Iterable[Hashable]) -> list:
    """Items in B but not in A (cell 01)."""
    return kquery(a, b, emit=('01',))['01']


def blind(
    a: Iterable[Hashable],
    b: Iterable[Hashable],
    universe: Iterable[Hashable],
) -> list:
    """Items in the universe absent from both A and B (cell 00).

    Surfaces shared blindness — the methodologically significant
    "what neither representation accounts for" against a bounded
    universe of discourse.
    """
    return kquery(a, b, universe=universe, emit=('00',))['00']


def coverage(a: Iterable[Hashable], b: Iterable[Hashable]) -> list:
    """Items covered by either A or B (cells 10 ∪ 01 ∪ 11)."""
    cells = kquery(a, b, emit=('10', '01', '11'))
    out = cells['10'] + cells['01'] + cells['11']
    out.sort(key=str)
    return out


# =============================================================================
# Catalogue-specific derived views
# =============================================================================

def axis_distribution(cat: SymmetryCatalogue) -> dict[str, int]:
    """Count of breaks per axis."""
    rows = cat.query(
        "SELECT axis, break_count FROM breaks_by_axis ORDER BY break_count DESC"
    )
    return {row['axis']: row['break_count'] for row in rows}


def mixed_breaks(cat: SymmetryCatalogue) -> list[dict]:
    """Breaks that commit to multiple axes (axis cardinality > 1)."""
    return cat.query("SELECT * FROM mixed_breaks")


def consistency(cat: SymmetryCatalogue, rule: str) -> list[dict]:
    """Run a named consistency check.

    Currently supports:
      * ``'q92'``: paged specs (Q89) require restart-suitable frames
        (Q92). Returns rows representing violations; an empty result
        means consistent.

    Internally a kquery: paged-specs (left) compared to
    specs-with-restart-suitable-frames (right); violations are the
    ``10`` cell.
    """
    if rule == 'q92':
        return cat.query("SELECT * FROM q92_violations")
    raise ValueError(f"Unknown consistency rule: {rule!r}")


def retroactive_attributions(cat: SymmetryCatalogue) -> list[dict]:
    """All breaks where origin year < first-seen year."""
    return cat.query("SELECT * FROM retroactive_attributions")


def top_originators(cat: SymmetryCatalogue, *, limit: int = 10) -> list[dict]:
    """Specs ordered by number of breaks they originated."""
    return cat.query(
        "SELECT * FROM new_breaks_per_spec "
        "WHERE breaks_originated > 0 "
        "ORDER BY breaks_originated DESC, spec_year "
        "LIMIT ?",
        limit,
    )


def agent_level_witnesses(cat: SymmetryCatalogue) -> list[dict]:
    """Witnesses scoped at agent level (e.g. 8087 Q87 'precedes')."""
    return cat.query("SELECT * FROM agent_level_witnesses")


def spec_axis_summary(cat: SymmetryCatalogue) -> list[dict]:
    """Per-spec 5-axis declaration summary."""
    return cat.query("SELECT * FROM spec_axis_summary")


def axis_distribution(cat: SymmetryCatalogue) -> dict[str, int]:
    """Count of breaks per axis.

    Reads the breaks_by_axis view. Returns a flat dict
    ``{axis_name: count}`` rather than the view's verbose form.
    """
    rows = cat.query(
        "SELECT axis, break_count FROM breaks_by_axis ORDER BY break_count DESC"
    )
    return {row['axis']: row['break_count'] for row in rows}


def mixed_breaks(cat: SymmetryCatalogue) -> list[dict]:
    """Breaks that commit to multiple axes (axis cardinality > 1)."""
    return cat.query("SELECT * FROM mixed_breaks")


def consistency(cat: SymmetryCatalogue, rule: str) -> list[dict]:
    """Run a named consistency check.

    Currently supports:
      - 'q92': paged specs (Q89) require restart-suitable frames (Q92).
        Returns rows representing violations; an empty result means
        consistent.
    """
    if rule == 'q92':
        return cat.query("SELECT * FROM q92_violations")
    raise ValueError(f"Unknown consistency rule: {rule!r}")


def wedge(a: Iterable[Hashable], b: Iterable[Hashable]) -> dict:
    """Wedge-product audit between two sets of items.

    Generic set difference: returns a dict with the asymmetric and
    symmetric portions. Caller decides what to feed in (break numbers,
    spec ids, (subject, predicate, object) triples — anything
    hashable).

    Result shape::

        {
          'in_a_not_b': [...],   # in a but missing from b
          'in_b_not_a': [...],   # in b but missing from a
          'in_both':    [...],   # intersection
        }
    """
    sa, sb = set(a), set(b)
    return {
        'in_a_not_b': sorted(sa - sb, key=str),
        'in_b_not_a': sorted(sb - sa, key=str),
        'in_both':    sorted(sa & sb, key=str),
    }


def retroactive_attributions(cat: SymmetryCatalogue) -> list[dict]:
    """All breaks where origin year < first-seen year.

    The "retroactive" case isn't special data — it's just the rows
    where the gap is positive.
    """
    return cat.query("SELECT * FROM retroactive_attributions")


def top_originators(cat: SymmetryCatalogue, *, limit: int = 10) -> list[dict]:
    """Specs ordered by number of breaks they originated."""
    return cat.query(
        "SELECT * FROM new_breaks_per_spec "
        "WHERE breaks_originated > 0 "
        "ORDER BY breaks_originated DESC, spec_year "
        "LIMIT ?",
        limit,
    )


def agent_level_witnesses(cat: SymmetryCatalogue) -> list[dict]:
    """Witnesses scoped at agent level (e.g. 8087 Q87 'precedes')."""
    return cat.query("SELECT * FROM agent_level_witnesses")


def spec_axis_summary(cat: SymmetryCatalogue) -> list[dict]:
    """Per-spec 5-axis declaration summary."""
    return cat.query("SELECT * FROM spec_axis_summary")
