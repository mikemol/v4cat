# RFS findings — doc-discipline (2026-05-03)

Sideways read of the user-facing doc-set against
[shadow_doc_discipline.md](shadow_doc_discipline.md)'s five
grade-contract clauses (G1–G5) and the three "shapes of bad"
the discipline rules out.

## External commitments inventoried (Step 1)

These are the fixed points any recomposition must preserve:

- All currently-resolving cross-references continue to resolve
- Self-hosting claim (theory.md § 14.8) — the docs remain
  witnesses of the methodology
- Depth-graded ladder ([shadow_docs_quartet.md](shadow_docs_quartet.md))
  preserved: README → tutorial → methodology → theory plus
  examples as sideways orbit-element
- Anti-pattern: additive only — existing prose is reorganised
  or absorbed, not deleted; new prose can replace appendages
  by integrating their content into the canonical narrative
- 189 tests green; doc reorgs that touch code references must
  preserve test-suite green
- Reader expectations: tutorial walkthrough still walks through;
  examples runnable; theory's foundational claims stated;
  methodology covers operational design

## Findings (Step 2)

### Finding 1 — README.md doesn't surface (β) at all

[README.md](../README.md) — first paragraph still names the CISC
verbs as the framework's primary surface:

> The ISA's `introduce_object`, `introduce_break`, `witness`,
> `refine` verbs and the analytic views work the same…

No mention of `introduce_node`, `edge`, RISC, the curry-spec
algebra, or the strengthened Theorem 14.5. No pointer to
[cotype/](.) as the architectural source-of-truth.

**G2 violation** (depth-grade signposted): a reader exiting
README doesn't know what (β) is or that it's the canonical
framing.
**G5 violation** (methodological coherence with (β)): the
framework's own central commitment is invisible at its lowest
grade.
**Shape-3 violation** (cross-grade smuggle, inverted): rather
than smuggling deep content into a shallow doc, README *omits*
the framework's primary commitment entirely. Same root cause:
no signposting.

**Severity: HIGH.** This is the first-touch doc; a new reader's
mental model gets seeded incorrectly.

### Finding 2 — methodology.md / theory.md / tutorial.md all use Shape-1 appendage style

Each of three primary docs has a trailing "(β) — added
2026-05-03" section bolted onto the existing body:

| Doc | Appendage location | Lines |
|-----|-------------------|-------|
| [methodology.md](../src/v4cat/methodology.md) | line 1007 onwards | "(β) RISC reframe — added 2026-05-03" |
| [theory.md](../src/v4cat/theory.md) | line 1792 onwards | "§ 14.9 (β) RISC strengthening of Theorem 14.5 — added 2026-05-03" |
| [tutorial.md](../src/v4cat/tutorial.md) | line 802 onwards | "§ 14 Using the RISC primitives directly — added 2026-05-03" |

Three same-grade instances of the same anti-pattern. The
appendages were the right move *during* the migration (S₅
discipline preserved existing prose under the additive-only
anti-pattern); they are *not* the right resting state. The
canonical narrative now reads as legacy + appendage rather than
as a single integrated story.

**G1 violation** (single canonical narrative): each doc has two
narratives — "tensions are concerns" then "tensions are named
kquery shapes"; "introduce_break is the verb" then "introduce_break
delegates to introduce_node"; "Theorem 14.5" then "Theorem 14.5
strengthened".
**G4 violation** (additive forward-thickening *at the prose
level*): the schema discipline ("absorb new content into the
canonical narrative") wasn't applied. Date-stamps in the doc
body are themselves a smell — dates belong in commits and the
cotype, not in the canonical narrative.
**Shape-1 violation** at three sites.

**Severity: HIGH.** Three of four primary docs.

**Classification per shadow-architecture rule 6:** the three
appendages are *not* free duplicates — they're orbit-elements of
"Shape-1 applied to a graded-narrative-doc." The orbit's
generator is "additive doc-pass S₅ executed without
integration." Recomposition addresses the generator (integrate
the appendage content into each canonical narrative) rather than
extracting a wrapper — which would be S2G-flavoured cataloguing
of the orbit, not RFS-flavoured extraction.

