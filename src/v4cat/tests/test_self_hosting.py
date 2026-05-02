"""
Regression test for Theorem 14.5 (self-hosting closure).

Per theory.md § 14.5.7: opens a fresh catalogue with
``check_self_hosting=True`` and asserts the closure check passes
(empty gap). When it passes, the framework is self-hosted at the
scope its ``Q-supported-claims`` declares.

Per theory.md § 14.8, this regression test is what licenses the
``v4cat`` rename: as long as it passes against any shipped
catalogue with self-hosting enabled, the framework constitutes (or
self-hosts as) a category over its declared scope.
"""
from __future__ import annotations

import sys
import traceback

from v4cat import SymmetryCatalogue
from v4cat.bootstrap import (
    CAT,
    IMPL,
    SelfHostingViolation,
    check_closure,
    enumerate_supported_cells,
    supported_kinds,
)
from v4cat.cells import Cell, Kind, tag
from v4cat.theory import SIGNATURE, by_id, by_kind


# -----------------------------------------------------------------------------
# Cell namespace (Definition 14.1)
# -----------------------------------------------------------------------------

def test_cells_are_hashable_and_comparable():
    """Cells are immutable, hashable, comparable by (id, kind)."""
    c1 = Cell('foo', Kind.O, 'first description')
    c2 = Cell('foo', Kind.O, 'second description')
    c3 = Cell('foo', Kind.B, 'first description')

    assert c1 == c2     # description ignored for equality
    assert c1 != c3     # kind matters
    assert hash(c1) == hash(c2)
    assert {c1, c2, c3} == {c1, c3}  # set deduplicates


def test_tag_projects_to_kind():
    c = Cell('x', Kind.K, 'kquery')
    assert tag(c) == Kind.K
    assert tag(c).value == 'K'


# -----------------------------------------------------------------------------
# IMPL and CAT predicates (Definitions 14.4, 14.5)
# -----------------------------------------------------------------------------

def test_IMPL_is_signature_membership():
    """IMPL(c) returns True iff c.id is in SIGNATURE's by_id()."""
    sig_index = by_id()
    for c in SIGNATURE:
        assert IMPL(c), f"signature cell {c.id!r} should pass IMPL"

    fictional = Cell('fictional-not-in-signature', Kind.O)
    assert not IMPL(fictional)


def test_CAT_finds_witnessed_break():
    """CAT(c, cat) is True iff Q-{c.id} has a witness in cat."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=True)
    # Every cell in SIGNATURE should pass CAT, by construction
    for c in SIGNATURE:
        assert CAT(c, cat), f"signature cell {c.id!r} should pass CAT"


def test_CAT_returns_false_when_no_witness():
    """A break with no witness fails CAT."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=True)
    cat.introduce_break('Q-orphan', 'Orphan break (no witness)')
    cat.commit()
    fake_cell = Cell('orphan', Kind.O)  # CAT looks for Q-orphan
    assert not CAT(fake_cell, cat)


# -----------------------------------------------------------------------------
# Scope enumeration (Lemma 14.4)
# -----------------------------------------------------------------------------

def test_supported_kinds_reads_initial_scope():
    """The seed declares scope {O, B, W, R, E, K, X}."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=True)
    kinds = supported_kinds(cat)
    assert kinds == {'O', 'B', 'W', 'R', 'E', 'K', 'X'}


def test_supported_kinds_empty_without_seed():
    """Without check_self_hosting, no Q-supported-claims; empty set."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    assert supported_kinds(cat) == set()


def test_enumerate_supported_cells_returns_two_sets():
    cat = SymmetryCatalogue(':memory:', check_self_hosting=True)
    impl_ids, cat_ids = enumerate_supported_cells(cat)

    # Both sets should contain Q-supported-claims and Q-kquery
    assert 'Q-supported-claims' in impl_ids
    assert 'Q-supported-claims' in cat_ids
    assert 'Q-kquery'           in impl_ids
    assert 'Q-kquery'           in cat_ids


# -----------------------------------------------------------------------------
# The main result: Theorem 14.5
# -----------------------------------------------------------------------------

def test_closure_check_passes_on_fresh_catalogue():
    """Theorem 14.5 regression test: a fresh catalogue with
    check_self_hosting=True passes the closure check."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=True)
    # If __init__ didn't raise, the check passed. Re-run to be sure.
    result = check_closure(cat)
    assert result is not None, "supported_kinds should be non-empty"
    assert result['10'] == [], (
        f"implicit cells (in IMPL, not CAT): {result['10']!r}"
    )
    assert result['01'] == [], (
        f"promissory cells (in CAT, not IMPL): {result['01']!r}"
    )


def test_closure_check_skips_when_seed_absent():
    """Without framework seed, check_closure returns None (no-op)."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    result = check_closure(cat)
    assert result is None


