# Shadow: D₆ — signposting pass

> Per [shadow_doc_cleanup_plan.md](shadow_doc_cleanup_plan.md).

## Form

3-line grade preamble added to each of the 5 user-facing docs,
just below their title. Each preamble states:

1. The doc's depth-grade in the ladder (with D₁–D₅ label per
   shadow_docs_quartet.md)
2. Pointers to shallower (where to go for less depth) and deeper
   (where to go for more depth) docs
3. A pointer to the cotype/ shadow library for architectural
   detail

The preamble pattern uses italicised blockquote (`> *...*`) so
it's structurally subordinate to the title and visually distinct
from body prose.

## Realisations

| Doc | Grade | Inserted preamble |
|-----|-------|--------------------|
| [README.md](../README.md) | D₁ (quick-start) | Just below title; refers to tutorial / methodology / theory + cotype/ |
| [tutorial.md](../src/v4cat/tutorial.md) | D₂ (hands-on) | Just below title; refers to README + methodology / theory + cotype/ |
| [methodology.md](../src/v4cat/methodology.md) | D₃ (operational) | Just below title; refers to README / tutorial + theory + cotype/ (with shadow_risc_core.md called out) |
| [theory.md](../src/v4cat/theory.md) | D₄ (foundations) | Just below title; refers to methodology / tutorial / README + cotype/ as authoritative |
| [examples.md](../src/v4cat/examples.md) | D₅ (sideways orbit) | Just below title; refers to tutorial / README + methodology + cotype/ |

## Composition with the ladder

The preambles thread the depth-graded ladder into the doc-set's
own surface — readers landing in any doc immediately see where
they are and where to go next. This addresses RFS Finding 9
(no doc declares its grade) directly and contributes to RFS
Finding 7 (cotype invisibility) by surfacing the cotype link
from every grade.

The 3-line format is deliberately small: it doesn't compete with
each doc's primary thesis, but it's reachable in a glance. G2
(grade signposted) is realised by structure, not by
text-volume.

## Step-witness

- ✓ All 5 docs have grade preambles
- ✓ Each preamble names the doc's grade (D₁–D₅)
- ✓ Each preamble has shallower + deeper pointers
- ✓ Each preamble points at cotype/ at appropriate depth (deeper
  grades emphasise specific shadows; shallower grades just point
  at the directory)
- ✓ No "added 2026-05-03" markers in any of the 5 docs
- ✓ All cross-refs resolve

## Cleanup orbit closure

D₆ closes the orbit. The 6 step-shadows
(`shadow_doc_cleanup_0[1-6]_*.md`) collectively realise
[shadow_doc_discipline.md](shadow_doc_discipline.md)'s G1–G5
clauses across the 5 user-facing docs:

- G1 (single canonical narrative) — D₁–D₅ integrated each appendage
- G2 (depth-grade signposted) — D₆ adds preambles
- G3 (cross-refs resolve) — verified per step
- G4 (additive forward-thickening) — appendages absorbed before
  deletion; cotype preserves migration history
- G5 (methodological coherence with (β)) — every doc now leads
  with RISC framing; CISC documented as sugar throughout

The doc-cleanup is the deepest test of v4cat's self-hosting
claim (theory.md § 14.8): the framework's own discipline applied
to its witnesses (the docs). The orbit closes cleanly because
the discipline holds — the additive-monoid composition operator
applies at the prose substrate just as cleanly as at the
schema/code substrates.
