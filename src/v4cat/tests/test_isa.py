"""
Framework tests for the symmetry-break cataloguing ISA.

Uses a synthetic mini-domain — three fictitious "objects" with three
fictitious breaks — that exercises every ISA verb and every analytic
view without depending on any specific domain (no processor data).

Run as a script::

    python -m v4cat.tests.test_isa

or via pytest if installed.
"""
from __future__ import annotations

import sys
import traceback

from v4cat import (
    SymmetryCatalogue,
    agent_level_witnesses,
    agree,
    axis_distribution,
    blind,
    coverage,
    kquery,
    left_residue,
    mixed_breaks,
    retroactive_attributions,
    right_residue,
    top_originators,
    wedge,
)


# -----------------------------------------------------------------------------
# Synthetic mini-domain: three objects with descent edges, three breaks
# spanning two axes, witnesses + refinements + a tension.
# -----------------------------------------------------------------------------

def populate_synthetic(cat: SymmetryCatalogue) -> None:
    """A small domain that exercises every framework primitive.

    Objects (with year + lineage):
      * object_alpha (1980)        — root of the fictitious lineage
      * object_beta  (1985, ← α)   — descendant; refines two breaks
      * object_gamma (1990, ← β)   — descendant; introduces one break

    Breaks:
      * F1 (axis: spatial)   — origin at α
      * F2 (axes: spatial,
                 temporal)  — origin at β (mixed-axis)
      * F3 (axis: parallel) — origin at γ; deferred-then-promoted
    """
    cat.introduce_object('alpha', 'Object Alpha', year=1980,
                         catalogue_order=1)
    cat.introduce_object('beta',  'Object Beta',  year=1985,
                         catalogue_order=2,
                         lineage=[('alpha', 'descended-from')])
    cat.introduce_object('gamma', 'Object Gamma', year=1990,
                         catalogue_order=3,
                         lineage=[('beta',  'descended-from')])

    # F1: simple break, single axis
    cat.introduce_break('F1', 'First fictitious break',
                        axes=['spatial'])
    cat.witness('alpha', 'F1', 'origin')
    cat.witness('alpha', 'F1', 'catalogue-introduces')
    cat.witness('beta',  'F1', 'inherits')

    # F2: refined cross-cutting break
    cat.introduce_break('F2', 'Second fictitious break',
                        axes=['spatial', 'temporal'])
    cat.witness('beta', 'F2', 'origin')
    cat.witness('beta', 'F2', 'catalogue-introduces')
    cat.refine('F2', 'beta', 'foo-extension', description='bar')
    cat.refine('F2', 'beta', 'baz-extension', description='qux')

    # F3: deferred-then-promoted
    cat.introduce_break('F3', 'Third fictitious break',
                        axes=['parallel'])
    cat.witness('gamma', 'F3', 'catalogue-introduces')
    cat.defer('F3', by='gamma', reason='not yet adopted')
    # promote will arrive in test_defer_then_promote_changes_status

    # A tension and a sibling-boundary
    cat.introduce_tension(
        't-test', 'Implementation lag',
        description='F2 needs schema reshuffling',
        breaks_involved=['F2'],
    )


# -----------------------------------------------------------------------------
# Framework bootstrap
# -----------------------------------------------------------------------------

def test_bootstrap_creates_schema():
    """A fresh in-memory catalogue creates the framework schema.

    Opens with ``check_self_hosting=False`` so the catalogue stays
    truly empty (no framework seed loaded). With the default
    ``check_self_hosting=True``, the catalogue has 15 framework
    breaks + 1 framework spec at open — see
    ``test_self_hosting.py`` for that path.
    """
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    # Core tables exist
    assert cat.query("SELECT name FROM sqlite_master "
                     "WHERE type='table' AND name='breaks'") != []
    assert cat.query("SELECT name FROM sqlite_master "
                     "WHERE type='table' AND name='specs'") != []
    assert cat.query("SELECT name FROM sqlite_master "
                     "WHERE type='table' AND name='witnesses'") != []
    assert cat.query("SELECT name FROM sqlite_master "
                     "WHERE type='table' AND name='lineages'") != []
    # Empty
    assert cat.all_breaks() == []
    assert cat.all_objects() == []