### Finding 3 — tutorial.md inverts the (β) ordering

[tutorial.md § 2](../src/v4cat/tutorial.md) is titled "The seven
verbs and one classifier" and walks through the *CISC* verbs as
if they were primary:

> | `INTRODUCE` | Add a witness-object … |
> | `WITNESS`   | Record a typed edge from a spec to a break |
> | `REFINE`    | Annotate a (break, spec) edge with a named attribute |
> | …                                                       |

§§ 3–13 build on this CISC frame. § 14 (the (β) appendage) then
says "actually all these delegate to a RISC core of 3."

Under (β), the structural primary is the RISC core; CISC verbs
are sugar. The tutorial *teaches* the inverted picture: sugar is
the core, primitives are an afterthought.

**Cross-grade smuggle reversed:** rather than smuggling deeper
material into a shallower doc, the tutorial buries the deeper
(structural) primitives behind the sugar. A new reader builds an
incorrect mental model of what is fundamental.

**Severity: MEDIUM-HIGH.** The tutorial is the doc that teaches
the framework. Wrong primary teaches wrong framework.

### Finding 4 — methodology.md has dual narrative on tensions

[methodology.md](../src/v4cat/methodology.md):

- **Body** (pre-(β)): tensions are *structural concerns about
  implementation alignment*. Origin: the framework's original
  framing.
- **Appendix** (β): tensions are *named curry-spec ASTs over
  kquery* with a disposition spectrum (concern / utility /
  diagnostic / audit).

Both are technically correct under their respective framings.
Neither is marked as canonical. A reader writing new code or
new docs has to guess.

**G5 violation** (methodological coherence). Specific instance
of Finding 2's broader pattern; called out separately because
the dual-narrative on a *load-bearing* term has higher reader-
confusion impact.

**Severity: HIGH.** Tension is a primary framework concept; its
ambiguity propagates.

### Finding 5 — examples.md uses the cleaner blockquote pattern

[examples.md](../src/v4cat/examples.md) added a brief
"(β) note (2026-05-03)" as a *blockquote at the top* rather than
as a trailing section. This is closer to the discipline:

- The reader meets the (β) signal *before* the legacy content
- The blockquote is structurally subordinate (a meta-note)
  rather than co-equal (an appendage section)
- Existing prose continues to apply

**Verdict: closest to compliance among the 5 docs.** Still not
fully integrated (the body still uses CISC throughout) but the
appendage pattern is avoided.

**Classification: already-aligned to within doc-grade
expectations.** examples.md is D₅ (sideways orbit-element); its
job is to provide domain templates, not to teach the framework.
The blockquote is sufficient signalling.

**Severity: LOW.**

### Finding 6 — shadow_docs_quartet.md still accurate

The 5-doc ladder it describes still exists; each doc still
plays the role it documents. No update needed.

**Severity: NONE** (already-aligned).

### Finding 7 — cotype/ is invisible from user-facing docs

The cotype/ shadow library now contains 17+ architectural
artefacts including
[shadow_risc_core.md](shadow_risc_core.md),
[shadow_migration_plan.md](shadow_migration_plan.md), and the
five per-step shadows. These are the authoritative source for
many decisions referenced (briefly) in methodology.md and
theory.md.

But: README.md doesn't mention cotype/. tutorial.md doesn't
mention cotype/ until § 14.4. The deepest-grade doc-set artefact
isn't reachable from the shallow-grade entry points.

**Composition violation** (cotype attachment): per the
discipline shadow, "D₃ and D₄ may reference cotype shadows;
shadow set is queryable from the deep end of the ladder, not
from the shallow end." But the threading rule also says the
*existence* of cotype/ should be discoverable from the shallow
end — a reader at README should know it exists, even if they
don't dive in.

