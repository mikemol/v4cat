# Symmetry-Break Cataloguing — a generic methodology with a small ISA

> *Grade: operational design (D₃).
> Shallower: [README.md](../../README.md) (quick-start), [tutorial.md](tutorial.md) (worked walk-through). Deeper: [theory.md](theory.md) (foundations).
> Architectural detail: [cotype/](../../cotype/) — see [shadow_risc_core.md](../../cotype/shadow_risc_core.md) for the (β) RISC reframe.*

This methodology catalogues a domain by accumulating *symmetry breaks*
— named structural distinctions — with witnesses, refinements, and
wedge-product audits. Time and lineage are themselves breaks-on-
objects, so attribution (including the so-called "retroactive" case)
emerges as a derived query rather than a primitive verb. The framework
is domain-agnostic; this document spells out the design.

## What the methodology gives you

1. **Domain of objects**: a set of structured artefacts the catalogue
   tracks — programming languages, processors, file system formats,
   cryptographic primitives, ML architectures, database systems,
   schema-versions of an evolving system, formal systems, anything
   with structure worth cataloguing.
2. **Symmetry breaks**: named structural distinctions. Generic: named
   partitions of the object space.
3. **Witnesses**: per-(object, break) edges with contribution kinds
   (`origin`, `confirms`, `refines`, ...). Generic: typed edges in a
   bipartite graph.
4. **Refinements**: child breaks introduced by a witness object's
   contribution to a parent break — first-class structural
   distinctions, not merely edge annotations. Generic: derivable
   from the witness graph as origin-witnessed children of
   refines-witnessed parents. (A legacy `refinements` table
   continues to act as a cache for backwards-compatible reads.)
5. **Axes**: meta-classification (Spatial/Temporal/Parallel/...). Generic:
   tags on breaks.
6. **Tensions**: named kquery shapes (curry-spec ASTs) over the
   witness graph, with a disposition axis (`concern` / `utility` /
   `diagnostic` / `audit`). Concern-disposition tensions are the
   "structural concerns about implementation alignment" framing;
   utility-disposition tensions are catalogued framework views like
   originator-attribution; diagnostic and audit dispositions name
   detector and verification reads. Generic: parameterised
   four-cell reads given names.
7. **Metric fields and lineage as breaks-themselves**: the
   catalogue's "originator" attribution and inheritance relation
   aren't special verbs *applied to* the graph; they're symmetry
   breaks *over* objects. Once the methodology admits a comparable
   metric field as a break (any ordered column on `specs`
   partitions objects by that order — `year` is one canonical
   default, but `version`, `paper_year`, `proof_depth`, etc. all
   work the same way) and lineage as a break (descent partitions
   objects), attribution emerges as a *derivation* via tropical
   query (MIN over the chosen axis, restricted to origin-class
   witnesses). "Retroactive" is just a label for the case where
   origin's metric value precedes catalogue-introduction's metric
   value — not a special primitive.
8. **Schema-itself-evolves-via-breaks**: the data shape grows as new
   structural primitives surface. Generic: schema breaks are additive
   rules over the meta-schema.
9. **Snap-to-grid**: when accumulated breaks match the original request,
   the deliverable is readable. Generic: convergence detection.
10. **Wedge-product audits**: cross-checking representation A against
    representation B to find gaps. Generic: paired-source reconciliation.

The methodology applies to any domain where:

- Objects accumulate over time
- Their structural distinctions can be named as symmetry breaks
- Multiple witnesses confirm or refine each break
- The catalogue's exposition order may differ from chronological order

## Examples of applicable domains

- **Programming languages**: breaks like "type-system soundness mode"
  (gradual / strict / latent), "garbage collection model" (refcount /
  tracing / region), "concurrency primitives" (threads / actors / fibers
  / async). Witnesses: C, Haskell, Rust, Python, Erlang, Go. Retroactive
  attribution: ALGOL 60 introduced lexical scoping, not LISP.
- **Processor architectures**: breaks like "paging model", "interrupt
  precedence", "vector facility". Witnesses: 8086, 80386, 68030,
  System/360/67, IBM z16. Retroactive attribution: System/360/67
  introduced two-level paging, not the 80386.
- **Cryptographic primitives**: breaks like "post-quantum security",
  "side-channel resistance", "constant-time guarantees". Witnesses:
  RSA, ECC, ML-KEM, AES, ChaCha20. Numbered breaks track structural
  innovations (random oracle model, IND-CCA security, ...).
- **Database systems**: breaks like "consistency model" (strong /
  eventual / causal), "partitioning scheme" (hash / range / consistent-
  hash), "transaction model" (ACID / BASE). Witnesses: PostgreSQL,
  Cassandra, FoundationDB, Spanner.
- **Mathematical structures**: breaks like "associativity", "identity",
  "inverses", "commutativity". Witnesses: magma, semigroup, monoid,
  group, abelian group, ring, field. Numbered breaks are *axioms*; the
  refinement-axiom-by-refinement-axiom approach is what magma theory
  *already does*.
- **File systems**: breaks like "journaling", "copy-on-write",
  "snapshots", "checksums", "deduplication". Witnesses: ext4, ZFS,
  btrfs, APFS, ReFS.
- **Network protocols**: breaks like "reliability", "ordering",
  "flow control", "encryption", "multiplexing". Witnesses: TCP, UDP,
  QUIC, HTTP/3, WireGuard.