def test_load_extension():
    """load_extension can layer additional schema/data on top."""
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    cat.commit()

    # Synthesise a small extension SQL inline by writing to a temp file
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.sql', delete=False) as f:
        f.write("""
            CREATE TABLE IF NOT EXISTS my_domain_facts (
                id TEXT PRIMARY KEY, value INTEGER
            );
            INSERT OR IGNORE INTO my_domain_facts VALUES ('x', 1);
        """)
        f.flush()
        cat.load_extension(f.name)

    rows = cat.query("SELECT * FROM my_domain_facts")
    assert rows == [{'id': 'x', 'value': 1}]


# -----------------------------------------------------------------------------
# Mutation: introduce / witness / refine
# -----------------------------------------------------------------------------

def test_introduce_break_idempotent():
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    cat.introduce_break('F1', 'Break one')
    cat.introduce_break('F1', 'Break one (duplicate)')
    breaks = cat.all_breaks()
    assert len(breaks) == 1
    # First insert wins (INSERT OR IGNORE)
    assert breaks[0]['name'] == 'Break one'


def test_introduce_object_auto_assigns_catalogue_order():
    """When catalogue_order is omitted, it defaults to next available."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_object('a', 'A', year=2000)
    cat.introduce_object('b', 'B', year=2001)
    objects = {o['id']: o for o in cat.all_objects()}
    assert objects['a']['catalogue_order'] == 1
    assert objects['b']['catalogue_order'] == 2


def test_introduce_object_attrs_populate_spec_attributes():
    """Domain-specific attrs go into the spec_attributes table."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_object('80386', 'Intel 80386', year=1985,
                         attrs={
                             'vendor': 'Intel',
                             'family': 'x86',
                             'data_bits': 32,
                             'address_bits': 32,
                         })
    attrs = cat.attributes_for_object('80386')
    assert attrs['vendor'] == 'Intel'
    assert attrs['family'] == 'x86'
    assert attrs['data_bits']    == '32'   # stored as string
    assert attrs['address_bits'] == '32'


def test_framework_specs_table_is_minimal():
    """The framework schema's specs has only framework-load-bearing
    columns: id, name, year, catalogue_order, notes."""
    cat = SymmetryCatalogue(':memory:')
    cols = cat.query("PRAGMA table_info(specs)")
    col_names = {c['name'] for c in cols}
    assert col_names == {'id', 'name', 'year', 'catalogue_order', 'notes'}
    # Domain-specific attributes don't live in specs
    assert 'vendor' not in col_names
    assert 'family' not in col_names
    assert 'data_bits' not in col_names
    assert 'address_bits' not in col_names


def test_witness_records_edge():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    edges = cat.witnesses_for_break('F1')
    by_kind = {w['kind']: w for w in edges if w['spec_id'] == 'alpha'}
    assert 'origin' in by_kind
    assert 'catalogue-introduces' in by_kind


def test_refine_admits_multiple_per_edge():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    refs = cat.refinements_for_break('F2')
    names = sorted(r['name'] for r in refs)
    assert names == ['baz-extension', 'foo-extension']


# -----------------------------------------------------------------------------
# Derived attribution (the methodology's central claim)
# -----------------------------------------------------------------------------

def test_origin_derived_from_witness_graph():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    o = cat.origin('F1')
    assert o['originator_id']   == 'alpha'
    assert o['originated_year'] == 1980


def test_first_seen_uses_catalogue_order():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    fs = cat.first_seen('F1')
    assert fs['first_seen_at_id'] == 'alpha'


