# Shadow: doc-discipline — what "clean, clear, elegant" decomposes to

> **Forward shadow (DBE output, 2026-05-03 fire).** Captures the
> criteria a v4cat doc-set must satisfy to be clean, clear, and
> elegant. Distinct from
> [shadow_docs_quartet.md](shadow_docs_quartet.md), which names
> the *current* depth-graded ladder; this shadow names the
> *criteria* each doc in the ladder must meet. RFS measures the
> current doc-set against these criteria; S2G registers findings.

## Form

The doc-set decomposes into a single **costructure** instantiated
at multiple depth-grades, threaded by a documented composition
operation. The costructure is **graded-narrative-doc**; the
composition is the **depth-graded ladder**; the entailment is
that satisfying the local grade-contract plus thread-coherence
implies the global "clean / clear / elegant" property.

```
Costructure:    graded-narrative-doc
Composition:    depth-graded ladder threading
Instances:      D₁=README, D₂=tutorial, D₃=methodology, D₄=theory,
                D₅=examples (sideways orbit-element of D₄)
Cotype links:   architectural shadows attach at D₃ and D₄ (deep grades)
```

## The costructure: graded-narrative-doc

A graded-narrative-doc is a doc satisfying **five grade-contract
clauses**:

### Clause G1 — single canonical narrative

The doc has *one* primary thesis appropriate to its depth-grade.
Multiple narratives in one file violate this (e.g., a
"legacy section + (β) appendage" structure forces the reader
to resolve which narrative to follow).

The framework's own anti-pattern (additive only, thickens
forward) applies at the prose level: new content extends the
existing narrative rather than appending an alternative one.

### Clause G2 — depth-grade is signposted

The doc states its grade (audience, prerequisites, what the
reader will know after) in the opening or via link conventions
to adjacent grades. A reader landing in the middle of theory.md
should be able to tell they're at the deep end of the ladder.

### Clause G3 — cross-references resolve and form a graph

Every link to another doc (or shadow, or section) points at
content that exists. The doc-set forms a navigable graph —
shallower docs have "go deeper" links; deeper docs have
"prerequisites / shallower" links. The cotype shadows are
reachable from D₃/D₄ as architectural references.

### Clause G4 — additive forward-thickening at the prose level

The framework's anti-pattern (no schema drops, additive only)
extends to docs: existing prose remains valid; new content
extends without contradicting prior text. The discipline is
*not* "no rewrites" — it's "the canonical narrative absorbs new
content rather than appending it as a parallel branch."

Practically: when an architectural shift like (β) lands, the
doc's main body integrates the shift into its existing
narrative rather than appending a "(β) — added on date X"
section. Dates land in commit messages and the cotype, not in
the docs' canonical narrative.

### Clause G5 — methodological coherence with (β)

The framework's structural commitments — tensions as named
kquery shapes, refinements as breaks, RISC primitives as the
core, additive-monoid migration discipline — appear in the
docs' own structure as well as content. The doc-set eats its
own dogfood.

Most concretely: docs don't say "tensions are concerns" in §1
and "tensions are named kquery shapes" in §14 without telling
readers which is canonical. The (β) reframe is the canonical
reading; legacy framings are sub-cases (concern-disposition is
one of four dispositions; CISC sugar is one mode of using the
RISC core). The doc structure reflects this.

## The composition: depth-graded ladder threading

Given graded-narrative-doc instances at the depths
`{D₁=README, D₂=tutorial, D₃=methodology, D₄=theory}` and the
sideways orbit-element `D₅=examples`, the composition operation
is:

1. **Vertical threading.** Each Dᵢ points up to D_{i+1}
   ("go deeper") and down to D_{i-1} ("stay shallower"). Boundary
   cases: D₁ has only "deeper" links; D₄ has only "shallower"
   links.
2. **Sideways thread.** D₅ (examples) is pointed at from D₂/D₃/D₄
   for "see this in a domain"; D₅ links inward only when needed
   for context.
3. **Cotype attachment.** D₃ and D₄ may reference cotype shadows
   for architectural detail. The shadow set is queryable from
   the deep end of the ladder, not from the shallow end (a
   first-touch reader of README shouldn't need to know what a
   cotype is).
4. **No cross-grade mention without depth-bridge.** A README
   that mentions "the strengthened Theorem 14.5 closure check"
   without pointing the reader at D₄ violates the grade-contract.
   Either rephrase at the README's grade or make the cross-ref
   explicit.

The composition is `clean ∧ clear ∧ elegant`-preserving when
each Dᵢ satisfies G1–G5 and the threading is connected.

## The entailment

