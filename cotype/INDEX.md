# cotype/ — accumulated shadows of v4cat-as-deliverable

This directory accumulates externalised shadows of v4cat itself,
treated as a self-hosted artefact (Theorem 14.5). Produced by the
`decomposable-by-entailment` fire of 2026-05-02; updated by
`regroup-from-shadows` and `snap-to-grid` fires thereafter.

A shadow here is a *named substructure of v4cat-as-goal* that
survives session boundaries. Each shadow entry states: (1) the
form, (2) where the form is realised in the repo, (3) the
composition operation that assembles instances into the whole, and
(4) the entailment claim that licenses the composition.

The fact that this directory is itself a v4cat-shaped artefact
(named substructures + closure claim) is the framework's design
intent at theory.md § 14: v4cat's deliverable IS the application
of v4cat to v4cat.

## Shadows (DBE fire, 2026-05-02)

- [shadow_cell.md](shadow_cell.md) — the unit of decomposition;
  every primitive is a `Cell(id, kind, desc)`.
- [shadow_dual_representation.md](shadow_dual_representation.md) —
  every primitive has paired IMPL (theory.py) and CAT
  (framework_seed.sql) realisations.
- [shadow_kind_stratification.md](shadow_kind_stratification.md) —
  the 8-way `O,B,W,R,E,A,K,X` partition (Definition 14.1) plus the
  `supported_kinds` refinement that carves scope.
- [shadow_kquery_universal_read.md](shadow_kquery_universal_read.md)
  — kquery as the level-0 read primitive; ≥7 named call sites.
- [shadow_layered_stack.md](shadow_layered_stack.md) — the L0→L7
  entailment chain from kquery up to docs.
- [shadow_docs_quartet.md](shadow_docs_quartet.md) — the
  README/tutorial/methodology/theory progression plus examples.

## Findings (RFS fire, 2026-05-02)

- [rfs_findings.md](rfs_findings.md) — sideways read against the
  six DBE shadows. Four findings, classified per
  shadow-architecture's orbit-saturation rule. One acted-on (RFS
  extraction: views.py duplication removed); three deferred to S2G.

## Shadows + classifications (S2G fire, 2026-05-02)

- [shadow_kquery_orbit.md](shadow_kquery_orbit.md) — the 6 named
  selections of kquery as orbit positions of a saturated orbit;
  Kind.K, not Kind.A.
- [s2g_classifications.md](s2g_classifications.md) — resolutions
  for the three RFS deferrals. Notably *corrects* RFS's "Kind.A
  vestigial" reading: theory.md reserves Kind.A for the
  bicategorical 2-cell lift (§14.6.5) and as the under-promising
  example (§14.6.1), so the slot is deliberately empty, not dead.
- [snap_report.md](snap_report.md) — snap-to-grid check against
  the 2026-05-02 user request. Snap occurred; deliverable
  readable.

## Audits

- [audit_processor_bias.md](audit_processor_bias.md) — removal
  of CPU-ISA bias inherited from the parent processor catalogue.
  Code is fully de-biased; surface docs (README) updated;
  methodology/theory/tutorial deferred for a follow-up pass.

## Doc-discipline analysis (2026-05-03 fire)

- [shadow_doc_discipline.md](shadow_doc_discipline.md) —
  DBE output: criteria for clean / clear / elegant docs.
  Costructure (graded-narrative-doc), composition (depth-graded
  ladder threading), entailment (G1–G5 + threading rules ⟹
  clean ∧ clear ∧ elegant). Reusable for future doc-set audits.
- [rfs_findings_doc_discipline.md](rfs_findings_doc_discipline.md)
  — RFS findings: 9 violations of the discipline criteria across
  the 5 user-facing docs, classified into 3 severity groups.
  Group A (HIGH): Shape-1 appendage style at 3 docs + dual
  narrative on tensions. Group B (MEDIUM): README missing (β),
  cotype invisible from shallow grades, no grade signposting.
  Group C (LOW): minor terminology drift. Recomposition
  feasibility verified across 6 external commitments.
- [snap_report_doc_discipline.md](snap_report_doc_discipline.md)
  — S2G snap on the doc-discipline analysis. 6 inter-shadow
  quotients including the **deep additive-monoid quotient**:
  the doc-cleanup recomposition has the same shape as the
  code migration plan (5 ordered additive operations
  preserving external commitments). The framework's
  additive-monoid composition discipline is substrate-
  independent.