**Severity: MEDIUM.** Deep readers find the cotype; shallow
readers don't know it exists.

### Finding 8 — terminology consistency

Spot-check across docs:

- "break" / "structural distinction" / "named distinction" —
  used for the same concept, mostly consistent
- "tension" — addressed by Finding 4
- "spec" / "object" / "witness object" — used for the same
  concept across docs; "spec" is the schema column name, "object"
  is the legacy ISA term, "witness object" is the methodological
  term

**Severity: LOW.** Real ambiguity but low reader-confusion impact
because context disambiguates locally. Worth a sweep but not
urgent.

### Finding 9 — no doc declares its depth-grade explicitly

No doc opens with "This is the [grade] doc; for shallower see X,
deeper see Y." The ladder is implicit (signalled by file
ordering and table-of-contents in methodology) but not explicit
in each doc's preamble.

**G2 violation** at every doc. The grade is recoverable but only
by reading shadow_docs_quartet.md or by inferring from contents.

**Severity: LOW.** Composition works without it because the
docs cluster by topic; signposting would make navigation cleaner
but isn't structurally broken.

## Quotient analysis (Step 3)

Findings group into three recomposition clusters:

### Group A — Shape-1 appendage integration (HIGH severity)

**Members:** F2 (3 docs) + F4 (a specific instance of F2 on
tensions).

**Pattern:** trailing "(β) — added 2026-05-03" section with
dual-narrative.

**Recomposition move:** for each affected doc, *integrate the
appendage's content into the canonical narrative*, then delete
the appendage. The framework's anti-pattern (additive only) is
satisfied at the cotype level — the migration history is
preserved in
[shadow_migration_plan.md](shadow_migration_plan.md) and the
five per-step shadows. The user-facing prose's "additive
forward-thickening" obligation is *to absorb new content, not to
freeze the old phrasing*.

**Severity composition:** three same-grade RFS sites. The
operator (Shape-1 detection) is not new; what's new is
*integration*. Per shadow-architecture rule 6, the integration is
an orbit-cataloguing move (S2G-flavoured) over the three sites,
*not* a wrapper extraction. Each integration is local to its
doc; no cross-doc abstraction is needed.

### Group B — depth-grade signposting + cotype discoverability (MEDIUM severity)

**Members:** F1 (README missing (β)) + F7 (cotype invisible) + F9
(no grade preamble).

**Pattern:** the ladder is real but not visible to readers
moving along it. Shallow readers can't see the depth-axis or
the cotype.

**Recomposition move:** add a small "where you are in the
ladder" preamble to each doc; add a README mention of (β) and
cotype/ at the appropriate shallow-grade abstraction; add
cross-grade pointers between adjacent rungs.

### Group C — minor / deferred (LOW severity)

**Members:** F5 (examples.md already-aligned), F6 (quartet
shadow current), F8 (terminology spot-check).

**Pattern:** small drift; can be addressed in a follow-up
sweep without urgent reader-confusion impact.

## Recomposition feasibility (Step 4)

Tracing each external commitment through the planned cleanup:

| Commitment | Mechanism |
|------------|-----------|
| Cross-refs continue to resolve | Integration moves content; existing anchors stay or get updated symmetrically |
| Self-hosting claim preserved | Docs as witnesses of methodology *strengthens* under integration (G5) |
| Depth-graded ladder preserved | Cleanup operates per-rung; ladder structure unchanged |
| Anti-pattern (additive only) | Migration history preserved in cotype/; user-facing prose absorbs new content into its canonical narrative — same discipline applied at the prose level |
| 189 tests green | No code changes in this cleanup; doc-only |
| Reader expectations | Tutorial still walks through; examples still domain templates; theory still has Theorem 14.5 — but with the (β) form as canonical and the legacy form as historical |

All commitments preserved. Recomposition is feasible.

## Recomposition design (Step 4 detail)

### Group A — appendage integration

**README.md** (Finding 1): rewrite the first paragraph to lead
with the RISC core (`introduce_node`, `edge`, `kquery`); present
CISC verbs as named conveniences; mention cotype/ briefly.

