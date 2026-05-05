# Shadow: Agda extraction gap — pragmas (Tier 3, item 14)

**Tracking**: [v4cat-oss/agda2v4cat#2](https://github.com/v4cat-oss/agda2v4cat/issues/2) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows split out from the
> original consolidated `shadow_agda_extraction_gap_tier3.md` per the
> workspace's per-future-fire shadow convention (mirroring
> `shadow_doc_cleanup_01..06`). At orbit position 1 of the Tier-3
> expansion. Region **#4** (S2G alone — pure cataloguing).*

## Form

Item **14** of the agda2v4cat extraction kquery 10-cell. agda2v4cat
v0.1 does not extract Agda pragmas; the design surface is named
here so a future v0.2 sub-fire picks up from named substructure.

## What to extract

- **Source in Agda**: `Agda.Syntax.Concrete.Pragma`. Pragma
  constructors include `COMPILE`, `INLINE`, `NO_POSITIVITY_CHECK`,
  `NON_TERMINATING`, `STATIC`, `DISPLAY`, `FOREIGN`, `BUILTIN`,
  `OPTIONS`, and others.
- **Where attached**: pragmas are attached to definitions and to
  modules. They appear in concrete syntax pre-typechecking but are
  preserved into the typechecked state.

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kind | `agda-pragma` |
| Edge-kind | `has-pragma` (def → pragma) |
| Plus     | per-pragma payload edges (e.g. `pragma-options-flag`) |

## Why deferred from v0.1

Pragmas live in concrete syntax that v0.1's Tier-1+2 walks don't
touch (those walk `Defn` and `Type`, both internal). Pragma
extraction is a separate AST walk with its own input source. Small
enough to be its own v0.2 sub-fire.

## Future fire

`agda2v4cat-pragmas` (v0.2 sub-fire).

## Closure

Closes when agda2v4cat ≥ v0.2 emits `agda-pragma` nodes for at
least the most-common pragma kinds (`COMPILE`, `INLINE`,
`NO_POSITIVITY_CHECK`, `BUILTIN`, `OPTIONS`) on the existing
fixture modules, with the corresponding `has-pragma` edges from
each affected def. Per the catalogue-thickens-forward discipline,
this shadow is then annotated with the closure trail.
