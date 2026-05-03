# Shadow: Migration step S₄ — SIGNATURE reclassification

> **Forward shadow, generated at S₄ implementation start.**
> Per [shadow_migration_plan.md](shadow_migration_plan.md)'s
> DBE-Step-7 discipline.

## Form

S₄ makes the RISC discipline **structurally visible in
SIGNATURE**: each cell declares whether it is RISC (irreducible)
or CISC/DERIVED (reducible to RISC by a documented rewrite). The
reduction chain is encoded as a new `derives_from` field on
`Cell`. The framework's existing closure check (Theorem 14.5)
gains a self-coherence verification: every CISC cell's
`derives_from` chain must terminate in RISC cells.

```python
# cells.py — Cell dataclass extension
@dataclass(frozen=True)
class Cell:
    id:           str
    kind:         Kind
    description:  str = ''
    derives_from: Optional[tuple[str, ...]] = None  # S₄ addition

# theory.py — SIGNATURE additions and annotations
Cell('introduce_node',  Kind.O, 'Universal node introduction', None)
Cell('edge',            Kind.W, 'Universal typed-edge introduction', None)
Cell('lineage_witness', Kind.W, 'CISC sugar over edge for spec-spec graph',
     derives_from=('edge',))

# Existing CISC cells annotated with their reductions:
Cell('introduce_break',   Kind.B, ..., derives_from=('introduce_node',))
Cell('introduce_object',  Kind.O, ..., derives_from=('introduce_node', 'edge'))
Cell('introduce_tension', Kind.O, ..., derives_from=('introduce_node',))
Cell('witness',           Kind.W, ..., derives_from=('edge',))
Cell('refine',            Kind.R, ..., derives_from=('introduce_node', 'edge'))
Cell('defer',             Kind.W, ..., derives_from=('witness',))
Cell('promote',           Kind.W, ..., derives_from=('witness',))
Cell('boundary',          Kind.W, ..., derives_from=('witness',))
Cell('tropical_min',      Kind.K, ..., derives_from=('kquery',))
Cell('tropical_max',      Kind.K, ..., derives_from=('kquery',))
```

## Realisations

| Form element | Target file | Position |
|--------------|-------------|----------|
| `derives_from` field | [cells.py](../src/v4cat/cells.py) | new field on `Cell`; default `None`; not consulted by hash/eq |
| New SIGNATURE cells | [theory.py](../src/v4cat/theory.py) | `introduce_node`, `edge`, `lineage_witness` added |
| Annotated existing cells | [theory.py](../src/v4cat/theory.py) | every CISC cell gets a `derives_from` tuple |
| New CAT entries | [framework_seed.sql](../src/v4cat/framework_seed.sql) | `Q-introduce_node`, `Q-edge`, `Q-lineage_witness` breaks + framework witnesses |
| Self-coherence check | [bootstrap.py](../src/v4cat/bootstrap.py) | new function verifying every cell's `derives_from` chain terminates in cells with `derives_from is None` (RISC) |

## Composition (with the migration plan)

S₄ is the *theorem-strengthening* step. After S₄:

- The RISC core is *visible in code*, not just in the shadow doc:
  cells with `derives_from is None` and `kind ∈ {O, W, K}` for the
  three RISC primitives (introduce_node, edge, kquery).
- Every CISC verb's `derives_from` documents its reduction; the
  closure check verifies these chains are valid (no orphan
  references; chains terminate in RISC).
- New IMPL ↔ CAT pairings for `introduce_node`, `edge`,
  `lineage_witness` keep the existing Theorem 14.5 closure check
  green while widening its scope.

## Theorem 14.5 strengthening

The original Theorem 14.5:

```text
∀c ∈ scope. (IMPL(c) ↔ CAT(c))   ⟹   gap = ∅
```

Strengthens to:

```text
∀c ∈ scope. (IMPL(c) ↔ CAT(c))                          (existing)
  ∧ ∀c. derives_from(c) is None
       ∨ derives_from(c) ⊆ {c' : c' is reachable in scope
                                  via cells.id matching}      (new)
  ∧ ∀c. closure(derives_from-chain from c) terminates in
        cells with derives_from = None                        (new)
  ⟹  the framework is RISC-disciplined
```

The strengthening is multiplicative — the original closure check
stays as-is, and the self-coherence check is an additional
predicate that must hold for the framework to claim RISC
discipline. This is **closure over a smaller primitive set is a
stronger claim** in action: the closure-relevant primitives are
now {introduce_node, edge, kquery} alone, with everything else
*derived* and verified-as-derived.

## External commitments preserved

| Commitment | Mechanism |
|------------|-----------|
| 184 tests pass | New SIGNATURE cells get matching CAT entries; existing cells gain metadata only (derives_from) which doesn't affect IMPL/CAT predicates |
| Public `SymmetryCatalogue` API | No change in S₄ |
| MCP tool surface | Unchanged |
| Closure check passes | Symmetric updates to SIGNATURE and framework_seed.sql; new self-coherence check passes by construction (derives_from chains terminate in RISC by construction) |
| Anti-pattern (no drops) | Pure additions: new field with default, new cells, new Q-breaks, new self-coherence verification |
| Database compatibility | Pure code additions; framework_seed.sql additions are idempotent via INSERT OR IGNORE |
| IMPL ↔ CAT pairings | Symmetric extension on both sides |

## Discipline check (per shadow-architecture rule 6)

S₄'s `derives_from` chains for `tropical_min` / `tropical_max`
encode that they are orbit-elements of the kquery-sweep evaluator
(both reduce to `('kquery',)`). Annotating them does not extract
a wrapper — they remain as individual SIGNATURE cells with the
documented orbit relationship to `kquery`. This matches the
prior decision in
[shadow_kquery_orbit.md](shadow_kquery_orbit.md): named
selections are catalogued orbit positions, not new universal
records.

Same logic for `defer`/`promote`/`boundary` deriving from
`witness`: orbit-elements over the witness-kind axis.

## Step-witness (the green-light criterion)

Implementation of S₄ is complete iff:

1. `Cell` dataclass has the `derives_from` field
2. SIGNATURE includes `introduce_node`, `edge`, `lineage_witness`
3. Every existing CISC cell has a documented `derives_from`
   chain; RISC cells have `derives_from=None`
4. `framework_seed.sql` has matching CAT entries (Q-numbered
   breaks + framework witnesses) for the new SIGNATURE cells
5. Self-coherence verification function exists in `bootstrap.py`
   and runs at catalogue open
6. All 184 existing tests still pass
7. New tests verifying the self-coherence invariant pass

## Cross-references

- [shadow_risc_core.md](shadow_risc_core.md) — Section
  "SIGNATURE reclassification" specifies the `derives_from` field
- [shadow_migration_plan.md](shadow_migration_plan.md) — S₄ of 5
- [shadow_dual_representation.md](shadow_dual_representation.md)
  — IMPL ↔ CAT pairing extends to the new SIGNATURE cells
- [shadow_kquery_orbit.md](shadow_kquery_orbit.md) — orbit
  framing reused for tropical_min/_max derives_from
