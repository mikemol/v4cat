# Shadow: doc-cleanup plan — projection of doc-discipline onto current docs

> **Forward shadow (DBE output, 2026-05-03 fire).** Captures the
> ordered additive composition by which
> [shadow_doc_discipline.md](shadow_doc_discipline.md)'s criteria
> land on the user-facing doc-set. Structurally analogous to
> [shadow_migration_plan.md](shadow_migration_plan.md) — the
> 6th inter-shadow quotient identified in the
> [snap report](snap_report_doc_discipline.md) is exactly that
> the doc-cleanup composition has the same shape as the code
> migration's S₁–S₅: ordered additive operations on the
> artefact axis preserving external commitments at every
> intermediate state.

## Form

The cleanup is an **ordered additive composition** of 6 named
steps. Each step is an instance of the project's already-
established additive-prose-pass discipline (G1–G5 grade-contract
clauses + threading rules) applied to a specific doc. No new
abstraction; the generator (additive thickening at the prose
level) is documented in
[shadow_doc_discipline.md](shadow_doc_discipline.md).

```
Composition shape:
  D₁ ; D₂ ; D₃ ; D₄ ; D₅ ; D₆
  with dependency partial order:  D₁ → D₂ → D₃ → D₄
                                  D₅ depends on D₂
                                  D₆ depends on D₁..D₅

Per-step invariant (preserved at every intermediate state):
  - all currently-resolving cross-references continue to resolve
  - depth-graded ladder structure preserved
  - 189 tests green (no code-touching changes)
  - closure check passes
  - reader expectations honoured (tutorial walks; theory states
    foundations; examples runnable)
  - methodological coherence with (β) strengthens monotonically
    through the sequence
```

The dependency order is forced by the *authoritative direction*
of the depth-graded ladder: theory (D₁) sets the canonical
theorem; methodology (D₂) operationalises it; tutorial (D₃)
teaches what methodology defines; README (D₄) summarises;
examples (D₅) apply; signposting (D₆) threads the navigation
graph once the per-doc work is settled.

## Costructure (already named — additive-prose-pass discipline)

The repeatable form is the doc-discipline shadow's contract:
each step satisfies G1–G5 for the doc it touches:

- **G1** (single canonical narrative) — integrated, not appended
- **G2** (depth-grade signposted) — D₆ delivers this transversely
- **G3** (cross-refs resolve) — verified after each step
- **G4** (additive forward-thickening at prose level) —
  appendages are *absorbed*, not deleted; the canonical
  narrative grows to include their content
- **G5** (methodological coherence with (β)) — each step makes
  its doc more coherent with the (β) framing, never less

The migration history (the fact that appendages existed) is
preserved in the cotype: [shadow_migration_05_doc_pass.md](shadow_migration_05_doc_pass.md)
records the additive S₅ pass that introduced them. Deleting
appendage sections in this cleanup pass is honest because the
record lives in the cotype, not because the appendages never
happened.

## Composition

Ordered additive application with dependency-induced partial
order:

| Step | Depends on | Doc | Primary move |
|------|-----------|-----|--------------|
| D₁ | — | [theory.md](../src/v4cat/theory.md) | Integrate § 14.9 (β) strengthening into § 14.5; strengthened Theorem 14.5 becomes canonical, pre-(β) form historical |
| D₂ | D₁ | [methodology.md](../src/v4cat/methodology.md) | Integrate "(β) RISC reframe" appendage into body; verbs section leads with RISC; tensions section leads with disposition spectrum |
| D₃ | D₂ | [tutorial.md](../src/v4cat/tutorial.md) | Reorder: § 2 leads with RISC primitives; CISC walkthrough becomes "named conveniences for common patterns"; § 14 appendage absorbed |
| D₄ | D₂, D₃ | [README.md](../README.md) | First paragraph mentions (β) RISC core; cotype/ pointer added; doc-layout description reflects post-cleanup state |
| D₅ | D₂ | [examples.md](../src/v4cat/examples.md) | Already cleanest (blockquote not appendage); optional update of 1–2 example domains to use RISC verbs directly |
| D₆ | D₁–D₅ | all 5 docs | Add 3-line grade preamble to each: grade declaration + shallower/deeper pointers + cotype reference at appropriate depth |

After each step, all currently-resolving cross-references must
still resolve and the test suite must still pass. This is the
per-step witness that the additive-prose-pass discipline was
upheld.

## Entailment

