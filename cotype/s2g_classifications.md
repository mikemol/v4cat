# S2G classifications (2026-05-02)

Responses to the three items RFS deferred to S2G. The answers are
catalogue-only — no code changes — except where the framework's
own theory licenses a clean cataloguing move.

## Response to RFS Finding 2 — V4 cell table is orbit-driven

**RFS classification:** orbit-element under "show V4 cells at
audience N's level" — extract is wrong.

**S2G classification:** confirmed. The 5-doc depth-quartet+ is
itself the orbit, and each doc's V4 cell table is one orbit
position. Per [shadow_docs_quartet.md](shadow_docs_quartet.md) the
orbit is *graded re-statement*, not *duplicate exposition*.

**Move:** none. The orbit is correct as-is. Cataloguing only:
the relation `(doc, cell-table-presentation)` is an orbit, not a
shadow needing extraction.

## Response to RFS Finding 3 — Kind.A is *reserved*, not vestigial

**RFS classification:** "vestigial slot — possible (a) delete, (b)
reserve, (c) repurpose." Implied that (a) was the cleanest option.

**S2G correction:** **Reserved, not vestigial.** RFS read the code
without consulting [theory.md](../theory.md). Two theory-level
commitments make Kind.A load-bearing in the foundation:

1. **Counterexample 14.6.1 (Under-promised scope)**
   ([theory.md:1634-1644](../theory.md#L1634-L1644)) names "wedge
   audits" as the canonical example of a kind the framework can
   use *implicitly* while under-promising in
   `Q-supported-claims`. Kind.A is the namespace slot for that
   example; its emptiness in `framework_seed.sql`'s scope (`'O,B,W,R,E,K,X'`,
   no `A`) IS the under-promising the counterexample describes.
   This is *deliberate* — it preserves the structural example.

2. **Boundary 14.6.5 (Strict vs. weak categorical structure)**
   ([theory.md:1677-1686](../theory.md#L1677-L1686)) reserves
   wedge audits as the **2-cells** of the bicategorical lift:
   "wedge audits as 2-cells between schema-extensions viewed as
   1-cells." Kind.A is the namespace slot for the 2-cell grade.

So Kind.A is not vestigial — it's a **deliberately empty slot**
licensed by two theory commitments. Removing it from `cells.py`
would create a gap.10 violation against theory.md's foundation.

**Move:** none — but with a docstring nudge. The current
`# wedge audits` comment at [cells.py:33](../cells.py#L33) is
correct but doesn't say *why* the slot is empty. A future fire
may want to extend the comment to: `# wedge audits — reserved
for the bicategorical 2-cell lift (theory.md § 14.6.5); empty in
the strict 1-categorical implementation`.

This is a candidate for a separate, single-purpose commit if
someone wants it; not necessary for this fire.

## Response to RFS Finding 4 — gap vocabulary is canonical

**RFS classification:** "canonical vocabulary in single use,
already correct, no move."

**S2G classification:** confirmed. The terms `gap.10`, `gap.01`,
`implicit`, `promissory` are defined once
([bootstrap.py:36-54](../bootstrap.py#L36-L54)) and used at
multiple sites as references. That IS the canonical vocabulary
pattern — no extraction needed.

## Quotient produced this fire

The 6 named selections of kquery quotient under "kquery instance
with fixed `emit` mask + projection" → externalised as
[shadow_kquery_orbit.md](shadow_kquery_orbit.md). This is the
single new shadow this S2G fire adds to the cotype.

## Deferred candidates

- **Kind.A docstring nudge** (Finding 3): not blocking; defer to
  a future single-purpose commit.
- **Catalogue-side orbit registration**: a future enhancement
  could add a refinement on `Q-kquery` enumerating the named
  selections as orbit-positions. Not necessary for self-hosting;
  the orbit-saturation discipline rule 6 makes the implicit
  registration fine.

## Cotype state after this fire

| Kind | Count | Items |
|------|-------|-------|
| Shadow (DBE)   | 6 | cell, dual_representation, kind_stratification, kquery_universal_read, layered_stack, docs_quartet |
| Shadow (S2G)   | 1 | kquery_orbit |
| Findings (RFS) | 1 | rfs_findings (4 findings, 1 acted) |
| Classifications (S2G) | 1 | this file |
| Snap report    | (next) | snap_report.md |

7 shadows + 2 process records covering 4 RFS findings, 1 code
extraction, and 3 S2G classifications.
