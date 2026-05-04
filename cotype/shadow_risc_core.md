# Shadow: RISC core + self-hosted type system

> **Forward shadow.** Captures an architectural commitment that
> does not yet exist in code. Other shadows in this directory
> describe the current state; this one describes a target state
> the project is committing to and entails the migration moves
> needed to land it. Once the architecture is realised, this
> shadow becomes a regroup-from-shadows substrate and the
> doc-set will decompose under v4cat's own self-hosting.

## Form

The framework's full declarative surface compresses to:

```
RISC core (3 verbs):
  introduce_node : (id, name, type, attrs?)            → ()
  edge           : (src, tgt, kind, notes?)            → ()
  kquery         : (Referent × Referent → KleinFour)   → KleinFour

Declarative artifacts (catalogued data, not verbs):
  node-types          (catalogued as nodes of type 'node-type')
  edge-kinds          (catalogued as nodes of type 'edge-kind')
  attribute-schemas   (witnessed as edges from node-types
                       to attribute-schema breaks)
  tensions            (named curry-spec ASTs over kquery)
```

Heterogeneity is exposed *organically* — by being catalogued.
Type information is data the framework reads via kquery,
not a distinction baked into code.

## Type signature: kquery as referent-comparison; tensions as curried kqueries

```
Referent       : Type
KleinFour      : Type = Referent⁴      (the four cells are each a referent)
kquery         : Referent × Referent → KleinFour
cell           : KleinFour × {00, 01, 10, 11} → Referent

closure (output ↪ input):
  kquery_∘_kquery(A, B, c, C)
    = kquery( cell(kquery(A, B), c), C )

currying (referent input + partial application of kquery):
  curry(A) : Referent → KleinFour
           ≡ packaging a referent into kquery's first slot
           ≡ producing a 1-curried tension
```

A **tension** is a kquery composition where some arguments
have been named and fixed. Currying degree partitions:

| Curry deg | Shape | Meaning |
|-----------|-------|---------|
| 0-curried | `Referent × Referent → KleinFour` | naked kquery — RISC primitive itself |
| 1-curried | `Referent → KleinFour` | tension with one referent fixed; "things in tension *against* X" |
| 2-curried | `KleinFour` | tension fully specialised — a named kquery whose result is fixed |

Tensions can be **concrete** (curry-spec embeds literal referents)
or **templated** (curry-spec embeds free `Param`s, bound at
evaluation). `break_origin` is templated over `(B, axis_column,
t)`; a "B₁ vs B₂ coupling" tension is concrete.

Cell-projection (`cell(kquery(...), c)`) re-enters kquery's
input slot — the algebra is fixpoint-closed. Composed tensions
are the structural mechanism for arbitrary structural questions.

## Realisations (target — does not yet exist in code)

| Form | Target file / location |
|------|------------------------|
| `introduce_node` | new method on `SymmetryCatalogue` ([catalogue.py](../src/v4cat/catalogue.py)); existing `introduce_break` / `introduce_object` / `introduce_tension` redirect to it |
| `edge`           | new method on `SymmetryCatalogue`; existing `witness` and the `lineage=...` parameter on `introduce_object` redirect to it |
| `kquery`         | already present ([views.py](../src/v4cat/views.py)) — no change |
| Curry-spec AST   | new module `curry.py` (or similar) holding the dataclass hierarchy |
| Tension evaluator | new method on `SymmetryCatalogue` — walks AST, binds Params, runs kquery |
| Type-system seed | extension of [framework_seed.sql](../src/v4cat/framework_seed.sql) — node-type, edge-kind, attribute-schema bootstrap rows |
| `tensions` schema delta | additive `ALTER TABLE` in [schema.sql](../src/v4cat/schema.sql): `disposition`, `parameters_json`, `shape_json` columns |
| SIGNATURE reclassification | [theory.py](../src/v4cat/theory.py) — `Cell` gains `derives_from: tuple[str, ...] | None`; non-RISC cells declare their reduction |
| Closure-check strengthening | [bootstrap.py](../src/v4cat/bootstrap.py) — verifies type-system self-coherence in addition to existing IMPL ↔ CAT check |

## Self-hosted type system

Three commitments operating in concert:

### Node-types are catalogued nodes of type `'node-type'`

```
introduce_node(id='break',     name='Break',          type='node-type', ...)
introduce_node(id='spec',      name='Spec',           type='node-type', ...)
introduce_node(id='tension',   name='Tension',        type='node-type', ...)
introduce_node(id='node-type', name='Node Type',      type='node-type', ...)   # self-typed
introduce_node(id='edge-kind', name='Edge Kind',      type='node-type', ...)
```

