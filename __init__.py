"""
v4cat — Python implementation of the symmetry-break cataloguing
methodology described in ../methodology.md.

Public API:

    SymmetryCatalogue             — the ISA as a class with method-per-verb
    wedge                         — wedge-product audit (set diff)
    consistency                   — run a named consistency rule
    axis_distribution             — breaks-per-axis count
    mixed_breaks                  — breaks committing to multiple axes
    retroactive_attributions      — origin-precedes-first-seen rows
    top_originators               — most prolific originator specs
    agent_level_witnesses         — agent-scope witnesses (e.g. 8087 Q87)
    spec_axis_summary             — per-spec 5-axis declarations

Quick start::

    from v4cat import SymmetryCatalogue

    with SymmetryCatalogue('/tmp/cat.db') as cat:
        cat.introduce_object('z16', 'IBM z16', year=2022,
                             vendor='IBM', family='mainframe',
                             lineage=[('system_370_xa', 'descended-from')])
        cat.introduce_break('Q94', 'Vector facility', axes=['parallel'])
        cat.witness('z16', 'Q94', 'origin')
        cat.witness('z16', 'Q94', 'catalogue-introduces')
        print(cat.origin('Q94'))
        print(cat.lineage('z16'))
"""
from .catalogue import SymmetryCatalogue
from .views import (
    agent_level_witnesses,
    agree,
    axis_distribution,
    blind,
    consistency,
    coverage,
    kquery,
    left_residue,
    mixed_breaks,
    retroactive_attributions,
    right_residue,
    spec_axis_summary,
    top_originators,
    wedge,
)

__all__ = [
    'SymmetryCatalogue',
    # The Klein-four primitive read operator and its named selections
    'kquery',
    'wedge', 'agree', 'left_residue', 'right_residue', 'blind', 'coverage',
    # Catalogue-specific views
    'agent_level_witnesses',
    'axis_distribution',
    'consistency',
    'mixed_breaks',
    'retroactive_attributions',
    'spec_axis_summary',
    'top_originators',
]
