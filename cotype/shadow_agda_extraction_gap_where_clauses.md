# Shadow: Agda extraction gap — where-clause local definitions (Tier 3, item 24)

**Tracking**: [v4cat-oss/agda2v4cat#10](https://github.com/v4cat-oss/agda2v4cat/issues/10) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows. Region **#4** (S2G
> alone — pure cataloguing).*

## Form

Item **24** of the agda2v4cat extraction kquery 10-cell.
agda2v4cat v0.1 walks `funClauses` and extracts pattern + RHS
references, but it does **not** descend into a clause's
where-clause local definitions; the design surface is named here.

## What to extract

- **Source in Agda**: the `Clause` record carries
  `clauseWhereModule :: Maybe ModuleName`. The where-clause local
  definitions are anonymous `QName`s belonging to that module,
  reachable via the standard typechecked `Definition` lookup.
- **Per-where-defn content**: nested anonymous `QName`s
  introduced inside `Clause` / `clauseTel`; each carries its own
  `Defn` like a normal definition.

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kind | `agda-where-defn` |
| Edge-kind | `has-where-defn` (clause → where-defn) |

`agda-where-defn` is a peer of `agda-clause` / `agda-pattern`
already in v0.1, attached to the parent clause via the new edge.

## Why deferred from v0.1

Walking where-clauses requires recursing through `clauseWhereModule`
to look up the introduced names — a separate hop beyond v0.1's
flat `funClauses` walk. The Agda compiler's MAlonzo backend
demonstrates the approach (it inlines/lifts where-defns); v0.2
would replicate the lookup but emit nodes rather than inlining.

## Future fire

`agda2v4cat-advanced-defs` (v0.2 sub-fire — shared with items 22
pattern-synonyms and 23 generalizable-vars).

## Closure

Closes when agda2v4cat ≥ v0.2 emits `agda-where-defn` nodes for
each anonymous `QName` introduced by a clause's where-block, with
`has-where-defn` edges from the parent clause node.
