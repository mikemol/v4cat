# Shadow: Agda extraction gap — polarity / variance (Tier 3, item 17)

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows. Region **#4** (S2G
> alone — pure cataloguing).*

## Form

Item **17** of the agda2v4cat extraction kquery 10-cell. agda2v4cat
v0.1 emits `agda-modality` for the (Relevance × Quantity ×
Cohesion × Polarity) tuple at each arg position, but the *Polarity*
component is collapsed into the modality string and not given its
own node-kind. The design surface for first-class polarity is
named here.

## What to extract

- **Source in Agda**: `defPolarity :: [Polarity]` field on
  `Definition`. One polarity per argument position (subject to the
  caveat in `Agda.TypeChecking.Monad.Base`'s data declaration:
  excludes dropped parameters to projection-likes / constructors).
- **Polarity values**: `Covariant`, `Contravariant`, `Invariant`,
  `Nonvariant`.

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kind | `agda-polarity` |
| Edge-kind | `has-polarity` (def-arg-position → polarity) |

The `agda-polarity` node is one per polarity-value (4 total),
emitted as a singleton anchor analogous to v0.1's
`agda-arg-visibility` anchors.

## Why deferred from v0.1

Polarity is currently subsumed in v0.1's `agda-modality` strings
(which are the printed `prettyShow` of the full Modality). Giving
polarity its own first-class anchor + edge requires splitting the
modality emission into orthogonal axes — a small but distinct
v0.2 sub-fire.

## Future fire

`agda2v4cat-modalities-deeper` (v0.2 sub-fire — splits the four
modality axes apart so each becomes a first-class anchor with its
own edge-kind).

## Closure

Closes when agda2v4cat ≥ v0.2 emits one `agda-polarity` node per
polarity-value, plus `has-polarity` edges from per-arg-position
nodes. The `agda-modality` collapsing of Polarity into the printed
tuple is then deprecated in favour of the orthogonal-axis form.