The `'node-type'` row is self-typed (its type column points at
itself) — the bootstrap fixpoint. Every other node's `type`
field references a catalogued row in the same table.

### Edge-kinds are catalogued nodes of type `'edge-kind'`

```
introduce_node(id='origin',          name='Origin',           type='edge-kind', ...)
introduce_node(id='descended-from',  name='Descended from',   type='edge-kind', ...)
...
```

Each edge-kind has source-type and target-type witnesses against
framework breaks `K-SOURCE-TYPE` and `K-TARGET-TYPE`:

```
edge('origin',         'spec',  'K-SOURCE-TYPE')
edge('origin',         'break', 'K-TARGET-TYPE')
edge('descended-from', 'spec',  'K-SOURCE-TYPE')
edge('descended-from', 'spec',  'K-TARGET-TYPE')
```

### Attribute-schemas are witnessed against attribute-breaks (option 2a)

For each attribute `A` admitted by any node-type, a framework
break `K-ATTR-A` exists. Each node-type witnesses against the
attribute-breaks for its required and optional attributes:

```
edge('break',  'K-ATTR-NUMBER',          'requires-attr')
edge('break',  'K-ATTR-NAME',            'requires-attr')
edge('break',  'K-ATTR-SHORT-DESC',      'admits-attr')

edge('spec',   'K-ATTR-ID',              'requires-attr')
edge('spec',   'K-ATTR-NAME',            'requires-attr')
edge('spec',   'K-ATTR-YEAR',            'admits-attr')
edge('spec',   'K-ATTR-CATALOGUE-ORDER', 'admits-attr')
edge('spec',   'K-ATTR-NOTES',           'admits-attr')

edge('tension', 'K-ATTR-ID',           'requires-attr')
edge('tension', 'K-ATTR-NAME',         'requires-attr')
edge('tension', 'K-ATTR-DISPOSITION',  'requires-attr')
edge('tension', 'K-ATTR-PARAMETERS',   'admits-attr')
edge('tension', 'K-ATTR-SHAPE',        'requires-attr')
```

Validation: when `introduce_node(id, name, type, attrs)` is called,
the framework runs `kquery` against the catalogued attribute-schema
for `type` to verify `attrs` covers all `requires-attr` edges and
references only `requires-attr ∪ admits-attr` keys. Cardinality and
value-domain refinements (if needed later) are added as further
witnessed attributes — additive.

### Bootstrap floor

The seed in [framework_seed.sql](../src/v4cat/framework_seed.sql)
inserts the floor *without* validation, in a documented
bootstrap-mode pass:

1. `'node-type'` (self-typed)
2. The other node-types: `'break'`, `'spec'`, `'tension'`,
   `'edge-kind'`, plus any framework-canonical types
3. The framework-canonical edge-kinds: `'origin'`, `'confirms'`,
   `'refines'`, `'descended-from'`, `'inherits-from'`,
   `'family-member'`, `'deferred-candidate'`, `'sibling-boundary'`,
   `'first-witness'`, `'precedes'`, `'cross-vendor'`,
   `'gates-with-fault'`, plus the schema-witness kinds
   `'requires-attr'`, `'admits-attr'`, `'K-SOURCE-TYPE'`,
   `'K-TARGET-TYPE'`
4. The attribute-schema breaks: `K-ATTR-NUMBER`, `K-ATTR-NAME`,
   `K-ATTR-YEAR`, `K-ATTR-CATALOGUE-ORDER`, `K-ATTR-NOTES`,
   `K-ATTR-ID`, `K-ATTR-DISPOSITION`, `K-ATTR-PARAMETERS`,
   `K-ATTR-SHAPE`, `K-ATTR-SHORT-DESC`, `K-SOURCE-TYPE`,
   `K-TARGET-TYPE`
5. The schema-witness edges binding (3) to (4) and to (2)
6. After seed load, validation engages on every subsequent
   `introduce_node` / `edge` call

The seed is the only place `INSERT` runs without `kquery`-driven
validation. Every later mutation is type-checked against the
catalogued data the seed established.

## Curry-spec AST

The language for tensions has exactly three productions: atomic
referent, kquery composition, parameter. Concretely (Python
target, but the shape is substrate-agnostic):

