# Shadow: Agda extraction gap — termination metadata (Tier 3, item 15)

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows. Region **#4** (S2G
> alone — pure cataloguing).*

## Form

Item **15** of the agda2v4cat extraction kquery 10-cell. agda2v4cat
v0.1 does not surface termination-checker output; the design
surface is named here.

## What to extract

- **Source in Agda**:
  - `funTerminates :: Maybe Bool` field of `FunctionData` in
    `Agda.TypeChecking.Monad.Base` (the typechecked-side flag).
  - `Agda.Termination.TerminationCheck` output (the structured
    pass result) for richer status.
- **Per-definition status**: `Terminating`, `MaybeTerminating`,
  `NonTerminating`, `Inlined`. (`Inlined` because inlined
  functions don't get termination-checked.)

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kind | `agda-termination-status` |
| Edge-kind | `has-termination-status` (def → status) |

The `agda-termination-status` node is one per status-token (4
total), each emitted as a singleton anchor — the per-status union
across all defs in the universe.

## Why deferred from v0.1

Requires either reading the `funTerminates` flag (simple but
post-v0.1) or invoking the termination-check pass output (more
substantial). Not in v0.1's Tier-1+2 surface.

## Future fire

`agda2v4cat-termination` (v0.2 sub-fire — shared with item 16
coverage, since both walk `FunctionData` flags).

## Closure

Closes when agda2v4cat ≥ v0.2 emits one `agda-termination-status`
node per status-value, plus a `has-termination-status` edge per
function-definition.