- [shadow_doc_cleanup_plan.md](shadow_doc_cleanup_plan.md) —
  ordered additive composition of 6 doc-cleanup steps realising
  shadow_doc_discipline.md's criteria; structural analogue of
  shadow_migration_plan.md (per the deep quotient). Dependency
  partial order: D₁ (theory) → D₂ (methodology) → D₃ (tutorial)
  → D₄ (README); D₅ (examples) depends on D₂; D₆ (signposting)
  depends on D₁–D₅. Each prefix is a valid resting state.

### Doc-cleanup step shadows (per-step DBE outputs — all complete)

- [shadow_doc_cleanup_01_theory_integration.md](shadow_doc_cleanup_01_theory_integration.md)
  — **D₁ COMPLETE.** § 14.9 absorbed into § 14.5 as new § 14.5.8;
  strengthened Theorem 14.5 is now the canonical statement.
- [shadow_doc_cleanup_02_methodology_reframe.md](shadow_doc_cleanup_02_methodology_reframe.md)
  — **D₂ COMPLETE.** Headline list items 4 + 6 reframed; ISA
  section restructured (RISC primitives lead, CISC documented as
  sugar with reductions); modal verbs labelled as orbit-elements
  of WITNESS; trailing (β) appendage deleted.
- [shadow_doc_cleanup_03_tutorial_reorder.md](shadow_doc_cleanup_03_tutorial_reorder.md)
  — **D₃ COMPLETE.** § 2 reframed to "Three RISC primitives + named
  conveniences"; § 14 retained but reframed from appendage to
  natural deep section; TOC updated; tables aligned.
- [shadow_doc_cleanup_04_readme_overview.md](shadow_doc_cleanup_04_readme_overview.md)
  — **D₄ COMPLETE.** First paragraph leads with RISC core +
  closure-check reference; cotype/ surfaced as architectural
  source-of-truth; Documentation list gains cotype/ entry.
- [shadow_doc_cleanup_05_examples_minor.md](shadow_doc_cleanup_05_examples_minor.md)
  — **D₅ COMPLETE.** Top blockquote reframed; date marker removed;
  cross-refs updated to post-D₃ tutorial § 14.
- [shadow_doc_cleanup_06_signposting.md](shadow_doc_cleanup_06_signposting.md)
  — **D₆ COMPLETE — DOC-CLEANUP FULLY REALISED.** 3-line grade
  preamble added to all 5 user-facing docs; depth-graded ladder
  is now signposted in the surface; cotype/ reachable from
  every grade.

  **All six doc-cleanup steps complete. The doc-set satisfies
  G1–G5 of shadow_doc_discipline.md; no "added 2026-05-03"
  markers remain in user-facing docs (their content absorbed
  into canonical narratives; migration history preserved in
  cotype/); 189/189 tests green; closure check passes.**

## Forward shadows (architectural commitments not yet realised)

- [shadow_risc_core.md](shadow_risc_core.md) — RISC compression
  to 3 verbs (`introduce_node`, `edge`, `kquery`) with
  self-hosted type system; tensions as named curry-spec ASTs
  over kquery; CISC reduction table for every existing verb;
  Theorem 14.5 strengthening to closure-plus-self-coherence.
  Captures the architecture; migration is staged and additive.
- [shadow_migration_plan.md](shadow_migration_plan.md) — ordered
  additive composition of 5 step-shadows realising
  shadow_risc_core; each step is an orbit-element of the
  project's existing additive-move discipline (anti-pattern +
  Theorem 14.5), no new abstraction needed; partial-order
  dependency `S₁ → S₂ → S₃ → S₄`, S₅ parallel-or-after.

### Step shadows (per-step DBE outputs, generated as steps begin)

- [shadow_migration_01_schema_seed.md](shadow_migration_01_schema_seed.md)
  — **S₁ COMPLETE.** `tensions` schema gained `disposition` /
  `parameters_json` / `shape_json` columns; `framework_seed.sql`
  gained the type-system seed (5 node-type tokens, 17 edge-kind
  tokens, 10 attribute-schema breaks, type-relation
  `spec_attributes`, `requires-attr`/`admits-attr` witness edges).
  All 169 tests pass; closure check unchanged (new rows fall
  outside the (impl_ids, cat_ids) sets).
- [shadow_migration_02_risc_dispatch.md](shadow_migration_02_risc_dispatch.md)
  — **S₂ COMPLETE.** New module `src/v4cat/curry.py` (curry-spec
  AST + evaluator). New methods on `SymmetryCatalogue`:
  `introduce_node`, `edge`, `evaluate_tension`. Validation reads
  the S₁ seed via SQL; `kind`'s target-type catalogues to
  witnesses/lineages dispatch; type/attr-schema enforcement
  active. 15 new RISC tests pass; full suite **184/184 green**.