def test_chronological_origin_emerges_without_retro_verb():
    """The methodology's central claim: the originator is always
    derived. Adding an earlier-year origin witness later just causes
    the view's MIN-year to pick it up."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_object('later',   'Later',   year=1990)
    cat.introduce_object('earlier', 'Earlier', year=1980)
    cat.introduce_break('Q-test', 'Test break', axes=['spatial'])

    # First, "later" gets the catalogue-introduces + origin
    cat.witness('later', 'Q-test', 'catalogue-introduces')
    cat.witness('later', 'Q-test', 'origin')
    assert cat.origin('Q-test')['originator_id'] == 'later'

    # Later, an earlier object is examined and adds an origin witness.
    # No special verb; just an additional witness edge.
    cat.witness('earlier', 'Q-test', 'origin')

    # The view's MIN-year automatically picks "earlier".
    o = cat.origin('Q-test')
    assert o['originator_id']   == 'earlier'
    assert o['originated_year'] == 1980

    # First-seen unchanged: "later" still holds catalogue-introduces.
    assert cat.first_seen('Q-test')['first_seen_at_id'] == 'later'


def test_retroactive_gap_is_arithmetic():
    """RETROACTIVE_GAP = first_seen.year - origin.year, no special case."""
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_object('newer', 'Newer', year=2000)
    cat.introduce_object('older', 'Older', year=1970)
    cat.introduce_break('Q-r', 'R', axes=['spatial'])
    cat.witness('newer', 'Q-r', 'catalogue-introduces')
    cat.witness('older', 'Q-r', 'origin')
    assert cat.retroactive_gap('Q-r') == 30


def test_retroactive_attributions_filters_positive_gap():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    # F1 / F2 / F3 all have origin == catalogue-introduces (no retroactive)
    rows = retroactive_attributions(cat)
    assert rows == []


# -----------------------------------------------------------------------------
# Lifecycle: defer / promote / boundary
# -----------------------------------------------------------------------------

def test_defer_sets_status_deferred():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    assert cat.status('F3') == 'deferred'


def test_promote_changes_status_to_active():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    cat.introduce_object('delta', 'Delta', year=1995)
    cat.promote('F3', by='delta', reason='confirmed at second witness')
    assert cat.status('F3') == 'active'


def test_boundary_yields_sibling_boundary_status():
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_object('s', 'Spec', year=2000)
    cat.introduce_break('F-bd', 'Boundary test', axes=['parallel'])
    cat.boundary('F-bd', 'deliberate non-extension', by='s')
    assert cat.status('F-bd') == 'sibling-boundary'


# -----------------------------------------------------------------------------
# Lineage (S11)
# -----------------------------------------------------------------------------

def test_lineage_transitive_closure():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    chain = cat.lineage('gamma')
    ancestors = [r['ancestor'] for r in chain]
    assert ancestors == ['beta', 'alpha']  # depth-ordered


def test_inherited_breaks_propagate_via_lineage():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    # gamma's ancestors are beta (F2 origin) and alpha (F1 origin).
    inherited = {r['break_number']: r for r in cat.inherited_breaks('gamma')}
    assert 'F1' in inherited and inherited['F1']['via_ancestor'] == 'alpha'
    assert 'F2' in inherited and inherited['F2']['via_ancestor'] == 'beta'


def test_introduce_object_with_lineage_pair():
    cat = SymmetryCatalogue(':memory:')
    cat.introduce_object('root', 'Root', year=1970)
    cat.introduce_object('child', 'Child', year=1980,
                         lineage=[('root', 'descended-from')])
    chain = cat.lineage('child')
    assert chain[0]['ancestor'] == 'root'


# -----------------------------------------------------------------------------
# Analytic queries
# -----------------------------------------------------------------------------

def test_axis_distribution_counts_per_axis():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    dist = axis_distribution(cat)
    # F1 spatial; F2 spatial+temporal; F3 parallel
    assert dist['spatial']  == 2
    assert dist['temporal'] == 1
    assert dist['parallel'] == 1


def test_mixed_breaks_finds_multi_axis():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    mixed = {b['number'] for b in mixed_breaks(cat)}
    assert mixed == {'F2'}


def test_top_originators_ranks_by_breaks_originated():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    top = top_originators(cat, limit=5)
    counts = {row['spec_name']: row['breaks_originated'] for row in top}
    # alpha: F1; beta: F2; gamma: F3 (all originated 1 each)
    assert counts.get('Object Alpha') == 1
    assert counts.get('Object Beta')  == 1
    assert counts.get('Object Gamma') == 1


def test_agent_level_witnesses_returns_only_agent_scope():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    # No agent-scope witnesses in synthetic domain
    assert agent_level_witnesses(cat) == []
    # Add one
    cat.introduce_break('F-agent', 'Agent-level test', axes=['equivalential'])
    cat.witness('alpha', 'F-agent', 'precedes',
                notes='agent-level pattern', scope='agent')
    rows = agent_level_witnesses(cat)
    assert len(rows) == 1
    assert rows[0]['break_number'] == 'F-agent'


# -----------------------------------------------------------------------------
# KQUERY — the Klein-four read primitive
# -----------------------------------------------------------------------------

def test_kquery_returns_four_cells():
    """Default emit returns all four cells with default universe = A ∪ B."""
    result = kquery(['a', 'b', 'c'], ['b', 'c', 'd'])
    assert result['11'] == ['b', 'c']
    assert result['10'] == ['a']
    assert result['01'] == ['d']
    assert result['00'] == []


def test_kquery_with_explicit_universe_surfaces_blind_spot():
    """The 00 cell — items in universe absent from both A and B."""
    result = kquery(
        ['a', 'b'],
        ['b', 'c'],
        universe=['a', 'b', 'c', 'd', 'e'],
    )
    assert result['00'] == ['d', 'e']
    assert result['11'] == ['b']


def test_kquery_emit_subset():
    result = kquery(['a', 'b'], ['b', 'c'], emit=('10', '01'))
    assert set(result.keys()) == {'10', '01'}


def test_kquery_normalize_gives_quotient():
    """Pre-applied normalization gives equivalence-class quotient."""
    result = kquery(
        ['Q89', 'Q90'],
        ['q89', 'Q91'],
        normalize=str.upper,
    )
    assert result['11'] == ['Q89']     # case-folded match
    assert result['10'] == ['Q90']
    assert result['01'] == ['Q91']


def test_kquery_named_selections_compose():
    """wedge / agree / coverage / blind / left/right_residue all
    decompose into kquery selections."""
    a = ['a', 'b', 'c']
    b = ['b', 'c', 'd']
    universe = ['a', 'b', 'c', 'd', 'e']

    assert agree(a, b)         == ['b', 'c']
    assert left_residue(a, b)  == ['a']
    assert right_residue(a, b) == ['d']
    assert blind(a, b, universe) == ['e']
    assert coverage(a, b)      == ['a', 'b', 'c', 'd']


def test_wedge_legacy_shape():
    """wedge() returns the legacy in_a_not_b / in_b_not_a / in_both shape."""
    result = wedge(['a', 'b', 'c'], ['b', 'c', 'd'])
    assert result['in_a_not_b'] == ['a']
    assert result['in_b_not_a'] == ['d']
    assert result['in_both']    == ['b', 'c']


def test_tropical_min_over_year_recovers_origin():
    """``tropical_min(axis_column='year', witness_kinds=('origin',
    'catalogue-introduces'))`` is the generic form of the
    break_origin view."""
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    rows = cat.tropical_min(
        axis_column='year',
        witness_kinds=('origin', 'catalogue-introduces'),
    )
    by_break = {r['break_number']: r for r in rows}
    # F1: origin alpha (1980); F2: origin beta (1985); F3: origin gamma (1990)
    assert by_break['F1']['spec_id']    == 'alpha'
    assert by_break['F1']['axis_value'] == 1980
    assert by_break['F2']['spec_id']    == 'beta'
    assert by_break['F2']['axis_value'] == 1985


def test_tropical_min_over_catalogue_order_recovers_first_seen():
    """The same operator with axis_column='catalogue_order' and
    witness_kinds=('catalogue-introduces',) recovers break_first_seen
    semantics."""
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    rows = cat.tropical_min(
        axis_column='catalogue_order',
        witness_kinds=('catalogue-introduces',),
    )
    by_break = {r['break_number']: r for r in rows}
    assert by_break['F1']['spec_id'] == 'alpha'
    assert by_break['F1']['axis_value'] == 1
    assert by_break['F2']['spec_id'] == 'beta'
    assert by_break['F2']['axis_value'] == 2


def test_tropical_min_can_filter_to_one_break():
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    rows = cat.tropical_min(
        axis_column='year',
        witness_kinds=('origin',),
        break_='F2',
    )
    assert len(rows) == 1
    assert rows[0]['spec_id'] == 'beta'


def test_tropical_max_picks_extremum():
    """tropical_max returns the latest matching witness."""
    cat = SymmetryCatalogue(':memory:')
    populate_synthetic(cat)
    # Add a confirms witness from a younger spec
    cat.introduce_object('omega', 'Omega', year=2020,
                         catalogue_order=99)
    cat.witness('omega', 'F1', 'confirms')
    cat.witness('alpha', 'F1', 'confirms')   # alpha re-confirms

    rows = cat.tropical_max(
        axis_column='year',
        witness_kinds=('confirms',),
        break_='F1',
    )
    # Among confirms witnesses, omega (2020) is the latest
    assert len(rows) == 1
    assert rows[0]['spec_id'] == 'omega'


def test_tropical_min_rejects_nonexistent_column():
    cat = SymmetryCatalogue(':memory:')
    try:
        cat.tropical_min(
            axis_column='nonexistent',
            witness_kinds=('origin',),
        )
    except ValueError as e:
        assert 'nonexistent' in str(e)
    else:
        raise AssertionError('expected ValueError')


def test_tropical_min_works_over_custom_axis_column():
    """A domain extension can ALTER the specs table to add an
    ordered column, then tropical_min over it. This demonstrates
    that year and catalogue_order aren't structurally privileged."""
    cat = SymmetryCatalogue(':memory:')
    # Domain extension: add a 'significance_rank' column
    cat.conn.execute("ALTER TABLE specs ADD COLUMN significance_rank INTEGER")
    populate_synthetic(cat)
    cat.conn.execute(
        "UPDATE specs SET significance_rank = ? WHERE id = ?", (1, 'alpha'))
    cat.conn.execute(
        "UPDATE specs SET significance_rank = ? WHERE id = ?", (2, 'beta'))
    cat.conn.execute(
        "UPDATE specs SET significance_rank = ? WHERE id = ?", (3, 'gamma'))

    rows = cat.tropical_min(
        axis_column='significance_rank',
        witness_kinds=('origin', 'catalogue-introduces'),
    )
    by_break = {r['break_number']: r for r in rows}
    # F1: alpha is rank 1 (most significant)
    assert by_break['F1']['spec_id']    == 'alpha'
    assert by_break['F1']['axis_value'] == 1


