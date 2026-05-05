# Shadow: Agda extraction gap — coverage check status (Tier 3, item 16)

**Tracking**: [v4cat-oss/agda2v4cat#4](https://github.com/v4cat-oss/agda2v4cat/issues/4) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows. Region **#4** (S2G
> alone — pure cataloguing).*

## Form

Item **16** of the agda2v4cat extraction kquery 10-cell. agda2v4cat
v0.1 does not surface coverage-checker output; the design surface
is named here.

## What to extract

- **Source in Agda**: `_funCovering :: [Clause]` field of
  `FunctionData` (covering clauses computed by the coverage
  checker).
- **Coverage status**: presence/absence + the covering-clause
  count. Optionally: the structural relationship between
  user-written clauses and synthesised covering clauses.

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kind | `agda-coverage-status` |
| Edge-kind | `has-coverage-status` (def → status) |

`agda-coverage-status` distinguishes at minimum `Covers` vs
`UnCovers` (the latter for partial functions, whose coverage check
fails or was suppressed).

## Why deferred from v0.1

The coverage flag is simple to read but its meaning depends on
which clauses are user-written vs synthesised — extracting that
relationship is a separate walk over `funCovering` vs `funClauses`.
Not in v0.1's Tier-1+2 surface.

## Future fire

`agda2v4cat-termination` (v0.2 sub-fire — shared with item 15
termination, since both walk `FunctionData` flags).

## Closure

Closes when agda2v4cat ≥ v0.2 emits one `agda-coverage-status`
edge per function-definition, with at minimum the binary
covers/doesn't-cover distinction.