The methodology's value: it produces *queryable structure* that survives
context loss across time, vendor disagreements, and shifting priorities.
A catalogue accumulated over months becomes a graph that answers "which
break was originated where?" in a query rather than via human memory.

## The data shape (NOSQL-flavour)

The framework ships a relational schema, but the underlying data is
fundamentally a **labelled bipartite graph**: breaks ↔ objects, with
typed edges. Three NOSQL representations capture it naturally. The
running example below uses a paging-related break (`Q89`) and a few
processor witness objects — one of many possible illustrations; the
shape is identical for any domain.

### Document store (JSON-shaped)

```json
{
  "kind": "break",
  "id": "Q89",
  "name": "Hierarchical address translation with cached lookup",
  "axes": ["spatial"],
  "status": "active",
  "invariant": {
    "partition": "Linear addresses partitioned by translation outcome",
    "preservation": "Translation preserved between TLB fills until invalidate",
    "temporal_axis_kind": "cycle_count"
  },
  "witnesses": [
    {"object": "system_360_67", "kind": "origin", "year": 1965},
    {"object": "80386", "kind": "catalogue-introduces", "year": 1985},
    {"object": "68030", "kind": "cross-vendor", "year": 1987,
     "notes": "tree-structured 1-4 levels via TC; ATC vs TLB"},
    {"object": "system_370_xa", "kind": "refines", "year": 1983,
     "refinements": ["dynamic-address-spaces", "access-register-mode"]}
  ],
  "instances": {
    "80386":      {"levels": 2, "page_size": 4096, "base_register": "CR3"},
    "68030":      {"levels": 4, "page_size": 4096, "base_register": "CRP"},
    "system_370": {"levels": 2, "page_size": 4096, "base_register": "CR1"}
  }
}
```

Each break is one document; witnesses are nested arrays; per-witness
detail (page_table / alias / atomic_op / etc.) lives in `instances`.

### Graph store (Cypher-shaped)

```cypher
CREATE (q89:Break {
  id: 'Q89',
  name: 'Hierarchical address translation with cached lookup'
})
CREATE (s_67:Spec {id: 'system_360_67', year: 1965})
CREATE (s_386:Spec {id: '80386', year: 1985})
CREATE (s_67)-[:ORIGINATED {kind: 'origin'}]->(q89)
CREATE (s_386)-[:CATALOGUE_INTRODUCES]->(q89)
CREATE (q89)-[:HAS_AXIS]->(:Axis {name: 'spatial'})
```

Edges carry the contribution kind directly. Originator-by-year emerges
from a path query that ranks origin-class edges by the object's year.

### Triple store (RDF-shaped)

```turtle
:q89  rdf:type           :Break .
:q89  :name              "Hierarchical address translation" .
:q89  :hasAxis           :spatial .
:s360_67  :originated    :q89 .
:s360_67  :year          1965 .
:s386     :catalogueIntroduces  :q89 .
:s386     :year          1985 .
```

Each fact is one triple; SPARQL handles tropical queries naturally
(`SELECT ?spec WHERE { ?spec :originated ?b . } ORDER BY ASC(?year) LIMIT 1`).

All three shapes are equivalent at the data-content level; they differ
in which queries are natural. The framework's `schema.sql` is a fourth
equivalent shape — relational normal form of the same graph.

The ISA below abstracts over which shape the runtime chooses.

## Metric fields and lineage are breaks themselves

A foundational observation that simplifies the ISA: *a metric field
(any comparable ordered column) and lineage are not special verbs
applied to the graph; they're symmetry breaks over objects,
recorded with the same machinery as every other break.*

This means:

- **A metric field** (e.g. year of articulation, version number,
  paper-publication date, proof-tree depth, NIST round) is a
  structural attribute on objects — partitioning the object space
  by that ordered field. The catalogue records it once per object;
  every "originator" question becomes a tropical query (MIN over
  the chosen axis, restricted to origin-class witness edges). The
  framework provides `year` as one canonical default but the
  generic `tropical_min(axis_column, witness_kinds)` operator and
  the parametric `origin(break, axis_column=...)` sugar work over
  any ordered column.
- **Lineage / descent** is a structural relation between objects —
  partitioning the object space by family / vendor / inheritance
  path. Recorded as edges of kind `inherits` or `descended-from`;
  "what does X inherit from Y?" becomes a transitive-closure
  query.
- **Catalogue-exposition order** is a third structural attribute —
  separate from any domain metric field because exposition follows
  the analyst's design lineage rather than the metric field's
  ordering. (A catalogue may add objects in an order that doesn't
  track their position on the chosen metric.) "First-seen-in-
  catalogue" is `MIN(catalogue_order)` over `catalogue-introduces`
  edges.

Once these three are recorded as primary data, **attribution is always
derived**. There's no special "retroactive attribution" verb because
there's no special case: every origin query is the same tropical-MIN
over the same edges; the *gap* between origin's metric value and
first-seen's metric value is just an arithmetic difference, named
"retroactive" only when positive.

The implication: the ISA below has *no* `RETRO` verb. The first time
the catalogue analyses break F1 at object β (year 1985), an `origin`
witness from β is added. Later, when an earlier-but-not-yet-
catalogued object α (year 1965) is examined, an `origin` witness
from α is added. The tropical-MIN-over-the-axis query naturally
picks α (1965) over β (1985); no correction step is needed. The catalogue
*re-derives* the originator on every read, so the answer always
reflects the current state of the witness graph.

