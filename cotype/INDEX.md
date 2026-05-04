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