def test_closure_check_recurses():
    """Definition 14.7 cond. (3): Q-supported-claims is itself in
    the scope, hence in the agreement cell."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=True)
    result = check_closure(cat)
    assert 'Q-supported-claims'  in result['11']
    assert 'Q-bootstrap-closure' in result['11']
    assert 'Q-check_closure'     in result['11']


def test_closure_violation_detects_implicit():
    """Adding a cell to SIGNATURE without seeding the catalogue
    breaks closure: gap.10 (implicit) becomes non-empty."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=True)
    # Inject an implicit cell by appending to SIGNATURE then re-checking
    fictional = Cell('fictional-impl-only', Kind.O)
    SIGNATURE.append(fictional)
    try:
        try:
            check_closure(cat)
        except SelfHostingViolation as e:
            assert 'Q-fictional-impl-only' in e.implicit
            assert e.promissory == []
        else:
            raise AssertionError('expected SelfHostingViolation')
    finally:
        SIGNATURE.pop()  # clean up


def test_closure_violation_detects_promissory():
    """Adding a Q-break + framework witness without a corresponding
    SIGNATURE entry breaks closure: gap.01 (promissory) is non-empty."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=True)
    cat.introduce_break('Q-fictional-cat-only', 'Promissory break')
    cat.witness('framework', 'Q-fictional-cat-only', 'catalogue-introduces')
    cat.commit()
    try:
        check_closure(cat)
    except SelfHostingViolation as e:
        assert 'Q-fictional-cat-only' in e.promissory
        assert e.implicit == []
    else:
        raise AssertionError('expected SelfHostingViolation')


def test_closure_check_constructive_failure_payload():
    """Corollary 14.5.1: a failing check produces the to-do list."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=True)
    cat.introduce_break('Q-promissory-1', 'Promissory 1')
    cat.witness('framework', 'Q-promissory-1', 'catalogue-introduces')
    cat.introduce_break('Q-promissory-2', 'Promissory 2')
    cat.witness('framework', 'Q-promissory-2', 'catalogue-introduces')
    cat.commit()
    try:
        check_closure(cat)
    except SelfHostingViolation as e:
        assert sorted(e.promissory) == ['Q-promissory-1', 'Q-promissory-2']
        assert e.implicit == []
        # The repr should be informative
        assert 'Self-hosting violated' in str(e)
        assert 'promissory' in str(e)
    else:
        raise AssertionError('expected SelfHostingViolation')


# -----------------------------------------------------------------------------
# Default behaviour — closure check runs at open
# -----------------------------------------------------------------------------

def test_default_constructor_runs_closure_check():
    """The default opens a catalogue with the framework seed loaded
    and the closure check passing — the kfour → v4cat transition.
    Theorem 14.5 is operative by default; opt out with
    ``check_self_hosting=False`` for tests that need an empty
    catalogue."""
    cat = SymmetryCatalogue(':memory:')
    # No exception means the closure check passed. The framework
    # seed contributes Q-numbered breaks and a 'framework' spec.
    breaks = {b['number'] for b in cat.all_breaks()}
    objects = {o['id'] for o in cat.all_objects()}
    assert 'Q-kquery' in breaks
    assert 'Q-supported-claims' in breaks
    assert 'framework' in objects


def test_opt_out_via_check_self_hosting_false():
    """``check_self_hosting=False`` keeps the catalogue empty —
    the path used by tests that exercise user-domain semantics."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    assert cat.all_breaks() == []
    assert cat.all_objects() == []


# -----------------------------------------------------------------------------
# Test harness
# -----------------------------------------------------------------------------

ALL_TESTS = [
    test_cells_are_hashable_and_comparable,
    test_tag_projects_to_kind,
    test_IMPL_is_signature_membership,
    test_CAT_finds_witnessed_break,
    test_CAT_returns_false_when_no_witness,
    test_supported_kinds_reads_initial_scope,
    test_supported_kinds_empty_without_seed,
    test_enumerate_supported_cells_returns_two_sets,
    test_closure_check_passes_on_fresh_catalogue,
    test_closure_check_skips_when_seed_absent,
    test_closure_check_recurses,
    test_closure_violation_detects_implicit,
    test_closure_violation_detects_promissory,
    test_closure_check_constructive_failure_payload,
    test_default_constructor_runs_closure_check,
    test_opt_out_via_check_self_hosting_false,
]


def main() -> int:
    passed = 0
    failed = 0
    for test in ALL_TESTS:
        try:
            test()
            print(f"  ✓ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