This is the methodology's structural commitment to a normal axis on
every symmetry plane: every break has a temporal axis along which
attribution parameterises. Treating time as a break-on-objects
(rather than a verb-on-the-catalogue) is the framework's
operational realisation of that commitment.

## The Klein-four read core

A symmetry of the methodology surfaces under one further compression:
*every read is a comparison*. There is no unary query. What looks
unary —"what breaks does spec X originate?", "what's missing from
the catalogue?" — is always a binary comparison whose right-hand
referent is hidden by convention (a default universe, a normative
expectation, a derived view).

Make the comparison explicit, and the read layer reduces to **one
primitive**.

### KQUERY: the classifier

Given two predicates over a bounded universe `U`:

```text
A : U → {0,1}
B : U → {0,1}
```

every `x ∈ U` lands in exactly one of four cells determined by its
membership signature:

```text
                B = 0           B = 1
            ┌────────────┬─────────────┐
   A = 0   │  00 BLIND  │  01 RIGHT   │
            ├────────────┼─────────────┤
   A = 1   │  10 LEFT   │  11 AGREE   │
            └────────────┴─────────────┘
```

Those four cells form a Klein four-group `V₄ ≅ ℤ₂ × ℤ₂`: the group
of *membership signatures* (not of truth values).

**KQUERY is a classifier**, not a filter. Algebraically:

```text
KQUERY(A, B; U) : U → ℤ₂ × ℤ₂
                  x ↦ (A(x), B(x))
```

The four cells are the fibers of this function. Selection
(`emit={cells}`) is the post-classifier projection.

### Every other read is sugar

Each named read in the methodology is a specific selection from the
KQUERY classifier:

```text
QUERY(A)         := KQUERY(A, U)        emit={11}
WEDGE(A, B)      := KQUERY(A, B)        emit={10, 01}
AGREE(A, B)      := KQUERY(A, B)        emit={11}
LEFT_RESIDUE     := KQUERY(A, B)        emit={10}
RIGHT_RESIDUE    := KQUERY(A, B)        emit={01}
COVERAGE(A, B)   := KQUERY(A, B)        emit={10, 01, 11}
BLIND(A, B; U)   := KQUERY(A, B; U)     emit={00}
SYM_DIFF(A, B)   := KQUERY(A, B)        emit={10, 01}   (= WEDGE)
INTERSECTION     := KQUERY(A, B)        emit={11}       (= AGREE)
```

The full Boolean algebra over A and B sits inside the four cells.
Nothing is lost; nothing further is reducible.

### The 00 cell — shared blindness as a methodological object

Most diff/audit tools see only `10` and `01`. KQUERY also exposes
`11` (agreement) and crucially `00` — *shared blindness*: items in
the universe that **neither** representation accounts for.

For a bounded universe `U`:

```text
00 = U \ (A ∪ B)    — what falls outside both representations
```

A consistency-check example, schematically (any domain that has a
"property A *requires* property B" rule looks like this):

```text
U = objects within scope of the rule
A = objects that exhibit property A
B = objects that exhibit property B

11 = both A and B          (rule satisfied)
10 = A but not B           (rule violated)
01 = B but not A           (fine: B without A is allowed)
00 = neither               (interesting: outside the rule's reach)
```

Concretely, a processor catalogue might bind `A` = "paged" and
`B` = "restart-suitable frames"; a database catalogue might bind
`A` = "row-locking" and `B` = "MVCC"; a language catalogue might
bind `A` = "static types" and `B` = "type inference". The
classifier and its four cells are the same.

The `00` cell isn't a violation of consistency; it's a
*methodological object* in its own right — the place where the
universe contains items that *neither* representation has anything
to say about. Surfacing it refuses what we might call the
**metaphysics of coverage**: the assumption that any A or B
together exhaust their domain.

### Why this lands philosophically

KQUERY tightens the Yoneda+Derrida commitments:

- **Yoneda exact.** No referent is ever inspected alone. Unary
  query is revealed as "binary comparison with an implicit universal
  on the right." Identity is *only* relational.
- **Derrida exact.** Each cell corresponds to a Derridean role:
  - `11` — apparent presence / agreement
  - `10`, `01` — différance / displacement (what one trace says the
    other does not)
  - `00` — trace of absence / shared blindness; what's *excluded*
    from both, and constitutive of what the comparison can mean
- **Errors become geometry.** Consistency-rule violations aren't an
  exception type; they're points in the `10` cell of a particular
  KQUERY. Convergence is `10 ∪ 01 = ∅` for a chosen comparison.
- **Paradigms are derived regions.** "Paradigm" is just a referent
  the user constructs explicitly; once explicit, it's subject to
  the same comparison machinery as everything else. There's no
  privileged paradigm-position from which everything else is read.

### One-line summary

> *A catalogue read is not a query but a comparison: every
> interrogation of structure is a Klein-four partition of a bounded
> universe induced by two traces.*

Everything else is sugar.

## The ISA

A small, orthogonal set of operations that compose to build up the
catalogue. The structural core is **three RISC primitives**;
everything else in the ISA is documented sugar reducible to those
three. Each is implementable against any of the four data-shape
options.

### RISC primitives — the structural core (3 verbs)

#### `INTRODUCE_NODE <id> <name> <type> [attrs]`