def test_origin_parametric_over_axis_column():
    """origin() routes through tropical_min and accepts any ordered
    column on specs. Demonstrates that 'year' is a default, not a
    structural commitment."""
    cat = SymmetryCatalogue(':memory:')
    cat.conn.execute("ALTER TABLE specs ADD COLUMN paper_year INTEGER")
    cat.introduce_object('a', 'A', year=2010)
    cat.introduce_object('b', 'B', year=2005)
    cat.conn.execute(
        "UPDATE specs SET paper_year = ? WHERE id = ?", (1990, 'a'))
    cat.conn.execute(
        "UPDATE specs SET paper_year = ? WHERE id = ?", (2000, 'b'))
    cat.introduce_break('F', 'F', axes=['spatial'])
    cat.witness('a', 'F', 'origin')
    cat.witness('b', 'F', 'origin')
    cat.witness('a', 'F', 'catalogue-introduces')

    # Default axis is year: b has earlier year (2005), so b is the originator
    by_year = cat.origin('F')
    assert by_year['originator_id']     == 'b'
    assert by_year['originated_year']   == 2005

    # On paper_year axis: a has earlier paper_year (1990), so a is the originator
    by_paper = cat.origin('F', axis_column='paper_year')
    assert by_paper['originator_id']         == 'a'
    assert by_paper['originated_paper_year'] == 1990


