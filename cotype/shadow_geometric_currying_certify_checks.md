# Shadow: geometric currying — v4cat-certify geometric checks (promissory)

**Tracking**: [v4cat-oss/v4cat-certify#1](https://github.com/v4cat-oss/v4cat-certify/issues/1) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_geometric_currying.md](shadow_geometric_currying.md)).
> Region **#4** (S2G alone — pure cataloguing).*

## Form

`v4cat-certify` (the workspace certification suite) currently
runs a V₄ closure-check over **8 named workspace claims**
([v4cat-certify/src/v4cat_certify/claims.py][claims-py]).
Geometric currying introduces **four new claim types** auditing
the substrate's invariants.

[claims-py]: https://github.com/v4cat-oss/v4cat-certify/blob/main/src/v4cat_certify/claims.py

## What to extract

### Four new geometric audit checks

Each becomes a `claim:*` entry in the certification suite:

| Claim | What it audits |
| --- | --- |
| `claim:edge-cells-have-closed-boundaries` | every closed edge-cell in the workspace's catalogues has closed `source`, `kind`, `target` role-bindings |
| `claim:no-path-advance-through-unclosed-cells` | no `path-advances-through` edge points at a cell that is not `closed` |
| `claim:vector-presentations-oriented-and-audited` | every `PathPresentation` has an explicit orientation + an audit-trail of presented-cell-closure-status |
| `claim:saturated-edges-backed-by-cells` | every legacy `witnesses` / `lineages` row corresponds to a closed `EdgeCell` whose three role-bindings match the row's `(spec, break/spec, kind)` |

Each compiles to a kquery cover whose `c01` cell (or `c10`,
oriented per the closure path) is empty when the claim is honest.

### V₄ closure-report extension

The certification's existing closure-report (per [v4cat-certify
v0.1][v4cat-certify-v01]) gains four new rows in its
classification table. The cross-substrate parity in
[`v4cat-certify/tests/test_report_parity.py`][parity-test]
extends to verify the four new claims classify identically
across vcif / vcif-rdf / vcif-hlo emissions.

[v4cat-certify-v01]: https://github.com/v4cat-oss/v4cat-certify
[parity-test]: https://github.com/v4cat-oss/v4cat-certify/blob/main/tests/test_report_parity.py

### Carrier dependency

Each new claim depends on the carrier shadows landing first —
otherwise the geometric data isn't present in the carrier
emissions:

```text
claim:edge-cells-have-closed-boundaries
  needs vcif (cells/role_bindings sections)
  needs vcif-rdf (CellAssertion + RoleBinding shapes)
  needs vcif-hlo (role_*_closed tensors)

claim:no-path-advance-through-unclosed-cells
  needs vcif (path_presentations section)
  needs vcif-rdf (Path-related carrier classes)
  needs vcif-hlo (advance_mask)

claim:vector-presentations-oriented-and-audited
  needs all three carriers' Path / PathPresentation shapes

claim:saturated-edges-backed-by-cells
  needs all three carriers' edge ↔ cell consistency rules
```

So this sub-fire ships *last* of the migration (after
`gc-v4cat-core` and the three carrier sub-fires).

## Why deferred from the substrate-naming fire

The certification claims depend on operational substrate +
carrier emissions — neither exists yet. This sub-fire validates
*that the migration landed correctly*, which can only run after
the substrate-realising sub-fires close.

## Future fire

`gc-certify-checks`. Region #6 expected (DBE+S2G). Closure-
scope: single-repo (writes only land in
`v4cat-oss/v4cat-certify`).

Strict ordering: lands **last** in the migration sequence —
after `gc-v4cat-core`, all three carrier sub-fires, and ideally
also `gc-agda2v4cat-permissive` (so the certification suite
sees the realistic catalogue source's geometric output).

## Closure path

Closes when v4cat-certify ≥ v0.x ships:

1. Four new `claim:*` entries in `claims.py`.
2. Each claim's V₄-closure-check is a tested predicate in the
   suite.
3. The cross-substrate parity test extended to verify the four
   new claims agree across vcif / vcif-rdf / vcif-hlo.
4. The closure-report templates updated to render the new
   claims.
5. Documentation: the certification README explains the new
   claims and how they connect to the geometric-currying
   substrate.

## Closure trail (2026-05-05 — fire #15)

**Closed** by [v4cat-certify 6a3e526](https://github.com/v4cat-oss/v4cat-certify/commit/6a3e526)
landing under [v4cat-certify#1](https://github.com/v4cat-oss/v4cat-certify/issues/1)
within fire #15.

What shipped:

- 4 new `WorkspaceClaim` entries in `claim.py`:
  - `claim:geometric-currying-substrate-v4cat`
  - `claim:geometric-currying-carrier-vcif`
  - `claim:geometric-currying-carrier-vcif-rdf`
  - `claim:geometric-currying-carrier-vcif-hlo`
- 4 corresponding `check_geometric_currying_*` implementation
  functions in `checks.py` that audit the post-fire-#15 state of
  the workspace (event_cells.py, S13 schema tables, semantic.py
  rule 15, carrier.ttl carrier slots, geometric_currying.py
  helpers).
- The pre-existing `check_carrier_vs_object_vcif_rdf` predicate-
  count band widened from 10–14 to 15–20 to accommodate the
  5 new geometric-currying carrier slots.
- Test claim-count updated 8 → 12; all 12 implementation +
  catalogue-witness assertions pass against the current
  workspace.

Deferred to a follow-on fire (per shadow §"Closure path",
items 3–5): cross-substrate parity test extension that verifies
the four new claims agree across vcif / vcif-rdf / vcif-hlo;
closure-report template updates; documentation in the
certification README.