The universal node-introduction primitive. Dispatches over the
catalogued node-type to land the new node in the appropriate
substrate region (`break`, `spec`, `tension`, or any
domain-introduced type). Validates that `type` is catalogued
and that `attrs` covers the type's required attribute schema.

```text
INTRODUCE_NODE F1    "Some structural distinction" break attrs={short_desc=...}
INTRODUCE_NODE alpha "Alpha" spec attrs={year=1965}
INTRODUCE_NODE T1    "Coupling concern" tension attrs={disposition=concern,...}
```

#### `EDGE <src> <tgt> <kind> [notes]`

The universal typed-edge primitive. Reads the catalogued
edge-kind's source-type and target-type to dispatch to the
witnesses or lineages substrate. Edge-kinds form the
methodology's vocabulary: `origin`, `catalogue-introduces`,
`confirms`, `refines`, `first-witness`, `precedes`,
`cross-vendor`, `inherits`, `deferred-candidate`,
`sibling-boundary`, `gates-with-fault`, `descended-from`,
`inherits-from`, `family-member`, plus the schema-witness kinds
`requires-attr`, `admits-attr`, `K-SOURCE-TYPE`, `K-TARGET-TYPE`.

```text
EDGE alpha F1 origin
EDGE beta  F1 catalogue-introduces
EDGE beta  alpha descended-from
EDGE gamma F1 cross-vendor "an alternate realisation of F1"
```

The originator emerges from the witness graph plus the year
attribute: `MIN(s.year)` over `origin` and `catalogue-introduces`
edges. With both alpha (1965) and beta (1985) carrying `origin`
edges to F1, the originator is alpha — derived, not declared.

#### `KQUERY <left> <right>; <universe> <equivalence> <emit>`

The Klein-four read primitive — the *only* primitive read.

Compares two referents (sets, views, sources, rules, projections,
closures, snapshots, expected covers — any predicate over the
universe) and returns the four-cell membership partition. The
output is itself a 4-tuple of referents, each of which can re-enter
KQUERY's input slot — the algebra is fixpoint-closed, which is
what licenses the **curry-spec algebra** for tensions (named
kquery shapes parameterised over free variables).

```text
KQUERY prose_breaks structured_breaks emit=10,01
   → drift between prose and structured form

KQUERY introduced_objects objects_with_witnesses emit=10
   → which introduced objects lack any witness?

KQUERY rule_premises rule_conclusions emit=10
   → consistency-rule violations: objects satisfying the
     premise but not the conclusion of a domain rule

KQUERY declared_breaks observed_phenomena emit=01 universe=U
   → which observed phenomena are uncovered by the schema?

KQUERY a b emit=00 universe=U
   → shared blindness — what's in U that neither A nor B touches
```

Conventional named reads are aliases (sugar):

```text
QUERY(A)        := KQUERY A U emit=11
WEDGE(A,B)      := KQUERY A B emit=10,01
AGREE(A,B)      := KQUERY A B emit=11
COVERAGE(A,B)   := KQUERY A B emit=10,01,11
BLIND(A,B,U)    := KQUERY A B emit=00 universe=U
```

### CISC sugar — named conveniences

The verbs below are documented sugar with published reductions to
the RISC primitives above. Each pairs a call-signature ergonomic
for catalogue authors with a precise reduction to RISC. The
reductions are recorded as `derives_from` chains in
`theory.py:SIGNATURE`; the strengthened closure check (theory.md
§ 14.5.8) verifies every chain terminates in RISC at every
catalogue open.

#### `INTRODUCE <kind> <id> [attrs]`     *(reduces to `INTRODUCE_NODE`)*

Add a new object of a given kind. Kinds: `break`, `object`, `axis`,
`tension` (and any user-defined). Idempotent on `id`. The `year`
and `lineage` attributes on `object` are first-class — they're how
time and lineage enter the graph. Each `INTRODUCE break F1` is a
`INTRODUCE_NODE F1 ... break ...`; each `INTRODUCE object beta` is
a `INTRODUCE_NODE beta ... spec ...` with optional lineage edges
trailing.

```text
INTRODUCE break  F1    name="Some structural distinction" axes=[spatial]
INTRODUCE object beta  year=1985 lineage=[some-family]
INTRODUCE object alpha year=1965 lineage=[earlier-family]
```

#### `WITNESS <subject> <break> <kind> [notes]`     *(reduces to `EDGE`)*

Record a contribution edge in the spec→break direction. Identical
in semantics to `EDGE <subject> <break> <kind>` for any kind whose
catalogued target-type is `break`; the verb's name preserves the
methodology's original framing.

```text
WITNESS alpha F1 origin
WITNESS beta  F1 catalogue-introduces
```

#### `REFINE <break> <object> <name> [description]`     *(reduces to `INTRODUCE_NODE` + `EDGE` × 2)*

Introduce a refinement of a parent break. A refinement-name *is* a
structural distinction — i.e., a child break — under (β). The
verb's reduction is:

```text
REFINE P spec R desc
  ≡ INTRODUCE_NODE R R break attrs={short_desc=desc}
  + EDGE spec R origin
  + EDGE spec P refines
```

The legacy `refinements` table is dual-written for
backwards-compatible reads. Multiple refinements per (break,
object) are admitted — each call introduces a fresh child break.

```text
REFINE F1 delta variant-a "first refinement of F1 at delta"
REFINE F1 delta variant-b "second refinement of F1 at delta"
```

### CISC sugar — modal verbs (lifecycle)

