# Shadow: migration plan for shadow_risc_core projection

> **Forward shadow (DBE output, 2026-05-03 fire).** Captures the
> ordered additive composition by which `shadow_risc_core.md` lands
> on the codebase. The 5 step-shadows are orbit-elements of the
> project's existing additive-move discipline (anti-pattern +
> Theorem 14.5 closure check); this doc is the index, not a new
> abstraction.

## Form

The migration is an **ordered additive composition** of 5 named
steps. Each step is an instance of the project's
already-established additive-move discipline applied to a specific
artifact. No new abstraction; the generator (additive-move) is
catalogued in the anti-pattern memory and verified on every
catalogue open by `bootstrap.check_closure`.

```
Composition shape:
  S₁ ; S₂ ; S₃ ; S₄ ; S₅
  with dependency partial order:  1 → 2 → 3 → 4
                                  5 parallel-or-after

Per-step invariant (preserved at every intermediate state):
  - closure-check passes
  - test suite green
  - no schema drops, no destructive verbs
  - existing public API behavior unchanged
```

## Costructure (already named — additive-move discipline)

The repeatable form is the project's pre-existing additive-move
discipline:

- **Anti-pattern memory** — never drop schema columns or tables;
  framework primitives only grow; CONTRADICT-style retractions
  rejected.
- **Theorem 14.5 closure check** — additive moves on `K` preserve
  `ClosureKQ(K, scope).gap = ∅`. Verified by
  [bootstrap.py:check_closure](../src/v4cat/bootstrap.py).

Each migration step *applies* this discipline to a different
artifact. None of the steps require a new costructure; the
costructure is the discipline, and the steps are its orbit-elements
under the artifact-axis.

## Composition

Ordered additive application with dependency-induced partial order:

| Step | Depends on | Artifact axis |
|------|-----------|---------------|
| S₁ Schema + seed | — | [schema.sql](../src/v4cat/schema.sql), [framework_seed.sql](../src/v4cat/framework_seed.sql) |
| S₂ RISC dispatch | S₁ | [catalogue.py](../src/v4cat/catalogue.py), new curry module |
| S₃ CISC redirect | S₂ | [catalogue.py](../src/v4cat/catalogue.py), [mcp_server.py](../src/v4cat/mcp_server.py) |
| S₄ SIGNATURE reclassify | S₃ | [theory.py](../src/v4cat/theory.py), [bootstrap.py](../src/v4cat/bootstrap.py), [framework_seed.sql](../src/v4cat/framework_seed.sql) |
| S₅ Doc pass | S₄ (or parallel) | methodology.md, theory.md, tutorial.md, examples.md |

The dependency order is forced by *what each step references*:
S₂ needs the seeded type-system from S₁ to validate against;
S₃ needs the RISC verbs from S₂ to delegate to;
S₄ needs the CISC reductions from S₃ to declare via
`derives_from`; S₅ documents the post-state.

After each step, the test suite + closure check must pass before
the next step begins. This is the per-step witness that the
additive-move discipline was upheld.

## Entailment

```
∀i ∈ {1..5}.  closure_check(K_after_Sᵢ).gap = ∅
            ∧ tests_pass(K_after_Sᵢ)
  ⟹ closure_check(K_after_S₅).gap = ∅
   ∧ tests_pass(K_after_S₅)
   ∧ shadow_risc_core.md realised in code
```

Why this holds: additive moves compose pairwise within each
category. `ALTER TABLE ADD COLUMN` operations commute with each
other; new method additions to `SymmetryCatalogue` commute; new
`Cell` entries with `derives_from` chains commute; doc-section
additions commute. Cross-category dependencies are handled by the
partial order. The cumulative state at every prefix `S₁ ∘ ... ∘ Sᵢ`
is itself an additive extension of the prior prefix, so the
closure check + test suite remain valid by induction.

This is the **additive-monoid property** of the migration
substrate. It's what makes the migration safe to do
incrementally — any partial completion is itself a valid project
state, and a session that ends after Sᵢ leaves a working
catalogue plus a known-correct continuation point.

## Step shadows (forward stubs — to be expanded per DBE Step 7)

Each step gets its own forward shadow at the named path when its
implementation begins. The shadows are stubs here; their
"Form / Realisations / Composition / Entailment" sections fill
in as part of the per-step work.

1. **[shadow_migration_01_schema_seed.md](shadow_migration_01_schema_seed.md)** — **COMPLETE (2026-05-03).**
   `tensions` `CREATE TABLE` extended with `disposition` /
   `parameters_json` / `shape_json` columns; `framework_seed.sql`
   gained the S12 type-system seed (5 node-type tokens, 17
   edge-kind tokens, 10 attribute-schema breaks, type-relation
   `spec_attributes`, `requires-attr`/`admits-attr` witness
   edges). All 169 tests pass; closure check unchanged.