```python
@dataclass(frozen=True)
class Param:
    """Free variable; bound when the tension is evaluated."""
    name: str

@dataclass(frozen=True)
class EdgeReferent:
    """Nodes at one end of edges matching the kind filter,
    pivoted on `pivot`. Unifies what under (α) would have been
    separate WitnessReferent (spec→break) and LineageReferent
    (spec→spec) — the kind catalogue makes the namespace
    implicit."""
    pivot:        Union[str, Param]
    kinds:        tuple[str, ...]
    pivot_role:   Literal['source', 'target']
    return_role:  Literal['source', 'target']

@dataclass(frozen=True)
class AxisCutReferent:
    """Nodes whose `axis_column` value satisfies `op threshold`."""
    axis_column:  Union[str, Param]
    op:           Literal['<', '<=', '>', '>=', '=']
    threshold:    Union[int, float, str, Param]

@dataclass(frozen=True)
class LiteralReferent:
    """Literal set of node ids — escape hatch."""
    ids: tuple[str, ...]

@dataclass(frozen=True)
class CellReferent:
    """Project a cell of a sub-kquery. The composition operator
    that makes the algebra fixpoint-closed."""
    sub:  'KqueryNode'
    cell: Literal['00', '01', '10', '11']

Referent = Union[
    EdgeReferent, AxisCutReferent, LiteralReferent,
    CellReferent, Param,
]

@dataclass(frozen=True)
class KqueryNode:
    a:        Referent
    b:        Referent
    universe: Union[Referent, None] = None

@dataclass(frozen=True)
class Tension:
    id:           str
    name:         str
    description:  Union[str, None]
    disposition:  Literal['concern', 'utility', 'diagnostic', 'audit']
    parameters:   tuple[str, ...]
    shape:        KqueryNode
```

Four leaf forms, one composition form, one kquery node, one
named-and-parameterised wrapper. That is the entire language.

### Worked example 1 — `break_origin` as templated utility-tension

```python
Tension(
    id='Q-break-origin',
    name='Originator',
    description='Earliest spec contributing an origin-class witness on B',
    disposition='utility',
    parameters=('B', 'axis_column', 't'),
    shape=KqueryNode(
        a=EdgeReferent(
            pivot=Param('B'),
            kinds=('origin', 'catalogue-introduces'),
            pivot_role='target',
            return_role='source',
        ),
        b=AxisCutReferent(
            axis_column=Param('axis_column'),
            op='<=',
            threshold=Param('t'),
        ),
    ),
)
```

Evaluation sweeps `t` over the value range; the threshold at
which the `11` cell first becomes non-empty *is* tropical-MIN.
This is the doctrinal "tropical = klein-four sweep" expressed
literally in code.

### Worked example 2 — concrete concern-disposition tension

```python
Tension(
    id='T-B1-B2-coupling',
    name='B1/B2 coupling',
    description='Specs engaging both — possible structural conflation',
    disposition='concern',
    parameters=(),
    shape=KqueryNode(
        a=EdgeReferent(
            pivot='B1',
            kinds=('origin', 'confirms', 'refines'),
            pivot_role='target', return_role='source',
        ),
        b=EdgeReferent(
            pivot='B2',
            kinds=('origin', 'confirms', 'refines'),
            pivot_role='target', return_role='source',
        ),
    ),
)
```

Live iff `11` cell is non-empty.

### Worked example 3 — composed tension (cell-projection)

```python
# Specs originating B1 from outside X-lineage, on early years
Tension(
    id='T-orphan-originators',
    name='Orphan originators of B1',
    disposition='diagnostic',
    parameters=('t',),
    description=None,
    shape=KqueryNode(
        a=CellReferent(
            sub=KqueryNode(
                a=EdgeReferent(
                    pivot='B1', kinds=('origin',),
                    pivot_role='target', return_role='source',
                ),
                b=EdgeReferent(
                    pivot='X', kinds=('descended-from',),
                    pivot_role='target', return_role='source',
                ),
            ),
            cell='10',  # B1-originators ∖ X-descendants
        ),
        b=AxisCutReferent(
            axis_column='year', op='<', threshold=Param('t'),
        ),
    ),
)
```

A kquery whose `a` is the `10`-cell of another kquery — the
fixpoint-closure of the algebra expressed in the AST.

## CISC sugar — every existing verb decomposed