The three modal verbs below are **orbit-elements of `WITNESS`**
parameterised by witness-kind: `defer` fixes `kind='deferred-candidate'`,
`promote` fixes `kind='confirms'`, `boundary` fixes
`kind='sibling-boundary'`. Each reduces to `WITNESS`, which itself
reduces to `EDGE`. The orbit positions are catalogued for ergonomic
reasons; `WITNESS` is the universal at the carrier-axis.

#### `DEFER <break>`

Mark a break as a deferred candidate (named but not structurally
adopted). Sets a witness with kind=`deferred-candidate`.

```text
DEFER F4    -- one object introduced F4 as a deferred candidate
```

#### `PROMOTE <break> [reason]`

Promote a deferred break to active. Requires a recent witness with
kind=`confirms` or `first-witness` from a different object.

```text
PROMOTE F4 reason="second independent witness"
```

#### `BOUNDARY <break> <reason>`

Mark a break as a deliberate metamodel non-extension (the
sibling-framework boundary). Use it when a candidate distinction is
real and adjacent to your metamodel, but you've decided the
metamodel shouldn't try to absorb it.

```text
BOUNDARY F-sib "this distinction lives in a sibling framework"
```

### Schema-evolution verbs

The schema itself evolves. These verbs add new raw structure when a
new structural primitive is forced.

#### `KIND.NEW <name> <attr_schema>`

Define a new object kind. The framework ships with `break`, `object`,
and `tension`; a domain extension might add `theorem`, `proof`,
`benchmark`, or anything else its analysis requires.

#### `PREDICATE.NEW <name> <signature>`

Define a new edge predicate. Adding new witness kinds (e.g.
`precedes`, `gates-with-fault`) when a domain forces them follows
this pattern.

#### `AXIS.NEW <name>`

Define a new meta-axis. Examples of axes the framework's defaults
already include: `spatial`, `temporal`, `parallel`, `eventual`,
`meta`. New ones (e.g., `eventual` was added when needed) follow
the same additive pattern.

These three verbs are *schema-breaks of the meta-schema* — each one
records that the methodology's own data shape has admitted a new kind
of fact.

### Analytic queries (derived; no state mutation)

Each is either a KQUERY selection or a tropical aggregate. None of
them mutate state.

Tropical aggregates (named functions over the witness graph; not
KQUERY but used together with it):

- **`TROPICAL_MIN(axis_column, witness_kinds, [break_], [direction])`** —
  the framework's *generic* tropical operator. For each break,
  finds the spec(s) where `axis_column` is at its extremum among
  witnesses with the given kinds. The framework's commitment is
  to tropical aggregates over ordered columns; `year` and
  `catalogue_order` are two canonical examples, but any ordered
  column on `specs` admits the same operator. See `theory.md` § 3.
- **`ORIGIN(break)`** — sugar: `TROPICAL_MIN(axis_column='year',
  witness_kinds=('origin', 'catalogue-introduces'))`.
- **`FIRST_SEEN(break)`** — sugar: `TROPICAL_MIN(axis_column=
  'catalogue_order', witness_kinds=('catalogue-introduces',))`.
- **`STATUS(break)`** — case logic over witness kinds.
- **`RETROACTIVE_GAP(break)`** — `FIRST_SEEN(b).year - ORIGIN(b).year`.
  Positive values surface as retroactive attributions; the case is
  derived, not flagged at write time.
- **`LINEAGE(object)`** — transitive closure over `inherits` /
  `descended-from` edges; returns the ancestor chain.
- **`INHERITED_BREAKS(object)`** — breaks whose witnesses on
  ancestors of `<object>` propagate via the `inherits` relation.

KQUERY selections (the read layer proper; everything below is sugar
over `KQUERY`):

- **`AXIS_DISTRIBUTION()`** — group-by count of breaks per axis;
  expressible as iterated KQUERY over per-axis predicates.
- **`MIXED(break)`** — true if break commits to ≥ 2 axes.
  Equivalent to `KQUERY(axes_of(break), {single_axis}, emit=10)`
  being non-empty for any single-axis predicate.
- **`CONSISTENCY(rule)`** — domain-extension consistency violations,
  parametric over rule name. The rule maps to a `<rule>_violations`
  view that the loaded extension defines. Equivalent to
  `KQUERY(rule_premise_set, rule_conclusion_set, emit=10)` for the
  domain's specific premise / conclusion predicates.
- **`WEDGE(a, b)`** — equivalent to `KQUERY(a, b, emit=10,01)`.
- **`COVERAGE(a, b)`** — equivalent to `KQUERY(a, b, emit=10,01,11)`.
- **`BLIND(a, b, U)`** — equivalent to `KQUERY(a, b, U, emit=00)`.

## The methodology's recurring shape

Across catalogues built with this framework, a few patterns recur.
They're not part of the ISA per se but constitute the *practice* of
using it:

- **Start abstract.** The seed schema has only the most abstract
  structure (`breaks` table with `(number, name)`). Add columns / tables
  only when an object forces it.
- **Witnesses populate breaks; breaks aren't authored top-down.** Each
  break crystallises around a structural distinction that some object
  forces into view. Speculative breaks (added before any witness) tend
  to drift.
- **Metric fields and lineage are breaks-themselves; attribution is
  derived.** A metric field (year by default; any ordered column) and
  lineage are recorded once per object as primary data. Every "who
  originated this?" question is then a tropical-MIN-over-the-axis
  query over origin-class edges; "what does X inherit?" is a
  transitive closure over lineage edges. There's no special-casing
  for catalogue exposition order versus the metric field's order.
