# RFS findings — RISC projection (2026-05-03)

Sideways read of the codebase against
[shadow_risc_core.md](shadow_risc_core.md) and
[shadow_migration_plan.md](shadow_migration_plan.md). For each
candidate, classified per the orbit-saturation refinement (rule 6
of `shadow-architecture/SKILL.md`): is the recurrence free
duplication (extract universal record = RFS), orbit-elements
under a generating operator (catalogue orbit position = S2G),
already-aligned, or pure additive (no extraction needed)?

External commitments fixed for behaviour preservation:

- 169 tests across `tests/test_isa.py` (39), `test_branch_coverage.py` (47), `test_mcp.py` (39), `test_sandbox.py` (28), `test_self_hosting.py` (16) — all must pass post-migration
- Public `SymmetryCatalogue` API — every existing method's call signature preserved
- MCP tool surface unchanged
- Closure check (Theorem 14.5) passes; strengthens additively in S₄
- Anti-pattern: additive only — no schema drops, no destructive verbs
- Database compatibility — pre-existing catalogues open without manual migration
- IMPL ↔ CAT pairings in `framework_seed.sql` remain consistent

## Findings

### Finding 1 — `kquery` is already at the RISC level

`kquery` is implemented in
[views.py](../src/v4cat/views.py) as the universal four-cell
classifier and is already named as `Cell.K` in
[theory.py:70-71](../src/v4cat/theory.py#L70-L71).

**Classification: already-aligned.**
**Lattice region: neither.** No work needed — `kquery` *is* the
RISC primitive the shadow names. Every other read in the system
already reduces to a kquery call (per
[shadow_kquery_universal_read.md](shadow_kquery_universal_read.md)).

**Migration impact:** S₂'s curry-spec evaluator wraps `kquery`
without modifying it. The strengthened closure check in S₄ adds
new verifications *around* `kquery`, leaving the primitive itself
untouched.

### Finding 2 — `introduce_break` ⊕ `introduce_object` → `introduce_node` (RFS)

[catalogue.py:133-154](../src/v4cat/catalogue.py#L133-L154) and
[catalogue.py:156-216](../src/v4cat/catalogue.py#L156-L216) are two
same-grade instances of "introduce a typed node into a
type-specific table with optional sub-edge population":

- `introduce_break(number, name, *, short_desc, axes)` — inserts
  into `breaks`; if `axes`, inserts into `break_axes`.
- `introduce_object(id, name, *, year, catalogue_order, notes,
  lineage, attrs)` — inserts into `specs`; if `lineage`, inserts
  into `lineages`; if `attrs`, inserts into `spec_attributes`.

Both share the shape "INSERT into typed table + optionally INSERT
into related sub-tables." The differences are exactly:
target-table, attribute-set, sub-edge-table.

**Classification: free duplication ⟹ RFS.** Two same-grade
instances; differences are quotient-able under
`introduce_node(id, name, type, attrs)` parametrised over `type`.
The universal record is the new RISC primitive; the existing
verbs become CISC sugar.

**Recomposition (executed in S₂ → S₃):** Add `introduce_node`
(S₂); rewrite `introduce_break` and `introduce_object` to delegate
to it (S₃). Sub-edge population (axes / lineages / attrs) becomes
ordinary `edge(...)` calls in the delegate.

**External commitments preserved:** Both verbs keep their full
signatures, so all call sites in tests and `framework_seed.sql`
continue to work unchanged.

### Finding 3 — `witness` ⊕ buried-lineage-write → `edge` (RFS)

[catalogue.py:383-404](../src/v4cat/catalogue.py#L383-L404) is the
public `witness(subject, break_, kind, *, notes, scope)` method
(spec→break edges). The lineage-edge-write is *buried* inside
`introduce_object` at
[catalogue.py:200-207](../src/v4cat/catalogue.py#L200-L207) — no
public verb writes spec→spec edges.

The asymmetry the shadow flagged is real and visible: two graphs
exist (`witnesses` and `lineages`), but only one has a public
write-verb. Both are typed-edge writes; the differences are
exactly: target-graph, kind-namespace.

**Classification: free duplication + buried instance ⟹ RFS.** The
abstraction is `edge(src, tgt, kind, *, notes)`. Extraction
surfaces the previously-buried lineage-edge-write as a first-class
public CISC sugar (`lineage_witness`). Type-validation against
the catalogued kind-typing decides which physical table receives
the row.

**Recomposition (S₂ → S₃):** Add `edge` (S₂); rewrite `witness`
to delegate (S₃); add `lineage_witness` as new CISC sugar
(S₃) and rewrite `introduce_object`'s `lineage=...` parameter
loop to call it.

**External commitments preserved:** `witness`'s public signature
unchanged; `introduce_object`'s public signature unchanged; the
*new* `lineage_witness` is purely additive (no existing call
sites to break).

### Finding 4 — `defer` / `promote` / `boundary` are orbit-elements (S2G, NOT RFS)

[catalogue.py:442-483](../src/v4cat/catalogue.py#L442-L483)
contains three near-identical CISC sugar verbs:

```python
def defer(...):     self.witness(by, break_, 'deferred-candidate', ...)
def promote(...):   self.witness(by, break_, 'confirms', ...)
def boundary(...):  self.witness(by, break_, 'sibling-boundary', ...)
```

Three same-grade instances. C7 threshold met. **But:** the
generator IS visible — they're orbit-elements of `witness(spec,
break, kind=K)` parametrised by K ∈ {'deferred-candidate',
'confirms', 'sibling-boundary'}. The operator `witness` already
serves as the universal at the carrier-axis.

**Classification: orbit-driven, NOT free duplication.** Per
shadow-architecture rule 6, extracting a "universal CISC-trivial
wrapper" would produce a wrapper-of-the-operator — the false-
positive case the rule guards against.

**Lattice region: S2G** (catalogue orbit position; resist
wrapper extraction). The trio remains as-is in code; in the
SIGNATURE reclassification (S₄) each gains
`derives_from=('witness',)` to mark its orbit-element status
explicitly.

**External commitments preserved:** Zero code change for the
orbit; behaviour identical.

### Finding 5 — `refine` bypasses RISC primitives (BLOCKING; RFS via composition)

[catalogue.py:406-424](../src/v4cat/catalogue.py#L406-L424) writes
*directly* to the `refinements` table:

```python
def refine(self, break_, object_, name, *, description=None):
    self.conn.execute(
        "INSERT INTO refinements "
        "(break_number, spec_id, name, description) "
        "VALUES (?, ?, ?, ?)",
        (break_, object_, name, description),
    )
```

This is the principal CISC-bypassing-RISC violation that
triggered the entire framing pass. The shadow's reduction is:

```
refine(P, spec, R, desc)
  ≡ introduce_node(id=R, name=R, type='break', attrs={short_desc=desc})
  + edge(spec, R, 'origin')
  + edge(spec, P, 'refines')
```

**Classification: composition extraction ⟹ RFS.** The "shadow" is
the three-step composition; the rebuilt `refine` is a thin CISC
wrapper that calls the composition.

**Recomposition (S₃):** Rewrite `refine` to the three-call
delegation. Continue dual-writing to `refinements` for backwards
compatibility (anti-pattern: no drops). The `refinements` table
becomes a derived index over the post-migration witness graph;
existing `refinements_for_break` reads continue to function from
the table.

**External commitments preserved:** `refine`'s signature unchanged;
the `refinements` table continues to exist and contain the same
rows; queries against it continue to return the same results;
all call sites in tests and `examples.md` continue to work.

### Finding 6 — `break_origin` / `break_first_seen` / `break_status` are tensions in disguise (RFS)

[schema.sql:238-302](../src/v4cat/schema.sql#L238-L302) defines
three SQL views over the witness graph:

- `break_origin` — kquery shape: (origin-class witnesses, year-axis-cut)
- `break_first_seen` — kquery shape: (catalogue-introduces witnesses, catalogue_order-axis-cut)
- `break_status` — kquery shape: (witness-kinds pattern detection)

Three same-grade instances of "named parameterised kquery shape
over the witness graph." The shadow's curry-spec algebra plus the
`Tension` wrapper is the universal record above them.

**Classification: free duplication of structure across SQL views
⟹ RFS** (the views are *currently* not catalogued as tensions;
extraction promotes them to first-class catalogued entries).

**Recomposition (S₁ → S₃):** S₁ adds the schema columns
(`disposition`, `parameters_json`, `shape_json`); the type-system
seed in S₁ catalogues these three plus any others as utility-
disposition tensions. S₂ adds the curry-spec evaluator. The SQL
views remain as physical caches (anti-pattern: no drops); they're
also reachable via `evaluate_tension('Q-break-origin', B='X', ...)`.

**External commitments preserved:** Views remain queryable;
existing reads via `cur.fetchone()` against `break_origin` etc.
continue to function. The catalogue's API methods (`origin`,
`first_seen`, `status`) optionally route through either path
(cache or evaluator) — initially the cache path, eventually the
evaluator path once stability is established.

### Finding 7 — `tropical_min` / `tropical_max` are tension-evaluator orbit-elements (S2G)

[catalogue.py:251-355](../src/v4cat/catalogue.py#L251-L355) defines
two methods that aggregate over an ordered axis with a witness-
kind filter. They share the entire body modulo `direction` —
clearly orbit-elements, not free duplicates.

**Classification: orbit-driven ⟹ S2G.** The generator is "the
templated-tension evaluator over an ordered-axis cut, parametrised
by direction." The shadow's curry-spec evaluator IS the universal;
once it exists (S₂), `tropical_min` / `tropical_max` are orbit
positions of it (sweep-direction = MIN vs MAX).

**Migration impact:** Both methods stay in `catalogue.py` for
ergonomics. SIGNATURE entries (S₄) gain
`derives_from=('kquery',)` and reference the catalogued
tension-evaluator. The implementation can stay as direct SQL
(no behavioural change); the *meaning* becomes a klein-four
sweep.

### Finding 8 — `origin` / `first_seen` / `retroactive_gap` are tension-consumer orbit-elements (S2G)

[catalogue.py:489-578](../src/v4cat/catalogue.py#L489-L578) defines
three derived-read methods. Each calls `tropical_min` (or reads a
SQL view that's a tropical-MIN materialisation) with different
fixed parameters. Three same-grade instances of "evaluate a
templated utility-tension."

**Classification: orbit-driven ⟹ S2G.** Per finding 7, the
templated-tension evaluator is the universal; these three are
orbit positions of it parametrised by (axis-column, witness-
kinds).

**Migration impact:** No code change beyond what S₃ produces
through `tropical_min`'s redirection. SIGNATURE doesn't currently
list these three (they're public methods on `SymmetryCatalogue`
without Cell entries) — they remain that way.

### Finding 9 — MCP server wrappers (already-aligned)

[mcp_server.py](../src/v4cat/mcp_server.py)'s tool functions are
thin remoting wrappers over `SymmetryCatalogue` methods. They have
no structural content beyond delegation.

**Classification: already-aligned.** Behaviour preservation is by
signature inheritance — when the underlying catalogue method
delegates to RISC, the MCP wrapper inherits the new path
transparently.

**Migration impact:** Zero direct change. New tools (`introduce_node`,
`edge`, possibly `evaluate_tension`) get added in S₂ as additional
remotings; existing tools keep working.

### Finding 10 — `Cell` dataclass needs `derives_from` field (additive)

[cells.py:44](../src/v4cat/cells.py#L44) defines the `Cell`
dataclass that backs `SIGNATURE`. The shadow's S₄ adds a
`derives_from: tuple[str, ...] | None` field so non-RISC cells
can declare their reduction chain.

**Classification: additive schema extension** — neither RFS nor
S2G, just the per-step delta required by S₄.

**Migration impact:** S₄'s primary code change. Existing cells
get `derives_from=None` (RISC) or a populated tuple (CISC /
DERIVED). The closure check in
[bootstrap.py:206-227](../src/v4cat/bootstrap.py#L206-L227) gains
verification that `derives_from` chains terminate in RISC cells.

## Recomposition feasibility (Step 4 verification)

Tracing each external commitment through the planned recomposition:

| Commitment | Preservation mechanism |
|------------|------------------------|
| 169 tests pass | All public APIs preserved by CISC-as-delegation; behaviour identical at the call-signature level |
| Public `SymmetryCatalogue` API | Existing methods preserved; new methods (`introduce_node`, `edge`, evaluator) added strictly additively |
| MCP tool surface | Inherits via delegation (Finding 9) |
| Closure check passes | Each step is additive over `K`; per Theorem 14.5, closure preserved (this is the migration's load-bearing claim) |
| Anti-pattern (no drops) | Every extraction is delegation, not replacement; legacy tables and methods retained |
| Database compatibility | Schema additions use `ALTER TABLE ... ADD COLUMN` with defaults; existing catalogues open without alteration |
| IMPL ↔ CAT pairings | New IMPL cells (`introduce_node`, `edge`) get matching CAT entries in `framework_seed.sql` (S₁); existing pairings unchanged |

All commitments preserved. Recomposition is feasible.

## Extraction queue (mapping to migration steps)

Per the migration plan's partial order:

| Step | Extractions / Recompositions |
|------|------------------------------|
| S₁ | Catalogue tensions in seed (Finding 6 prep); add `disposition`/`parameters_json`/`shape_json` columns; seed type-system rows |
| S₂ | Add `introduce_node` (Finding 2 universal); add `edge` (Finding 3 universal); add curry-spec AST + evaluator (Finding 6 universal); validation hooks |
| S₃ | Redirect `introduce_break`/`introduce_object` (Finding 2 recomposition); redirect `witness` + add `lineage_witness` (Finding 3); rewrite `refine` (Finding 5); update MCP wrappers (Finding 9 — automatic via delegation) |
| S₄ | Add `derives_from` to `Cell` (Finding 10); annotate orbit-element CISC entries (Findings 4, 7, 8); strengthen closure check |
| S₅ | methodology.md / theory.md / tutorial.md / examples.md updates |

## Discipline notes

- Findings 1, 9, 10 require no extraction (already-aligned or pure additive).
- Findings 2, 3, 5, 6 are RFS extractions — universal records above ≥2 same-grade instances.
- Findings 4, 7, 8 are orbit-S2G — the operator is already the universal; no wrapper extraction.
- The split is empirically: 4 RFS extractions, 3 S2G orbit-cataloguings, 3 already-aligned/additive. Predicts that S₃'s commit cadence will be wider than S₄'s (more substantive extractions vs. mostly metadata).

The recomposition does not introduce any singleton "shadow"
extractions (no helper-functions-extracted-once); every named
substructure has demonstrated reuse across at least two call
sites or a quotient class.

## Cross-references

- [shadow_risc_core.md](shadow_risc_core.md) — the target architecture
- [shadow_migration_plan.md](shadow_migration_plan.md) — the ordered additive composition this RFS pass populates
- [rfs_findings.md](rfs_findings.md) — prior RFS pass (2026-05-02) on views.py duplication; this doc follows the same format
- [INDEX.md](INDEX.md) — registers both the prior and current findings
