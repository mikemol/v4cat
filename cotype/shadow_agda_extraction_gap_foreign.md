# Shadow: Agda extraction gap — foreign declarations (Tier 3, item 20)

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows. Region **#4** (S2G
> alone — pure cataloguing).*

## Form

Item **20** of the agda2v4cat extraction kquery 10-cell. agda2v4cat
v0.1 does not extract Agda's `FOREIGN` blocks (raw target-language
code attached to a backend); the design surface is named here.

## What to extract

- **Source in Agda**: the foreign-block stash maintained on the
  `TCState` (look up `Foreign` in
  `Agda.TypeChecking.Monad.Base`). Each backend (e.g. `MAlonzo`,
  `JS`) has its own bucket of raw code-strings.
- **Per-block content**: the backend-name + raw foreign code
  string + (optionally) the source-range that produced it.

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kind | `agda-foreign-block` |
| Edge-kind | `has-foreign-binding` (module → foreign-block) |

The `agda-foreign-block`'s label may carry the backend-name; the
raw code-string belongs in an `attrs` payload (preserved
verbatim, never re-parsed).

## Why deferred from v0.1

The `Foreign` stash is a backend-specific data store, distinct
from per-definition `Defn` walking. Extracting it requires a
separate `useTC` over `stImports`/`stForeign` lenses. Small enough
to share a v0.2 sub-fire with item 21 (import directives).

## Future fire

`agda2v4cat-foreign-and-imports` (v0.2 sub-fire — shared with
item 21 since both walk module-level non-`Defn` state).

## Closure

Closes when agda2v4cat ≥ v0.2 emits an `agda-foreign-block` node
per (module, backend) tuple containing foreign code, with the raw
code carried in `attrs` and a `has-foreign-binding` edge from the
module to each block.
