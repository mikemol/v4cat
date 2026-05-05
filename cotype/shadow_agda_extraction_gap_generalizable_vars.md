# Shadow: Agda extraction gap — generalizable variables (Tier 3, item 23)

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows. Region **#4** (S2G
> alone — pure cataloguing).*

## Form

Item **23** of the agda2v4cat extraction kquery 10-cell.
agda2v4cat v0.1 already classifies `Defn`s headed by Agda's
`GeneralizableVar` constructor as `DefGeneralizableVar` and emits
them as `agda-postulate` (via the v0.1 `defKindLabel` collapse —
generalizable vars don't have a dedicated v0.1 node-kind). The
design surface for first-class treatment is named here.

## What to extract

- **Source in Agda**: the `GeneralizableVar` constructor of `Defn`
  in `Agda.TypeChecking.Monad.Base`. Bound via the `variable {...}`
  block in surface Agda; tracked separately on the typechecked
  Definition.
- **Per-variable content**: the `defGeneralizedParams` list on
  `Definition` (which carries the per-arg generalisation status of
  the variable's *consumers*, not the variable itself); plus the
  `defArgGeneralizable :: NumGeneralizableArgs` flag.

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kind | `agda-generalizable-var` |
| Edge-kind | `is-generalizable` (def → kind anchor) |

`agda-generalizable-var` becomes a peer of v0.1's
`agda-function`, `agda-datatype`, etc. — first-class instead of
collapsed under `agda-postulate`.

## Why deferred from v0.1

Generalizable vars are an Agda 2.6+ feature with low frequency in
typical code. The v0.1 `agda-postulate` collapse is honest for the
common case but loses information when the user actually uses
generalisation. Sub-fire-sized.

## Future fire

`agda2v4cat-advanced-defs` (v0.2 sub-fire — shared with items 22
pattern-synonyms and 24 where-clauses).

## Closure

Closes when agda2v4cat ≥ v0.2 emits `agda-generalizable-var`
nodes for each `Defn` headed by `GeneralizableVar`, and replaces
the v0.1 `agda-postulate` collapse for these defs with the
first-class kind.