```
∀i ∈ {1..6}.  cross_refs_resolve(D_after_i)
            ∧ tests_pass(D_after_i)
            ∧ G1–G5 hold for the doc(s) touched by step i
  ⟹ doc-set after D₆ satisfies G1–G5 globally
   ∧ depth-graded ladder threading is connected
   ∧ shadow_doc_discipline.md is realised in the doc-set
```

Why this holds: additive prose-passes compose pairwise within
each category. Per-doc integrations commute with each other (no
content shared across docs is rewritten by both ends; cross-refs
resolve symmetrically). Cross-doc dependencies are handled by
the partial order. The cumulative state at every prefix
`D₁ ∘ ... ∘ Dᵢ` is itself a valid project state, and a session
that ends after Dᵢ leaves a working doc-set plus a known-correct
continuation point.

This is the **additive-monoid property at the prose level** —
the same operator the code migration used at the schema/code/
seed/signature levels, applied here to the prose substrate.

The cleanup pass is the deepest test of v4cat's self-hosting
claim: the docs are themselves witnesses of the methodology
(theory.md § 14.8), so cleaning them up *under the methodology's
own discipline* is the project applying itself to itself at the
prose layer.

## Step shadows (forward stubs — to be expanded per DBE Step 7)

Each step gets its own forward shadow at the named path when
its implementation begins.

