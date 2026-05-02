"""
v4cat.cells — the Cell tagged union and the Kinds enum.

Per theory.md § 14.5.1: a *cell* is any structural commitment the
framework makes — an object, a break, a witness edge, a refinement,
a schema-extension, a wedge audit, a kquery instance, or a
closure-check instance. Cells carry a tag in :class:`Kind`
identifying their kind; the tag is recoverable but is *not*
consulted by ``kquery`` (level-blindness, Lemma 14.1).

Note on the filename: this module exists alongside ``theory.md``
(the design doc) and ``theory.py`` (the framework signature).
The naming follows § 14.5.1's spec: ``cells.py`` defines the cell
namespace, ``theory.py`` declares the IMPL set over those cells.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Kind(str, Enum):
    """The eight cell kinds (Definition 14.1).

    Subclassing ``str`` makes Kind values JSON-serialisable
    directly and comparable to their single-letter codes.
    """
    O = 'O'    # objects (and object-introduction operations)
    B = 'B'    # breaks
    W = 'W'    # witnesses
    R = 'R'    # refinements
    E = 'E'    # schema-extensions
    A = 'A'    # wedge audits — reserved for the bicategorical 2-cell lift
               # (theory.md § 14.6.5) and as the under-promising example
               # (theory.md § 14.6.1); empty in the strict 1-categorical
               # implementation. Named selections of kquery (wedge, agree,
               # blind, coverage, left/right_residue) are orbit-elements
               # of Kind.K, NOT Kind.A — see cotype/shadow_kquery_orbit.md.
    K = 'K'    # kquery instances / read operators
    X = 'X'    # closure-check instances


@dataclass(frozen=True)
class Cell:
    """A structural commitment of one of the eight :class:`Kind`s.

    Cells are the units the closure check (Theorem 14.5) audits.
    Two cells are equal iff their ``id`` and ``kind`` match;
    ``description`` is informational and ignored for hashing.
    """
    id: str
    kind: Kind
    description: str = ''

    def __hash__(self) -> int:
        return hash((self.id, self.kind))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return NotImplemented
        return self.id == other.id and self.kind == other.kind


def tag(c: Cell) -> Kind:
    """Project a cell to its kind.

    Per Definition 14.2 and Lemma 14.1, ``kquery`` does *not*
    consult ``tag``; predicates that wish to be kind-aware may
    consult it explicitly.
    """
    return c.kind


__all__ = ['Cell', 'Kind', 'tag']