def test_retroactive_gap_parametric_over_axis_column():
    """retroactive_gap() takes any ordered column. Default 'year'
    preserves legacy behaviour; other columns give domain-specific
    gaps."""
    cat = SymmetryCatalogue(':memory:')
    cat.conn.execute("ALTER TABLE specs ADD COLUMN version INTEGER")
    cat.introduce_object('newer', 'Newer', year=2010, catalogue_order=1)
    cat.introduce_object('older', 'Older', year=1980, catalogue_order=2)
    cat.conn.execute(
        "UPDATE specs SET version = ? WHERE id = ?", (10, 'newer'))
    cat.conn.execute(
        "UPDATE specs SET version = ? WHERE id = ?", (3,  'older'))
    cat.introduce_break('F', 'F', axes=['spatial'])
    cat.witness('newer', 'F', 'catalogue-introduces')
    cat.witness('older', 'F', 'origin')

    # Default 'year' axis: gap = newer.year - older.year = 30
    assert cat.retroactive_gap('F') == 30
    # 'version' axis: gap = newer.version - older.version = 7
    assert cat.retroactive_gap('F', axis_column='version') == 7


def test_retroactive_gap_rejects_invalid_axis():
    """retroactive_gap raises on a non-existent axis column."""
    cat = SymmetryCatalogue(':memory:')
    try:
        cat.retroactive_gap('F', axis_column='nope')
        assert False, "expected ValueError"
    except ValueError as e:
        assert 'nope' in str(e)