1. **`shadow_doc_cleanup_01_theory_integration.md`** —
   theory.md integration. § 14.9 ("(β) RISC strengthening of
   Theorem 14.5 — added 2026-05-03") is absorbed into § 14.5
   ("Implementation"). The strengthened theorem statement
   becomes the canonical Theorem 14.5; the pre-(β) form is
   shown as a historical predecessor inline. The "added on date"
   marker is removed; the cotype's
   [shadow_migration_04_signature_reclassify.md](shadow_migration_04_signature_reclassify.md)
   preserves the migration history. Cross-refs to methodology
   continue to resolve.

2. **`shadow_doc_cleanup_02_methodology_reframe.md`** —
   methodology.md integration. Verbs section: introduce_node /
   edge / kquery presented as canonical RISC core; CISC verbs
   table follows as "named conveniences with documented
   reductions." Tensions section: lead with disposition
   spectrum (concern / utility / diagnostic / audit); the
   "structural concerns about implementation alignment" framing
   becomes the concern-disposition reading. The trailing
   "(β) RISC reframe — added 2026-05-03" section is deleted
   once its content is absorbed. Cross-refs to theory.md updated
   to point at the integrated § 14.5 (post-D₁).

3. **`shadow_doc_cleanup_03_tutorial_reorder.md`** —
   tutorial.md reorder. New § 2 introduces the three RISC
   primitives + curry-spec algebra. CISC walkthrough (formerly
   §§ 1–13) becomes a follow-on "named conveniences" section
   that walks through the ergonomic CISC verbs as RISC
   compositions. § 14 (the (β) appendage) is deleted once its
   content has been integrated into the new ordering. The
   tutorial still walks the reader from empty catalogue to
   small populated domain — the *reader experience* is
   preserved; only the verb-introduction order changes.

4. **`shadow_doc_cleanup_04_readme_overview.md`** — README.md
   refresh. First paragraph rewrites to lead with the RISC core
   ("introduce_node, edge, kquery — three primitive verbs plus
   the Klein-four read classifier"); CISC verbs mentioned as
   "named conveniences"; cotype/ mentioned as the architectural
   source-of-truth for deep readers; doc-layout description
   updated to reflect post-cleanup canonical-narrative state.
   Quartet shadow's claim about README enumerating the ladder
   continues to hold.

5. **`shadow_doc_cleanup_05_examples_minor.md`** — examples.md
   minor pass. The existing blockquote-at-top "(β) note" stays.
   Optionally: 1–2 example domains gain a side-by-side RISC
   alternative ("here's how the same template would look using
   introduce_node directly"). This is *optional* — examples.md
   is already the cleanest of the 5 docs per RFS Finding 5.
   The step is named primarily so signposting (D₆) has a
   placeholder to attach to.

6. **`shadow_doc_cleanup_06_signposting.md`** — transverse pass
   across all 5 docs. Each gains a 3-line preamble:

   ```
   > Grade: {tutorial|methodology|theory|...}.
   > Shallower: see {previous}.  Deeper: see {next}.
   > Architectural detail: see [cotype/](cotype/) shadows.
   ```

   The cotype/ pointer makes the shadow library reachable from
   every grade. Cross-grade smuggle (Shape-3) is prevented by
   the explicit "if you want X-grade detail, see Y" pattern.

## External commitments preserved

Per [rfs_findings_doc_discipline.md](rfs_findings_doc_discipline.md)'s
Step 1 inventory:

| Commitment | Mechanism |
|------------|-----------|
| Cross-refs resolve | Each step's witness includes a cross-ref check; integration moves content while updating all anchors symmetrically |
| Self-hosting claim (theory § 14.8) | Strengthens under integration: clean docs ARE the methodology applied to itself at the prose layer |
| Depth-graded ladder | Quartet shadow's structure unchanged; only doc-internal narratives reorganise |
| Anti-pattern (additive only) | Each step absorbs new content into canonical narrative; appendages deleted only after absorption complete; migration history preserved in cotype |
| 189 tests green | No code touched in any step; doc-only changes |
| Reader expectations | Tutorial still walks through; examples still domain templates; theory still has Theorem 14.5 — but with the (β) form as canonical and the legacy form as historical predecessor inline |
| Methodological coherence with (β) | Each step makes its doc *more* coherent with (β); coherence increases monotonically through the sequence |

All commitments preserved. Recomposition is feasible.

## Step-witness pattern

Per the migration plan's discipline notes, when implementation
of step Dᵢ begins:

1. Generate `shadow_doc_cleanup_0i_<name>.md` with full
   Form/Realisations/Composition/Entailment sections.
2. Implement the step's prose changes.
3. Verify all cross-refs in the affected doc still resolve.
4. Run `grep -r "{appendage marker}"` to confirm absorption
   (e.g., for D₂, no remaining "(β) RISC reframe — added
   2026-05-03" marker in methodology.md).
5. Run the test suite (sanity check; doc changes shouldn't
   touch tests).
6. Commit with the step-shadow as deliverable; update INDEX.md.
7. Snap-to-grid: register step-shadow as "completed" in this
   plan; proceed to next step.

If a session ends mid-step, the partial state is recoverable
from the step-shadow stub plus the partial doc edits; the next
session fires `snap-to-grid`, reads the partial residue, and
continues from the named substructure.

## Composition with prior shadows

| Prior shadow | Relation |
|--------------|----------|
| [shadow_doc_discipline.md](shadow_doc_discipline.md) | Provides the criteria (G1–G5) each step must satisfy. |
| [rfs_findings_doc_discipline.md](rfs_findings_doc_discipline.md) | Provides the per-doc concrete recomposition design that each step shadow expands on. |
| [shadow_docs_quartet.md](shadow_docs_quartet.md) | Documents the depth-graded ladder structure preserved through cleanup. |
| [shadow_migration_plan.md](shadow_migration_plan.md) | The structural template — the additive-monoid quotient (snap report quotient #6) means doc-cleanup follows the same composition shape. |
| [shadow_risc_core.md](shadow_risc_core.md) | The (β) commitment that determines what "methodologically coherent" content looks like. |

## Discipline notes

- **The cleanup is doc-only.** No code, schema, seed, or
  SIGNATURE changes. Test suite stays at 189/189 across the
  whole sequence.
- **Each step shadow is generated when its step begins**, per
  DBE Step 7. The 6 step shadows above are stubs naming what
  each will contain; their full forms get generated as the
  implementation starts.
- **Per shadow-architecture rule 6**, the 3 appendage sites in
  D₁–D₃ are orbit-elements of the same Shape-1 anti-pattern;
  the cleanup catalogues each integration locally rather than
  extracting a meta-abstraction. The discipline (additive
  thickening) is already named in the doc_discipline shadow;
  per-step work is its application, not the discovery of a new
  pattern.
- **The deep additive-monoid quotient** with the migration plan
  means the cleanup's success criterion mirrors the migration's:
  every prefix is a valid resting state. A session that
  authorises only D₁ leaves a coherent doc-set with theory.md
  cleaned up and the other 4 docs unchanged — useful even
  without completing the rest.

## End-state criterion

The cleanup is complete iff:

- All 5 user-facing docs satisfy G1–G5
- The depth-graded ladder threading is explicit (D₆'s
  signposting in place)
- No "(β) — added 2026-05-03" markers remain in user-facing
  docs (the markers' content has been absorbed into canonical
  narratives; the migration record lives in the cotype)
- Cross-refs resolve; navigation graph is connected
- 189 tests green
- The doc-set IS the framework's discipline applied to itself
  at the prose layer — closing v4cat's self-hosting claim at
  the deepest substrate
