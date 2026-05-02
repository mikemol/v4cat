# Snap-to-grid report (2026-05-02)

Snap check for the session of 2026-05-02 against the user's
request: "make the initial commit (with a .gitignore), run the
test suite to confirm green, and then let's apply the
shadow-architect skill, the regroup-from-shadows skill, the
decompose-by-entailments skill and the snap-to-grid skill to the
repository."

## Cotype contents at snap

| Artefact | Origin | Role |
|----------|--------|------|
| [INDEX.md](INDEX.md) | DBE | cotype index |
| [shadow_cell.md](shadow_cell.md) | DBE | unit of decomposition |
| [shadow_dual_representation.md](shadow_dual_representation.md) | DBE | IMPL ↔ CAT pairing |
| [shadow_kind_stratification.md](shadow_kind_stratification.md) | DBE | 8-way Kinds partition |
| [shadow_kquery_universal_read.md](shadow_kquery_universal_read.md) | DBE | kquery as primitive |
| [shadow_layered_stack.md](shadow_layered_stack.md) | DBE | L0–L7 entailment chain |
| [shadow_docs_quartet.md](shadow_docs_quartet.md) | DBE | depth-graded doc ladder |
| [rfs_findings.md](rfs_findings.md) | RFS | 4 findings, 1 acted, 3 deferred |
| [shadow_kquery_orbit.md](shadow_kquery_orbit.md) | S2G | orbit of named selections |
| [s2g_classifications.md](s2g_classifications.md) | S2G | resolutions of deferrals |

Plus the code-level effect: [views.py](../views.py) reduced from
297 to 212 lines (8 duplicate function definitions removed; the
kquery-mediated `wedge` restored as the live implementation).

## Request × delivery

| User asked for | Cotype/repo state | Status |
|----------------|-------------------|--------|
| Initial commit with .gitignore | Commit `7e02713`; 23 files; .gitignore covers `__pycache__/`, `*.pyc`, `*.db`, venvs | ✓ delivered |
| Tests green | 36 (ISA) + 38 (MCP) + 28 (sandbox) + 16 (self-hosting) = **118 green; 0 failed** at HEAD | ✓ delivered |
| shadow-architecture skill | Lattice classification: region #8 (DRS-triple, substantive structural arc); arc rotation D→R→S; orbit-saturation rule applied | ✓ delivered |
| decomposable-by-entailment | 6 named, externalised shadows in [cotype/](.) with type, realisations, property, composition, entailment, reuse | ✓ delivered |
| regroup-from-shadows | 4 candidates classified per orbit-saturation; 1 acted (views.py dedup, behaviour-preserving); 3 deferred with full classification | ✓ delivered |
| snap-to-grid | This report; +1 new shadow (kquery_orbit); +1 classification doc resolving RFS deferrals; cotype refreshed | ✓ delivered |

## Snap declaration

The cotype's entailment is **consistent with and slightly more
informative than** the user's request. The user asked for the
four skills to fire; the cotype delivers (a) the firings as
evidence, (b) one acted-on extraction, (c) three classified
deferrals, and (d) the orbit-saturation analysis as a
generalisation that protects future RFS fires from the
wrapper-extraction misfire.

**Snap-to-grid: occurred.**

The session's accumulated work is coherent and the deliverable is
readable: a self-hosted v4cat repository at commit `7e02713`+1
(post-dedup), with a populated cotype/ directory ready to inherit
into future sessions.

## Generalisation produced (bonus)

The session validates the shadow-architecture meta-frame
empirically against v4cat itself:

- **DBE = carrier frequency**: produced 6 shadows that frame the
  whole fire; everything else operates inside that frame.
- **RFS = burst**: fired exactly when blocking duplication was
  detected (views.py); silent on the other findings.
- **S2G = sampling rate**: fires at the session boundary; reads
  the cotype, classifies the deferrals, and writes this report.
- **Region #8 (DRS-triple)** dominated the fire as predicted; no
  forbidden regions (#3, #5) entered.

The session is itself a region-#8 instance against the empirical
22-commit trace's 50% DRS-dominance.

## Drift?

None. The user's request was open compound; every clause
delivered with evidence in the cotype. The S2G correction of
RFS's "Kind.A vestigial" framing is *internal* to the
shadow-architecture process (RFS findings get S2G review), not
drift against the user's request.

## What remains

Optional follow-ups, all single-purpose:

1. **Commit cotype + dedup**. The cotype/ files and the views.py
   dedup are uncommitted. A second commit would land them
   together with a message noting the shadow-architecture session.
2. **Kind.A docstring nudge**. Extend [cells.py:33](../cells.py#L33)'s
   comment to record the reservation rationale. Tiny; not
   load-bearing; defer if the user doesn't want it.
3. **Catalogue-side orbit registration**. Add a refinement on
   `Q-kquery` enumerating named-selection orbit positions. Not
   necessary for self-hosting; nice-to-have.

None of these are required for snap; all are deferred candidates
the cotype already names.

## End state

- 118 tests green at the post-dedup state.
- Closure check passes: v4cat is self-hosting (Theorem 14.5).
- Cotype populated and indexed; ready for future sessions.