```
∀i ∈ {1..5}.  grade-contract(Dᵢ)              (G1–G5 each clause)
  ∧ ∀(i, i+1) vertical pair.  cross-ref-graph(Dᵢ, D_{i+1}) connected
  ∧ ∀i ∈ {2,3,4}.  D₅ is reachable from Dᵢ via sideways thread
  ∧ ∀d ∈ D₃ ∪ D₄.  cotype-shadow links are present where
                   architectural detail exceeds doc grade
  ⟹  doc-set is clean (no contradictions, no dual narratives,
                       additive forward-thickening preserved)
   ∧ doc-set is clear (depth-grading + navigation + signposting)
   ∧ doc-set is elegant (framework's own discipline applied to
                          its docs; the doc-set IS a v4cat-shaped
                          artefact, per theory.md § 14.8)
```

The elegance clause is load-bearing for v4cat specifically: the
project's central claim is self-hosting (v4cat applied to v4cat
is v4cat). The docs are themselves witnesses of v4cat's
methodology — they're a cataloguing-domain whose objects are
prose-units, whose breaks are conceptual distinctions, whose
witnesses are the cross-references. A doc-set that fails G5
(methodological coherence with (β)) is *evidence* that the
framework can't apply to itself — which would be a self-hosting
violation at the doc level.

## Three "shapes of bad" the discipline rules out

These are the failure modes the criteria above are designed to
prevent. RFS will look for instances of these in the current
docs.

### Shape 1: the appendage-style doc

The doc's body covers concept X under the legacy framing; a
trailing section ("X reframed — added on date Y") covers the
same concept under a new framing. Reader-facing problem: which
is canonical? G1 violation (dual narrative); G4 violation
(non-additive — the appendage doesn't extend the canonical
narrative, it bolts on a parallel one).

### Shape 2: the orphaned reference

A doc references a concept whose detailed exposition lives in
another doc (or in the cotype) but doesn't link there. Reader-
facing problem: where do I go to learn more? G3 violation.

### Shape 3: the cross-grade smuggle

A doc mentions a concept appropriate to a deeper grade without
pointing the reader there. Reader-facing problem: a tutorial
suddenly invokes a theorem-grade detail that the reader can't
unpack. Composition violation (no depth-bridge).

## Realisations (target — RFS measures current docs against this)

| Doc | Grade | Primary thesis (target) | Key cross-refs |
|-----|-------|-------------------------|----------------|
| README.md  | D₁ | "What v4cat is, in 5 minutes" | tutorial, methodology |
| tutorial.md | D₂ | "How to use v4cat to catalogue a domain" | methodology, examples |
| methodology.md | D₃ | "Why the catalogue is shaped this way; the operational design under (β)" | theory, tutorial, cotype/shadow_risc_core.md |
| theory.md | D₄ | "Foundations: kquery, klein-four, Theorem 14.5 (S₄-strengthened), RISC discipline" | methodology, cotype shadows |
| examples.md | D₅ (sideways) | "Domain templates" | methodology, tutorial |

The (β) reframe should be **integrated into each doc's primary
thesis** at its appropriate grade — not appended as a separate
section. RFS findings will identify gaps between current state
and this target.

## Composition with prior shadows

- [shadow_docs_quartet.md](shadow_docs_quartet.md) names the
  ladder structure; this shadow names the criteria each rung
  must satisfy. The two compose: quartet describes shape;
  discipline describes quality.
- [shadow_layered_stack.md](shadow_layered_stack.md) names the
  L0→L7 entailment from kquery up to docs; this shadow refines
  the L7 layer's success criteria.
- [shadow_risc_core.md](shadow_risc_core.md) is the
  authoritative source for (β) commitments; this shadow
  requires the doc-set to be coherent with it.

## Entailment chain

```text
G1 (single narrative)
  + G4 (additive thickening)
    ⟹ no appendage-style sections; (β) integrated, not bolted-on

G2 (signposted grade)
  + G3 (resolved cross-refs)
    ⟹ navigable graph; depth-progression visible to readers

G5 (methodological coherence)
  ⟹ docs reflect (β) commitments; tensions read as named
     kquery shapes throughout, not as "concerns" in some sections

  All five clauses + threading
    ⟹  clean ∧ clear ∧ elegant
```

## Discipline note

This shadow is itself a graded-narrative-doc — at the cotype
grade. Its primary thesis is the criteria above; its
cross-references resolve to other shadows; its grade is
"architectural" (alongside other cotype shadows); it doesn't
contain dual narratives. If this shadow couldn't satisfy its
own criteria, the criteria would be self-incoherent.