| Verb | Class | Reduction |
|------|-------|-----------|
| `introduce_break(num, name, ...)`     | CISC | `introduce_node(id=num, name=name, type='break', attrs={...})` |
| `introduce_object(id, name, ...)`     | CISC | `introduce_node(id=id, name=name, type='spec', attrs={...})` + `edge(id, anc, kind)` for each lineage entry |
| `introduce_tension(id, name, ...)`    | CISC | `introduce_node(id=id, name=name, type='tension', attrs={shape, parameters, disposition, ...})` |
| `witness(spec, break, kind, ...)`     | CISC | `edge(src=spec, tgt=break, kind=kind, notes=...)` |
| `lineage_witness(desc, anc, kind)`    | CISC (new sugar) | `edge(src=desc, tgt=anc, kind=kind)` — the previously-buried lineage write surfaces here |
| `refine(P, spec, R, desc)`            | CISC | `introduce_node(id=R, name=R, type='break', attrs={short_desc=desc})` + `edge(spec, R, 'origin')` + `edge(spec, P, 'refines')` |
| `defer(B, by, reason)`                | CISC (trivial) | `edge(by, B, 'deferred-candidate', notes=reason)` |
| `promote(B, by, reason)`              | CISC (trivial) | `edge(by, B, 'confirms', notes=reason)` |
| `boundary(B, reason, by)`             | CISC (trivial) | `edge(by, B, 'sibling-boundary', notes=reason)` |
| `tropical_min(axis, kinds, B)`        | DERIVED | evaluate template-tension `Q-break-origin` (or analog) with parameter bindings; tropical-MIN sweep semantics |
| `tropical_max`                        | DERIVED | tropical_min with reversed comparison |
| `origin(B, axis)`                     | DERIVED | tropical_min specialised to `('origin', 'catalogue-introduces')` kinds |
| `first_seen(B)`                       | DERIVED | tropical_min on `axis_column='catalogue_order'`, kinds=`('catalogue-introduces',)` |
| `status(B)`                           | DERIVED | evaluate `Q-break-status` tension (kquery over witness-kind patterns) |
| `retroactive_gap(B, axis)`            | DERIVED | `first_seen(B).axis − origin(B, axis)` |
| `lineage(o)`                          | DERIVED | EdgeReferent traversal of `('descended-from', 'inherits-from', 'family-member')` kinds with closure |
| `inherited_breaks(o)`                 | DERIVED | composed kquery: lineage-ancestors × witness-edges |
| `query_wedge(a, b)`                   | CISC | `kquery(a, b, emit=['11', '10', '01'])` |
| `query_*` MCP wrappers                | DERIVED | thin remoting over the above |
| `query` (raw SQL)                     | ESCAPE | bypasses ISA; substrate-coupled |
| `load_extension`                      | ENV | substrate lifecycle |
| `check_closure`                       | META | verifies bootstrap closure |

Every CISC entry has a documented rewrite chain ending in RISC.
Every DERIVED entry evaluates a named tension or composes
kqueries via the curry-spec AST. Nothing structural remains
that doesn't reduce.

## SIGNATURE reclassification

