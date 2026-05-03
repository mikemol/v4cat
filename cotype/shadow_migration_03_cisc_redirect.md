# Shadow: Migration step S₃ — CISC redirect

> **Forward shadow, generated at S₃ implementation start.**
> Per [shadow_migration_plan.md](shadow_migration_plan.md)'s
> DBE-Step-7 discipline. The largest step by code volume.

## Form

S₃ rewrites every existing CISC verb's *implementation* to delegate
to the S₂ RISC primitives, while preserving every public signature
and behaviour exactly. No new abstractions; the work is mechanical
substitution of bodies guided by the published rewrites in
[shadow_risc_core.md](shadow_risc_core.md)'s CISC reduction table.

```python
# Public signatures unchanged; bodies redirect:

introduce_break(num, name, *, short_desc=None, axes=None) →
    introduce_node(num, name, type='break', attrs={'short_desc': short_desc})
    + edge calls for axes (after S₃ extends edge-kind vocab if needed)

introduce_object(id, name, *, year=None, ..., lineage=None, attrs=None) →
    introduce_node(id, name, type='spec', attrs={year, catalogue_order, notes, **attrs})
    + lineage_witness(id, anc, kind) for each (anc, kind) in lineage

introduce_tension(id, name, *, description=None, ..., breaks_involved=None) →
    introduce_node(id, name, type='tension', attrs={description, ...})
    + tension_breaks INSERT for each break (legacy table dual-write)

witness(subject, break_, kind, *, notes=None, scope='spec') →
    edge(subject, break_, kind, notes=notes)
    + (scope still written via direct INSERT to preserve agent-level distinction)

refine(break_, object_, name, *, description=None) →
    introduce_node(name, name, type='break', attrs={'short_desc': description})
    + edge(object_, name, kind='origin')
    + edge(object_, break_, kind='refines')
    + INSERT into refinements (legacy table dual-write)

defer/promote/boundary(...)  →  edge(by, break_, kind=K, notes=reason)

lineage_witness(descendant, ancestor, kind, *, notes=None)  [NEW] →
    edge(descendant, ancestor, kind, notes=notes)
```

## Realisations

| Verb | File | Nature of edit |
|------|------|----------------|
| `introduce_break` | [catalogue.py](../src/v4cat/catalogue.py) | body replaced; signature unchanged |
| `introduce_object` | [catalogue.py](../src/v4cat/catalogue.py) | body replaced; signature unchanged |
| `introduce_tension` | [catalogue.py](../src/v4cat/catalogue.py) | body replaced; signature unchanged |
| `witness` | [catalogue.py](../src/v4cat/catalogue.py) | body replaced; signature unchanged |
| `refine` | [catalogue.py](../src/v4cat/catalogue.py) | body replaced; signature unchanged |
| `defer` / `promote` / `boundary` | [catalogue.py](../src/v4cat/catalogue.py) | bodies redirect via internal `witness` (which now delegates to `edge`) — already orbit-elements per RFS Finding 4 |
| `lineage_witness` | [catalogue.py](../src/v4cat/catalogue.py) | new public method; CISC sugar over `edge` |
| MCP wrappers | [mcp_server.py](../src/v4cat/mcp_server.py) | no change — they delegate to catalogue.py's CISC verbs which now route through RISC; behaviour preserved by signature inheritance |

The `axes` parameter on `introduce_break` writes to `break_axes`,
which is its own table not covered by the RISC `edge` (since axes
are break→axis-string, not break→break or spec→break). Rather
than expand `edge` to cover axes (a third graph would inflate the
RISC core), `introduce_break`'s axes-handling stays as a direct
INSERT — a localised CISC-internal detail, not a RISC violation.
Same reasoning for `introduce_tension`'s `tension_breaks`
sub-INSERTs and `refine`'s `refinements` dual-write.

## Composition (with the migration plan)

S₃ is the *substantive* step. After S₃:

- Every public CISC verb's body is a thin redirect to RISC primitives
- The framework's data flow is: user calls CISC → CISC invokes RISC →
  RISC validates against type-system seed → RISC writes to legacy
  physical storage
- The RISC discipline is realised in code, not just declared

S₃ does *not* yet:

