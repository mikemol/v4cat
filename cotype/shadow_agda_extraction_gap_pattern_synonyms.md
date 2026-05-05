# Shadow: Agda extraction gap — pattern synonyms (Tier 3, item 22)

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows. Region **#4** (S2G
> alone — pure cataloguing).*

## Form

Item **22** of the agda2v4cat extraction kquery 10-cell. agda2v4cat
v0.1 does not extract Agda pattern synonyms (`pattern P x = c x`);
the design surface is named here.

## What to extract

- **Source in Agda**: pattern-synonym declarations land in the
  Definition's `theDef` as a `PatternSynDefn`-shaped record (or as
  an entry in the dedicated pattern-synonym map on `TCState`,
  depending on Agda version — agda2v4cat targets 2.6.3.x).
- **Per-synonym content**: the pattern's argument names + the RHS
  pattern shape (resolves to a constructor head + sub-patterns).

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kind | `agda-pattern-synonym` |
| Edge-kind | `has-pattern-synonym-arg` (synonym → argument) |

The synonym's RHS-target constructor is wired up via
`references-def` (already in v0.1's vocabulary) so no new edge is
needed for that.

## Why deferred from v0.1

Pattern synonyms are a niche but real Agda feature; their AST
extraction requires its own walk over the synonym map (or
`PatternSynDefn` constructors) distinct from v0.1's `Defn` walk.
Sub-fire-sized.

## Future fire

`agda2v4cat-advanced-defs` (v0.2 sub-fire — shared with items 23
generalizable-vars and 24 where-clauses, since all three are
"advanced definition forms" beyond the core Function / Datatype /
Record discrimination).

## Closure

Closes when agda2v4cat ≥ v0.2 emits one `agda-pattern-synonym`
node per declared pattern synonym in the typechecked input, with
`has-pattern-synonym-arg` edges per argument position.