[theory.py:Cell](../src/v4cat/theory.py#L44) gains a
`derives_from: tuple[str, ...] | None` field. RISC cells have
`derives_from=None`; CISC and DERIVED cells declare their
reduction chain. The `Kind` enum stays as a functional category
(O, B, W, R, E, K, X) but is augmented by an audit-classification
axis (RISC / CISC / DERIVED / ENV / META / ESCAPE).

After the move, the SIGNATURE primitive set shrinks from
~13 cells to **3 RISC cells** plus catalogued data (node-types,
edge-kinds, attribute-schemas, tensions in
`framework_seed.sql`).

The closure check (Theorem 14.5) closes over the smaller set
and gains a *new* verification: that the catalogued type-system
is internally coherent (every node's `type` field points at a
catalogued row; every node's `attrs` cover the requires-attr
witnesses for that type; every edge's `kind` is catalogued and
its `src`/`tgt` types match the kind's K-SOURCE-TYPE /
K-TARGET-TYPE witnesses).

This is a *strengthening* of Theorem 14.5: closure over fewer
primitives plus self-coherence of the type system is a stronger
claim than the current closure-over-13-primitives.

## Methodology reframe

`tensions` are not "structural concerns about implementation
alignment" (current methodology.md framing). They are **named
kquery shapes** with a *disposition* axis:

| Disposition | Meaning |
|-------------|---------|
| `concern`   | something to resolve (the original framing) |
| `utility`   | a regularly-read view (origin, first_seen, status) |
| `diagnostic` | a detector for a structural condition |
| `audit`     | a verification-mode read |

`break_origin`, `break_first_seen`, and `break_status` —
currently SQL views the framework consumes but does not
witness against itself — get *promoted* to first-class
catalogued tensions in `framework_seed.sql` with
`disposition='utility'`. The framework gains the ability to
point at its own utility-views as catalogued objects rather
than as un-self-witnessed substrate. methodology.md needs a
pass to reflect this.

## Migration / phasing

All moves are additive per the project's anti-patterns
(no schema column drops, no table drops, no destructive
verbs). The migration is staged:

1. **Schema additions.** New columns on `tensions`
   (`disposition`, `parameters_json`, `shape_json`); seed
   data for node-types, edge-kinds, attribute-schemas in
   `framework_seed.sql`. Existing tables (`breaks`, `specs`,
   `tensions`, `witnesses`, `lineages`, `refinements`)
   retained as physical storage.

2. **RISC verbs as new dispatch layer.** `introduce_node`,
   `edge`, the curry-spec evaluator added to
   `SymmetryCatalogue`. They dispatch to the existing typed
   tables based on `type` / `kind` lookup in the catalogued
   type-system.

3. **CISC sugar redirected.** `introduce_break` /
   `introduce_object` / `introduce_tension` rewritten to
   delegate to `introduce_node`. `witness` rewritten to
   delegate to `edge`. `refine` rewritten to the three-call
   RISC composition. The legacy `refinements` table
   continues to be dual-written for backwards compatibility,
   readable as either a direct lookup or as a
   curry-spec-derived view.

4. **`SIGNATURE` reclassification.** `Cell` gains
   `derives_from`. Non-RISC cells gain explicit reduction
   chains. The closure check is extended to verify type-system
   self-coherence in addition to the IMPL ↔ CAT gap.

5. **Methodology / theory doc pass.** methodology.md and
   theory.md updated to reflect the RISC discipline and the
   tension-as-named-kquery framing. tutorial.md and
   examples.md follow.

Each step preserves Theorem 14.5's closure check; existing
tests continue to pass; new tests verify the RISC core's
type-validation semantics.

## Composition

Every other shadow in this directory composes through the form
captured here:

- [shadow_kquery_universal_read.md](shadow_kquery_universal_read.md) — kquery is the RISC read primitive; this shadow extends it with the curry-spec algebra and tension-naming
- [shadow_kquery_orbit.md](shadow_kquery_orbit.md) — the named selections are kquery's 1-curried tensions; this shadow names the discipline by which they're catalogued
- [shadow_dual_representation.md](shadow_dual_representation.md) — IMPL ↔ CAT pairing extends to the type-system seed; under (β), IMPL becomes thinner (3 RISC cells) and CAT becomes thicker (catalogued type-system)
- [shadow_kind_stratification.md](shadow_kind_stratification.md) — the existing 8-way Kind partition gains a parallel reducibility-classification axis
- [shadow_layered_stack.md](shadow_layered_stack.md) — L0 (kquery) stays at the floor; the layers above are reorganised around the RISC core

## Entailment

```text
Three RISC primitives (introduce_node, edge, kquery)
  + self-hosted type system catalogued as data
  + curry-spec algebra closed under output ↪ input
  ⟹ every catalogue read is a klein-four contrast over
    referents drawn from the catalogued substrate
  ⟹ every catalogue mutation either creates a node or an
    edge, validated against the catalogued type system
  ⟹ heterogeneity is exposed organically (catalogue's own
    primitives expose the catalogue's own type structure)
  ⟹ Theorem 14.5 strengthens to closure-plus-self-coherence
```

The framework's design intent — "v4cat's deliverable IS the
application of v4cat to v4cat" (theory.md § 14) — finds its
maximally compressed form in this shadow. Three primitives;
everything else is data.

## Algebraic anchor (2026-05-04 cont'd)

Re-read under
[shadow_assertion_history_group.md](shadow_assertion_history_group.md):
the three RISC primitives are the **generators of the
assertion-translation group plus the V₄-coordinate-chart action**.
Concretely:

- `introduce_node` → translation by `Nₓ ∈ 𝔄_node` in `H = ℤ^𝔄`.
- `edge` → translation by `Eₛ,ₖ,ₜ ∈ 𝔄_edge`.
- `kquery` → equivariant V₄-coordinate map of the observer-pair
  group `O_U = V₄^U` over a declared universe `U`; if materialized,
  also a translation by the cover-cell assertion payload.

This algebraic factoring confirms the "three primitives, everything
else is data" reading: the three primitives generate the entire
mutation group `G_mut = ℤ^(𝔄_node ⊔ 𝔄_edge)` plus the family of
observer-coordinate actions `{V₄^U}` indexed by declared universes.
Any CISC sugar (introduce_break, witness, refine, defer/promote/
boundary, the analytic views) decomposes into a sequence of these
three. See [theory.md § 15.11](../src/v4cat/theory.md) for the
group-theoretic restatement of each primitive.