def test_kquery_against_synthetic_catalogue():
    """A useful application: which breaks have origin and which are
    deferred? KQUERY over (active-breaks, deferred-breaks) over the
    universe of all breaks."""
    cat = SymmetryCatalogue(':memory:', check_self_hosting=False)
    populate_synthetic(cat)
    all_breaks   = [b['number'] for b in cat.all_breaks()]
    deferred     = [b['break_number'] for b in cat.query(
        "SELECT * FROM break_status WHERE status = 'deferred'"
    )]
    active       = [b['break_number'] for b in cat.query(
        "SELECT * FROM break_status WHERE status = 'active'"
    )]

    cells = kquery(active, deferred, universe=all_breaks)
    # No break can be both active and deferred → 11 cell empty
    assert cells['11'] == []
    # 10 cell contains the active breaks (F1, F2)
    assert set(cells['10']) == {'F1', 'F2'}
    # 01 cell contains deferred breaks (F3)
    assert cells['01'] == ['F3']


# -----------------------------------------------------------------------------
# Test harness
# -----------------------------------------------------------------------------

ALL_TESTS = [
    test_bootstrap_creates_schema,
    test_load_extension,
    test_introduce_break_idempotent,
    test_introduce_object_auto_assigns_catalogue_order,
    test_introduce_object_attrs_populate_spec_attributes,
    test_framework_specs_table_is_minimal,
    test_witness_records_edge,
    test_refine_admits_multiple_per_edge,
    test_origin_derived_from_witness_graph,
    test_first_seen_uses_catalogue_order,
    test_chronological_origin_emerges_without_retro_verb,
    test_retroactive_gap_is_arithmetic,
    test_retroactive_attributions_filters_positive_gap,
    test_defer_sets_status_deferred,
    test_promote_changes_status_to_active,
    test_boundary_yields_sibling_boundary_status,
    test_lineage_transitive_closure,
    test_inherited_breaks_propagate_via_lineage,
    test_introduce_object_with_lineage_pair,
    test_axis_distribution_counts_per_axis,
    test_mixed_breaks_finds_multi_axis,
    test_top_originators_ranks_by_breaks_originated,
    test_agent_level_witnesses_returns_only_agent_scope,
    test_kquery_returns_four_cells,
    test_kquery_with_explicit_universe_surfaces_blind_spot,
    test_kquery_emit_subset,
    test_kquery_normalize_gives_quotient,
    test_kquery_named_selections_compose,
    test_wedge_legacy_shape,
    test_tropical_min_over_year_recovers_origin,
    test_tropical_min_over_catalogue_order_recovers_first_seen,
    test_tropical_min_can_filter_to_one_break,
    test_tropical_max_picks_extremum,
    test_tropical_min_rejects_nonexistent_column,
    test_tropical_min_works_over_custom_axis_column,
    test_origin_parametric_over_axis_column,
    test_retroactive_gap_parametric_over_axis_column,
    test_retroactive_gap_rejects_invalid_axis,
    test_kquery_against_synthetic_catalogue,
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
