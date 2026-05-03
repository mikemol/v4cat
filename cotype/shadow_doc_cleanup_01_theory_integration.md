# Shadow: D₁ — theory.md integration

> **Forward shadow, generated at D₁ implementation start.**
> Per [shadow_doc_cleanup_plan.md](shadow_doc_cleanup_plan.md)'s
> DBE-Step-7 discipline.

## Form

Integrate § 14.9 ("(β) RISC strengthening of Theorem 14.5 —
added 2026-05-03") into § 14.5 as a new subsection 14.5.8,
making the strengthened theorem statement visible *within* the
canonical Implementation section. § 14.9 (the appendage) is
deleted once its content is absorbed.

The closing paragraph of § 14.5 (lines 1641–1647) currently
lists primitives by their pre-(β) names (`Q-kfour`, `Q-witness`,
`Q-refine`, `Q-schema-extend`, etc.). Under (β) the canonical
RISC core is `{Q-introduce_node, Q-edge, Q-kquery}` plus the
bootstrap breaks; CISC verbs are derived. Updating this paragraph
keeps theory.md's foundational claims aligned with the realised
state.

## Realisations

| Site | File | Action |
|------|------|--------|
| § 14.5.8 (new) | [theory.md](../src/v4cat/theory.md) | Add new subsection within § 14.5 documenting the (β) RISC strengthening |
| § 14.5 closing paragraph | [theory.md](../src/v4cat/theory.md) | Update primitive list to reflect post-(β) RISC core |
| § 14.9 | [theory.md](../src/v4cat/theory.md) | Delete (content absorbed into 14.5.8) |

## External commitments preserved

- All cross-references to § 14.5 and § 14.9 audited; § 14.9 has
  no inbound references in user-facing docs (the (β) reframe
  references methodology.md and cotype/shadow_risc_core.md, not
  theory.md § 14.9 directly).
- The strengthened Theorem 14.5 statement is *clearer* in its
  new home (within Implementation) than as an appendage.
- Migration history preserved at
  [shadow_migration_04_signature_reclassify.md](shadow_migration_04_signature_reclassify.md)
  and [shadow_migration_plan.md](shadow_migration_plan.md).
- 189 tests still green (no code touched).

## Step-witness

D₁ complete iff:
1. § 14.5.8 exists with the (β) RISC strengthening content
2. § 14.9 marker removed
3. § 14.5 closing paragraph references the post-(β) primitive list
4. No "added 2026-05-03" markers remain in theory.md
5. Cross-refs in theory.md continue to resolve
6. Test suite still 189/189 green
