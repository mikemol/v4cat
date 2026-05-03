# Shadow: Migration step S₂ — RISC dispatch layer

> **Forward shadow, generated at S₂ implementation start.**
> Per [shadow_migration_plan.md](shadow_migration_plan.md)'s
> DBE-Step-7 discipline.

## Form

S₂ adds the **three RISC primitives** as new methods on
`SymmetryCatalogue` plus a curry-spec algebra realised as a new
module. The primitives dispatch over the type-system seed
catalogued by S₁, validating each call via `kquery` against the
catalogued type-typing data.

```python
# New module: src/v4cat/curry.py
class Param: ...
class EdgeReferent: ...
class AxisCutReferent: ...
class LiteralReferent: ...
class CellReferent: ...
class KqueryNode: ...
class Tension: ...

def evaluate_tension(t: Tension, cat, **bindings) -> dict[str, list[str]]:
    """Walk the AST, bind Params, run kquery; return klein-four partition."""

# New methods on SymmetryCatalogue (catalogue.py):
def introduce_node(self, id, name, type, *, attrs=None) -> None: ...
def edge(self, src, tgt, kind, *, notes=None) -> None: ...
def evaluate_tension(self, tension_id, **bindings) -> dict: ...
```

## Realisations

| Form element | Target file | Position |
|--------------|-------------|----------|
| Curry-spec AST | new `src/v4cat/curry.py` | new module |
| `evaluate_tension` walker | `src/v4cat/curry.py` | top-level function |
| `introduce_node` | [catalogue.py](../src/v4cat/catalogue.py) | new method, dispatches by type |
| `edge` | [catalogue.py](../src/v4cat/catalogue.py) | new method, dispatches by kind's target-type |
| Type-system helpers | [catalogue.py](../src/v4cat/catalogue.py) | private `_type_system_loaded`, `_kind_target_type` |
| `evaluate_tension` method | [catalogue.py](../src/v4cat/catalogue.py) | thin wrapper that loads tension + calls curry.evaluate_tension |

## Composition (with the migration plan)

S₂ is the *enabling* step for S₃. It provides:

- **`introduce_node`** — the universal record above S₁'s
  `introduce_break` / `introduce_object` / `introduce_tension`
  per RFS finding 2; S₃ rewrites those CISC verbs to delegate
  here.
- **`edge`** — the universal record above `witness` and the
  buried lineage-edge-write per RFS finding 3; S₃ rewrites
  `witness` to delegate, and surfaces `lineage_witness` as new
  CISC sugar.
- **Curry-spec evaluator** — enables tensions as named curry-spec
  ASTs to be evaluated against the live witness graph; S₃
  catalogues the framework's existing SQL views (break_origin,
  break_first_seen, break_status) as utility-disposition tensions.

S₂ does *not* redirect any existing verbs — those keep their
current implementations and continue to pass all 169 tests. The
new RISC verbs are purely additive.

## Validation semantics

When the type-system seed is loaded (detected via
`SELECT 1 FROM specs WHERE id = 'node-type'`):

- **`introduce_node(id, name, type, attrs)`** validates:
  - `type` is a catalogued node-type (has `spec_attributes`
    entry `(spec_id=type, name='type', value='node-type')`)
  - `attrs` keys are subset of the requires-attr ∪ admits-attr
    set for `type` (with `id` and `name` implicitly satisfying
    K-ATTR-ID and K-ATTR-NAME)
  - all `requires-attr` keys for `type` are present (in `attrs`,
    `id`, or `name`)
- **`edge(src, tgt, kind, notes)`** validates:
  - `kind` is a catalogued edge-kind (has spec_attribute
    `(name='type', value='edge-kind')`)
  - `kind`'s declared `source-type` and `target-type` (read from
    `spec_attributes`) are non-empty
  - dispatches to `witnesses` table if target-type='break',
    `lineages` table if target-type='spec'

When the seed is *not* loaded (catalogue opened with
`check_self_hosting=False`), both verbs raise `RuntimeError`
with a message pointing at the seed-required path. Tests that
need the new RISC verbs use `check_self_hosting=True`; tests
that exercise legacy CISC paths use the existing verbs which
don't require the seed.

## Entailment

```text
S₁ catalogued type-system seed is intact
  + introduce_node validates against the catalogued attribute-schema
  + edge validates against the catalogued kind-typing
  + curry-spec evaluator dispatches over known referent shapes
  ⟹ each RISC verb reads the seed via kquery to determine well-formedness
  ⟹ heterogeneity (which graph each kind belongs to, which attributes
     each type requires) is exposed via catalogued data, not by code
     distinctions — the (β) commitment realised
  ⟹ S₂'s additions don't modify SIGNATURE or 'framework'-witnessed rows
  ⟹ closure check unchanged; ClosureKQ(K, scope).gap = ∅ preserved
```

## External commitments preserved

| Commitment | Mechanism |
|------------|-----------|
| 169 tests pass | New methods are additive; no existing method modified; no SIGNATURE change; no `framework`-witnessed rows added |
| Public `SymmetryCatalogue` API | Existing methods unchanged; new methods added |
| MCP tool surface | Unchanged in S₂ (S₃ adds `introduce_node` / `edge` as MCP tools if needed) |
| Closure check passes | New methods don't touch `SIGNATURE`; new `framework`-witnesses absent |
| Anti-pattern (no drops) | Pure additions: new module, new methods, new helpers |
| Database compatibility | Pure code additions; no schema change |
| IMPL ↔ CAT pairings | S₂ doesn't add new SIGNATURE cells (S₄ does); existing pairings unchanged |

## Step-witness (the green-light criterion)

Implementation of S₂ is complete iff:

1. New module `src/v4cat/curry.py` exists with the AST + evaluator.
2. New methods `introduce_node`, `edge`, `evaluate_tension` exist
   on `SymmetryCatalogue`.
3. New methods are tested with at least: a `break` introduction
   via `introduce_node`, an `origin` edge via `edge`, a simple
   templated tension evaluated against a populated catalogue.
4. The full existing test suite (169 tests) still passes.
5. New tests for the RISC primitives pass.

## Cross-references

- [shadow_risc_core.md](shadow_risc_core.md) — parent target;
  this step delivers the three RISC verbs declared in "RISC core".
- [shadow_migration_plan.md](shadow_migration_plan.md) — S₂ of 5.
- [shadow_migration_01_schema_seed.md](shadow_migration_01_schema_seed.md)
  — S₁ provided the type-system seed this step's verbs validate
  against.
- [rfs_findings_risc_projection.md](rfs_findings_risc_projection.md)
  — Findings 2 (introduce_node), 3 (edge), 6 (Tension AST).
