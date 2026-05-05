# Shadow: Agda extraction gap — mutual blocks (Tier 3, item 25)

**Tracking**: [v4cat-oss/agda2v4cat#11](https://github.com/v4cat-oss/agda2v4cat/issues/11) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows. Region **#4** (S2G
> alone — pure cataloguing).*

## Form

Item **25** of the agda2v4cat extraction kquery 10-cell. agda2v4cat
v0.1 emits `references-def` edges that include cross-references
between mutually-recursive defs (e.g. `even` references `odd` and
vice versa), but it does **not** record the *mutual block* itself
as a structural unit. The design surface is named here.

## What to extract

- **Source in Agda**: each `Definition` carries `defMutual ::
  MutualId`. Defs sharing a `MutualId` belong to the same mutual
  block. The `_funMutual :: Maybe [QName]` field on
  `FunctionData` carries the mutually-recursive partners
  (post-positivity-check).
- **Per-block content**: the `MutualId` + the set of `QName`s in
  the block. Optionally: an "orientation" indicating whether the
  block was user-declared (`mutual { ... }`) or
  inferred/promoted.

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kind | `agda-mutual-block` |
| Edge-kind | `in-mutual-block` (def → block) |

The `agda-mutual-block` node groups all defs sharing a `MutualId`;
the `in-mutual-block` edge is a per-def membership statement (so
querying "give me everything in the same mutual block as X" is a
two-hop kquery: X → block → members).

## Why deferred from v0.1

Mutual-block extraction requires building the `MutualId`-keyed
groupings across **all** defs before emission — a phase that
v0.1's per-def serialisation doesn't naturally accommodate.
Sub-fire-sized.

## Future fire

`agda2v4cat-mutual` (v0.2 sub-fire — single-item, since the
grouping pass is its own concern).

## Closure

Closes when agda2v4cat ≥ v0.2 emits one `agda-mutual-block` node
per distinct `MutualId` present in a module, with `in-mutual-block`
edges from each member def. Singleton mutual blocks (the common
case) may either be elided or emitted uniformly — that choice is
itself a small design point of the v0.2 fire.
