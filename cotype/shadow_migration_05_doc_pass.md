# Shadow: Migration step S₅ — doc pass

> **Forward shadow, generated at S₅ implementation start.**
> Per [shadow_migration_plan.md](shadow_migration_plan.md)'s
> DBE-Step-7 discipline. The final migration step.

## Form

S₅ adds **(β)-reframe sections** to the four core docs without
rewriting their existing content. The existing prose remains
correct for the legacy CISC API; the new sections document the
RISC discipline, the tension-as-named-kquery framing, and the
strengthened closure check, with cross-references to the cotype
shadow docs as the authoritative source for architectural detail.

```
methodology.md  + new section "(β) RISC reframe"
                + new disposition spectrum for tensions
                + cross-ref to cotype/shadow_risc_core.md

theory.md       + new subsection on Theorem 14.5 strengthening
                + cross-ref to cotype/shadow_risc_core.md

tutorial.md     + new section "Using the RISC primitives directly"
                + RISC equivalents alongside existing CISC walkthrough

examples.md     + brief (β) note + cross-references
```

The rule: existing prose is *additive substrate* — it keeps
working for the legacy API surface. New prose is additive
*content* — it documents (β) without contradicting prior text.
This is the doc-level analogue of the anti-pattern that's
governed every prior step: thicken forward, don't rewrite.

## Realisations

| Doc | Insertion point | Content |
|-----|-----------------|---------|
| [methodology.md](../src/v4cat/methodology.md) | new top-level section after the existing methodology proper | "(β) RISC reframe" — 3 RISC primitives, CISC reduction table, tension disposition spectrum |
| [theory.md](../src/v4cat/theory.md) | new subsection within § 14 | "S₄ strengthening of Theorem 14.5" — derives_from chains, RiscDisciplineViolation, smaller-but-stronger closure |
| [tutorial.md](../src/v4cat/tutorial.md) | new section after the witness/refinement walkthrough | "Using the RISC primitives directly" — `introduce_node` / `edge` / curry-spec evaluator with worked examples |
| [examples.md](../src/v4cat/examples.md) | brief note + cross-refs at top | pointer to RISC/CISC equivalence; existing examples still work |

## Composition (with the migration plan)

S₅ is the *human-facing* close-out. After S₅:

- A reader of methodology.md sees both the legacy framing
  (tensions as concerns, refinements as edge annotations) and
  the (β) framing (tensions as named kquery shapes, refinements
  as breaks)
- A reader of theory.md sees both the original Theorem 14.5
  and its S₄ strengthening
- A user reading tutorial.md sees both `cat.witness(...)` (CISC)
  and `cat.edge(...)` (RISC) as valid paths
- The cotype shadows remain the authoritative source for
  architectural commitments; the docs reference them rather
  than duplicating their content

## Discipline note (anti-pattern × doc level)

Per the project's additive-only discipline, the existing prose
is not deleted or rewritten — it remains valid for the legacy
CISC API. New prose is purely additive. This matches every
prior migration step:

- S₁ added schema columns and seed rows (no drops)
- S₂ added new methods and a new module (no existing methods modified)
- S₃ added new bodies to existing methods, retaining the legacy
  direct-INSERT path as a fallback
- S₄ added new SIGNATURE cells and a new validation, leaving
  existing cells in place
- **S₅ adds new doc sections, leaving existing prose in place**

## External commitments preserved

| Commitment | Mechanism |
|------------|-----------|
| 189 tests pass | Doc-only changes; no code modified |
| Public API | Unchanged in S₅ |
| MCP tool surface | Unchanged |
| Closure check passes | No SIGNATURE / framework_seed.sql changes |
| Anti-pattern | Pure additions to docs; no deletion |
| Database compatibility | No schema changes |

## Step-witness (the green-light criterion)

Implementation of S₅ is complete iff:

1. methodology.md gained a (β) RISC reframe section
2. theory.md gained a Theorem 14.5 strengthening note
3. tutorial.md gained a RISC primitives walkthrough
4. examples.md gained a brief (β) note + cross-references
5. The 189-test suite still passes (sanity check; S₅ is doc-only)
6. INDEX.md updated to mark S₅ — and the migration as a whole —
   complete

## Scope discipline

S₅ does *not*:

- Rewrite existing documentation. The legacy CISC framing remains
  valid; new prose adds rather than replaces.
- Mark any existing concept as deprecated. Tensions-as-concerns
  remains a valid disposition (`disposition='concern'`); refinements
  via the legacy `refinements` table remain readable.
- Delete examples or restructure the doc set. Example domains keep
  their existing shape; cross-references make the (β) extension
  visible.

## Cross-references

- [shadow_risc_core.md](shadow_risc_core.md) — authoritative source
  for the (β) reframe; docs link to it
- [shadow_migration_plan.md](shadow_migration_plan.md) — S₅ of 5
- All four prior step shadows
  ([_01_](shadow_migration_01_schema_seed.md),
  [_02_](shadow_migration_02_risc_dispatch.md),
  [_03_](shadow_migration_03_cisc_redirect.md),
  [_04_](shadow_migration_04_signature_reclassify.md)) are
  complete; S₅ closes the migration
