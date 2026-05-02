# RFS findings (2026-05-02)

Sideways read of v4cat against the DBE-produced shadows. Classified
each candidate against the orbit-saturation refinement (rule 6 of
`shadow-architecture/SKILL.md`): is the recurrence free duplication
(extract universal record = RFS), or is it orbit-elements under a
generating operator (catalogue orbit position = S2G, resist wrapper
extraction)?

## Findings

### Finding 1 — views.py contains 8 duplicate function definitions

**Severity: BLOCKING.** RFS automatic-firing condition met.

[views.py](../views.py) defines 8 functions twice. Most pairs are
byte-identical; one pair is behaviourally divergent.

| Function | First copy | Second copy | Equivalent? |
|----------|------------|-------------|-------------|
| `axis_distribution` | line 159 | line 215 | yes (modulo docstring) |
| `mixed_breaks`      | line 167 | line 227 | yes |
| `consistency`       | line 172 | line 232 | yes (modulo docstring) |
| `retroactive_attributions` | line 189 | line 269 | yes (modulo docstring) |
| `top_originators`   | line 194 | line 278 | yes |
| `agent_level_witnesses` | line 205 | line 289 | yes |
| `spec_axis_summary` | line 210 | line 294 | yes |
| `wedge`             | line 103 | line 245 | **NO — divergent implementation** |

Python's last-write-wins import semantics means the second copy is
the live definition for each function. For 7 of the 8, this is
silently equivalent. For `wedge`, the second copy bypasses kquery
and uses raw set operations — directly contradicting the framework's
central thesis ([views.py:13-18](../views.py#L13-L18) and
methodology.md "The Klein-four read core") that *every* read is a
kquery selection.

Tests pass only because both `wedge` definitions return the same
legacy-shape dict. The contradiction is structural, not behavioural
on test inputs.

**Classification: free duplication.** Each pair is two competing
definitions for the same name; not orbit-elements under any
operator. The recurrence is accidental (likely a copy-paste
accident during early authorship), not structural.

**Lattice region: RFS.** Extraction target is degenerate — the
"shadow" is just the canonical first-copy definition, and the
recomposition is deletion of lines 215-296 of views.py.

**External commitments preserved by the move:**
- `__init__.py`'s 14 exports remain importable.
- `test_wedge_legacy_shape` still passes (kquery-mediated wedge
  returns the same legacy shape).
- All 7 catalogue-view tests unchanged.
- The framework's "every read is a kquery" claim is restored as a
  realised invariant of the codebase.

### Finding 2 — V4 cell table across docs is orbit-driven

**Severity: not actionable; S2G territory.**

The V4 cell table (the 4-cell `11/10/01/00` enumeration) appears
~20 times across theory.md, tutorial.md, and README.md. On first
look this resembles RFS-bait (≥3 instances of the same pattern).

**Classification: orbit-element.** Each occurrence is one
*depth-graded re-statement* of the same canonical structure. The
generator is "show V4 cells at audience N's level":

- README: glance — table form, one paragraph.
- tutorial: hands-on — worked through with example data.
- methodology: reference — formal cell semantics.
- theory: proof — cells as ℤ₂ × ℤ₂ group elements.
- examples: application — cells as audit operators per domain.

Each level *reformulates* the shared content; extracting them into
a single shared snippet would erase the grading that is the doc
suite's reason for existing.

**Lattice region: S2G.** The V4 cell table is the orbit *generator*;
each doc's cell-table appearance is an orbit-element. S2G should
catalogue the orbit positions, not extract a universal record.

### Finding 3 — Kind.A is a vestigial orbit slot

**Severity: not actionable by RFS; S2G territory.**

[cells.py:34](../cells.py#L34) declares `Kind.A` as "wedge audits."
But:

- No `Cell` in `theory.py:SIGNATURE` uses `Kind.A`.
- `'A'` is absent from `supported_kinds = 'O,B,W,R,E,K,X'`
  ([framework_seed.sql:106](../framework_seed.sql#L106)).
- `wedge`, `agree`, `blind`, `coverage`, `left_residue`,
  `right_residue` are exported by `__init__.py` but have no Cell
  entries.

**Classification: orbit-element of kquery.** All six named
selections are kquery-orbit-positions:

```
wedge(a, b)         ≡ kquery(a, b, emit={10, 01, 11}).reformatted
agree(a, b)         ≡ kquery(a, b, emit={11})['11']
left_residue(a, b)  ≡ kquery(a, b, emit={10})['10']
right_residue(a, b) ≡ kquery(a, b, emit={01})['01']
blind(a, b, U)      ≡ kquery(a, b, U, emit={00})['00']
coverage(a, b)      ≡ kquery(a, b, emit={10,01,11}).flatten
```

The carrier-axis is **kquery itself** as the universal read
operator (`Kind.K`). Promoting these six to their own Cells under
`Kind.A` would be the "wrapper-of-an-existing-operator" misfire
warned against in the orbit-saturation refinement: kquery already
serves as the universal at the carrier-axis, so the wrapper would
be vacuous.

**Lattice region: S2G.** The right move is to catalogue the orbit
of kquery (which named selections it covers, and that the orbit is
saturated), not to register six new Cells. `Kind.A` itself can be
either:

- (a) deleted from `cells.py` since no Cell uses it and `'A'` is
  not in scope — clean removal of a vestigial slot.
- (b) repurposed for a future kind not currently realised.
- (c) documented as "reserved" with a `# RESERVED` comment.

The decision belongs to S2G — but RFS notes the classification so
S2G has the orbit-saturation diagnosis pre-computed.

### Finding 4 — gap.10/gap.01 vocabulary is not duplicated

**Severity: none.**

The terms `gap.10`, `gap.01`, `implicit`, `promissory` recur across
[bootstrap.py](../bootstrap.py), [theory.py](../theory.py),
[framework_seed.sql](../framework_seed.sql), [theory.md](../theory.md),
[methodology.md](../methodology.md), and the
`SelfHostingViolation` payload. Every recurrence is a *use* of the
vocabulary at a different site, not a *definition* of it.

**Classification: canonical vocabulary in single use.** Already
correct. No move.

## Summary

| # | Finding | Lattice region | Action this fire |
|---|---------|----------------|-------------------|
| 1 | views.py duplication | RFS | **Extract & rebuild** |
| 2 | V4 cell table across docs | S2G | Defer to S2G fire |
| 3 | Kind.A vestigial slot | S2G | Defer to S2G fire |
| 4 | gap vocabulary | n/a | No move |

Findings 2–4 are recorded so S2G's snap fire has them pre-classified.
