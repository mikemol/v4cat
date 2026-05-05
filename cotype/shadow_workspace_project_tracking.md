# Shadow: workspace project tracking — SoT split + disciplines

> *DBE+RFS+S2G fire of 2026-05-05. Region **#8** of the
> shadow-architecture lattice. **DBE-led** (a new tracking
> costructure: the SoT split between cotype shadows and GH
> Projects + issues), **RFS** (regroups the existing audit gap
> registry + the trajectory table as instances of GH-Project
> items), **S2G** (this file). Operationalised at the
> [v4cat-oss workspace GH Project][project] +
> [v4cat-oss/methodology][methodology] (host repo for
> workspace-level issues).*

[project]: https://github.com/orgs/v4cat-oss/projects
[methodology]: https://github.com/v4cat-oss/methodology

## Form

The v4cat-oss workspace splits its work-tracking source-of-truth
(SoT) along an **orthogonal-axis** decomposition:

| Axis | Canonical surface | Why |
|---|---|---|
| **Status** (open / in-progress / closed / blocked) | GitHub Issues + the org-level Project | Visibility for outside observers without cloning; queryable across repos; familiar tooling |
| **Structure** (form, entailment, lattice-region, why) | Cotype shadows in `v4cat/cotype/` | Forever, thickens forward; deep prose; the structural memory of the workspace |
| **Linkage** | Mutual back-references | Issue body links to shadow file path; shadow's `Tracking` line links to issue # |

Closure events have **two writes by design**, not duplication:

- Close the issue (canonical for status).
- Append a closure-trail annotation to the shadow (canonical for
  *what closure looked like*, structurally).

These are different content. The issue close says "this is done";
the cotype annotation says "this is what closure produced + how
it composes with the rest of the catalogue."

## Where realised

- **Public methodology repo**: [v4cat-oss/methodology][methodology]
  — hosts workspace-level issues + the public reconciliation of
  the four skills.
- **Per-distribution repos**: each hosts its own distribution-level
  issues.
- **Cotype**: `v4cat/cotype/` continues to be the SoT for
  structural content (no change).
- **Audit**: [audit_workspace_2026_05_04.md](audit_workspace_2026_05_04.md)
  loses its standalone gap-registry section in favour of a
  one-line pointer to the GH Project. Future audit fires will
  re-derive their gap registry by querying the Project's status
  field rather than maintaining a separate prose registry.

## Composition operation

### Issue-host (closure-scope) rule

> An issue's home is determined by **where the writes land**, not
> where the discovery happened.
>
> - **Cross-repo closure** (writes span ≥2 repos in v4cat-oss) →
>   `v4cat-oss/methodology`.
> - **Single-repo closure** → that repo.
> - **Distribution-introducing fires** count as cross-repo
>   (they expand the workspace shape; the v4cat-side cotype work is
>   not negligible) → `v4cat-oss/methodology`.

Worked classifications:

- G3 (bridge round-trip tests for vcif-hlo) → `vcif-hlo`.
- G4 (examples as test fixtures, vcif-hlo) → `vcif-hlo`.
- G5 (vcif/v4cat bootstrap gap) → `methodology` (cross-repo).
- FFI (Agda code calling into v4cat) → `methodology`
  (cross-repo: agda2v4cat ↔ v4cat).
