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
    agent_level_witnesses         — witnesses scoped finer than spec
    spec_axis_summary             — per-spec 5-axis declarations

Quick start::

    from v4cat import SymmetryCatalogue

    with SymmetryCatalogue('/tmp/cat.db') as cat:
        cat.introduce_object('alpha', 'Alpha', year=1980)
        cat.introduce_object('beta',  'Beta',  year=1985,
                             lineage=[('alpha', 'descended-from')])
        cat.introduce_break('F1', 'My first break', axes=['spatial'])
        cat.witness('alpha', 'F1', 'origin')
        cat.witness('alpha', 'F1', 'catalogue-introduces')
        cat.witness('beta',  'F1', 'inherits')
        print(cat.origin('F1'))
        print(cat.lineage('beta'))

The framework is domain-agnostic — the witness objects above could
be processors, programming languages, cryptographic primitives,
file systems, or any other class of structured artefact. See
``examples.md`` for domain templates.
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
