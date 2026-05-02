# Theory — the foundations underneath the methodology

`methodology.md` describes *what the framework does*: the ISA, the
schema, the Klein-four read primitive, the MCP interface. This file
describes *why it has the shape it does* — the theoretical lineages
that converge on the methodology, and the structural commitments
those lineages license.

A reader (LLM or human) who has read `methodology.md` will recognise
many concepts here in deeper form. A reader who hasn't can start here
and pick up the operational details later.

## Contents

1. [The shadow-architecture skill set](#1-the-shadow-architecture-skill-set)
2. [Symmetry breaks as (partition, preservation-theorem) pairs](#2-symmetry-breaks-as-partition-preservation-theorem-pairs)
3. [Ordered axes and tropical queries](#3-ordered-axes-and-tropical-queries)
4. [The Klein-four read core](#4-the-klein-four-read-core)
5. [Magma theory: the slot-with-deferred-contents pattern](#5-magma-theory-the-slot-with-deferred-contents-pattern)
6. [Pointfree topology: the algebra is primary](#6-pointfree-topology-the-algebra-is-primary)
7. [Yoneda relationality](#7-yoneda-relationality)
8. [Derridean traces and the refusal of presence](#8-derridean-traces-and-the-refusal-of-presence)
9. [The recursive schema-as-symmetry-breaks](#9-the-recursive-schema-as-symmetry-breaks)
10. [The structural dual to CRUD schemas](#10-the-structural-dual-to-crud-schemas)
11. [Convergence: when the metamodel closes](#11-convergence-when-the-metamodel-closes)
12. [Trace-thickening: the catalogue moves forward, not back](#12-trace-thickening-the-catalogue-moves-forward-not-back)
13. [What the framework rules out](#13-what-the-framework-rules-out)
14. [Self-hosting closure via level-blind kquery](#14-self-hosting-closure-via-level-blind-kquery)

---

## 1. The shadow-architecture skill set

The methodology emerged from applying three named skills to the
problem of sustaining structural work across context boundaries —
the same problem the methodology then solves at scale.

The three skills:

### `decompose-by-entailment` (forward)

Given an intact goal, produce *named substructures* (called shadows)
that compose to satisfy it. Externalise each shadow before
implementing the whole. The skill's success criterion isn't
"complete the goal in this session" but "leave reusable named
costructure on disk that future sessions can extend."

When applied to the cataloguing problem itself, decompose-by-
entailment produced:

- The break primitive (named structural distinctions)
- The witness primitive (typed edges from objects to breaks)
- The refinement primitive (named per-edge attribute additions)
- The lineage primitive (descent edges between objects)
- The schema-break primitive (additive growth of the data shape)

Each shadow is a discrete, externalised artefact. A break that's
named in the catalogue survives any individual session that named
it.

### `regroup-from-shadows` (sideways)

Given an existing artefact that works, identify reusable
substructures within it, abstract them where possible, and recompose
the artefact using the abstractions. Behaviour-preserving by
construction.

When applied to the cataloguing problem, regroup-from-shadows
produced:

- The 4/5-axis Spec record (Spatial / Temporal / Parallel /
  Equivalential / Eventual) — a cross-cutting quotient of the
  named breaks. Most breaks turned out to commit to one of these
  axes; the few that committed to multiple landed in the `mixed`
  view.
- The (partition, preservation-theorem) decomposition of every
  break — applied uniformly across breaks regardless of domain.
- The KQUERY classifier — a regrouping that subsumes every
  read-mode (query, wedge, agreement, coverage, blind) into one
  primitive plus selection.

### `snap-to-grid` (backward)

Given an accumulator (called a cotype) that has received many
shadows over time, recognise the moment when its contents become
consistent with the user's request. The deliverable is *readable*
from the cotype at that moment.

When applied to the cataloguing problem, snap-to-grid is exactly
what the framework does at every read:

- The catalogue's current entailment is whatever the trace-set
  licenses *now*
- A read is a snap-to-grid check: "does this trace-set match what
  I asked for?"
- Drift is when the entailment doesn't match — surfaced via wedge
  audits or the 00 cell of a KQUERY

The methodology doesn't *implement* snap-to-grid as a verb; it
*is* snap-to-grid, made into a queryable substrate.

### Why this matters

The catalogue is the cotype made concrete. The witnesses are
shadows externalised. The schema breaks are decompositions
recorded. The Klein-four read is the snap-to-grid check
generalised. Each of the three skills's structural commitments
shows up in the framework's concrete shape:

- *Externalise substructures before implementing* → the catalogue
  is the externalisation
- *Allow cotypes to accumulate without forcing structure* → the
  schema grows additively; nothing is dropped
- *Recognise snap-to-grid when the trace-set licenses it* → every
  read is a deferred snap-to-grid check

The methodology is what shadow-architecture skills look like when
they're not interventions in an authoring process but the
substrate of the work itself.

---

## 2. Symmetry breaks as (partition, preservation-theorem) pairs

A *symmetry break* in this methodology isn't just a "named
distinction." It's a structured object with two parts:

### The partition

A function `partition : O → C` that maps every object `O` in the
domain to an equivalence class in some set `C`. Two objects in the
same class are *symmetric* with respect to this break — they share
whatever property the break carves up the domain by.

Examples:

- *Privilege rings* (a break a processor catalogue might carry):
  `partition` maps each instruction to {privileged, unprivileged}.
  The classes partition the instruction set.
- *Aliased state*: `partition` maps each architectural field
  to {has-alias, no-alias}.
- *Halt modes*: `partition` maps each spec's halt mechanism
  to {sticky, resumable, multi-mode-halt}.

(These illustrate the shape of `partition` for one possible
domain. The same shape applies to any domain whose objects can
be carved into equivalence classes by some property.)

### The preservation theorem

A claim of the form: *the partition is preserved as the temporal
coordinate advances*. Formally:

```text
∀ s, s' : O.
  partition(s) = partition(s') ⇒
    partition(step(s)) = partition(step(s'))
```

where `step` is the spec's step rule (per-cycle advancement, per-
reduction-step, per-instruction, etc.).

This is what makes a break *structural* rather than merely
classificatory. A naming convention partitions the space; only a
preservation theorem makes the partition load-bearing for analysis.

### Examples of preservation theorems

Each is paired with the break it secures. The examples below come
from a processor-catalogue context to make them concrete; the
*shape* of preservation theorem applies to any domain.

- **Bit-identical equality**: if two states have identical
  field values at time T, they remain identical at T+1 under
  deterministic step.
- **Bus-trace equivalence**: if two implementations produce
  identical bus traces through cycle T, they produce identical
  traces through T+k for all k.
- **Classification universality**: if an instruction is classified
  by some scheme at decode time, that classification is preserved
  by the analyser that consumes it.
- **Cache substrate state**: cache hit/miss outcome is
  determined by substrate state, and that substrate state evolves
  deterministically under the spec's program — so a fixed program
  produces a fixed cache trajectory.

### Why partitions need preservation theorems

Stating a break this way — explicitly as `(partition, preservation-
theorem)` — is what lets the framework *do work* with breaks. The
partition gives queryable structure (which states share an
equivalence class?); the preservation theorem gives semantic
guarantees (the structure persists under evolution). A break
without a preservation theorem is just a label; a label can be
catalogued but it can't be reasoned with.

The `break_invariants` table in the schema records both
explicitly. Not every break populates it (some are too meta —
Q71 is a *meta-claim about other breaks*, not itself a partition
of objects), but every concrete domain-level break should.

---

## 3. Ordered axes and tropical queries

One of the methodology's deepest structural commitments.

### The observation

Every symmetry plane named in the framework parameterises *along
an axis*. The axis is *some ordered field* — sometimes literal
clock time, sometimes a more abstract ordering — across which the
symmetric side varies while the partition is preserved:

- Bit-identical equality parameterises along **wall-clock time**
  (or its substrate-cycle proxy).
- Bus-trace equivalence parameterises along **cycle count**.
- α-equivalence (lambda calculus) parameterises along
  **reduction-step**.
- Confluence parameterises along **which-redex-first** (a
  partial order).
- DSL substrate-portability parameterises along
  **substrate-choice** (numpy / cupy / megakernel / abstract).
- Soundness regime lattice parameterises along **analysis-step**.

In every case, the symmetry plane carves states into equivalence
classes, and there's a column whose *order* lets us aggregate over
the witnesses to find a structurally-significant minimum (or
maximum).

### The structural claim

> **Every symmetry plane has a normal axis that admits a total
> (or partial) order. Tropical queries — `MIN`/`MAX` aggregates
> — over that order, restricted by witness-kind predicates,
> derive every "first," "earliest," "latest" question the
> catalogue can answer.**

This is the **symmetries-are-temporal-translation-invariances**
commitment — where "temporal" is read broadly as "an ordered axis
along which evolution preserves the partition."

### Time is one such axis; catalogue_order is another; domains add more

The framework provides two canonical ordered columns out of the
box:

- **`year`** — chronological order of articulation. Tropical-MIN
  over this answers *who originated this break?* (earliest year
  among origin-class witnesses).
- **`catalogue_order`** — exposition order in the catalogue.
  Distinct from year because exposition order doesn't have to
  be chronological. Tropical-MIN over this answers *where did
  the catalogue first analyse this break?*

Each canonical column has a documented semantic and a pre-defined
view (`break_origin`, `break_first_seen`). But neither is
structurally privileged. Domain extensions can add additional
ordered columns by `ALTER TABLE specs ADD COLUMN`, and the
framework's `tropical_min(axis_column, witness_kinds)` operator
works over any of them. Examples a domain might want:

- **`released_version`** — for software where "first version to
  ship X" is more meaningful than year.
- **`paper_publication_date`** — for academic catalogues where
  the paper-publication year matters more than the
  implementation year.
- **`significance_rank`** — for catalogues where importance
  weighting matters; tropical-MIN picks the lowest-rank (most
  important) witness.
- **`tournament_seed`** — for domains where artefacts are ranked
  by competitive performance.

The framework's commitment isn't to time *as such*; it's to
**tropical aggregates over ordered columns**. Time and exposition
order are two such columns the framework instantiates by default
because they answer the most common questions; domain-specific
ordered columns are admissible and use the same machinery.

### What it licenses

Once tropical-MIN-over-an-ordered-column is named as the universal
read primitive, several things follow:

#### (a) Originator queries become tropical aggregates

"Who originated this break?" is asking, *along an ordered axis*,
for the extremum witness with an origin-class kind. Concretely:
`MIN(<axis>)` over a filtered edge set — a tropical-algebra (min-plus)
aggregate. The framework provides `year` as the canonical default
axis, but any ordered column on `specs` works (`version`,
`paper_year`, `proof_depth`, …). No need for a `RETRO` verb;
attribution is always derived this way. The same machinery handles
"first to confirm cross-vendor," "earliest to refine," "most-recent
to deprecate" — each is a tropical query over a different ordered
axis with a different witness-kind filter.

#### (b) Time and lineage are breaks-themselves

If ordered axes are how the framework derives attribution, then
*the columns that carry orderings* (year, exposition order,
version, ...) are themselves the framework's privileged data.
Partitioning objects by their position on the year axis is itself
a symmetry break. Same for lineage — partitioning objects by
descent equivalence-classes is a break. Both are recorded as
primary data on the witness graph (year as object attribute;
lineage as edges).

This is the methodology's deepest structural simplification:
**temporal and lineage attributions aren't special; they're
applications of the framework's own primitives to its own
substrate.** Yoneda's "everything is its hom-set" applies *to the
catalogue itself*.

#### (c) Convergence is detectable

If the metamodel for a domain is closed, additions become
refinements rather than fresh breaks. Operationally: N consecutive
additions to the catalogue produce no new break entries in the
break_invariants table. The catalogue_order axis lets us *detect*
this — look at the most recent additions, count fresh breaks vs
refinements.

#### (d) Substrate-portability is structural

If the framework's protocol is "step rule advances along an
ordered axis; symmetries are preserved across the step," then
*any substrate that respects the order preserves the methodology*.
Numpy, cupy, megakernel, abstract analyser, FPGA Verilog — any of
them can carry the framework's protocol. Substrate-choice is
itself an ordered axis at coarse grain (each substrate produces
the same trajectory because the order is preserved).

### When ordered axes are partial

Most catalogues use totally-ordered axes (year, version number,
catalogue_order — all integers or strings with natural total
order). But some domains have partial orders:

- *Confluence* (lambda calculus): the "which-redex-first" axis is
  a partial order; redexes are interleavable.
- *Lineage in multi-inheritance domains*: the descent partial
  order admits sibling-relations.

Tropical-MIN over a partial order returns a *set* of minima (the
incomparable smallest elements), not a single element. The
framework's `tropical_min` helper currently assumes a total order
on the column; partial-order extensions are a future refinement.

### What "axis" doesn't mean

An axis in this framework is *not* wall-clock time specifically.
It's the column along which the spec's step rule (or articulation
sequence, or version sequence) advances. Different specs and
different domains have different ordered axes:

- 6502: `cycle` (8-bit microprocessor cycles)
- Lambda calculus: `reduction-step`
- Brainfuck: `step-count` (per-command)
- Compiler: `analysis-step` (each transformation pass)
- A schema-version catalogue: deployment date, or sequence
  number
- A cryptographic catalogue: paper publication year, or NIST
  competition round

The framework's commitment is to *the abstract pattern*: ordered
axes admit tropical queries; tropical queries derive attribution
without storing it.

---

## 4. The Klein-four read core

A separate document section on KQUERY exists in `methodology.md`;
this expands the algebraic and philosophical content.

### The classifier (not a filter)

KQUERY is fundamentally a *function* `U → ℤ₂ × ℤ₂`:

```text
KQUERY(A, B; U) : U → ℤ₂ × ℤ₂
                  x ↦ (A(x), B(x))
```

For every element `x ∈ U`, KQUERY returns the membership signature
`(in A, in B)` as a pair of bits. The four cells are the *fibers*
of this function. Operationally, when we say "emit cell `10`" we
mean "return all elements whose signature is `(1,0)`."

This is structurally important because it means KQUERY doesn't
*select* a subset — it *labels* the universe with a four-way
classification. Every operation people normally call a query
(filter, intersect, diff) is a *post-classifier projection*.

### The Klein-four group V₄

The four cells form `V₄ ≅ ℤ₂ × ℤ₂`, the Klein four-group:

```text
                B = 0           B = 1
            ┌────────────┬─────────────┐
   A = 0   │  00 BLIND  │  01 RIGHT   │
            ├────────────┼─────────────┤
   A = 1   │  10 LEFT   │  11 AGREE   │
            └────────────┴─────────────┘
```

The group structure means: cells compose under the obvious bit-
parity addition. `10 + 01 = 11`, `10 + 10 = 00`, etc. This is
*membership-signature addition*, not truth-value logic.

### Every Boolean operation lives in the four cells

Conventional Boolean operations on `A` and `B` correspond to cell
unions:

| Operation                | Cells          |
| ------------------------ | -------------- |
| `A`                      | `10 ∪ 11`      |
| `B`                      | `01 ∪ 11`      |
| `A ∩ B`                  | `11`           |
| `A ∪ B`                  | `10 ∪ 01 ∪ 11` |
| `A △ B` (symmetric diff) | `10 ∪ 01`      |
| `A \ B`                  | `10`           |
| `B \ A`                  | `01`           |
| `¬A ∧ ¬B`                | `00`           |
| coverage                 | `10 ∪ 01 ∪ 11` |

The full Boolean algebra over `{A, B}` fits inside the four cells.
Nothing is reducible further without information loss; any unary
operation throws away at least two cells.

### KQUERY is the terminal read primitive

For this methodology, KQUERY is *terminal* in the category-theory
sense: any read can be expressed via KQUERY plus selection, and
KQUERY itself can't be expressed as something even more primitive
without losing information.

This is unusual for an ISA's read layer. Most systems have many
read primitives (SELECT, WHERE, JOIN, GROUP BY, etc.) that
*could* be reduced to a few but conventionally aren't. KQUERY
*is* the reduction.

### The 00 cell as constitutive absence

The cell most diff/audit tools erase is `00` — items in the
universe absent from both A and B. Most tools don't even ask "what
isn't here?" because they collapse the universe to `A ∪ B` by
default.

The methodology elevates `00` because:

#### (a) It's structurally significant

Some catalogue questions only have meaningful answers in the `00`
cell. Schematically — for any consistency rule of the form
"objects exhibiting A should also exhibit B":

```text
U = objects within scope of the rule
A = objects exhibiting property A
B = objects exhibiting property B

00 = U \ (A ∪ B)
   = objects in scope that exhibit neither A nor B
```

The `00` cell isn't a violation of the rule (the rule fires on
the `10` cell: A but not B). It's the "object outside the rule's
reach entirely" cell — informationally rich and not visible from
ordinary diff. A processor catalogue might find that the 80286
lands in this cell of the paged/restart-suitable kquery (it has
frames but neither paging nor restart-suitable framing); a
language catalogue might find that statically-typed-without-
inference languages land in the corresponding cell.

#### (b) It refuses the metaphysics of coverage

By default, a diff tool implicitly assumes `A ∪ B = U` — that A
and B exhaust their domain. The 00 cell breaks this. It says: *the
universe contains items that neither representation accounts for,
and we can name them.*

#### (c) It's the Derridean trace cell

In Derrida's vocabulary, presence is constituted through
displacement and absence. The `00` cell records constitutive
absence — what's *not* in either representation but is implicitly
relied on for the comparison to be meaningful. Section 8 develops
this further.

### KQUERY normalisation (equivalence-class quotient)

KQUERY accepts a `normalize` callable that pre-applies to each
universe element before set membership. This gives an *equivalence-
class quotient*:

```text
KQUERY(A, B; U, normalize)
  ≡ KQUERY(normalize(A), normalize(B); normalize(U))
```

Examples:

- Case-folding (`normalize=str.lower`): `'F1'` and `'f1'` agree
- Identifier canonicalisation (`normalize=lambda s: s.split('-')[0]`):
  `'F1-rev1'` and `'F1-rev2'` agree
- Lineage projection (`normalize=lineage_of`): siblings agree

The quotient is itself a small symmetry-break of the read layer:
*the equivalence relation* under which membership is judged.

---

## 5. Magma theory: the slot-with-deferred-contents pattern

The methodology's structural pattern of *naming the role abstractly,
deferring the contents to per-spec declaration* isn't novel. It's
the same shape that magma theory already names.

### Magmas

A *magma* is a set with a binary operation — and nothing else. No
axioms; no associativity; no identity; no inverses.

```text
Magma = (S, ⋆ : S × S → S)
```

The structure *is* the slot (the operation `⋆`). The magma
admits any operation without commitment to what the operation
satisfies.

### The refinement chain

Algebraic structures elaborate magmas by adding axioms:

```text
Magma         (no axioms)
   ↓ + associativity
Semigroup
   ↓ + identity
Monoid
   ↓ + inverses
Group
   ↓ + commutativity
Abelian group
```

Each refinement *names* a property the slot must now satisfy.
None imposes a specific operation; they constrain the operation
class.

### The methodology applies the same shape

Several primitives in the catalogue's metamodel are magma-shaped:

- **`EqualityMode`** — the slot is "a comparison protocol"; the
  contents are spec-supplied. The default is bit-identical;
  α-equivalent and observational are admissible refinements.
- **`StepRule`** — the slot is "advance the temporal coordinate
  one tick"; contents are spec-supplied. Examples: a processor
  spec supplies `prepare ∘ bus ∘ latch`, a lambda calculus
  supplies `find_redex ∘ substitute`, a Turing-tape language
  supplies `dispatch_one_command`.
- **`BatchProtocol`** — the slot is "lockstep semantics for
  parallel rows"; contents are spec-supplied.
- **`Space.cell_overflow`** — the slot is "what happens on
  arithmetic overflow"; contents are `wrap` / `saturate` / `error`
  per spec.

In each case, the framework names *what role* the slot plays
without committing to *which* operation fills it. Specs supply
the contents; refinements add axioms.

### What this licenses

When the framework hits a structural question it hasn't yet
answered, magma theory tells us where to look:

- *What axioms must the slot satisfy for some specific use?*
  → Magma-theoretic literature catalogues these (associativity
  for sequencing, identity for scalar mults, inverses for undo).
- *What's the minimal commitment that still gives me what I
  need?* → Pick the loosest position on the refinement chain.
- *What happens if I weaken the axioms?* → Look at the
  pre-refinement structure (semigroup vs monoid vs group).

The framework borrows from a mature literature; it doesn't have
to invent the shape itself.

---

## 6. Pointfree topology: the algebra is primary

Classical topology defines a *space* by its set of *points* plus a
collection of *open subsets*. Points come first; opens are
relations on points.

Pointfree topology *inverts* this. It takes the *lattice of opens*
(the algebra) as primary; points are derived from the algebra as
"completely prime filters" or analogous constructs. The shift makes
*the algebra* the structural carrier; points fall out where the
algebra licenses them.

### The methodology applies the same inversion

In the catalogue:

- **Spaces, temporal coordinates, protocols, axes** are the
  algebra.
- **Concrete state** (which byte at which address at which cycle)
  is derived from the algebra plus a trajectory along the temporal
  axis.

The framework's protocols express what's true *for any spec*. The
specific bit values fall out per-trajectory, per-row.

### Why this matters for the catalogue

Pointfree topology gives us license to:

- **Write protocols in terms of relations**, not specific instances.
  The 9P-style namespace (Z31) names *paths and binds* — relations,
  not particular memory cells.
- **Treat instances as derived data**. A spec's behaviour at
  cycle 12345 isn't a primary object; it's derived from the spec's
  algebra applied along the temporal axis to that point.
- **Refine the algebra without rewriting instances**. Adding a
  Q-numbered break extends the algebra; existing trajectories
  re-derive under the richer algebra without re-declaration.

This is structurally why **per-spec parameterisation is the
universal escape valve**. Whenever an earlier commitment turns
out to be too concrete, the resolution is to make it a per-spec
declaration — i.e., to lift the concrete content into the per-
spec algebra and let instances fall out.

### Together with magma theory

Pointfree topology + magma theory give the framework:

- *Magma theory*: name the structural slot abstractly; defer
  axioms. Refinement chains catalogue what additional axioms
  enable.
- *Pointfree topology*: the algebra is primary. Specific instances
  fall out where the algebra licenses them.

The methodology's "spec-is-everything-the-framework-would-otherwise-
have-to-fix-universally" pattern is exactly this. The framework
fixes the *algebra* (the protocols, the schema, the read primitive);
specs supply the *contents* (which spaces, which step rule, which
equivalence mode). Concrete states are derived from the
combination.

---

## 7. Yoneda relationality

The Yoneda lemma in category theory states (informally): *an
object in a category is fully characterised by the morphisms into
it (its hom-functor), or equivalently the morphisms out of it (its
co-hom-functor).*

You cannot know an object except through its relationships. There
is no "essence" of the object beyond its participation in the
category's hom-set.

### The methodology's Yoneda commitment

In the catalogue:

- **An object is its witnesses.** A spec's identity is exactly the
  edges it participates in: `(kind, break, refinements, scope)`
  edges. Nothing about a spec is recorded outside its relations.
  Even attributes like `year` and `lineage` are themselves
  witness-edges — to time and lineage breaks.
- **A break is its witnesses.** A break's identity is exactly the
  edges from objects to it. There's no break "in itself" outside
  the witness graph.
- **Substrate is irrelevant; only relations matter.** Whether the
  catalogue lives in SQL, a triple store, a graph DB, or JSON
  files is invisible from the relational stance. The same hom-set
  is presented across all four substrates. The ISA is the
  hom-set-preserving translation between them.

### The unary-query-is-binary insight

A consequence of strict Yoneda relationality: *every read is
binary, never unary*.

What looks like a unary query — "what breaks does spec X
originate?" — is actually:

```text
binary comparison: edges where spec_id = X   AND   kind ∈ origin-class
                   ────────────────────────── ──────────────────────────
                   left referent              right referent
                   (one spec)                 (a kind-set)
```

Only the *left* referent is named in the query; the right is an
implicit kind-class. Once both referents are made explicit, the
query is a KQUERY against an implicit universe.

This is exactly Yoneda's insight: an object can only be known
through its morphisms with another object. There's no inspecting
an object alone.

### Substrate-portability formalised

Yoneda's lemma also formalises the substrate-portability claim:

> Two substrates are equivalent for the methodology's purposes
> iff they preserve the hom-set.

If a triple-store and a relational DB both expose the same `(spec,
break, kind, notes)` edge structure plus the derived views, they
present the same Yoneda functor. Anything that holds in one holds
in the other. The ISA verbs are the morphism-preserving
translation.

---

## 8. Derridean traces and the refusal of presence

Jacques Derrida's reading of structuralism observes that *no element
of a sign-system is self-present*. Meaning is constituted through
*difference* (separation from other terms) and *deferral* (no term
delivers its meaning unilaterally). The trace is what remains: a
mark whose meaning is always already pointing elsewhere.

### The methodology's Derridean commitment

The catalogue refuses presence at every level:

- **No foundational break.** No break is a privileged origin from
  which other breaks descend. Each is named because some object's
  analysis surfaced it; each remains revisable as future objects
  contribute traces.
- **No foundational origin.** The originator of any break isn't
  a fact stamped into the schema. It's *derivation* — tropical
  MIN over the catalogue's chosen metric axis, restricted to
  origin-class witness edges. An earlier reading isn't wrong;
  it's what the trace-set then licensed.
- **No foundational schema.** Schema breaks emerged additively;
  none was specified in advance. The schema is itself a sediment
  of traces.
- **No foundational object.** Objects and breaks are constituted
  by their participation in the witness graph. Nothing about
  an object is "intrinsic" outside its relations.

### The retroactive moment

The acutest Derridean moment in the methodology is the retroactive-
attribution pattern. Schematically (with a processor catalogue
example to make it concrete):

- 1985 (or whenever the catalogue is built): the catalogue
  analyses object β (the 80386), names break F1 (paging),
  records β as F1's originator. This is what the trace-set then
  licenses.
- Later catalogue session: an earlier object α (System/360/67,
  1965) is examined, found to have already exhibited the break
  twenty years earlier. An `origin` witness from α is added.
- *The originator of F1 is now α* — automatically, via the
  tropical-MIN-over-the-axis query.

Crucially: **the prior reading wasn't false.** It was the originator
*as the trace-set then licensed*. The new originator is the
originator *as the trace-set now licenses*. Both readings are
valid relative to their trace-sets.

The catalogue doesn't *correct* itself backwards. It *thickens*
itself forward, and the derived global structure is whatever the
current trace-set licenses. There is no privileged moment of "the
right answer"; there are only progressively richer trace-sets and
the queries they license.

### The four KQUERY cells, Derridean read

Each cell of the KQUERY classifier corresponds to a Derridean role:

| Cell | Membership signature | Derridean role                              |
| ---- | -------------------- | ------------------------------------------- |
| `11` | in A ∧ in B          | apparent presence / agreement               |
| `10` | in A ∧ ¬ in B        | différance / left-displacement              |
| `01` | ¬ in A ∧ in B        | différance / right-displacement             |
| `00` | ¬ in A ∧ ¬ in B      | trace of absence; constitutive blind spot   |

The 11 cell is *apparent presence*. Derrida would say even this
is constituted through the differential structure of the others;
nothing is purely present even at the agreement cell.

The 10 and 01 cells are *différance* in Derrida's specific sense:
each represents what one trace says the other doesn't. They're the
*productive displacements* — where the comparison is informative.

The 00 cell is the *trace of absence* — what's *not* in either
representation but is in the universe. It's constitutive: without
implicitly bounding the universe, the comparison wouldn't have
meaning. The 00 cell makes the implicit boundary explicit.

### Together with Yoneda

Derrida + Yoneda yields the methodology's working stance:

1. **Identity is relational** (Yoneda): objects are constituted
   by their participation in the relevant category.
2. **Relations are traces** (Derrida): each relationship is a
   deferral that points to others; no relationship is the
   privileged ground.
3. **Global structure is derived, never imposed**: views,
   queries, the metamodel itself are functions over the trace
   graph, re-derivable as the trace-set thickens.

This is the methodology's metaphysical commitment. It's not
decorative philosophy — it's the structural reason the catalogue
survives context loss: *because no element is self-present, every
element is queryable from its traces, and any substrate that
preserves the hom-set preserves the methodology.*

---

## 9. The recursive schema-as-symmetry-breaks

The methodology's data shape — the SQL schema in `schema.sql` —
is itself an instance of the methodology applied to its own
structure.

### Schema breaks (S0 through S11)

Each step of the schema's evolution corresponds to a structural
pressure that earlier objects didn't force into view but later
ones did:

- **S0**: `breaks` table — the seed. Just `(number, name,
  short_desc)`.
- **S1**: `specs` table — needed witnesses; objects had to be
  recorded.
- **S2**: framework-load-bearing spec metadata columns — needed
  `year` for tropical attribution and `catalogue_order` for
  exposition-ordering; `notes` for free-form annotation. This is
  the minimal set: only attributes load-bearing for framework
  views are first-class columns.
- **S2b**: `spec_attributes` table — domain-specific
  `(name, value)` triples on specs. Anything not framework-load-
  bearing (vendor, family, register width, paradigm, hardness
  assumption, ...) lives here as trace data, queryable through
  the same KQUERY apparatus as everything else.
- **S3**: `witnesses` table — the bipartite contribution graph
  needed; named-edge vocabulary forced documented kinds.
- **S4**: `refinements` table — finer-grained per-edge
  annotations; multiple per (break, spec) pair.
- **S5**: per-break-family detail tables — domain-specific (the
  framework leaves these to extensions).
- **S6**: `break_axes` table — per-break axis classification;
  forced by the meta-claim that breaks should be tagged with
  their axes.
- **S7**: `tensions` table — implementation-alignment concerns;
  forced by the need to record meta-claims that don't yet have
  the structure of a break.
- **S8**: `scope` column on witnesses — agent vs spec
  distinction; forced when one named witness object turns out to
  contain multiple distinguishable contributors.
- **S9**: `spec_axes` + `spaces` tables — per-spec 5-axis
  declarations; forced by Brainfuck's per-Space refinements.
- **S10**: `break_invariants` table — Z78's (partition,
  preservation-theorem) decomposition; forced by the time-axis
  insight.
- **S11**: `lineages` table — descent edges; forced by
  methodology.md's commitment that lineage is a break-on-objects.

Each schema break is *additive*. The schema never drops a column
or table. New structure piles on; existing rows are unchanged.

### The recursion

The methodology applies to its own data shape:

- *Decompose-by-entailment*: each schema break decomposes the
  data shape into a costructure (a new table or column) plus a
  composition (the existing schema absorbs it).
- *Regroup-from-shadows*: when several breaks force the same kind
  of refinement, the schema regroups (e.g., the per-break detail
  tables form a family).
- *Snap-to-grid*: the schema is "complete enough" when it admits
  the existing trace-set without forcing per-domain workarounds.

The catalogue's ability to *grow with usage* is exactly this
recursion working at the data-shape level.

### Why the recursion matters

If the methodology weren't recursive — if the data shape were
fixed in advance — the framework couldn't admit new domains or new
structural pressures. The recursion is what makes the framework
extensible *without rewriting itself*.

The MCP server's schema-evolution verbs (`KIND.NEW`,
`PREDICATE.NEW`, `AXIS.NEW`) name this explicitly. They're the
methodology's verbs for adding new schema breaks programmatically.

---

## 10. The structural dual to CRUD schemas

A consequence of the recursive schema commitment in § 9: the
catalogue framework isn't competing with relational databases —
it's the *structural dual* of one. Every CRUD schema *is*
(implicitly) a catalogue of structural decisions; the framework
just makes that latent structure explicit and queryable.

### Translation table

The duality is direct and total:

| Relational schema (instance level) | Catalogue (meta level)                          |
| ---------------------------------- | ----------------------------------------------- |
| Table                              | Object kind (`KIND.NEW`)                        |
| Column                             | Schema break adding a partition                 |
| `NOT NULL` constraint              | Partition + preservation theorem (totality)     |
| `UNIQUE` constraint                | Partition + preservation theorem (injectivity)  |
| `CHECK` constraint                 | Partition + preservation theorem (predicate)    |
| Foreign key (`REFERENCES`)         | Lineage edge (`descended-from` / relational)    |
| `INDEX`                            | Materialised derivation (a view's index)        |
| Default value                      | Refinement annotation                           |
| Migration                          | Schema-evolution verb sequence (additive)       |
| Migration history                  | Trace-thickening over the schema's lifetime     |
| `CREATE VIEW`                      | Named selection / KQUERY emission               |
| Generated/computed column          | Derived view (no primary data)                  |
| Partitioning (range/list/hash)     | Spatial-axis declaration                        |
| Triggers                           | Event-driven verbs (Q74-style perturbations)    |

Every entry on the left is making a structural decision; every
entry on the right is the catalogue framework's vocabulary for the
same decision.

### What the catalogue makes queryable

A CRUD schema *embodies* its structural decisions but doesn't
*expose* them as queryable structure. You can read DDL and infer
why each constraint exists, but the *forcing pressures* (which
business case, which data anomaly, which compliance requirement)
live in commit messages, ticket trackers, post-mortems — outside
the schema itself.

The catalogue framework, applied to the schema as a domain, lets
you record:

- *Which break* each migration instantiates (e.g., "added
  `email UNIQUE` to enforce account-uniqueness — instantiates
  the `unique-identifier` break")
- *The forcing object* (which user story, audit, or incident
  forced the decision)
- *The preservation theorem* the constraint guards (e.g., "no
  two active accounts can share an email")
- *Lineage* of the schema across versions (each migration is a
  descendant of the prior version's schema)
- *Tensions* the schema currently embodies but hasn't resolved
  (e.g., "soft-delete via `deleted_at` versus hard-delete via
  `DELETE FROM`")

These are the same primitives the framework provides for any
domain. The schema-as-domain instance just happens to be
self-referential: the catalogue is recording the structure of a
data-shape, using a data-shape (its own schema in `schema.sql`).

### The Yoneda reading

In Yoneda terms (see § 7), a relational schema and a catalogue
present the *same* hom-set at different levels:

- The relational schema's hom-set: morphisms between rows,
  determined by table structure, FKs, constraints.
- The catalogue's hom-set: morphisms between structural decisions,
  determined by witness edges, lineage, refinements.

A migration is a hom-set-preserving translation between two
relational schemas: it adds rows to the catalogue's
breaks/witnesses tables (recording what the migration commits to)
*and* adds tables/columns/constraints to the relational schema
(realising the commitment in instance form).

The two co-evolve. Catalogue and schema are functorially related:
each is the structure-of the other.

### The Derridean reading

In Derridean terms (see § 8), the schema is *traces of past
decisions*. Every column, constraint, and FK is the residue of a
moment when some pressure forced a structural decision. Reading
the schema, you're reading deferred meaning: each column says
"someone decided this, somewhere, somewhen, for some reason."

The catalogue makes these traces *explicit and queryable*. The
implicit Derridean traces in the schema become explicit witnesses
in the catalogue. Nothing was hidden; everything was already
trace; the catalogue just makes the trace addressable.

### Practical applications

When you apply the catalogue framework to your own database
schema:

#### Onboarding

New team members typically learn the schema by reading DDL and
guessing rationale. With a catalogue:

```sql
SELECT
    b.name AS structural_decision,
    o.name AS migration_that_introduced_it,
    o.year AS year,
    r.description AS rationale
FROM breaks b
JOIN witnesses w  ON w.break_number = b.number
JOIN specs    o   ON o.id = w.spec_id
JOIN refinements r ON r.break_number = b.number AND r.spec_id = o.id
ORDER BY o.year;
```

Each row tells the structural story: which decision, which
migration introduced it, when, why.

#### Migration planning

Before adding a migration, ask: *what break is this
instantiating?*

- Existing break with refinement: extend an existing structural
  pattern (low-risk).
- Existing break, but cross-vendor / cross-table: confirms the
  pattern in a new context.
- New break: introducing genuinely new structure (high-risk;
  warrants explicit (partition, preservation-theorem) statement).

#### Refactoring decisions

When a constraint or column seems vestigial, query: *which break
does this witness, and is the break still active?*

If the break is still load-bearing, the constraint is needed.
If the break has been superseded (a different break now covers
the same pressure), the constraint may be removable.

#### Cross-team schema understanding

When two teams' schemas seem related, KQUERY between their break
sets:

```text
KQUERY(team_a_breaks, team_b_breaks, universe=all_known_breaks)
```

The 11 cell shows shared structural primitives; the 10 / 01 cells
show team-specific specialisations; the 00 cell shows
methodologically-relevant breaks neither team has captured.

### Why this matters for the framework

This dual reading isn't a special-case application. It's the
methodology applied to the case the methodology was *built around*.
Recall: the catalogue framework's own schema (in `schema.sql`)
evolved through schema breaks S0-S11, each forced by a structural
pressure that earlier objects didn't surface. The catalogue is its
own first instance.

Every CRUD database in the world is a (silent, implicit)
catalogue. Most have no view that asks "why this column?" or
"which breaks are still load-bearing?" The framework provides
exactly that view, applicable to any CRUD database whose
designers care to record their decisions explicitly.

The catalogue is what your schema *is*, viewed from the structural
side. The CRUD database is what your catalogue *generates* at the
instance level. They aren't alternatives; they're a co-evolving
pair.

---

## 11. Convergence: when the metamodel closes

A domain's metamodel is "closed" when no new objects produce new
structural breaks — only refinements and confirmations of existing
ones.

### Operational signal

Convergence shows up as: **N consecutive additions to the
catalogue produce zero new break entries.**

For example, in a processor catalogue's growth history:

- Several early processors each introduce one or two new breaks
  (paging, modal specs, joint instruction execution, ...).
- Later processors in the same lineage add successively fewer
  new breaks; they mostly *confirm* existing breaks
  (cross-vendor) or contribute *refinements* of them.
- Eventually a streak of additions produces *zero new breaks*:
  the new objects fit entirely within the metamodel that prior
  additions already named. That's the convergence signal — the
  metamodel for the processor domain is closing.

The same pattern applies to any domain. A language catalogue
converges when new languages stop forcing new structural
primitives and start refining ones already named (e.g., a new
language introduces a slight variant of an already-catalogued
gradual-typing model rather than a wholly new typing discipline).

### What convergence means

When the metamodel closes:

- New objects in the domain confirm or refine existing breaks.
- The framework's primitives are sufficient; no new structural
  primitive is needed.
- Cross-vendor and cross-lineage convergence appears — different
  designs reaching the same primitive shape.

Convergence isn't proof that the metamodel is *complete* in some
absolute sense — only that the trace-set so far hasn't required
extension. A novel domain (quantum computing, neuromorphic
hardware) might force a new primitive.

### Why convergence is informative

If the metamodel converges, the framework has *correct shape* for
the domain: the primitives genuinely partition what's structurally
relevant. If it doesn't converge — if every new object forces a
new break — the framework's primitives are too narrow.

The catalogue's `new_breaks_per_spec` view and the absence of new
break-rows over recent additions are how convergence is detected
operationally.

---

## 12. Trace-thickening: the catalogue moves forward, not back

A core methodological commitment that follows from the Yoneda+
Derrida stance: *the catalogue thickens forward; it doesn't correct
backward.*

### What this means

When new traces (witnesses, refinements, lineage edges) are added:

- Existing traces are *not modified*.
- Existing readings are *not invalidated*.
- The derived global structure (originator, status, retroactive
  gap) is *re-derived* under the richer trace-set.

The new derivation may differ from the old, but neither was wrong
— each was what its trace-set licensed.

### The retroactive case

The cleanest example, schematically (with a processor catalogue
illustration to make it concrete):

- Initial analysis: catalogue records object β (the 80386, year
  1985) as the originator of break F1 (paging).
- Later session: catalogue examines an earlier object α (the
  System/360/67, year 1965) and adds an `origin` witness from it.
- Now: the originator query (`MIN(year)` over origin-class — or
  `MIN(<other-axis>)` for catalogues that have chosen a different
  metric field) returns α — the earlier originator.

The first reading isn't corrected. β still holds its
`catalogue-introduces` witness. The `first_seen` view still returns
β. What changed: α now has an `origin` witness that the
tropical-MIN-over-the-axis query picks up.

There's no `RETRO` verb because there's no correction. There's
just additional trace material and re-derivation.

### Why trace-thickening matters

If the methodology *did* correct backward, several problems would
arise:

- **History becomes fragile.** Past readings would have to be
  invalidated; downstream artefacts (papers, documentation,
  prior conversations) would be stranded.
- **Atomic correctness becomes ambiguous.** If readings can be
  invalidated, what was a "correct" reading at any moment? The
  Derridean answer is that there are no atomically-correct
  readings — only readings relative to trace-sets.
- **Substrates can't sync.** If readings change, substrates that
  cached them must invalidate caches. Trace-thickening lets
  substrates accumulate without invalidation.

Trace-thickening is the structural reason the catalogue is
*append-only* in spirit, even if the database technology supports
update.

### Practical implication

When you add a new object to the catalogue, *don't worry about
existing readings*. They'll re-derive under the richer trace-set
automatically. The MCP server's tools and the SymmetryCatalogue
class all assume trace-thickening — they don't expose verbs for
correction.

If you need to mark a prior trace as "superseded" (e.g., a typo
in a witness's notes), the methodology proposes a future
`CONTRADICT` verb that *adds* a contradicting trace rather than
*deleting* the original. This is a deferred concern noted in
methodology.md's open questions.

---

## 13. What the framework rules out

The methodology's commitments rule out several classes of system.
Surfacing the boundaries makes the framework's identity explicit
and tells us when a sibling framework would be needed.

### Systems without a coherent temporal axis

Distributed systems where observation order varies across observers,
agent-based simulations where each agent has its own local time,
consensus protocols with no global ordering. These need a sibling
metamodel where the temporal axis is partial-ordered (Lamport-time)
rather than totally-ordered.

The framework's Q72 commitment (symmetries-are-temporal-translation-
invariances) assumes a *single* axis. Partial-ordered axes are a
real generalisation, but they require different machinery for the
preservation theorems.

### Continuous-time evolution

Analog computation, ODE solvers, real-time control loops with
sub-step semantics. The framework's step rule is discrete; the
temporal axis is integer-indexed. Continuous-time would require
generalising StepRule to a flow rule and the preservation theorem
to a continuous form.

### Non-deterministic step semantics

Probabilistic computation, branching futures, quantum superposition.
Each step's result is itself a *distribution* over slices, not a
single slice. The framework's witness graph and trace-set assume
deterministic evolution.

A probabilistic sibling metamodel would lift `Slice` to
`Distribution(Slice)` and the preservation theorem to a
distributional form (preserve the partition almost-surely, in
distribution, in expectation, etc.).

### Why these matter

The framework's identity is its commitments. A system that requires
relaxing them — partial-ordered time, continuous time, non-
deterministic steps — needs a *different* framework that shares
some structure with this one but isn't subsumed by it.

The framework's `BOUNDARY` verb is the operational form of this
stance. A break that's *adjacent* to the framework's identity but
not subsumed by it (e.g., a candidate distinction whose proper
treatment requires a sibling framework's machinery) gets recorded
with a `sibling-boundary` witness rather than absorbed into the
metamodel.

The same stance applies more broadly: sibling frameworks compose
where their hom-sets agree on shared substrates.

---

## A summary of the framework's commitments

The methodology can be stated in seven commitments. Each follows
from the previous; each is structurally load-bearing:

1. **Externalise structure as traces** (shadow architecture): the
   substrate is a graph of named breaks, witnesses, refinements,
   lineage edges.

2. **Each break is a (partition, preservation-theorem) pair**:
   structure isn't classification; it's structure-with-semantic-
   guarantee.

3. **Time is normal to every symmetry plane**: the temporal axis
   is the universal one; tropical-MIN attributions follow.

4. **Reads are Klein-four classifications**: KQUERY is the only
   primitive read; everything else is sugar; the 00 cell is
   constitutive.

5. **Identity is relational** (Yoneda): an object is its hom-set;
   substrate-portability is hom-set preservation.

6. **No element is self-present** (Derrida): traces accumulate;
   prior readings aren't false but trace-set-relative; the
   catalogue thickens forward.

7. **The schema is itself the methodology applied to its own data
   shape**: schema breaks are additive; convergence shows when
   the metamodel closes; recursion makes the framework
   extensible.

These are the foundations. The methodology, ISA, schema, MCP
interface, and tutorial are how the foundations operationalise.

---

## 14. Self-hosting closure via level-blind kquery

§§ 1-13 above describe a methodology in which the catalogue
accumulates named structural distinctions about a domain, and § 9
gestures at the recursion in which the catalogue's own primitives
become Q-numbered breaks the catalogue catalogues about itself.
This section makes that recursion explicit and constructive: it
defines the level-blind variant of `kquery`, the closure kquery
that audits the framework's self-hosting, and the runtime invariant
that licenses the framework to claim self-hosting at a stated
scope.

The result is a single property the framework can check on every
catalogue open. Passing the check is the framework's snap-to-grid
against itself; failing it produces the precise to-do list of which
structural commitments are *implicit* (implemented but not
catalogued) or *promissory* (catalogued but not implemented).

Prerequisites: §§ 1-13 of this document, especially § 2
((partition, preservation-theorem) pairs), § 4 (the Klein-four
read core), § 9 (recursive schema-as-symmetry-breaks), and § 11
(convergence). Operationally: `methodology.md` §§ 2-7,
`README.md` quick start, and the user-side governing charter
*"constructible → reachable → observable → coverable"* (cited
below as **the charter**).

### 14.1 Notation

Notation introduced for this section, in order of appearance:

- **`Kinds`** — the finite set of cell kinds the framework admits
  (enumerated in Definition 14.1). Used as the target of the tag
  projection.
- **`C`** — the universe of *cells*. A cell is any structural
  commitment the framework makes — an object, a break, a witness
  edge, a refinement, a schema-extension, a wedge audit, a kquery
  instance, or a closure-check instance. Cells carry a tag in
  `Kinds` identifying their kind; the tag is recoverable but is
  not consulted by `kquery`.
- **`tag : C → Kinds`** — the projection assigning each cell its
  kind.
- **`P : C → 𝟚`** — a *level-blind predicate*. Returns `1` on
  cells the predicate addresses and asserts, `0` otherwise. The
  "otherwise" is silent: a predicate that does not address a given
  cell kind returns `0` rather than raising.
- **`kquery(A, B; U)`** — the level-blind read primitive, with
  `A, B : C → 𝟚` and `U ⊆ C`. Returns the four cells
  `{11, 10, 01, 00}` of the partition induced by `(A, B)` on `U`.
- **`V₄`** — the Klein four-group, written multiplicatively as
  `{e, a, b, ab}` with `a² = b² = e` and `ab = ba`. The four cells
  of `kquery` are the orbits of the action `Z/2 × Z/2 ↷ U`
  induced by `(A, B)`.
- **`Q-X`** — a Q-numbered break in the level-0 catalogue, named
  `X`. `Q-bootstrap-closure` and `Q-supported-claims` are
  introduced below (§ 14.5).
- **`◇C`** (read "diamond C") — the *scope* of a self-hosting
  claim, a subset of `C` the catalogue claims to host. Recorded
  as data via `Q-supported-claims`.
- **`IMPL`, `CAT`** — the implementation and catalogue
  predicates, defined in § 14.2.
- **`ClosureKQ(K, ◇C)`** — the closure kquery of catalogue `K` at
  scope `◇C`, defined in § 14.2.
- **`.gap`** — for any kquery result, the union of its `01` and
  `10` cells.
- **The charter** — the user-side governing principle: *"if a
  distinction is real, it must be constructible; if constructible,
  it must be behaviorally reachable; if reachable, it must be
  observable; if observable, it must be coverable; if not, it is
  not a valid runtime distinction."*

Recurring assumption: every cell in `C` has a stable identifier
drawn from the catalogue's own ID space, and is addressable by
that identifier in SQL. This is what makes `U ⊆ C` enumerable.

### 14.2 Definitions

**Definition 14.1 (Cell namespace).**
Let `Kinds = {O, B, W, R, E, A, K, X}` where `O` is objects, `B`
is breaks, `W` is witnesses, `R` is refinements, `E` is
schema-extensions, `A` is wedge audits, `K` is kquery instances,
`X` is closure-check instances. The cell namespace `C` is the
disjoint union of cells of each kind:

```text
C = O ⊔ B ⊔ W ⊔ R ⊔ E ⊔ A ⊔ K ⊔ X
```

The set `Kinds` is itself catalogued (§ 14.5 via
`Q-supported-claims`), and may be extended by additive
schema-breaks per `methodology.md` ("What's generalisable",
item 8).

**Definition 14.2 (Level-blind predicate).**
A *predicate* over `C` is a total function `P : C → 𝟚` with the
convention that if `P` does not address a given cell kind, it
returns `0` on every cell of that kind. Equivalently: a predicate
is implicitly the characteristic function of a subset of `C`, and
predicates that fail to address a given kind treat that kind as
outside their subset.

**Definition 14.3 (Level-blind kquery).**
For predicates `A, B : C → 𝟚` and a finite universe `U ⊆ C`,

```text
kquery(A, B; U) := {
  11 : { c ∈ U | A(c) = 1 ∧ B(c) = 1 },
  10 : { c ∈ U | A(c) = 1 ∧ B(c) = 0 },
  01 : { c ∈ U | A(c) = 0 ∧ B(c) = 1 },
  00 : { c ∈ U | A(c) = 0 ∧ B(c) = 0 }
}
```

The four cells are pairwise disjoint and cover `U`. We write
`kquery(A, B; U).gap := kquery(A, B; U).10 ∪ kquery(A, B; U).01`.

**Definition 14.4 (Implementation predicate).**
`IMPL : C → 𝟚` is the predicate "is implemented in the framework's
code." Concretely: `IMPL(c) = 1` iff `c.tag` corresponds to a
callable, table, or runtime invariant declared in the framework's
signature module (`theory.py`, § 14.5).

**Definition 14.5 (Catalogue predicate).**
`CAT : C → 𝟚` is the predicate "is catalogued with sufficient
witnesses to reconstruct." Concretely: `CAT(c) = 1` iff there
exists a Q-numbered break `Q-c` in the level-0 catalogue with at
least the witnesses and refinements demanded by `c.tag`'s
associated preservation theorem (per § 2).

**Definition 14.6 (Closure kquery).**
The *closure kquery* of a catalogue `K` at scope `◇C` is

```text
ClosureKQ(K, ◇C) := kquery(IMPL, CAT; ◇C).
```

Its `.gap` is the set of cells where implementation and catalogue
disagree.

**Definition 14.7 (Self-hosting at scope `◇C`).**
A catalogue `K` is *self-hosting at scope `◇C`* iff:

1. `ClosureKQ(K, ◇C).gap = ∅`, and
2. The cell representing `ClosureKQ(K, ◇C)` itself is in `◇C`,
   and
3. The cell representing `Q-supported-claims` (which encodes
   `◇C` as data) is in `◇C`.

Conditions (2) and (3) are the recursion: the closure check
covers itself, and the scope-declaration covers itself.

### 14.3 Lemmas

**Lemma 14.1 (V₄ is level-blind).**
For any `A, B : C → 𝟚` and any `U ⊆ C`, the orbits of the action
`Z/2 × Z/2 ↷ U` induced by `(A, B)` depend only on the values
`(A(c), B(c))` for `c ∈ U`, and not on `tag(c)`.

*Proof sketch.* The action of `(α, β) ∈ Z/2 × Z/2` flips `A(c)`
if `α = 1` and flips `B(c)` if `β = 1`. The orbit of `c` is
`{(A(c) ⊕ α, B(c) ⊕ β) : (α, β) ∈ Z/2 × Z/2}`, determined entirely
by the pair `(A(c), B(c))`. The tag is not consulted. ∎

**Corollary 14.1.1.** The Klein-four read primitive is preserved
across cell kinds. A kquery whose universe contains cells of mixed
kind classifies them by the same `(A, B)`-pair partition as it
would a single-kind universe.

**Lemma 14.2 (Cross-kind kquery is well-defined under
silent-as-False).**
If `A` addresses kinds `K_A ⊆ Kinds` and `B` addresses
`K_B ⊆ Kinds`, then `kquery(A, B; U)` is well-defined for any
`U ⊆ C`, and its semantics agree with the level-blind reading:
cells outside `K_A ∪ K_B` fall into the `00` cell.

*Proof sketch.* By Definition 14.2, predicates return `0` on cell
kinds they do not address. Hence for `c ∈ U` with
`tag(c) ∉ K_A ∪ K_B`, `A(c) = B(c) = 0`, so
`c ∈ kquery(A, B; U).00`. The cells `11, 10, 01` are populated
only by cells of kinds in `K_A ∩ K_B`, `K_A ∖ K_B`, `K_B ∖ K_A`
respectively. The classification is total and disjoint. ∎

*Remark.* Lemma 14.2 is the technical content of the
silent-as-False choice. The alternative — `kquery` raising on
unaddressed cells — would force all kqueries to be level-uniform,
foreclosing cross-level audits. Silent-as-False is what licenses
`ClosureKQ`.

**Lemma 14.3 (Recursion: the closure kquery is itself a cell).**
Let `K` be a catalogue with a `ClosureKQ` instance at scope `◇C`.
Then `ClosureKQ(K, ◇C) ∈ X ⊆ C`.

*Proof sketch.* `ClosureKQ` is invoked at runtime; each invocation
produces a kquery instance with a stable identifier (catalogue
hash plus scope hash, or catalogue ID plus invocation timestamp,
depending on whether content-addressed identifiers are used).
Kquery instances inhabit the kind `K`; closure-check kquery
instances are a sub-kind `X ⊆ K` per Definition 14.1. Therefore
`ClosureKQ(K, ◇C) ∈ X ⊆ K ⊆ C`. ∎

**Lemma 14.4 (Finite presentability of the scope).**
For any catalogue admitting a finite `Kinds` set, the scope `◇C`
is finitely presentable: it is the union over `Kinds` of the cells
of each kind currently catalogued, and `Kinds` itself is finite
and recorded as a refinement of `Q-supported-claims`.

*Proof sketch.* `Kinds` is finite by Definition 14.1. For each
`k ∈ Kinds`, the cells of kind `k` in `K` are enumerable from the
catalogue's tables in finite time. The union is finite. The
encoding of `Kinds` as a refinement of `Q-supported-claims` is
finite text. ∎

### 14.4 Main result

**Theorem 14.5 (Self-hosting closure).**
A catalogue `K` is self-hosting at scope `◇C` iff the runtime
invariant

```text
∀ c ∈ ◇C : IMPL(c) ⇔ CAT(c)
```

holds, where `◇C` includes the `Q-supported-claims` cell, the
`Q-bootstrap-closure` cell, and the `ClosureKQ(K, ◇C)` instance
itself.

Equivalently: `ClosureKQ(K, ◇C).gap = ∅` and
`Q-bootstrap-closure ∈ ClosureKQ(K, ◇C).11`.

*Proof sketch.* (⇒) Suppose `K` is self-hosting at `◇C` per
Definition 14.7. Then `ClosureKQ(K, ◇C).gap = ∅`: no `c ∈ ◇C`
has `IMPL(c) ≠ CAT(c)`. Equivalently `IMPL(c) ⇔ CAT(c)` for all
`c ∈ ◇C`. The cells `Q-supported-claims`, `Q-bootstrap-closure`,
and `ClosureKQ(K, ◇C)` are in `◇C` by Definition 14.7's clauses
(2) and (3) (and Lemma 14.3 for the third). The gap-empty
condition forces them into `11`.

(⇐) Suppose the runtime invariant holds. Then `gap = ∅` directly.
Conditions (2) and (3) of Definition 14.7 are satisfied because
`Q-supported-claims`, `Q-bootstrap-closure`, and
`ClosureKQ(K, ◇C)` are stipulated members of `◇C` and have
`IMPL = CAT = 1`: the closure check is implemented in
`bootstrap.py` and catalogued as `Q-bootstrap-closure`; the
scope is implemented as data in `theory.py` and catalogued as
`Q-supported-claims`; the closure instance is constructed at
runtime (Lemma 14.3) and its presence in the catalogue's
kquery-instance log is recorded as a side effect of evaluation.
Hence `K` is self-hosting at `◇C`. ∎

**Corollary 14.5.1 (Constructive content of failure).**
The proof of Theorem 14.5 is constructive: failure of the
invariant produces the witness sets `gap.10` (implicit structure
— implemented but not catalogued) and `gap.01` (promissory notes
— catalogued but not implemented). These sets are the precise
to-do list to restore self-hosting.

**Corollary 14.5.2 (Charter alignment).**
The charter is satisfied at every step of the closure check:
`ClosureKQ` is *constructible* (Definition 14.6); *reachable*
from any catalogue open (called from `__enter__`, § 14.5);
*observable* as the kquery's return value; *coverable* in that
every cell of `◇C` lands in exactly one of `11`, `10`, `01`, `00`,
and each cell carries a definite remediation semantics.

### 14.5 Implementation

The constructive content of Theorem 14.5 corresponds to a
five-file diff against the catalogue as currently lifted. Order
matters: each step's output is the next step's input.

**14.5.1.** `cells.py` *(new)*. Defines `Cell` as a tagged union
over the kinds of Definition 14.1. Each subtype carries a stable
identifier and the data its kind requires. The module exposes
`tag : Cell → Kinds` as a projection. `tag` is *not* consulted
by `kquery`; it is consulted by predicates that choose to be
kind-aware.

**14.5.2.** `theory.py` *(new)*. Declares the framework's
signature: the operations the framework offers, their arities,
and the equations they satisfy. This is *data*, not code — read
at runtime by `bootstrap.py`. Each entry corresponds to a Cell
with `IMPL = 1`. The file is the witness referent for `IMPL`.

**14.5.3.** `views.py` *(modified)*. The signature of `kquery`
widens from `kquery(A : O → 𝟚, B : O → 𝟚, U : Set[O])` to
`kquery(A : Cell → 𝟚, B : Cell → 𝟚, U : Set[Cell])`. Predicates
are required to be silent-as-False per Definition 14.2.
Existing object-level call sites are unaffected: object-level
predicates are level-blind in the trivial sense (they return `0`
on non-object cells). This step is typing-only — no behavioural
change.

**14.5.4.** `bootstrap.py` *(new)*. Computes `ClosureKQ` per
Definition 14.6. The single load-bearing line:

```python
result = kquery(IMPL, CAT, enumerate_supported_cells())
assert result['10'] == [] and result['01'] == [], (
    f"Self-hosting violated: "
    f"implicit={result['10']}, promissory={result['01']}"
)
```

`enumerate_supported_cells()` reads `Q-supported-claims` from the
catalogue (Definition 14.7, condition 3) and unions over the
kinds it lists. `IMPL` introspects `theory.py`; `CAT` queries
the catalogue's own tables.

**14.5.5.** `schema.sql` *(modified)*. Adds two bootstrap rows:

- `Q-supported-claims` — refinement enumerates the kinds in
  `◇C` (initially `{O, B, W, R, E, K, X}`; `A` and any future
  kinds added when their `IMPL` ships).
- `Q-bootstrap-closure` — refinement encodes the preservation
  theorem of Theorem 14.5 ("additive moves on `K` preserve
  `gap = ∅`").

Both are introduced via `catalogue-introduces` witnesses from the
framework itself.

**14.5.6.** `catalogue.py` *(modified)*.
`SymmetryCatalogue.__enter__` (and `__init__` for non-context
use) calls `bootstrap.check_closure()`, which raises
`SelfHostingViolation` on non-empty `gap`. The exception's
payload is `(gap.10, gap.01)` — Corollary 14.5.1's to-do list.

**14.5.7.** `tests/test_self_hosting.py` *(new)*. Opens an empty
catalogue and asserts the closure check passes. This is the
regression test for Theorem 14.5 itself.

The first run of step (14.5.4) on the existing codebase will
fail loudly. The failure message is the to-do list. The work to
reach a passing check is the work of cataloguing the framework's
own primitives — at minimum `Q-kfour`, `Q-witness`, `Q-refine`,
`Q-schema-extend`, `Q-introduce-break`, `Q-introduce-object`,
`Q-lineage`, plus `Q-bootstrap-closure` and `Q-supported-claims`
themselves — each with witnesses and a preservation theorem.

### 14.6 Counterexamples and boundaries

**Counterexample 14.6.1 (Under-promised scope).**
Let `K` declare `Q-supported-claims` listing only `{O, B}`. Then
`◇C ⊆ O ∪ B` and `ClosureKQ(K, ◇C)` may have empty gap while the
framework still uses (say) wedge audits implicitly. The catalogue
passes Theorem 14.5 *at the scope it claims*, but the scope it
claims under-describes its own operation. The remedy is forced
by the recursion clause: `Q-supported-claims` is itself in `◇C`,
so its under-promising surfaces when any actually-used kind has
`IMPL = 1, CAT = 0`. The boundary is not eliminated, but it is
*forced into the gap*, which is the strongest property the kquery
primitive can give.

**Counterexample 14.6.2 (Promissory note).**
Let `K` declare a kind `K_future` in `Q-supported-claims` for
which no `IMPL` exists yet. Then `gap.01` is non-empty (cells of
kind `K_future` are catalogued but not implemented). The closure
check fails, correctly diagnosing the catalogue as dishonest.
This is the intended behaviour of the check.

**Counterexample 14.6.3 (Non-fixed point under iteration).**
If `IMPL` and `CAT` were time-dependent — e.g., `IMPL` consulted
a remote service whose definition of "implemented" drifts — the
check could pass at time `t` and fail at `t + ε` without local
change to `K`. The framework forecloses this by requiring `IMPL`
and `CAT` to depend only on local state (`theory.py` as a file,
the catalogue's tables as a SQLite database). The fixed point is
then a fixed point of a *local* function and Theorem 14.5 is
robust under this restriction.

**Boundary 14.6.4 (Universal properties as cells).**
Universal properties (e.g., the freeness of the empty catalogue,
the uniqueness of factorizations through it) are addressable as
cells but stretch the `IMPL` predicate's semantics. `IMPL` for a
universal-property cell asks not "does a callable exist" but
"does the property hold over all possible inputs." A property
test serves as a finite witness, but property-test-passing is
weaker than universal-property-holding. A more careful treatment
splits `IMPL` into `IMPL_callable`, `IMPL_tested`, and
`IMPL_proved`, yielding three kqueries with progressively
stronger semantics. This section commits only to `IMPL_callable`,
and notes the others as a deliberate scope restriction recorded
in `Q-supported-claims`'s refinement.

**Boundary 14.6.5 (Strict vs. weak categorical structure).**
Theorem 14.5 assumes `IMPL` and `CAT` are equality predicates —
agreement is on the nose. If the framework moves to bicategorical
2-cells (e.g., wedge audits as 2-cells between schema-extensions
viewed as 1-cells), `IMPL` and `CAT` become
equality-up-to-coherent-2-cell predicates, and the kquery's `11`
cell admits non-identity coherence 2-cells as evidence. The
closure check becomes a 2-categorical pasting condition. This
section commits only to the strict 1-categorical reading; the
bicategorical lift is a separate construction.

**Boundary 14.6.6 (Adjacent constructions to avoid confusing).**
The closure check is *not* a fixed-point operator in the
denotational sense; it is a runtime invariant whose violation is
a refusal-to-start. It is *not* a soundness proof of the
catalogue's logic; it is an audit that the catalogue's syntactic
self-description matches its operational self-implementation. It
is *not* a totality check on the framework's coverage of its
domain; it is a totality check on the framework's coverage of
*itself*.

### 14.7 Related work within the project

Theorem 14.5 is the constructive content of three claims already
present in the project's documents.

`theory.md` § 9 (recursive schema-as-symmetry-breaks) gestures at
the framework cataloguing its own primitives but does not specify
what "sufficient" cataloguing looks like. Theorem 14.5 supplies
the criterion: the closure kquery has empty gap. The
"schema-itself-evolves-via-breaks" commitment (`methodology.md`,
"What's generalisable" item 8) is exactly the additive-only
schema discipline `IMPL` and
`CAT` are well-defined under (no drops, no renames — both
predicates remain stable as `Kinds` grows).

`theory.md` § 11 (convergence) names the moment when accumulated
breaks match the original request as snap-to-grid. Theorem 14.5
specializes this to the framework's reflexive case: snap-to-grid
*against itself* is the closure check passing. The framework
converges relative to `◇C` iff `ClosureKQ(K, ◇C).gap = ∅`.

`methodology.md` § 2 (and `theory.md` § 2) name the unit of
structural knowledge as a (partition, preservation-theorem) pair.
Theorem 14.5 *is* a (partition, preservation-theorem) pair
applied to the framework's own primitives: the partition is
`(IMPL, CAT)` over `◇C`; the preservation theorem is "additive
moves on `K` preserve `gap = ∅`." This is what
`Q-bootstrap-closure`'s refinement records.

The user-side governing charter is materialized at four points
in this section's construction:

- *Constructible:* `ClosureKQ` is defined as a kquery instance
  (Definition 14.6); the level-blind `kquery` is the construction
  primitive (Lemma 14.1).
- *Reachable:* the check is invoked from
  `SymmetryCatalogue.__enter__` (§ 14.5.6), making it reachable
  on every catalogue open.
- *Observable:* the four cells of `ClosureKQ` are the
  observation; the gap is the partial-failure observation.
- *Coverable:* the `00` cell of `ClosureKQ` covers cells the
  framework neither implements nor catalogues — *correctly
  absent*. The `01` and `10` cells cover the dishonesty types:
  implicit and promissory. The `11` cell covers honest
  commitments. No cell is uncovered.

The charter's contrapositive — *"if not coverable, it is not a
valid runtime distinction"* — is what licenses the framework to
refuse to start when `gap` is non-empty: any non-empty gap is a
distinction the framework asserts but cannot honestly cover, and
per the charter such distinctions are not valid.

### 14.8 Naming consequence

A naming question raised earlier in the lifting work has an
answer in this section. The candidate name `v4cat` reads as "the
category of V₄-equipped domain catalogues." Until Theorem 14.5
is operative — that is, until `bootstrap.py` exists,
`Q-bootstrap-closure` is in the schema, and
`ClosureKQ(K, ◇C).gap = ∅` for every shipped catalogue — the
second half of `v4cat` is a promissory note: the framework uses
V₄ but does not constitute (or self-host as) a category. After
Theorem 14.5 is operative, the framework is self-hosted at the
scope `Q-supported-claims` declares, and the name's second half
is delivered for that scope.

Until then, **`kfour`** is the honest name: it commits only to
V₄ as the read primitive at level 0, which the code already
delivers. **`v4cat`** becomes available at the moment the
regression test in § 14.5.7 passes against a catalogue whose
`Q-supported-claims` honestly enumerates the kinds the framework
operates with.

The renaming is not an act of nomination; it is a transition
triggered by a runtime invariant. The project does not name
itself — the closure check names it, by passing.

---

*See also: `methodology.md` (the operational design),
`tutorial.md` (LLM-friendly walk-through),
`examples.md` (domain templates), `README.md` (quick-start).*