- **Schema breaks are additive.** Don't drop columns; add new ones.
  `ALTER TABLE ADD COLUMN` is the typical move; `CREATE TABLE` for
  genuinely new raw structure that domain extensions force.
- **Derived properties live in views.** Status, origin, retroactive
  gap, consistency violations — none belong in the raw data.
- **Wedge-product audits keep representations consistent.** When a
  structural artefact has multiple representations (e.g., a prose
  description ↔ a structured catalogue), periodically check that
  each fact in one is reflected in the other. Drift is information.
- **Convergence shows up as "no new breaks in N consecutive
  additions."** When a domain's metamodel is closing, additions
  become refinements rather than new structural primitives. Late-
  arriving objects that *only* trigger refinements (no new
  breaks) are convergence signals.

## A worked example — adding an object that forces a new break

The typical sequence when a new object is added to a catalogue and
forces a new break:

```text
INTRODUCE object beta year=1980 lineage=[some-family]

INTRODUCE break F-new name="Some structural distinction" axes=[parallel]
WITNESS   beta F-new origin
WITNESS   beta F-new catalogue-introduces

REFINE F-existing beta variant-name
       "specifies how beta realises an already-known break"
WITNESS beta F-existing refines
```

A retroactive case — an earlier-but-not-yet-catalogued object becomes
the originator after the fact, with no `RETRO` verb:

```text
INTRODUCE object delta year=1970 lineage=[earlier-family]
INTRODUCE object alpha year=1965 lineage=[much-earlier-family]

INTRODUCE break F-temporal name="A temporal-axis distinction" axes=[temporal]
WITNESS   delta F-temporal origin
WITNESS   delta F-temporal catalogue-introduces

-- Earlier addition: F-old was introduced at gamma's commit
-- (catalogue-introduces). Now we add an origin edge from alpha. The
-- tropical-MIN-over-axis query naturally picks 1965 over gamma's
-- year; "retroactive" is a derived label. (The default axis is
-- `year`; the same shape applies if the catalogue uses a
-- different metric field — version, paper-publication-date, etc.)
WITNESS alpha F-old origin
```

A wedge-product audit between two representations of the same
structural content — for example, prose documentation and the
structured catalogue:

```text
WEDGE prose_breaks structured_breaks
  → flagged: items in prose missing from the structured catalogue;
             items in the structure missing from prose;
             representational drift surfaced as actionable diff
  → response: add the missing items to whichever side is canonical,
              or flag the divergence as a structural discovery.
```

This is how an existing artefact becomes an instance of the
methodology — the methodology names what good cataloguing already
does.

## Reference implementation sketch

A minimal Python implementation of the ISA against SQLite (using the
relational shape):

```python
class SymmetryCatalogue:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._bootstrap()    # mirrors schema.sql S0-S11

    def introduce(self, kind: str, id_: str, **attrs):
        if kind == 'break':
            self.conn.execute(
                "INSERT INTO breaks (number, name, short_desc) "
                "VALUES (?, ?, ?)",
                (id_, attrs.get('name'), attrs.get('short_desc'))
            )
        elif kind == 'object':
            self.conn.execute(
                "INSERT INTO specs (id, name, year, ...) "
                "VALUES (?, ?, ?, ...)",
                (id_, attrs['name'], attrs.get('year'), ...)
            )
        # ... other kinds

    def witness(self, subject: str, break_: str, kind: str,
                notes: str = None):
        self.conn.execute(
            "INSERT INTO witnesses (spec_id, break_number, kind, notes) "
            "VALUES (?, ?, ?, ?)",
            (subject, break_, kind, notes)
        )

    def refine(self, break_: str, object_: str, name: str,
               desc: str = None):
        self.conn.execute(
            "INSERT INTO refinements "
            "(break_number, spec_id, name, description) "
            "VALUES (?, ?, ?, ?)",
            (break_, object_, name, desc)
        )

    def origin(self, break_: str) -> dict | None:
        return self.conn.execute(
            "SELECT * FROM break_origin WHERE break_number = ?",
            (break_,)
        ).fetchone()

    def query(self, pattern: str, **bindings) -> list:
        # Pattern compiles to SQL via a small DSL or directly
        ...
```

The actual reference implementation would be a couple hundred lines —
small enough to embed and reason about. The point is that the ISA's
*verbs* are stable; the *substrate* (SQLite / Neo4j / triple store /
JSON files) is interchangeable, mirroring the framework's own
DSL-trees-as-substrate-portability principle (Z22).

## MCP interface — exposing the catalogue to LLM clients

The Model Context Protocol (MCP) is Anthropic's standard for letting
LLM clients call tools, read resources, and invoke prompts against a
server. An MCP server exposing the catalogue makes the methodology
*interactively maintainable* by any MCP-aware client (Claude Desktop,
Claude Code, other agents): new object analyses become tool calls;
audits become resource fetches; templates for analyzing a new
witness object become prompts.

### Tools (the ISA verbs as callable functions)

Each ISA verb maps to one MCP tool. The tool name and parameters
mirror the verb's signature directly.

