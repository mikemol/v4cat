# Audit: workspace state, 2026-05-04

> *S2G-alone fire (region #4 of the shadow-architecture lattice).
> Late-arc audit of the v4cat-oss workspace following the
> algebraic-foundations + carrier-grid trajectory. No DBE forward;
> no RFS extraction; this is pure cataloguing of the structural
> state plus a list of named gap-shadows for future fires.*

## Lattice classification

Region #4 (S2G alone). Empirically rare (≈9% of substantive work
per the trace) — typically used for cotype refreshes and audit-memo
regeneration. This audit is the late-arc S2G-dominant fire predicted
by shadow-architecture's meta-S₃ rotation across multi-arc sessions.

## Aggregate state

| Distribution | Repo | Tests | Role |
| --- | --- | --- | --- |
| v4cat | [v4cat-oss/v4cat](https://github.com/v4cat-oss/v4cat) | 156 | Kernel — RISC ISA + schema + kquery |
| v4cat-mcp | [v4cat-oss/v4cat-mcp](https://github.com/v4cat-oss/v4cat-mcp) | 68 | RPC presentation (Model Context Protocol) |
| vcif | [v4cat-oss/vcif](https://github.com/v4cat-oss/vcif) | 43 | Data-at-rest carrier — JSON Schema substrate |
| vcif-rdf | [v4cat-oss/vcif-rdf](https://github.com/v4cat-oss/vcif-rdf) | 22 | Data-at-rest carrier — RDF/SHACL/SPARQL substrate |
| vcif-hlo | [v4cat-oss/vcif-hlo](https://github.com/v4cat-oss/vcif-hlo) | 58 | Data-at-rest carrier — tensor/OpenHLO substrate |
| v4cat-certify | [v4cat-oss/v4cat-certify](https://github.com/v4cat-oss/v4cat-certify) | 37 | Workspace certification — V₄ closure-check over workspace claims |
| agda2v4cat | [v4cat-oss/agda2v4cat](https://github.com/v4cat-oss/agda2v4cat) | TBD (Haskell + 1 Python smoke-test) | Catalogue source — Agda → VCIF extractor |
| v4cat-octave | [v4cat-oss/v4cat-octave](https://github.com/v4cat-oss/v4cat-octave) | 7 (Octave) + parity-check.sh | Reference carrier — algebraic Octave reimplementation of v4cat's RISC core |
| **Total** | | **~384 + agda2v4cat + 7 (Octave)** | |

Cotype size: 31 shadow_*.md files plus index, audit, methodology files.

## Discipline checks (all passing)

| Rule | Status |
| --- | --- |
| 1. Sideways grid moves are S2G; up-grade extractions are RFS | ✓ |
| 2. Mid-session region-transitions are symmetry-discoveries (not errors) | ✓ |
| 3. Forbidden region #3 (RFS-only) avoided | ✓ — no fire fits |
| 4. Forbidden region #5 (DBE+RFS without S2G) avoided | ✓ — every extraction registered a shadow |
| 5. Recognise region BEFORE acting | ✓ — every fire's plan named its region up front |
| 6. Orbit-saturation refines C7 | ✓ — no `Carrier` / `Profile` / `Substrate` wrapper extracted at three substrate columns |

Coupling discipline:

- v4cat itself: zero runtime deps (kernel cell).
- Each presentation depends on v4cat plus its substrate-specific tooling only.
- No sibling-to-sibling deps. v4cat-mcp, vcif, vcif-rdf, vcif-hlo are mutually independent.
- vcif-hlo lists `vcif` and `vcif-rdf` as *optional* extras (`pip install vcif-hlo[vcif,vcif-rdf]`) for the bridge-load paths only; the core kernels are independent.

Carrier-vs-object discipline:

- vcif: no `eval` / `exec`; no executable fields; safe AST dispatch on `expr['op']`.
- vcif-rdf: 12 RDF carrier predicates only (`vc:source`, `vc:edgeKind`, `vc:target`, `vc:cover`, `vc:cell`, `vc:member`, `vc:identifier`, `vc:label`, `vc:universe`, `vc:leftObserver`, `vc:rightObserver`, `vc:closurePolicy`); no `:foo a rdfs:Property` for object-language items.
- vcif-hlo: strings only at `IdDictionary.intern` / `name` boundaries; no string ops on per-row tensor data.

## Trajectory

Six fires across this trajectory, each with a recorded shadow:

| # | Fire | Region | Shadow file | Issue |
| --- | --- | --- | --- | --- |
| 1 | v4cat ↔ v4cat-mcp split | #8 | shadow_distribution_seam_mcp.md | [methodology#3][m3] |
| 2 | VCIF v0.1 (JSON carrier) | #8 | shadow_vcif_distribution.md | [methodology#4][m4] |
| 3 | Group-theoretic reading | #8 RFS-dominant | shadow_assertion_history_group.md (+6 algebraic-anchor footers) | [v4cat#1][v1] |
| 4 | vcif-rdf v0.1 (RDF carrier) | #8 | (combined into shadow_carrier_grid.md) | [methodology#5][m5] |
| 5 | (depth × substrate) carrier grid | #8 + #4 | shadow_carrier_grid.md + shadow_event_log_gap.md | [v4cat#2][v2] |
| 6 | vcif-hlo v0.1 (tensor carrier) | #8 DBE-dominant | shadow_vcif_hlo_distribution.md + shadow_stablehlo_export_gap.md | [methodology#6][m6] |
| 7 | This audit | **#4 (S2G alone)** | this file | [v4cat#3][v3] |
| 8 | G1 closure (cross-substrate parity tests) | #8 DBE-led | this file (closure section below) | [vcif-hlo#3][h3] |
| 9 | G2 closure (v4cat-certify suite) | #8 | shadow_workspace_certification.md | [methodology#7][m7] |
| 10 | agda2v4cat v0.1 (catalogue source — Agda) | #8 DBE-led | shadow_agda2v4cat_distribution.md + shadow_agda_ffi_gap.md + 10 per-item `shadow_agda_extraction_gap_<item>.md` | [methodology#8][m8] |
| 11 | v4cat-octave v0.1 (reference carrier — Octave) | #8 DBE+RFS+S2G | shadow_v4cat_octave_distribution.md + 5 per-future-fire `shadow_v4cat_octave_<topic>.md` | [methodology#9][m9] |
| 12 | geometric-currying semantic substrate (recognition + 7 migration promissories) | #8 DBE+RFS+S2G recognition-led | shadow_geometric_currying.md + 7 per-repo `shadow_geometric_currying_<repo>.md` + closure-trail update on shadow_event_log_gap.md | [v4cat#4][v4] |
| 13 | epic-shape audit (split gc-v4cat-core into 5 sub-issues; surface 2 orphan promissories; add 2 discipline rules) | #4 (S2G alone) | shadow_workspace_project_tracking.md (extended with promissory-has-issue + epic-shape-recognition rules); Tracking annotations on shadow_event_log_gap.md + shadow_stablehlo_export_gap.md | [v4cat#11][v11] |

[m3]: https://github.com/v4cat-oss/methodology/issues/3
[m4]: https://github.com/v4cat-oss/methodology/issues/4
[m5]: https://github.com/v4cat-oss/methodology/issues/5
[m6]: https://github.com/v4cat-oss/methodology/issues/6
[m7]: https://github.com/v4cat-oss/methodology/issues/7
[m8]: https://github.com/v4cat-oss/methodology/issues/8
[m9]: https://github.com/v4cat-oss/methodology/issues/9
[v1]: https://github.com/v4cat-oss/v4cat/issues/1
[v2]: https://github.com/v4cat-oss/v4cat/issues/2
[v3]: https://github.com/v4cat-oss/v4cat/issues/3
[v4]: https://github.com/v4cat-oss/v4cat/issues/4
[v11]: https://github.com/v4cat-oss/v4cat/issues/11
[h3]: https://github.com/v4cat-oss/vcif-hlo/issues/3

Meta-S₃ rotation observed across the trajectory:

- Early-arc: D-dominant (split design, package design).
- Mid-arc: DRS-triple (the three carrier builds).
- Late-arc: S-dominant (this audit).

The rotation is the textbook empirical pattern from shadow-architecture's empirical 22-commit trace.

## Gap registry — four named follow-up fires

Each gap below names a structural commitment the workspace honours
*by design* but does not yet *test or enforce*. None is a discipline
violation; each is a candidate for a future small fire.

**Status as of 2026-05-04 (later in same session)**: G1 and G2
closed (see below). G3 and G4 remain open. **G5 added** at the
end-of-session agda2v4cat fire.

**Status canonicalised** (2026-05-05): live status for each gap
moved to the [v4cat-oss workspace GH
Project](https://github.com/orgs/v4cat-oss/projects) per
[shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md).
The per-gap structural detail below remains canonical for
structure; the open / closed / in-progress flag is canonical at
the issue. The next audit memo will re-derive its gap registry
by querying the Project's status field rather than maintaining
this prose registry.

### G1 — cross-substrate parity tests ✓ **CLOSED 2026-05-04**

**Tracking**: closure recorded at [v4cat-oss/vcif-hlo#3](https://github.com/v4cat-oss/vcif-hlo/issues/3) (Fire #8 trajectory entry, closed).

**Claim**: a snapshot read from any of {vcif, vcif-rdf, vcif-hlo} and
classified by kquery yields *identical* V₄ cell membership.

**Closure**: implemented at vcif-hlo commit `c0c6d48`. Adds 8
parametrized cross-substrate parity tests in
[vcif-hlo/src/vcif_hlo/tests/test_parity.py](https://github.com/v4cat-oss/vcif-hlo/blob/main/src/vcif_hlo/tests/test_parity.py):

- **Two fixtures**: `PARITY_SYNTHETIC` (4-cell coverage — one
  identifier in each of {00, 01, 10, 11}) and `PARITY_HF_DBE`
  (boundary case — only cell 11 has a member).
- **Three substrate extractors** (`cells_via_vcif`,
  `cells_via_vcif_rdf`, `cells_via_vcif_hlo`), each returning the
  *parity_canonical_form* — `{cell: sorted[str]}` of identifier
  strings.
- **3 pairings × 2 fixtures = 6 pairwise parity tests** plus **2
  all-three convergence tests** = 8 total.
- All 8 pass on first run; vcif-hlo test count rises 50 → 58.

**Shadows produced** (DBE costructure now realised):

- `parity_canonical_form` — the renaming-canonicalised cells dict
  every extractor returns.
- `parity_check_function` — the pairwise comparison pattern.

**Discipline preserved**:

- vcif extractor uses literal-only set_exprs (no `eval`/`exec`).
- vcif-rdf extractor constructs `ex:inSet` as a `vc:NodeAssertion`
  (never as an RDF predicate) — carrier-vs-object discipline holds.
- vcif-hlo extractor passes only `Id` tensors through kernels;
  string conversion happens only at the `IdDictionary` boundary.

### G2 — automated coupling-invariant test ✓ **CLOSED 2026-05-04**

**Tracking**: closure recorded at [v4cat-oss/methodology#7](https://github.com/v4cat-oss/methodology/issues/7) (Fire #9 trajectory entry — v4cat-certify v0.1, closed).

**Claim**: pyproject.tomls never develop sibling-to-sibling
runtime deps. v4cat itself depends on nothing.

**Closure**: implemented at
[v4cat-oss/v4cat-certify](https://github.com/v4cat-oss/v4cat-certify) v0.1
(initial commit `ac80d44`). The placement question (raised in the
DBE pass on G2) was resolved by the user's "certification suite"
counter-framing: the test lives in a *workspace-level* role, not as
a sibling-of-the-carriers concern. The new repo introduces:

- **WorkspaceClaim** + 8 named claims including
  `claim:v4cat-zero-runtime-deps` and
  `claim:no-sibling-runtime-deps` (the original G2 invariants).
- **V₄ closure-report** classifying every claim into
  `{11 honest, 10 uncatalogued, 01 unimplemented, 00 absent}`.
- **Three-substrate emission**: closure-reports in vcif JSON,
  vcif-rdf Turtle, vcif-hlo JSON tensor dump simultaneously, with
  a meta-level cross-substrate parity test verifying the three
  emissions agree.
- **CLI**: `v4cat-certify {run, report, claims, status}`.

**Discipline**: per shadow-architecture rule 6, this is the
**second instance** of the V₄-closure-check pattern (the first
being v4cat's Theorem 14.5). Two instances; below the C7 ≥3
threshold; orbit-driven; **S2G to catalogue, no `ClosureCheck`
wrapper extracted**. v4cat itself remains the universal at the
kernel-cell.

See [shadow_workspace_certification.md](shadow_workspace_certification.md)
for the structural shadow.

37 v4cat-certify tests green. 6 distributions in workspace now;
total tests: 384 across the workspace.

### G3 — bridge round-trip tests for vcif-hlo

**Tracking**: [v4cat-oss/vcif-hlo#2](https://github.com/v4cat-oss/vcif-hlo/issues/2) (status canonical there).

**Claim**: `bridge_v4cat.apply_derive_mask` correctly calls
`cat.edge` per cell-10 row; idempotent on re-application.

**Currently tested**: only `bridge_v4cat.load_node_universe`
([vcif-hlo/test_bridge_v4cat.py](https://github.com/v4cat-oss/vcif-hlo/blob/main/src/vcif_hlo/tests/test_bridge_v4cat.py)),
1 test. The apply side is untouched.

**Future fire**: 2-3 tests covering: (1) `apply_derive_mask` writes
the expected edges; (2) re-apply is idempotent (suppresses
IntegrityError); (3) `apply_derive_pair_mask` over a K=2 universe
works equivalently.

### G4 — examples as test fixtures

**Tracking**: [v4cat-oss/vcif-hlo#1](https://github.com/v4cat-oss/vcif-hlo/issues/1) (status canonical there).

**Claim**: vcif-hlo's three example scripts in `docs/examples/`
work as documented.

**Currently tested**: their underlying recognizer DAGs are unit-
tested via `test_recognizers.py`, but the example scripts
themselves only run via `python docs/examples/<script>.py`.

**Future fire**: small wrapper tests in `test_examples.py` that
import each example as a module and call its `main()`, asserting
no exceptions and verifying key outputs.

### G5 — vcif/v4cat bootstrap gap (NEW, surfaced 2026-05-04 by agda2v4cat)

**Tracking**: [v4cat-oss/methodology#1](https://github.com/v4cat-oss/methodology/issues/1) (status canonical there).

**Claim**: `vcif.apply(doc, catalogue)` works against any
default-bootstrapped `SymmetryCatalogue` without preliminaries.

**Reality**: it doesn't. `vcif.apply` registers each declared
node-kind as a node-of-kind `'node-kind'`, but v4cat's
`framework_seed.sql` does not pre-declare `'node-kind'` as a
node-type, and `v4cat.introduce_node` is strict: any value passed
in the type slot must already be a registered node-type. So
`vcif.apply` immediately fails on the first vocabulary entry —
including on vcif's own `agda-import.json` fixture.

**Discovered by**: agda2v4cat v0.1's end-to-end smoke test
(reproduced on the existing fixture, so the gap is upstream of
agda2v4cat).

**Workaround**: agda2v4cat's smoke test pre-introduces
`'node-kind'`, `'edge-kind'`, and every per-doc vocabulary entry
as a node-type before calling `vcif.apply`.

**Future fire**: small change to `vcif/src/vcif/importer.py` to
dual-register vocabulary entries (first as a node-type, then as a
node-of-kind=`'node-kind'`) plus a one-line addition to
`v4cat/src/v4cat/framework_seed.sql` so `'node-kind'` is
pre-declared symmetrically with `'edge-kind'`.

**Shadow**:
[shadow_v4cat_vcif_bootstrap_gap.md](shadow_v4cat_vcif_bootstrap_gap.md).

## What this audit does NOT do

- **Does not extract a `Carrier` wrapper** above the three substrate
  columns. Per discipline rule 6, the orbit is parameterised; v4cat
  is the universal at the kernel-cell.
- **Does not extract a `MetaTestFramework`** above the three
  per-substrate test suites. Same rule: each substrate has its own
  native test surface; the recurrence is orbit-driven.
- **Does not promote the gaps to immediate fires**. Each is a
  candidate for a future DBE+S2G or DBE+RFS+S2G fire with explicit
  costructure design. This audit *names* them so the catalogue
  thickens forward.

## Snap-to-grid check

User's request: "Audit the entire workspace and apply the four
skills."

Cotype's entailment after this shadow lands:

> The v4cat-oss workspace is structurally sound across all five
> distributions: dependency graph is kernel-and-spokes, no sibling
> coupling, no Carrier wrappers. 339 tests green. Six prior fires
> registered six shadows; this audit is the seventh fire and is
> region #4 (S2G alone) — the textbook late-arc fire. Four named
> gap-shadows surface follow-up work without forcing it now.

Snap valid. The audit's deliverable IS the cotype's awareness of its
own current shape, including the four registered gaps.

## The slogan, applied at the audit level

> The catalogue thickens forward.
> Prior shadows aren't corrected; they're re-derived as the
> trace-set grows.
> The catalogue knows what it knows it doesn't yet know.