- [shadow_migration_03_cisc_redirect.md](shadow_migration_03_cisc_redirect.md)
  — **S₃ COMPLETE.** Every CISC verb's body redirected to RISC
  primitives when the type-system seed is loaded; legacy
  direct-INSERT path retained as fallback for
  `check_self_hosting=False`. `lineage_witness` surfaces as new
  public sugar; `defer`/`promote`/`boundary` inherit the
  redirect through `witness` (orbit-elements per discipline rule
  6, no code change). `refine` decomposed to RISC composition
  (`introduce_node` + `edge` × 2) with `refinements` table
  dual-writing for backwards compat. The (β) semantic — that
  refinement-names are first-class breaks — is now realised in
  the witness graph; one legacy test (`test_top_originators`)
  updated to reflect that beta originates F2 + foo-extension +
  baz-extension under (β). Full suite **184/184 green**.
- [shadow_migration_04_signature_reclassify.md](shadow_migration_04_signature_reclassify.md)
  — **S₄ COMPLETE.** `Cell` gained `derives_from`; SIGNATURE
  now distinguishes 3 RISC primitives (`introduce_node`, `edge`,
  `kquery`) from 11 CISC sugar cells with explicit reduction
  chains. New SIGNATURE cells (`introduce_node`, `edge`,
  `lineage_witness`) and matching CAT entries in
  `framework_seed.sql` keep IMPL ↔ CAT gap empty. Closure check
  strengthened with `check_risc_discipline()` — verifies every
  `derives_from` chain terminates in RISC cells (raises
  `RiscDisciplineViolation` for dangling refs or cycles).
  Theorem 14.5 now closes over the smaller {RISC} primitive set
  with the discipline-coherence invariant as additional
  predicate — a stronger claim than the pre-S₄ closure. 5 new
  RISC discipline tests; full suite **189/189 green**.