```text
introduce_break(number, name, axes=[], short_desc=None)
introduce_object(id, kind, name, year=None, lineage=[],
                 catalogue_order=None, notes=None)
introduce_axis(name, description=None)
introduce_tension(id, name, description, breaks_involved=[],
                  status='open')

witness(subject, break_number, kind, notes=None, scope='spec')
refine(break_number, object_id, name, description=None)

defer(break_number, reason=None)
promote(break_number, reason=None)
boundary(break_number, reason)

# Schema-evolution
kind_new(name, attr_schema)
predicate_new(name, signature)
axis_new(name)
```

### Resources (read-only views of the catalogue)

Resources are addressed by URI; clients can fetch them on demand.

```text
catalogue://breaks                  → all breaks (number, name, axes, status)
catalogue://breaks/{number}         → one break with its witnesses + refinements
catalogue://objects                 → all objects (specs / non-spec witnesses)
catalogue://objects/{id}            → one object with its contributions
catalogue://retroactive             → derived: breaks with origin year < first-seen year
catalogue://tensions                → tensions list with status
catalogue://violations/{rule}       → domain-extension consistency rule (parametric)
catalogue://axes                    → axis list with break counts
catalogue://lineages                → object lineage graph
catalogue://wedge?a=...&b=...       → wedge-product audit between two sources
```

### Prompts (templates for common tasks)

Prompts are slot-filled templates the client invokes; the server
returns a fully-rendered prompt the LLM then acts on.

```text
analyze_new_object(spec_doc_url) →
  "Examine the spec at <url>. For each section, identify:
   - Existing breaks this object inherits unchanged
   - Refinements of existing breaks
   - New breaks this object forces
   For each break, provide a (partition, preservation-theorem) pair.
   Then propose ISA operations to record the analysis."

audit_md_vs_sql(md_path, sql_path) →
  "Run a wedge-product audit between <md_path> and <sql_path>.
   For each item in either, check whether it's represented in the
   other. Output a list of: (item, present_in_md, present_in_sql,
   suggested_action)."

next_object(domain) →
  "The catalogue's most recent additions are <last_3>. Suggest the
   next object to analyze, with reasoning: which existing break
   would it confirm? what new break might it force?"

snap_to_grid_check(deliverable_description) →
  "Compare the catalogue's current entailment against
   <deliverable_description>. Report: consistent / generalisation /
   specialisation / drift. If gap, name what's missing."
```

### Server topology

```text
                  ┌────────────────────────────────────┐
  MCP client ◄────┤  catalogue-mcp-server (Python)     │
  (Claude /       │                                    │
   Code / agent)  │  - exposes ISA verbs as tools      │
                  │  - exposes views as resources      │
                  │  - exposes templates as prompts    │
                  │                                    │
                  │  ┌──────────────────────────────┐  │
                  │  │ SymmetryCatalogue (Python)   │  │
                  │  │   ↑                          │  │
                  │  │   substrate-portable ISA     │  │
                  │  └─────────┬────────────────────┘  │
                  └────────────┼───────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        catalogue.db     triple-store      Neo4j
        (SQLite,         (federated        (graph
        local)           catalogue)        analytics)
```

A single MCP server can expose multiple substrates; clients don't
need to know which is in use.

### Example session

```text
Client → Server: introduce_object(id="omega", year=2022,
                                  lineage=[("delta", "descended-from")])
Server → Client: ok

Client → Server: introduce_break(number="F-new", name="Some structural distinction",
                                 axes=["parallel"])
Server → Client: ok

Client → Server: witness("omega", "F-new", "first-witness",
                         "first realised at omega")
Server → Client: ok

Client → Server: GET catalogue://breaks/F-new
Server → Client: {
                   "number": "F-new",
                   "name": "Some structural distinction",
                   "axes": ["parallel"],
                   "status": "active",
                   "originator": {"object": "omega", "year": 2022},
                   "witnesses": [
                     {"object": "omega", "kind": "first-witness", ...}
                   ]
                 }

Client → Server: invoke_prompt("next_object", domain="my-domain")
Server → Client: "<rendered prompt>"
LLM → Client → Server: <calls introduce_object / witness / refine
                       to record the next object's analysis>
```

The MCP interface makes the methodology *self-bootstrapping*: an LLM
client maintains the catalogue across sessions without losing
structural state, and any human can review the changes via the
catalogue's queryable substrate.

## Why this matters

A catalogue built with this methodology can grow over many sessions
without losing structural content, because every distinction is
externalised as a break, witness, or refinement — concrete artefacts
that can be queried, audited, and extended.

The framework's value is that *any domain with accumulating
structural distinctions can use the same scaffolding*. The cost is
one schema-bootstrap and a handful of verbs; the payoff is a
queryable catalogue that:

- Doesn't lose structure across context boundaries
- Makes drift explicit (wedge-product audits)
- Keeps derived properties consistent with raw facts (views)
- Treats time and lineage as breaks-themselves, so attribution
  emerges from queries rather than from a special verb
- Converges visibly when the metamodel closes

The methodology applies to any structural-knowledge domain — the
ISA + NOSQL schema is factored to the point where the domain
specifics live entirely in extensions.

## Philosophical lineage — Derridean traces and Yoneda relationality

The methodology's structural commitments — *no break, origin, or
schema element is foundational; identity is constituted only through
witnessed traces; global structure is always derived* — align with
two well-developed positions in continental philosophy and category
theory.

### Derridean critique of presence

Derrida's reading of structuralism observes that no element of a
sign-system is *self-present*: the meaning of any term is constituted
through its differences from and deferrals to other terms (the
*différance* move). There's no foundational "ground" that grants
meaning unilaterally; meaning is the trace of relationships.