**methodology.md** (Findings 2 + 4): integrate the (β) RISC
reframe section into the body. Specifically:

- The "Verbs" section (currently lists CISC verbs) becomes "RISC
  primitives + CISC sugar" with a leading subsection on the
  three RISC verbs and a subsequent table mapping CISC to RISC
  reductions
- The "Tensions" section: lead with "tensions are named
  curry-spec ASTs over kquery" as canonical; present the
  disposition spectrum with concern as one of four; the legacy
  "concerns" framing becomes one disposition rather than the
  primary definition
- Delete the trailing "(β) — added 2026-05-03" section once its
  content has been absorbed

**theory.md** (Finding 2): integrate § 14.9 into § 14.5 (the
Theorem 14.5 implementation section). The strengthened form
becomes the canonical theorem statement; the pre-(β) form is
shown as a historical predecessor inline. Delete § 14.9 once
absorbed.

**tutorial.md** (Findings 2 + 3): reorder. New § 2 introduces
RISC primitives first (small, three verbs); a CISC walkthrough
becomes "named conveniences for common patterns" later. The
existing §§ 3–13 walkthrough either rewrites in RISC terms or
becomes a "CISC walkthrough — equivalent to the RISC version
above" appendix. Delete § 14 once absorbed.

**examples.md** (Finding 5): minor — keep blockquote, optionally
update one or two examples to use RISC primitives directly so
domain authors see both styles.

### Group B — signposting

**Each doc gains a 3-line preamble** stating its grade and
adjacent-grade pointers. Format:

```
> Grade: {tutorial|methodology|theory|...}.
> Shallower: see {previous}.  Deeper: see {next}.
> Architectural detail: see [cotype/](cotype/) shadows.
```

**README.md gains a paragraph** mentioning cotype/ as the
architectural source-of-truth for deep readers, and mentioning
(β) in its first paragraph.

### Group C — deferred

Terminology sweep (F8) and explicit grade-declarations (F9) are
nice-to-haves; defer to a follow-up pass.

## Extraction queue summary

| Site | Class | Action |
|------|-------|--------|
| README.md | RFS recompose | Lead with RISC; mention cotype |
| methodology.md | RFS recompose | Integrate (β) appendage into body; tensions section reframed |
| theory.md | RFS recompose | Integrate § 14.9 into § 14.5 |
| tutorial.md | RFS recompose | Reorder: RISC first; CISC as conveniences |
| examples.md | already-aligned | Optional one-or-two example RISC update |
| Each doc | S2G signposting | 3-line grade preamble |

## Discipline notes

- The recomposition does *not* delete the cotype/ migration
  history. The five per-step shadows + shadow_risc_core.md +
  shadow_migration_plan.md remain the authoritative record of
  *how* the framework arrived at (β). The user-facing docs
  document the post-(β) state as canonical; readers wanting the
  migration trace go to cotype/.
- Per shadow-architecture rule 6, the three appendage sites are
  orbit-elements; the recomposition is per-site (catalogue the
  orbit positions by integrating each), not via a meta-extraction.
- The cleanup itself, when executed, is a region-#8 (DRS-triple)
  fire: DBE produces the criteria (this shadow's cousin
  [shadow_doc_discipline.md](shadow_doc_discipline.md)), RFS
  produces these findings, S2G registers the snap when the
  cleanup completes.

## Cross-references

- [shadow_doc_discipline.md](shadow_doc_discipline.md) — the
  criteria these findings measured against
- [shadow_docs_quartet.md](shadow_docs_quartet.md) — the
  current ladder structure (preserved under cleanup)
- [shadow_risc_core.md](shadow_risc_core.md) — authoritative
  source for (β) commitments referenced by the recomposition
- [rfs_findings.md](rfs_findings.md),
  [rfs_findings_risc_projection.md](rfs_findings_risc_projection.md)
  — prior RFS passes; this one follows the same format