- [shadow_migration_05_doc_pass.md](shadow_migration_05_doc_pass.md)
  — **S₅ COMPLETE — MIGRATION FULLY REALISED.** Doc pass adds
  (β) reframe sections to all four core docs: methodology.md
  ("(β) RISC reframe" — primitive table, disposition spectrum,
  refinements-as-breaks, schema-witness vocabulary, strengthened
  closure), theory.md (§ 14.9 "(β) RISC strengthening of
  Theorem 14.5"), tutorial.md (§ 14 "Using the RISC primitives
  directly" with RISC equivalents for §§ 1–13), examples.md
  (brief (β) note + cross-references). Existing prose unchanged
  — additive doc discipline. 189/189 tests still green.

  **All five migration steps complete. The (β) RISC reframe
  documented in shadow_risc_core.md is fully realised in code,
  schema, seed, signature, closure check, and docs.**

## Findings (RFS fire, 2026-05-03)

- [rfs_findings_risc_projection.md](rfs_findings_risc_projection.md)
  — sideways read mapping every existing-code candidate to its
  shadow position. 10 findings: 4 RFS extractions
  (`introduce_node`, `edge`, `refine`-rewrite, `Tension`), 3
  orbit-S2G cataloguings (`defer/promote/boundary`,
  `tropical_min/_max`, `origin/first_seen/retroactive_gap`), 3
  already-aligned/additive (`kquery`, MCP wrappers, `Cell`
  field). Recomposition feasibility verified across all 7
  external commitments.

## Shadows + classifications (S2G fire, 2026-05-03)

- [snap_report_risc_projection.md](snap_report_risc_projection.md)
  — snap-to-grid check against the 2026-05-03 user request to
  apply the four skills. Snap occurred; cotype's entailment
  consistent with the request and slightly more informative
  (5 inter-shadow quotients identified that connect the new
  architecture to the existing shadow library).

## Distribution seam (DBE+RFS+S2G fire, 2026-05-04)

- [shadow_distribution_seam_mcp.md](shadow_distribution_seam_mcp.md)
  — the MCP server moved out of v4cat into a sibling distribution
  `v4cat-mcp` (repo `v4cat-oss/v4cat-mcp`). The seam runs at the
  import boundary; the catalogue's identity is unchanged. Region
  #8 fire (all three skills active); sequential rotation across
  three commits. v4cat-side tests pass with `mcp` uninstalled;
  v4cat-mcp-side tests pass against the installed v4cat package.

- [shadow_vcif_distribution.md](shadow_vcif_distribution.md) — the
  VCIF interchange format lands as a second sibling distribution
  `vcif` (repo `v4cat-oss/vcif`), data-at-rest counterpart to
  v4cat-mcp's RPC presentation. Region #8 fire; DBE-heavy, light
  RFS (re-grouping methodology.md's existing JSON example), S2G
  registers the second presentation row. Two presentation seams
  now exist; below the ≥3-instance threshold for RFS-extraction of
  a universal `PresentationDistribution` record. 43 vcif tests
  green.

## Algebraic foundations (DBE+RFS+S2G fire, 2026-05-04 cont'd)

- [shadow_assertion_history_group.md](shadow_assertion_history_group.md)
  — the structural shadow companion to [theory.md § 15](../src/v4cat/theory.md).
  Names the universal at the assertion-axis: v4cat is a free-abelian
  assertion-history group action `H = ℤ^𝔄`; the visible catalogue
  is the support quotient `π(H)`; `kquery` is the V₄-equivariant
  coordinate chart of the observer-pair group `V₄^U`. The slogan:
  **RISC writes are translations; kquery is the V₄ coordinate
  chart.** Region #8 fire, **RFS-dominant** — six prior shadows
  acquire "Algebraic anchor" footers: shadow_kquery_universal_read,
  shadow_kquery_orbit, shadow_layered_stack,
  shadow_distribution_seam_mcp, shadow_vcif_distribution,
  shadow_risc_core. No prior shadow is invalidated; the catalogue
  thickens forward.

- [shadow_carrier_grid.md](shadow_carrier_grid.md) — names the
  (depth × substrate) carrier grid. Vertical axis: projection-depth
  (operation-log < snapshot < V₄-cover < residue). Horizontal
  axis: substrate (JSON × RDF × …). Two columns now filled:
  [v4cat-oss/vcif](https://github.com/v4cat-oss/vcif) (JSON) and
  [v4cat-oss/vcif-rdf](https://github.com/v4cat-oss/vcif-rdf)
  (RDF/SHACL/SPARQL). v4cat sits at the centre as the universal;
  every grid cell is a co-projection of v4cat parameterised by
  (depth, substrate). Per discipline rule 6: no `Carrier` wrapper
  extracted at any number of filled cells.

- [shadow_event_log_gap.md](shadow_event_log_gap.md) — promissory
  cell. v4cat does not yet expose an explicit event-log API;
  the patch profile (in vcif and vcif-rdf) is therefore
  theoretically group-faithful but operationally downgraded until
  the event-log surface ships. Region #4 (S2G alone) — registers
  the gap, no v4cat code change this turn.

- [shadow_vcif_hlo_distribution.md](shadow_vcif_hlo_distribution.md)
  — third substrate column (tensor / OpenHLO). v4cat's RISC
  operations compile to branchless tensor DAGs over interned
  identity IDs: `cell_code = 2·A_live + B_live`. Realised at
  [v4cat-oss/vcif-hlo](https://github.com/v4cat-oss/vcif-hlo) v0.1
  with NumPy backend; JAX + StableHLO export available as an
  optional path. Region #8 fire, **DBE-dominant** — the tensor types
  (ReferentUniverseTensor, CoverTensor) are genuinely new costructure.
  Discipline rule 6: at three substrate columns we still do *not*
  extract a `Carrier` wrapper; v4cat remains the universal at the
  kernel-cell. 50 vcif-hlo tests green; cross-substrate parity with
  vcif demonstrated.

- [shadow_stablehlo_export_gap.md](shadow_stablehlo_export_gap.md)
  — promissory cell. vcif-hlo ships NumPy-only in v0.1; the
  StableHLO export path via `jax.export` exists in principle but is
  not yet exercised. Region #4 (S2G alone) — registers the gap;
  closes when vcif-hlo>=0.2 ships `compile_to_stablehlo`.

## Workspace audit (S2G-alone fire, 2026-05-04 cont'd)

- [audit_workspace_2026_05_04.md](audit_workspace_2026_05_04.md) —
  late-arc audit fire. Region #4 (S2G alone) — pure cataloguing;
  no DBE forward, no RFS extraction. Confirms structural
  soundness across all five distributions (339 tests green; no
  sibling deps; no `Carrier` wrapper at three substrate columns;
  carrier-vs-object discipline honoured everywhere). Names four
  gap-shadows as candidates for future small fires (G1: cross-
  substrate parity tests; G2: automated coupling-invariant test;
  G3: vcif-hlo bridge round-trip tests; G4: examples as test
  fixtures). The catalogue thickens forward by registering what
  the catalogue knows it doesn't yet test. **G1 and G2 closed in
  same session; G3 and G4 remain open.**

- [shadow_workspace_certification.md](shadow_workspace_certification.md)
  — closes G2 by introducing
  [v4cat-oss/v4cat-certify](https://github.com/v4cat-oss/v4cat-certify) v0.1.
  The **second instance** of v4cat's V₄-closure-check pattern
  (Theorem 14.5), lifted from framework-internal scope to
  workspace-wide scope. 8 declared workspace claims, all
  classified into cell 11 by the runner. Closure-report emitted
  in all three carrier substrates simultaneously; cross-substrate
  parity verified at the meta level (the certification suite is
  itself certified across substrates). Region #8 fire,
  DBE-dominant. Per discipline rule 6: at 2 instances of the
  V₄-closure-check pattern, no `ClosureCheck` wrapper extracted;
  v4cat remains the universal at the kernel-cell.

## Catalogue sources (DBE+RFS+S2G fire, 2026-05-04)

A new role distinct from kernel / RPC / carriers / certification:
**catalogue source** — produces VCIF documents from a domain.

- [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)
  — first instance of the catalogue-source role, realised at
  [v4cat-oss/agda2v4cat](https://github.com/v4cat-oss/agda2v4cat).
  An Agda backend (Haskell, cabal-built, mise-pinned to
  `cabal 3.10.3.0` + system `/usr/bin/ghc-9.6.6` + Agda library
  `>=2.6.3 && <2.6.4`) that walks every typechecked definition
  and emits a `v4cat.snapshot` profile JSON document per Agda
  module. v0.1 covers Tier 1 + Tier 2 of the kquery 10-cell
  against vcif's existing `agda-import.json` fixture (15 of 25
  named items); 19 node-kinds, 18 edge-kinds; bijective slug
  encoding for non-ID-safe Agda identifiers. Region #8 fire,
  DBE-led. Per discipline rule 6: at orbit position 1, no
  `DomainExtractor` wrapper extracted; v4cat remains the
  universal at the kernel-cell.

- [shadow_agda_ffi_gap.md](shadow_agda_ffi_gap.md) — promissory
  cell. Agda code calling into v4cat at runtime (FFI) is the
  v0.2 deliverable; v0.1 ships export-only. Region #4 (S2G
  alone). Closes when agda2v4cat ≥ v0.2 ships an `Agda2V4cat.FFI`
  module + Agda-side `V4cat` library.

- Tier-3 extraction gap shadows — ten per-item promissory cells
  for the deferred extraction items. Each names its source-in-Agda,
  its expected node-kind, and its expected edge-kind, so a future
  v0.x sub-fire picks up from named substructure. Region #4 (S2G
  alone). Closes incrementally; future-fire grouping suggested in
  each shadow:
  - [shadow_agda_extraction_gap_pragmas.md](shadow_agda_extraction_gap_pragmas.md) (item 14)
  - [shadow_agda_extraction_gap_termination.md](shadow_agda_extraction_gap_termination.md) (item 15)
  - [shadow_agda_extraction_gap_coverage.md](shadow_agda_extraction_gap_coverage.md) (item 16)
  - [shadow_agda_extraction_gap_polarity.md](shadow_agda_extraction_gap_polarity.md) (item 17)
  - [shadow_agda_extraction_gap_foreign.md](shadow_agda_extraction_gap_foreign.md) (item 20)
  - [shadow_agda_extraction_gap_import_directives.md](shadow_agda_extraction_gap_import_directives.md) (item 21)
  - [shadow_agda_extraction_gap_pattern_synonyms.md](shadow_agda_extraction_gap_pattern_synonyms.md) (item 22)
  - [shadow_agda_extraction_gap_generalizable_vars.md](shadow_agda_extraction_gap_generalizable_vars.md) (item 23)
  - [shadow_agda_extraction_gap_where_clauses.md](shadow_agda_extraction_gap_where_clauses.md) (item 24)
  - [shadow_agda_extraction_gap_mutual_blocks.md](shadow_agda_extraction_gap_mutual_blocks.md) (item 25)

- [shadow_v4cat_vcif_bootstrap_gap.md](shadow_v4cat_vcif_bootstrap_gap.md)
  — G5 promissory cell, surfaced by agda2v4cat's smoke test.
  `vcif.apply` registers each declared node-kind as a
  node-of-kind=`'node-kind'`, but v4cat's framework seed doesn't
  pre-declare `'node-kind'` as a node-type, so apply against a
  default-bootstrap catalogue fails immediately on the first
  vocabulary entry. Closure: dual-register vocabulary entries on
  the vcif side + symmetric pre-declaration in
  `framework_seed.sql`. Region #4 (S2G alone).

## Reference carrier (DBE+RFS+S2G fire, 2026-05-05)

A new role distinct from kernel / RPC / data-at-rest carriers /
certification / catalogue source: **reference carrier** — a full
re-implementation of the v4cat kernel itself in a substrate where
the finite incidence geometry is painfully visible. The first
instance is Octave; the algebraic anchor is the same V₄ coordinate
chart in `theory.md` § 15.

- [shadow_v4cat_octave_distribution.md](shadow_v4cat_octave_distribution.md)
  — first instance of the reference-carrier role, realised at
  [v4cat-oss/v4cat-octave](https://github.com/v4cat-oss/v4cat-octave).
  Reimplements the RISC core + sparse incidence + QueryDAGs +
  self-hosting closure + VCIF snapshot round-trip in GNU Octave.
  The geometric-currying invariant (`edge` introduces its boundary
  nodes if absent) is named as load-bearing. Kernel-parity (Octave
  ↔ Python on shared VCIF input) is recognised as a sibling of
  carrier-parity. Region #8 fire, DBE-led. Per discipline rule 6:
  kernel-implementation orbit at position 2 (Python + Octave),
  reference-carrier orbit at position 1 -- no wrapper extracted on
  either.

- [shadow_v4cat_octave_cisc_sugar.md](shadow_v4cat_octave_cisc_sugar.md)
  — promissory cell. The 16 CISC sugar verbs (`introduce_break`,
  `introduce_object`, `witness`, `lineage_witness`, `refine`,
  `defer`, `promote`, `boundary`, `tropical_min`/`tropical_max`,
  `origin`, `first_seen`, `status`, `retroactive_gap`, `lineage`,
  `inherited_breaks`) catalogued for `v4cat-octave-cisc` sub-fire.

- [shadow_v4cat_octave_framework_seed.md](shadow_v4cat_octave_framework_seed.md)
  — promissory cell. Ports `v4cat/src/v4cat/framework_seed.sql`
  (5 node-types + 18 edge-kinds + 10 K-ATTR breaks) to Octave
  struct-of-arrays form so type-strict mode is reachable.

- [shadow_v4cat_octave_vcif_profiles.md](shadow_v4cat_octave_vcif_profiles.md)
  — promissory cell. Extends VCIF round-trip beyond `snapshot` to
  the other five profiles (patch, vocabulary, recognizer-package,
  closure-report, residue-report).

- [shadow_v4cat_octave_classdef.md](shadow_v4cat_octave_classdef.md)
  — promissory cell. Optional `classdef` wrapper around the
  function/struct API, deferred until the API stabilises.

- [shadow_v4cat_octave_edge_strict.md](shadow_v4cat_octave_edge_strict.md)
  — promissory cell. The strict-mode complement of
  geometric-currying: emits residue when boundary nodes aren't
  pre-introduced. Best paired with the framework-seed sub-fire so
  type-strict mode is end-to-end usable when both close.

## Geometric currying substrate (DBE+RFS+S2G fire, 2026-05-05)

A recognition-led fire that names a new semantic substrate
beneath the existing RISC projection: edges are not typed
relation rows but **closed event-cells whose boundaries contain
three role obligations** (source / kind / target). The current
permissiveness of v4cat's `edge()` becomes intentional rather
than accidental; closure-before-traversal supplies the
path-identity primitive the
[event-log gap](shadow_event_log_gap.md) was missing.

The substrate is named here; the cross-repo migration is named
as seven per-future-fire promissory shadows. Each promissory
closes inside one repo; their epic is workspace-level (cross-
repo) and lives in the methodology repo.

- [shadow_geometric_currying.md](shadow_geometric_currying.md)
  — the central structural shadow. 11 new node-kinds + 17 new
  edge-kinds defining HF-GeometricCurrying. Three new closure
  covers (boundary-closure, cell-closure, path-advancement).
  Disambiguates the existing `CellReferent` (kquery cell) from
  the new `EventCell` (geometric cell). Region #8 fire,
  recognition-led. Per discipline rule 6: orbit position 1 of
  "geometric semantic substrate"; no `CellFramework` wrapper
  extracted.

- [shadow_geometric_currying_v4cat_refactor.md](shadow_geometric_currying_v4cat_refactor.md)
  — promissory cell. Internal cell layer in v4cat: introduces
  `introduce_cell` / `bind_role` / `close_boundary` /
  `close_cell` / `advance_path` underneath the existing public
  RISC API. Adds the HF-GeometricCurrying vocabulary to
  `framework_seed.sql` and ships the four T-* closure
  recognizers as bootstrap tensions. The load-bearing sub-fire;
  recommended ordering: lands first.

- [shadow_geometric_currying_vcif_carrier.md](shadow_geometric_currying_vcif_carrier.md)
  — promissory cell. Adds `cells`, `role_bindings`,
  `boundaries`, `path_presentations` sections to the VCIF
  schema; the compact `{source, kind, target}` form remains as
  a saturated projection.

- [shadow_geometric_currying_vcif_rdf_carrier.md](shadow_geometric_currying_vcif_rdf_carrier.md)
  — promissory cell. Adds `vc:CellAssertion` + `vc:RoleBinding`
  shapes to vcif-rdf; resolves the `CellAssertion` name
  collision (rename existing to `KqueryCellAssertion`); SHACL
  Layer 2 extended to enforce edge-projection-backed-by-cell.

- [shadow_geometric_currying_vcif_hlo_carrier.md](shadow_geometric_currying_vcif_hlo_carrier.md)
  — promissory cell. Adds `role_source_closed` /
  `role_kind_closed` / `role_target_closed` Bool tensors to
  vcif-hlo; `edge_closed` is their elementwise AND. Fusion-
  friendly compilation to OpenHLO ops.

- [shadow_geometric_currying_agda2v4cat_permissive.md](shadow_geometric_currying_agda2v4cat_permissive.md)
  — promissory cell. Strips agda2v4cat's pre-emission anchor
  ceremony; the importer trusts the geometric-currying
  semantics in the receiving v4cat catalogue.

- [shadow_geometric_currying_certify_checks.md](shadow_geometric_currying_certify_checks.md)
  — promissory cell. Four new `claim:*` entries in the
  v4cat-certify suite auditing the substrate's invariants
  (boundaries closed, paths advance only through closed cells,
  presentations oriented + audited, saturated edges backed by
  cells). Recommended ordering: lands last.

- [shadow_geometric_currying_octave_role_matrices.md](shadow_geometric_currying_octave_role_matrices.md)
  — promissory cell. Adds explicit role-matrix encoding to
  v4cat-octave so role closure is sparse-matrix algebra. Pairs
  with v4cat-octave's existing `edge_strict` and
  `framework_seed` promissories.

This fire annotates [shadow_event_log_gap.md](shadow_event_log_gap.md)
with a "Substrate update (2026-05-05)" pointer: the
path-identity primitive the gap was missing is supplied by
closure-before-traversal. The gap remains promissory until the
per-repo migration lands.

## Geometric-currying core landed (DBE+S2G fire, 2026-05-05)

Fire #14 lands the geometric-currying core layer in v4cat,
closing the v4cat#5 epic + its 5 sub-issues + the long-standing
event-log gap (open since fire #5, substrated at fire #12).

- **Closed-fire trajectory entry**: see audit_workspace_2026_05_04.md
  fire #14 row.
- **Implementation**: `event_cells.py`, S13 schema additions
  (`cells`, `role_bindings`, `path_steps`, `event_log` tables),
  HF-GeometricCurrying vocabulary in `framework_seed.sql` (11
  node-kinds and 17 edge-kinds), 4 T-* diagnostic tensions,
  curry.py rename (`CellReferent` → `KqueryCellReferent`), 3 new
  event-cell referents, plus the `cat.events.append/replay/invert`
  ISA verbs.
- **Test impact**: +39 tests (5 new test files); v4cat suite
  156 → 195. Cross-substrate kernel-parity (against
  v4cat-octave) preserved.
- **Closure trails**: appended to
  [shadow_geometric_currying_v4cat_refactor.md](shadow_geometric_currying_v4cat_refactor.md)
  (per-stage commit table) + [shadow_event_log_gap.md](shadow_event_log_gap.md)
  (gap closed; closure-trail with the new ISA verbs catalogued).

The remaining geometric-currying migration sub-fires
(`gc-vcif-carrier`, `gc-vcif-rdf-carrier`, `gc-vcif-hlo-carrier`,
`gc-agda2v4cat-permissive`, `gc-certify-checks`,
`gc-octave-role-matrices`) now have an operational substrate to
consume.

## Geometric-currying migration epic landed (DBE+S2G fire, 2026-05-05)

Fire #15 lands the cross-repo geometric-currying migration epic,
closing [methodology#10](https://github.com/v4cat-oss/methodology/issues/10)
along with its 6 sub-fires across 6 repos. The substrate
(shipped at fire #14) is now consumed by every sibling carrier.

- **Closed-fire trajectory entry**: see audit_workspace_2026_05_04.md
  fire #15 row.
- **Sub-fires + commits**:
  - [vcif 0785ebb](https://github.com/v4cat-oss/vcif/commit/0785ebb) — `gc-vcif-carrier` (4 schema sections + rule 15)
  - [vcif-rdf 4fd9777](https://github.com/v4cat-oss/vcif-rdf/commit/4fd9777) — `gc-vcif-rdf-carrier` (vc:EventCellAssertion + 5 carrier slots)
  - [vcif-hlo b54ef5e](https://github.com/v4cat-oss/vcif-hlo/commit/b54ef5e) — `gc-vcif-hlo-carrier` (role-closure tensors + advance_mask)
  - [v4cat-octave 8582d70](https://github.com/v4cat-oss/v4cat-octave/commit/8582d70) — `gc-octave-role-matrices` ([S, K, T] matrices + edge_closed)
  - [v4cat-certify 6a3e526](https://github.com/v4cat-oss/v4cat-certify/commit/6a3e526) — `gc-certify-checks` (4 new audit claims; total 12)
  - [agda2v4cat 7527c94](https://github.com/v4cat-oss/agda2v4cat/commit/7527c94) — `gc-agda2v4cat-permissive` (anchor ceremony stripped from Vcif.hs)
- **Closure trails**: appended to all 6 promissory shadows
  (`shadow_geometric_currying_vcif_carrier.md`,
  `_vcif_rdf_carrier.md`, `_vcif_hlo_carrier.md`,
  `_octave_role_matrices.md`, `_certify_checks.md`,
  `_agda2v4cat_permissive.md`).
- **Cross-substrate kernel-parity** (`v4cat-octave/tools/parity-check.sh`)
  continues to pass — saturated-edge projection unchanged for
  legacy consumers.

The geometric-currying migration epic is now fully landed across
the workspace. Follow-on sub-sub-fires (the deferred items in
each shadow's closure trail) become candidates for future fires.

## Workspace project tracking (DBE+RFS+S2G fire, 2026-05-05)

A new SoT split: GitHub Issues + the org-level Project become
canonical for **status** (open / in-progress / closed / blocked);
cotype shadows remain canonical for **structure**. The two
surfaces are linked by mutual back-references (issue body →
shadow path; shadow's `Tracking` line → issue #).

- [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)
  — DBE+RFS+S2G fire establishing the split. Defines the
  closure-scope rule (cross-repo issues → `methodology`,
  single-repo → that repo), the pedagogical-issue-body
  convention, the parent-child archive rule, and the
  audit-rederivation procedure. Region #8 fire. Per discipline
  rule 6: at orbit position 1 of "v4cat-oss workspace tracking
  surface", no `MetaTrackingFramework` extracted.

## Methodology repo (cross-reference, 2026-05-05)

The four-skill methodology is published at
[v4cat-oss/methodology](https://github.com/v4cat-oss/methodology)
as the public reconciliation of the shadow-architecture skills
(canonical specs live as Claude Code skill definitions on the
workstation that drives this workspace). Issue bodies referencing
*region #N*, *orbit position*, *S2G/DBE/RFS* terminology link to
that repo for definitions. The repo additionally hosts
**workspace-level issues** — those whose closure-scope spans ≥2
repos in v4cat-oss.

- [shadow-architecture.md](https://github.com/v4cat-oss/methodology/blob/main/shadow-architecture.md)
  — the 8-region lattice + the two forbidden regions.
- [discipline-rules.md](https://github.com/v4cat-oss/methodology/blob/main/discipline-rules.md)
  — the six rules.
- [glossary.md](https://github.com/v4cat-oss/methodology/blob/main/glossary.md)
  — short definitions for the workspace's vocabulary.

Reconciliation issues (where the public docs disagree with
canonical workstation skill behaviour) are filed against
`v4cat-oss/methodology` tagged `reconciliation`.

## Composition

The shadows compose under **Theorem 14.5's preservation theorem**:

> Additive schema moves on K preserve `ClosureKQ(K, scope).gap = ∅`.

Operationally, the four-step move from `theory.py`'s docstring:
implement → add Cell → catalogue → run closure check. Anything
landing in v4cat passes through this composition or it isn't part
of v4cat.

## Entailment

```text
∀ cells c in scope. (IMPL(c) ↔ CAT(c))
  ⟹ check_closure(cat) returns gap = ∅
  ⟹ v4cat is self-hosting at scope
```

Verified by `tests/test_self_hosting.py::test_closure_check_passes_on_fresh_catalogue`.
118 tests green at 7e02713.
