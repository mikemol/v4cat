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
|---|---|---|---|
| v4cat | [v4cat-oss/v4cat](https://github.com/v4cat-oss/v4cat) | 156 | Kernel — RISC ISA + schema + kquery |
| v4cat-mcp | [v4cat-oss/v4cat-mcp](https://github.com/v4cat-oss/v4cat-mcp) | 68 | RPC presentation (Model Context Protocol) |
| vcif | [v4cat-oss/vcif](https://github.com/v4cat-oss/vcif) | 43 | Data-at-rest carrier — JSON Schema substrate |
| vcif-rdf | [v4cat-oss/vcif-rdf](https://github.com/v4cat-oss/vcif-rdf) | 22 | Data-at-rest carrier — RDF/SHACL/SPARQL substrate |
| vcif-hlo | [v4cat-oss/vcif-hlo](https://github.com/v4cat-oss/vcif-hlo) | 50 | Data-at-rest carrier — tensor/OpenHLO substrate |
| **Total** | | **339** | |

Cotype size: 31 shadow_*.md files plus index, audit, methodology files.

## Discipline checks (all passing)

| Rule | Status |
|---|---|
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

| # | Fire | Region | Shadow file |
|---|---|---|---|
| 1 | v4cat ↔ v4cat-mcp split | #8 | shadow_distribution_seam_mcp.md |
| 2 | VCIF v0.1 (JSON carrier) | #8 | shadow_vcif_distribution.md |
| 3 | Group-theoretic reading | #8 RFS-dominant | shadow_assertion_history_group.md (+6 algebraic-anchor footers) |
| 4 | vcif-rdf v0.1 (RDF carrier) | #8 | (combined into shadow_carrier_grid.md) |
| 5 | (depth × substrate) carrier grid | #8 + #4 | shadow_carrier_grid.md + shadow_event_log_gap.md |
| 6 | vcif-hlo v0.1 (tensor carrier) | #8 DBE-dominant | shadow_vcif_hlo_distribution.md + shadow_stablehlo_export_gap.md |
| 7 | This audit | **#4 (S2G alone)** | this file |

Meta-S₃ rotation observed across the trajectory:

- Early-arc: D-dominant (split design, package design).
- Mid-arc: DRS-triple (the three carrier builds).
- Late-arc: S-dominant (this audit).

The rotation is the textbook empirical pattern from shadow-architecture's empirical 22-commit trace.

## Gap registry — four named follow-up fires

Each gap below names a structural commitment the workspace honours
*by design* but does not yet *test or enforce*. None is a discipline
violation; each is a candidate for a future small fire.

### G1 — cross-substrate parity tests

**Claim**: a snapshot read from any of {vcif, vcif-rdf, vcif-hlo} and
classified by kquery yields *identical* V₄ cell membership.

**Currently tested**: vcif↔vcif-hlo, but only at node/edge count
granularity ([vcif-hlo/test_parity.py:51-83](https://github.com/v4cat-oss/vcif-hlo/blob/main/src/vcif_hlo/tests/test_parity.py#L51-L83)).
The two other pairs (vcif↔vcif-rdf, vcif-rdf↔vcif-hlo) and the
all-three convergence are untested.

**Future fire**: a small parameterized test set that:

1. Loads `agda-import` and `hf-dbe-closure` fixtures via each
   substrate's loader.
2. Runs an identical kquery against the same `(A, B; U)` triple in
   each.
3. Asserts cell-membership equality, not just counts.

Lives most cleanly in vcif-hlo (which already has bridges to both
JSON and RDF inputs).

### G2 — automated coupling-invariant test

**Claim**: pyproject.tomls never develop sibling-to-sibling
runtime deps. v4cat itself depends on nothing.

**Currently tested**: nothing. Discipline is enforced by human
audit only.

**Future fire**: a small script that parses all five pyproject.tomls
and asserts: (a) v4cat has no runtime deps; (b) each sibling lists
v4cat plus its substrate-specific libs (no other v4cat-oss/* deps in
the runtime set; optional extras are fine). The test should NOT
live in v4cat itself (kernel doesn't know about presentations).
Cleanest home: a new `v4cat-oss/audit` repo (region #8 fire to
introduce that), or as a script in any one of the presentation
repos that imports the others' metadata.

### G3 — bridge round-trip tests for vcif-hlo

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

**Claim**: vcif-hlo's three example scripts in `docs/examples/`
work as documented.

**Currently tested**: their underlying recognizer DAGs are unit-
tested via `test_recognizers.py`, but the example scripts
themselves only run via `python docs/examples/<script>.py`.

**Future fire**: small wrapper tests in `test_examples.py` that
import each example as a module and call its `main()`, asserting
no exceptions and verifying key outputs.

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