- Reclassify SIGNATURE (deferred to S₄)
- Catalogue the framework's SQL views as utility-tensions in the
  seed (deferred to S₄/S₅; the curry-spec evaluator already exists,
  and the views can be catalogued data later)
- Update methodology/theory/tutorial docs (S₅)

## Validation note: scope on witnesses

The existing `witness(subject, break_, kind, *, notes, scope='spec')`
takes a `scope` parameter (S8-introduced agent vs spec
distinction). The RISC `edge` doesn't carry scope. Resolution:
`witness`'s body delegates to `edge` for the spec-scoped case
(default), and for `scope='agent'` falls through to a direct
INSERT into witnesses with the agent scope. This preserves the
agent-level distinction without inflating `edge`.

## Entailment

```text
Each CISC verb's signature ≡ pre-S₃ signature
  ∧ each verb's body delegates to RISC primitives whose validation
    is congruent with the pre-S₃ behaviour
  ⟹ all 184 tests pass without modification
  ∧ the RISC discipline is realised: every mutation flows through
    introduce_node or edge or remains a localised CISC-internal
    sub-INSERT for the carrier-axis tables (break_axes,
    tension_breaks, refinements) that the RISC core deliberately
    doesn't cover
  ⟹ S₃ is additive at the discipline level (RISC adoption) and
    behaviour-preserving at the user level (signatures + tests)
```

## External commitments preserved

| Commitment | Mechanism |
|------------|-----------|
| 184 tests pass | Public signatures unchanged; behaviour identical at the call-signature level; legacy tables continue to be populated |
| Public `SymmetryCatalogue` API | Method signatures unchanged; new `lineage_witness` is purely additive |
| MCP tool surface | Inherits via delegation — MCP wrappers call catalogue.py methods unchanged |
| Closure check passes | S₃ doesn't touch SIGNATURE or `framework`-witnessed rows |
| Anti-pattern (no drops) | Bodies replaced, but no method or column removed; dual-write to legacy tables preserves data presence |
| Database compatibility | Pre-S₂ catalogues (without type-system seed) keep working with the *legacy* paths only — for them, CISC verbs delegate to internal helper that writes directly without going through RISC; check via `_type_system_loaded` toggles the path |
| Refinements table consistency | `refine` continues to populate the table (dual-write); existing `refinements_for_break` reads continue to function |

## Backwards-compat path: `_type_system_loaded` gates RISC delegation

CISC verbs need to work in two modes:

- **`check_self_hosting=True`** (default): type-system seed loaded → CISC delegates to RISC, full validation engages
- **`check_self_hosting=False`**: type-system seed absent → CISC writes directly to legacy tables (the pre-S₂ behaviour); validation skipped (matching the `bootstrap=False` semantics of `supported_kinds`/closure check)

Each rewritten verb begins with:

```python
if self._type_system_loaded():
    self.introduce_node(...)  # or self.edge(...)
else:
    # Fall through to the legacy direct-INSERT path
    ...
```

This is the additive bridge that lets the migration land without
breaking `check_self_hosting=False` tests.

## Step-witness (the green-light criterion)

Implementation of S₃ is complete iff:

1. All eight CISC verbs (`introduce_break`, `introduce_object`,
   `introduce_tension`, `witness`, `refine`, `defer`, `promote`,
   `boundary`) have RISC-delegating bodies in their
   `_type_system_loaded()=True` branches
2. New CISC sugar `lineage_witness` exists
3. Full test suite (now 184) still passes — including the
   pre-existing `check_self_hosting=False` tests
4. New tests verifying CISC→RISC delegation pass

## Cross-references

- [shadow_risc_core.md](shadow_risc_core.md) — CISC reduction
  table specifies the rewrite for each verb
- [shadow_migration_plan.md](shadow_migration_plan.md) — S₃ of 5
- [shadow_migration_02_risc_dispatch.md](shadow_migration_02_risc_dispatch.md)
  — provides the RISC primitives this step delegates to
- [rfs_findings_risc_projection.md](rfs_findings_risc_projection.md)
  — Findings 2, 3, 4, 5 covered here; Finding 6 (tensions
  schema delta) already done in S₁