The methodology refuses presence at every level:

- **No foundational break.** No break is a privileged origin from
  which other breaks are derived. Each is named only because some
  object's analysis surfaced it; each remains revisable as future
  objects contribute traces that re-position it.
- **No foundational origin.** The originator of a break isn't a fact
  stamped into the schema; it's a *derivation* (tropical MIN over
  the chosen metric axis, restricted to origin-class witness
  edges). Adding an earlier object's
  origin trace to a previously-attributed break doesn't *correct*
  the catalogue — it *re-derives* the originator. The earlier
  reading wasn't wrong; it was what the trace-set licensed at the
  time.
- **No foundational schema.** The framework's schema breaks S0-S11
  emerged additively; none was specified in advance. The schema is
  itself a sediment of traces — each break records that a
  particular structural concern forced the data shape to admit a
  new column or table.
- **No foundational object.** Objects and breaks are constituted by
  their participation in the witness graph. An object isn't an
  essence outside the catalogue; it's the trace-set its witnesses,
  refinements, and lineage edges accumulate to.

The "retroactive attribution" pattern is the most acute Derridean
moment: when an earlier object becomes the origin of a break in a
later catalogue analysis, the prior reading wasn't false — it was
what the trace-set then licensed. The catalogue doesn't *correct*
itself backwards; it *thickens* itself forward, and the derived
originator is whatever the current trace-set licenses. There is no
privileged moment of "the right answer"; there are only
progressively richer trace-sets and the queries they license.

### Yoneda-style relational stance

The Yoneda lemma in category theory states that an object is fully
characterised by the morphisms into and out of it (its hom-functor).
You cannot know the object except through its relationships; there
is no "essence" of an object beyond what its participation in a
category determines.

The methodology adopts this stance:

- **An object is its witnesses.** A spec's identity in the catalogue
  is exactly the (kind, break, refinements, scope) edges it
  participates in. Nothing about a spec is recorded outside its
  relations — even attributes like year and lineage are themselves
  witness-edges to the time-and-lineage breaks.
- **A break is its witnesses.** A break's identity is exactly the
  edges from objects to it. There's no break "in itself" outside
  the witness graph.
- **Substrate is irrelevant; only relations matter.** Whether the
  catalogue lives in SQL, a triple store, a graph DB, or JSON files
  is invisible from the relational stance — the same hom-set is
  presented in each substrate. (This is why methodology.md treats
  the four shapes as equivalent.)

Yoneda lets us state the methodology's substrate-portability claim
formally: any two substrates that present the same hom-set are
equivalent for the methodology's purposes. The ISA is *the* hom-set
preserving translation between them.

### Their combination

Derrida + Yoneda yields the methodology's working stance:

1. **Identity is relational** (Yoneda): objects are constituted by
   their participation in the relevant category.
2. **Relations are traces** (Derrida): each relationship is a
   deferral that points to others; no relationship is the privileged
   ground.
3. **Global structure is derived, never imposed**: views, queries,
   and the metamodel itself are functions over the trace graph,
   re-derivable as the trace-set thickens.

A working catalogue demonstrates the stance: a new object doesn't
update a privileged Object record; it adds witnesses, refinements,
and lineage edges that re-derive every dependent view. The wedge-
product audit doesn't compare the catalogue to a master copy; it
cross-checks two representations to surface drift, treating both as
equally provisional.

This isn't decorative philosophy. It's the structural reason the
methodology survives context loss: *because no element is
self-present, every element is queryable from its traces, and any
substrate that preserves the hom-set preserves the methodology*.

## Open questions

- **Schema interoperability across instances.** If two domains both
  use this methodology, can they share schema breaks? E.g., does
  "paging" in a processor catalogue map to a similar break in a
  language-runtime catalogue (managed-heap layout)? The
  wedge-product audit generalises to cross-domain comparison.
- **Federation.** Multiple catalogues maintained independently might
  share a common substrate. The triple-store representation is most
  natural for federation.
- **Versioning.** The methodology is *additive* — but what about
  corrections (e.g., reassigning a break from one axis to another
  after later analysis)? A `CONTRADICT` verb is a candidate but
  not yet adopted.
- **Reasoning over the catalogue.** Once enough breaks accumulate,
  can derivation rules infer new facts? E.g., "if X originates F1
  and Y inherits from X, then Y inherits F1." Datalog-style
  inference is a natural fit.

These are real but downstream of the basic ISA. The current scope is:
*formalise what good cataloguing already does*, then build out from
there.

---

This document and the artefacts it describes (the package's `.md`
files, `schema.sql`, the Python ISA implementation) are themselves
witnesses of the methodology. Each is a substrate (prose, relational
SQL, executable Python) for the same underlying graph. Other
substrates (document, graph, triple store) would carry the same
content. The methodology is the equivalence-class; the substrates
are representatives.

The framework's strengthened self-hosting closure check (`theory.md`
§ 14.5.8) verifies that every CISC verb's `derives_from` chain
terminates in the RISC core (`introduce_node`, `edge`, `kquery`),
and that the catalogue's IMPL ↔ CAT gap is empty, on every
`check_self_hosting=True` open. The architectural detail of the
RISC reframe lives in
[`cotype/shadow_risc_core.md`](../../cotype/shadow_risc_core.md);
deep readers should follow that thread.
