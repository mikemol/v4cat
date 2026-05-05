# Shadow: v4cat-octave CISC-sugar gap (promissory cell)

**Tracking**: [v4cat-oss/v4cat-octave#2](https://github.com/v4cat-oss/v4cat-octave/issues/2) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_v4cat_octave_distribution.md](shadow_v4cat_octave_distribution.md)).
> Region **#4** (S2G alone -- pure cataloguing).*

## Form

`v4cat-octave` v0.1 ships only the RISC core (`node`, `edge`,
`intern`, `kquery`, `kquery_rel`) plus the algebraic primitives
(sparse incidence, QueryDAG). The **16 CISC sugar verbs** that
v4cat (Python) exposes -- which compose RISC writes into
domain-natural shapes (introduce_break / introduce_object /
witness / refine / lineage / tropical_min / etc.) -- are
catalogued here for a future v0.x sub-fire.

## What to implement

Sourced from `v4cat/src/v4cat/catalogue.py` (lines 35--1073):

| Verb | Octave function | Equivalent Python signature |
| --- | --- | --- |
| `introduce_break` | `+v4cat/introduce_break.m` | `(number, name, *, short_desc, axes)` |
| `introduce_object` | `+v4cat/introduce_object.m` | `(id, name, *, year, catalogue_order, notes, lineage, attrs)` |
| `introduce_tension` | `+v4cat/introduce_tension.m` | `(id, name, *, description, status, addressing_stage, breaks_involved)` |
| `witness` | `+v4cat/witness.m` | `(subject, break_, kind, *, notes, scope)` |
| `lineage_witness` | `+v4cat/lineage_witness.m` | `(descendant, ancestor, kind, *, notes)` |
| `refine` | `+v4cat/refine.m` | `(break_, object_, name, *, description)` |
| `defer` | `+v4cat/defer.m` | `(break_, *, by, reason)` |
| `promote` | `+v4cat/promote.m` | `(break_, *, by, reason)` |
| `boundary` | `+v4cat/boundary.m` | `(break_, reason, *, by)` |
| `tropical_min` | `+v4cat/tropical_min.m` | `(*, axis_column, witness_kinds, break_, direction)` |
| `tropical_max` | `+v4cat/tropical_max.m` | `(*, axis_column, witness_kinds, break_)` |
| `origin` | `+v4cat/origin.m` | `(break_, *, axis_column='year')` |
| `first_seen` | `+v4cat/first_seen.m` | `(break_)` |
| `status` | `+v4cat/status.m` | `(break_)` |
| `retroactive_gap` | `+v4cat/retroactive_gap.m` | `(break_, *, axis_column='year')` |
| `lineage` | `+v4cat/lineage.m` | `(object_)` |
| `inherited_breaks` | `+v4cat/inherited_breaks.m` | `(object_)` |

Each compiles to a sequence of RISC writes (`v4cat.node`,
`v4cat.edge`) plus an inline structure-of-arrays for any per-spec
attributes that v4cat (Python) currently stores in
`spec_attributes` rows.

## Why deferred from v0.1

The brief's slogan ("Use Octave to make the geometry obvious")
points at the **geometry** -- the kquery + sparse incidence + the
ternary edge structure. CISC sugar is composition, not geometry.
v0.1 ships exactly what the slogan says.

Implementing the sugar entails reproducing v4cat (Python)'s schema
(including spec_attributes, witnesses, lineages tables) in
Octave's struct-of-arrays form. That's a meaningful sub-fire of
its own.

## Future fire

`v4cat-octave-cisc` (single sub-fire, since the verbs share a
common storage substrate). Decomposition by verb-cluster is
acceptable but not required.

## Closure

Closes when v4cat-octave ≥ v0.x exposes all 17 CISC sugar verbs
(16 + `lineage_witness` which v4cat (Python) currently has as a
distinct CISC verb above `edge`). Verified by extending
test_kernel_parity.m to additionally compare each verb's
domain-faithful side effects against v4cat (Python)'s on a
shared fixture.