2. **[shadow_migration_02_risc_dispatch.md](shadow_migration_02_risc_dispatch.md)** — **COMPLETE (2026-05-03).**
   New module `src/v4cat/curry.py` realises the curry-spec AST
   (Param, EdgeReferent, AxisCutReferent, LiteralReferent,
   CellReferent, KqueryNode, Tension) plus the evaluator
   (evaluate_tension, evaluate_node, resolve). New methods on
   `SymmetryCatalogue`: `introduce_node`, `edge`,
   `evaluate_tension`. Validation runs `kquery` against the S₁
   type-system seed. Both RISC verbs require the seed (open with
   `check_self_hosting=True`). 15 new tests pass; full suite
   184/184 green.

3. **[shadow_migration_03_cisc_redirect.md](shadow_migration_03_cisc_redirect.md)** — **COMPLETE (2026-05-03).**
   `introduce_break`, `introduce_object`, `introduce_tension`,
   `witness`, `refine` rewritten to delegate to RISC primitives
   (`introduce_node` / `edge`) when the type-system seed is
   loaded; legacy direct-INSERT path retained for
   `check_self_hosting=False`. New CISC sugar `lineage_witness`
   surfaces what was previously buried in
   `introduce_object`'s `lineage=...` parameter.
   `defer`/`promote`/`boundary` inherit RISC delegation via the
   `witness` redirect (orbit-elements per discipline rule 6).
   K-ATTR-SHAPE relaxed to admits-attr (legacy concern-tensions
   omit shape). Tension type made open-schema (closed-schema is
   only `break`). One test updated (`test_top_originators`) to
   reflect the (β) semantic that refinements are first-class
   breaks. Full suite **184/184 green**.

4. **[shadow_migration_04_signature_reclassify.md](shadow_migration_04_signature_reclassify.md)** — **COMPLETE (2026-05-03).**
   `Cell` gained `derives_from: Optional[tuple[str, ...]]`.
   SIGNATURE now declares **3 RISC primitives**
   (`introduce_node`, `edge`, `kquery` with
   `derives_from=None`) plus **11 CISC cells** with explicit
   `derives_from` chains (e.g., `defer.derives_from=('witness',)`,
   `refine.derives_from=('introduce_node','edge')`,
   `tropical_min.derives_from=('kquery',)`). New SIGNATURE cells:
   `introduce_node`, `edge`, `lineage_witness`. New Q-* breaks
   in `framework_seed.sql`:
   `Q-introduce_node`, `Q-edge`, `Q-lineage_witness` (with
   matching framework witnesses). Closure check
   strengthened to verify every `derives_from` chain terminates
   in RISC cells (raises `RiscDisciplineViolation` for dangling
   refs or cycles). 5 new RISC discipline tests; full suite
   **189/189 green**.

5. **[shadow_migration_05_doc_pass.md](shadow_migration_05_doc_pass.md)** — **COMPLETE (2026-05-03).**
   methodology.md gained a "(β) RISC reframe" section
   documenting the 3 RISC primitives, the CISC reduction table,
   the tension disposition spectrum, the schema-witness edge
   kinds, and the strengthened closure check. theory.md gained
   § 14.9 "(β) RISC strengthening of Theorem 14.5" with the
   strengthened theorem statement. tutorial.md gained § 14
   "Using the RISC primitives directly" with RISC equivalents
   for the existing CISC walkthrough plus a curry-spec AST
   example. examples.md gained a brief (β) note + cross-refs.
   Existing prose in all four docs unchanged (additive
   discipline). 189/189 tests still green (sanity check
   confirms doc-only changes).

## Composition with shadow_risc_core

This plan composes with the parent shadow as
**costructure-instances ⟶ whole**:

- [shadow_risc_core.md](shadow_risc_core.md) is the *whole* — the
  target architecture.
- This document is the *composition operation* — ordered additive
  application of 5 step-shadows.
- The 5 step-shadows (forward stubs above) are the *instances*
  of the additive-move discipline applied to specific artifacts.

Per the cotype's existing entailment (INDEX.md):

```
Additive schema moves on K preserve ClosureKQ(K, scope).gap = ∅.
```

— each step here is one such move, and the migration's success is
exactly the conjunction of per-step closure-check passes.

## Cross-references

- [shadow_risc_core.md](shadow_risc_core.md) — the parent forward
  shadow this plan realises.
- [INDEX.md](INDEX.md) — registers both shadows; this one under
  "Forward shadows."
- [shadow_dual_representation.md](shadow_dual_representation.md) —
  IMPL ↔ CAT pairing each step preserves.
- [shadow_layered_stack.md](shadow_layered_stack.md) — the L0→L7
  entailment chain reorganises around the RISC core post-S₄ but
  the chain itself survives the migration.

## Discipline notes (per DBE Step 7)

When implementation of step Sᵢ begins:

1. Generate `shadow_migration_0i_<name>.md` with full
   Form/Realisations/Composition/Entailment sections.
2. Implement the step's additive delta.
3. Run the test suite + closure check.
4. Commit with the step-shadow as deliverable; update INDEX.md.
5. Snap-to-grid: register the step-shadow in this index doc as
   "completed" and proceed to the next step.

If a session ends mid-step, the partial state is recoverable from
the step-shadow stub plus the partial code; the next session
fires `snap-to-grid`, reads the partial residue, and continues
from the named substructure.