- The 10 Tier-3 extraction items + their epic → `agda2v4cat`.
- All distribution-introducing fires (#1, #2, #4, #6, #9, #10) →
  `methodology`.
- Pure-cotype recognition fires (#3, #5, #7) → `v4cat`.
- Single-distribution closures (#8 G1 in vcif-hlo) → that repo.

### Pedagogical issue-body rule

Issue bodies must be **pedagogical** about shadow-architecture
terminology. Every region number, orbit position, S2G/DBE/RFS
mention, or `region #N` reference should link to the canonical
definition in
[v4cat-oss/methodology](https://github.com/v4cat-oss/methodology).

Issue body convention (template):

```markdown
**Tracking**: see structural shadow `<path>` in v4cat/cotype/.
**Lattice region**: [#N (<region name>)](https://github.com/v4cat-oss/methodology/blob/main/shadow-architecture.md#the-lattice).
**Closure scope**: <list of repos whose writes close this>.

## Summary
<one-paragraph what / why>

## Closure path (for promissory; what realises this)
<concrete next-step plan>

## Worked example / context
<links to relevant shadows or theory.md sections>
```

The body is a *projection* of the shadow's leading content
oriented for action; the shadow remains the deep record.

### Parent-child archive rule

A closed issue is **archived** only when (a) its parent issue is
closed and (b) every sibling under that parent is closed. Until
then, closed children remain visible on the board.

Implementation: the org Project's `parent` custom field links
sub-issues to their parent. When a parent closes, a manual sweep
checks all children and archives the subtree if every child is
closed.

The board's state-density stays bounded at the granularity of
**complete fires**, not individual sub-tasks. Trajectory becomes
queryable in one place without flat-list cruft accumulating.

Worked example (the agda2v4cat-Tier-3 expansion):

- Parent: epic "agda2v4cat Tier-3 extraction expansion" (host:
  `agda2v4cat`).
- Children: 10 individual Tier-3 issues (pragmas, termination,
  …, mutual blocks).
- Each Tier-3 child closes when its v0.x sub-fire lands; closed
  children stay on the board.
- When the 10th Tier-3 child closes → parent epic closes → the
  entire subtree archives in one sweep.

### Promissory-shadow-has-issue rule (added 2026-05-05)

> Every shadow that names a *promissory cell* (a structural
> commitment with a `Closure path` or `When this shadow closes`
> section) must have a corresponding GitHub issue and a
> `Tracking:` line near the top pointing at that issue.

This is the SoT-split discipline applied to its own corpus: the
cotype is canonical for *structure*, but for the **subset of
shadows that name future work**, the GitHub Project board must
have a parallel item so status (open / in-progress / closed) is
queryable.

Auditable invariant: a workspace audit can `grep -L 'Tracking:'
cotype/shadow_*.md | xargs grep -l 'promissory cell\|Closure
path'` and the result must be empty.

Origin: a 2026-05-05 epic-shape audit (region #4 fire #13)
discovered two promissory shadows (`shadow_event_log_gap.md`,
`shadow_stablehlo_export_gap.md`) catalogued in cotype but
without issues — invisible on the Project board. Both got
issues; this rule was added so future audits can mechanically
verify the invariant.

### Epic-shape recognition rule (added 2026-05-05)

> An open issue should be promoted to an `epic` when its body
> lists ≥2 independently-closeable closure-path components AND
> implementation work has begun (or is imminent).

The "implementation has begun" qualifier prevents premature
epic-promotion: many promissory shadows enumerate fine-grained
closure paths that are tightly coupled at implementation time.
Splitting into sub-issues only when the work starts keeps the
Project board's epic-shape signal honest.

Counter-pattern: a closure-path-multi-component issue that
ships in a single PR is operationally region-#5-flirting (DBE
and RFS, without per-step S2G). The epic + sub-issues
structure makes partial progress visible and keeps the lattice
region honest.

### Audit-rederivation procedure

The next workspace audit fire (a region #4 cataloguing fire)
re-derives its gap registry by querying the GH Project's status
field rather than maintaining a separate prose registry. The
audit memo's gap section becomes:

> **Gap registry**: see the [v4cat-oss workspace
> Project](https://github.com/orgs/v4cat-oss/projects). Open
> items in this audit window: [N]. Closed items in this audit
> window: [M]. Per-item structural detail in
> `cotype/shadow_<name>.md` for each gap.

Trajectory remains in prose form (it's structural-history
content, not status), with each row linking to its closed
issue # for back-pointers.

## Entailment

If this discipline is honoured:

1. Outside observers see workspace status without cloning. The
   GH Project answers "what's open / who's working on what /
   what's been closed" in one queryable surface.
2. Cotype shadows preserve the depth (the *why* + the structural
   composition). They are not pulled towards a task-list
   aesthetic.
3. The audit memo loses a recurring maintenance burden — its
   gap registry was always a derived view, now it's queryable
   directly.
4. Reconciliation issues against the methodology repo provide a
   feedback path so the public methodology docs stay faithful
   to the canonical workstation skill specs.

If this discipline is broken (a status update lands in a shadow
without a corresponding issue update; or a structural fact ends
up in an issue body without a shadow):

- The split inverts. The cotype becomes a write-only log;
  observers lose deep context. Or:
- Issues accumulate prose that should be in shadows; the cotype
  thins; structural memory decays.

The discipline check at every fire-close: **did status flow
issue → shadow-annotation, and structural fact flow shadow →
issue-body?** Both must be one-way.

## Lattice classification

Region **#8** (DBE+RFS+S2G).

- **DBE**: forward design of the SoT split + closure-scope rule
  + parent-child archive rule + pedagogical-body convention +
  audit-rederivation procedure.
- **RFS**: regroups the existing audit gap registry + the
  workspace trajectory table + the per-shadow `Closure` sections
  as instances of GH Project items, under the new tracking
  costructure.
- **S2G**: this file.

### Discipline rule 6 (orbit-saturation) check

Orbit position **1** of "v4cat-oss workspace tracking surface".
Below the C7 ≥3 threshold; orbit-driven recurrence parameterised
by *workspace*; **S2G to catalogue, no `MetaTrackingFramework`
wrapper extracted**. v4cat itself remains the universal at the
kernel-cell.

A future second instance would be a different OSS workspace
adopting the same SoT split. At three workspaces the C7
threshold tips toward RFS-eligible.

## Trace integrity

Prior structural content unchanged:

- All cotype shadows retain their `Form / Entailment / Lattice
  classification / Trace integrity` sections. The only addition
  is a one-line `Tracking: see issue #N` near the top of
  promissory shadows.
- The trajectory table in the audit memo retains its rows; each
  row gains a per-row issue-# back-pointer.
- The four-skill methodology is unchanged in substance — what
  changes is its *publication surface* (now in
  `v4cat-oss/methodology`).

## Snap-to-grid check

User's request: "I would like to make gh projects and issues
the SoT for status; it provides a degree of visibility and
clarity to other observers which is otherwise obscured by our
in-repo methodologies."

Cotype's entailment after this shadow lands:

> The v4cat-oss workspace tracks status canonically in
> GitHub Projects + Issues, scoped per the closure-scope rule
> (cross-repo issues in `methodology`, single-repo issues in
> their distribution). Cotype shadows remain canonical for
> structure. The two surfaces are linked by mutual
> back-references; closure events write to both. Audit memos
> re-derive gap registries by querying the Project. The
> four-skill methodology has a public reconciliation surface at
> `v4cat-oss/methodology` so issue bodies are pedagogically
> meaningful to outside observers.

Snap valid. The fire produces a working SoT split *and* the
seam discipline that makes it sustainable.

## Closure path

This shadow is **structural**, not promissory — the discipline
it names is operational from the moment the GH Project + issues
are seeded. The shadow does not have a closure-state; it
thickens with annotations as each future fire applies the
discipline (e.g., when each closed issue triggers a closure-trail
annotation in its corresponding shadow).
