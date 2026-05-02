# Tutorial — a walk-through of the symmetry-break catalogue

This file is written for an LLM (or human) who's encountering the
catalogue framework for the first time, perhaps via the MCP server.
It walks through the methodology by *doing it* on a small synthetic
domain, with each step explained in terms of the framework's
primitives.

If you've read `methodology.md`, this is the operational
companion. If you haven't, this tutorial gives you enough to
operate the framework; circle back to `methodology.md` for the
design, `theory.md` for the foundations, or `README.md` for the
quick-start.

## Contents

1. [What this framework is for](#1-what-this-framework-is-for)
2. [The seven verbs and one classifier](#2-the-seven-verbs-and-one-classifier)
3. [Starting from empty](#3-starting-from-empty)
4. [Adding the first object and break](#4-adding-the-first-object-and-break)
5. [Witnessing](#5-witnessing)
6. [Lineage and inheritance](#6-lineage-and-inheritance)
7. [Refining](#7-refining)
8. [Lifecycle: defer / promote / boundary](#8-lifecycle-defer--promote--boundary)
9. [The Klein-four read primitive](#9-the-klein-four-read-primitive)
10. [The retroactive-attribution case](#10-the-retroactive-attribution-case)
11. [Detecting drift via wedge audits](#11-detecting-drift-via-wedge-audits)
12. [A small worked example](#12-a-small-worked-example)
13. [What to do next](#13-what-to-do-next)

---

## 1. What this framework is for

The catalogue framework helps you accumulate **named structural
distinctions about a domain**, with **witnesses** (objects that
exhibit those distinctions), **refinements** (what specifically
each object contributes), and **lineage** (descent relations
between objects).

It's appropriate when:

- You have a *domain* with multiple *objects* (processors,
  programming languages, cryptographic primitives, file systems,
  mathematical structures, schema migrations in an evolving
  database, ...).
- The objects have *structural distinctions* that aren't reducible
  to flat attributes — patterns that need names, not just labels.
- These distinctions accumulate over time; you can't enumerate
  them up-front.
- You want the structure to *survive context loss* — be queryable
  by future sessions, future contributors, future LLM agents.

The catalogue is *complementary*, not competitive, to other data
stores:

- Operational data (high-volume transactions, fixed schema, reads
  dominated by primary-key lookups) belongs in a CRUD database.
  The catalogue records the *structural decisions* that produced
  that schema, not its row-level data.
- Time-series telemetry belongs in a TSDB. The catalogue records
  the *categories of metric* and their preservation theorems, not
  the data points.
- Pure analytical workloads belong in a notebook or warehouse.
  The catalogue tracks the *structural primitives* the analysis
  depends on, not the analytic tables.

In fact the catalogue is the **structural dual of a CRUD database
schema**: a CRUD schema *is* a (partial, implicit) catalogue of
structural decisions — each table is an object kind, each
constraint is a `(partition, preservation-theorem)` pair, each
migration is a schema-evolution verb. The catalogue framework
makes that latent structure explicit and queryable. See
`theory.md` § 10 for the dual reading and `examples.md` § 11 for
a worked example of cataloguing your own database's schema.

The framework's payoff is that **structural identity is constituted
through witnessed traces** — once you've recorded the trace, the
catalogue derives global structure (originator, status, lineage
inheritance, drift) automatically and re-derivably as you add
more.

## 2. The seven verbs and one classifier

The framework's ISA is small. Seven mutation verbs:

| Verb                                      | Purpose                                              |
| ----------------------------------------- | ---------------------------------------------------- |
| `INTRODUCE`                               | Add a new object (break / spec / tension)            |
| `WITNESS`                                 | Record a typed edge from a spec to a break           |
| `REFINE`                                  | Annotate a (break, spec) edge with a named attribute |
| `DEFER`                                   | Mark a break as a deferred candidate                 |
| `PROMOTE`                                 | Promote a deferred break to active                   |
| `BOUNDARY`                                | Mark a break as a deliberate metamodel non-extension |
| `KIND.NEW` / `PREDICATE.NEW` / `AXIS.NEW` | Schema-evolution helpers (rare)                      |

And one read classifier:

| Verb     | Purpose                                                 |
| -------- | ------------------------------------------------------- |
| `KQUERY` | Klein-four classifier (every read decomposes into this) |

KQUERY classifies a universe `U` of items by their `(in A, in B)`
membership signature, returning four cells: `11`, `10`, `01`, `00`.
Every conventional read (filter, intersect, diff, coverage) is a
named selection from these four cells. Section 9 walks through it.

## 3. Starting from empty

Open a fresh catalogue:

```python
from v4cat import SymmetryCatalogue

cat = SymmetryCatalogue('/tmp/tutorial.db')
print(cat.all_breaks())   # → []
print(cat.all_objects())  # → []
```

Or via MCP:

```text
GET catalogue://breaks   → []
GET catalogue://objects  → []
```

The framework's schema is bootstrapped automatically (tables and
views created via `CREATE TABLE IF NOT EXISTS`), but no data is
populated. The catalogue is empty but functional.

## 4. Adding the first object and break

We'll model a small fictitious domain: a sequence of programming
languages with structural breaks.

### Add an object

```python
cat.introduce_object('alpha-lang', 'Alpha (a hypothetical language)',
                     year=1980,
                     attrs={'vendor': 'AlphaCorp',
                            'paradigm': 'imperative-typed'})
```

Or as an MCP tool call:

```text
introduce_object(
    id='alpha-lang',
    name='Alpha (a hypothetical language)',
    year=1980,
    attrs={'vendor': 'AlphaCorp', 'paradigm': 'imperative-typed'}
)
```

The framework's `introduce_object` signature is *minimal*: only
attributes that are load-bearing for framework views are
first-class arguments (`year` for tropical-MIN attribution,
`catalogue_order` for catalogue-introduction tracking,
`notes` for free-form annotation, `lineage` for descent edges).

Domain-specific attributes (`vendor`, `paradigm`, `data_bits`,
`hardness_assumption`, etc.) go in `attrs`, which populates the
`spec_attributes` table as `(spec_id, name, value)` triples.
Values are stored as strings; cast at query time.

The `year` is structurally significant — it's the temporal axis
along which originator queries derive (see `theory.md` § 3 and
§ 12).

### Add a break

```python
cat.introduce_break('L1', 'Static type system',
                    short_desc='compile-time type checking',
                    axes=['equivalential'])
```

The `axes` parameter classifies the break by the methodology's
universal axes (Spatial / Temporal / Parallel / Equivalential /
Eventual / Meta). A type system makes a *equivalence-mode*
commitment about state comparison, so `equivalential` is right.

Multiple axes are allowed: a break that commits to both spatial
and temporal axes is a *mixed-axis break* and surfaces in the
`mixed_breaks` view.

### Verify

```python
print(cat.all_breaks())
# → [{'number': 'L1', 'name': 'Static type system', 'status': 'active',
#     'originator_name': None, 'originated_year': None, ...}]
```

The break exists but has no originator yet — no spec has witnessed
it. Section 5 fixes that.

## 5. Witnessing

A *witness* is a typed edge from a spec to a break. Recording a
witness is how we say "this object exhibits this break in this
specific way."

### Witness kinds

The framework admits eleven witness kinds:

| Kind                   | Meaning                                              |
| ---------------------- | ---------------------------------------------------- |
| `origin`               | chronologically first articulator                    |
| `catalogue-introduces` | catalogue's first analysis of this break             |
| `confirms`             | additional witness; no structural change             |
| `refines`              | extends with new attributes / cardinality            |
| `first-witness`        | concrete instance of a previously-deferred break     |
| `precedes`             | surfaces an abstract pattern at a different scope    |
| `cross-vendor`         | independent confirmation in another lineage          |
| `inherits`             | successor retains an ancestor's contribution         |
| `deferred-candidate`   | named the candidate but not yet adopted              |
| `sibling-boundary`     | deliberate metamodel non-extension                   |
| `gates-with-fault`     | reveals structural inadequacy                        |

The vocabulary isn't arbitrary; each kind has documented semantics
that the views consume (e.g., `break_status` looks for
`sibling-boundary` and `deferred-candidate`; `break_origin` looks
for `origin` and `catalogue-introduces`).

### Record a witness

```python
cat.witness('alpha-lang', 'L1', 'origin')
cat.witness('alpha-lang', 'L1', 'catalogue-introduces',
            notes='First spec to introduce static typing in our catalogue')
```

The same spec can have multiple witnesses on the same break with
different kinds. `origin` and `catalogue-introduces` are commonly
paired.

### See the originator emerge

```python
print(cat.origin('L1'))
# → {'break_number': 'L1', 'break_name': 'Static type system',
#    'originator_id': 'alpha-lang', 'originator_name': 'Alpha (a hypothetical language)',
#    'originated_year': 1980}
```

The originator wasn't *stored* — it was *derived* from the witness
graph. The view's tropical query: `MIN(year)` over witnesses with
kind in `('origin', 'catalogue-introduces')`.

This is the methodology's central commitment in action: **global
structure is always derived, never imposed.**

## 6. Lineage and inheritance

Many domains have descendant relations between objects. Programming
languages descend from each other; processors do too. The catalogue
records descent as edges in the `lineages` table.

### Add a descendant

```python
cat.introduce_object('beta-lang', 'Beta (descendant of Alpha)',
                     year=1985,
                     attrs={'vendor': 'AlphaCorp',
                            'paradigm': 'imperative-typed-with-rows'},
                     lineage=[('alpha-lang', 'descended-from')])
```

The `lineage` parameter is a list of `(ancestor_id, kind)` pairs.
`'descended-from'` is the canonical kind; others (`'inherits-from'`,
`'family-member'`) are admitted but not transitively closed by
default.

### Query the lineage chain

```python
print(cat.lineage('beta-lang'))
# → [{'descendant': 'beta-lang', 'ancestor': 'alpha-lang', 'depth': 1, ...}]
```

The view `lineage_ancestry` does transitive closure. If beta-lang
had its own descendants, they'd see beta-lang at depth 1 and
alpha-lang at depth 2.

### Inherited breaks

Breaks witnessed by an ancestor automatically apply to descendants
(structurally — they're inherited via the lineage chain):

```python
print(cat.inherited_breaks('beta-lang'))
# → [{'break_number': 'L1', 'break_name': 'Static type system',
#     'via_ancestor': 'alpha-lang', 'depth': 1}]
```

beta-lang inherits L1 from alpha-lang. If beta-lang has its own
witness on L1 (e.g., `kind='refines'`), that's separate — the
inherited record shows the ancestor's contribution.

## 7. Refining

A *refinement* annotates a (break, spec) edge with a named
attribute. Use refinements when a spec doesn't introduce a new
break but extends an existing one with specific structure.

### Add a witness with refinement

```python
cat.witness('beta-lang', 'L1', 'refines',
            notes='Adds row polymorphism')
cat.refine('L1', 'beta-lang', 'row-polymorphism',
           description='Records can be subtyped by row width')
cat.refine('L1', 'beta-lang', 'higher-rank',
           description='Polymorphism crosses function arrows')
```

Multiple refinements per (break, spec) are admitted. They're stored
in the `refinements` table; query with:

```python
print(cat.refinements_for_break('L1'))
# → [{'name': 'row-polymorphism', 'spec_id': 'beta-lang', ...},
#    {'name': 'higher-rank',       'spec_id': 'beta-lang', ...}]
```

### Refinements vs witnesses

The distinction:

- A `witness` is the *typed edge* (here: `beta-lang refines L1`).
- A `refinement` is the *named annotation* on that edge (here:
  `row-polymorphism` and `higher-rank`).

Witness records *that* something happened; refinement records
*what specifically* was added. Both are needed for a complete
record.

## 8. Lifecycle: defer / promote / boundary

Sometimes a break is *named* but not *structurally adopted*:

- Alpha mentions a structural pattern but doesn't fully exercise
  it.
- We name the pattern in the catalogue as a *deferred candidate*.
- Later, beta exercises the pattern concretely. We *promote* the
  break.

### Defer

```python
cat.introduce_break('L2', 'Lazy evaluation',
                    axes=['temporal'])
cat.witness('alpha-lang', 'L2', 'catalogue-introduces')
cat.defer('L2', by='alpha-lang',
          reason='alpha-lang names the pattern but doesn\'t implement it')
print(cat.status('L2'))   # → 'deferred'
```

`defer` writes a witness with `kind='deferred-candidate'`. The
`break_status` view detects this and reports `'deferred'` — *unless*
there's a confirms/origin witness from a *different* spec (which
would mean the break has been promoted).

### Promote

When another spec exercises the pattern concretely:

```python
cat.witness('beta-lang', 'L2', 'first-witness',
            notes='Implements lazy thunking with sharing')
cat.promote('L2', by='beta-lang', reason='Concrete instance arrived')
print(cat.status('L2'))   # → 'active'
```

`promote` writes a witness with `kind='confirms'` from a different
spec; the status view re-derives to `'active'`.

### Boundary

Some breaks are deliberately *not* extended into the framework.
The `boundary` verb marks them as sibling-framework non-extensions:

```python
cat.introduce_break('L3', 'Effect system',
                    axes=['temporal', 'equivalential'])
cat.boundary('L3',
             reason='Effect systems live in a sibling framework; '
                    'not adopted into this metamodel',
             by='alpha-lang')
print(cat.status('L3'))   # → 'sibling-boundary'
```

This is rare. The processor catalogue uses it once (Q81 — multi-CPU
shared-memory architectures live in a sibling framework rather
than extending the per-spec metamodel).

## 9. The Klein-four read primitive

`KQUERY` is the framework's only primitive read. Every other
read — filter, intersect, diff, coverage — is sugar over KQUERY
plus a cell selection.

### The classifier

```text
KQUERY(A, B; U)  classifies every x ∈ U by its (in A, in B) signature

                B = 0           B = 1
            ┌────────────┬─────────────┐
   A = 0   │  00 BLIND  │  01 RIGHT   │
            ├────────────┼─────────────┤
   A = 1   │  10 LEFT   │  11 AGREE   │
            └────────────┴─────────────┘
```

### Default behaviour

```python
from v4cat import kquery

kquery(['a', 'b', 'c'], ['b', 'c', 'd'])
# → {'00': [],
#    '01': ['d'],
#    '10': ['a'],
#    '11': ['b', 'c']}
```

When `universe` isn't specified, it defaults to `A ∪ B` — which
collapses the `00` cell to empty.

### Bounded universe surfaces shared blindness

```python
kquery(['a', 'b'], ['b', 'c'],
       universe=['a', 'b', 'c', 'd', 'e'])
# → {'00': ['d', 'e'],   # ← shared blindness
#    '01': ['c'],
#    '10': ['a'],
#    '11': ['b']}
```

The `00` cell records *items in the universe absent from both A
and B*. Most diff tools erase this; the methodology elevates it
as a structural object (see `theory.md` § 4).

### Named selections

Conventional reads are named cell-selections:

```python
from v4cat import wedge, agree, blind, coverage

# Wedge: the symmetric residue (cells 10 + 01)
wedge(['a', 'b'], ['b', 'c'])
# → {'in_a_not_b': ['a'], 'in_b_not_a': ['c'], 'in_both': ['b']}

# Agree: intersection (cell 11)
agree(['a', 'b'], ['b', 'c'])
# → ['b']

# Blind: shared absence (cell 00) relative to a universe
blind(['a', 'b'], ['b', 'c'], ['a', 'b', 'c', 'd'])
# → ['d']

# Coverage: union over the universe (cells 10 + 01 + 11)
coverage(['a', 'b'], ['b', 'c'])
# → ['a', 'b', 'c']
```

### Equivalence-class normalisation

`KQUERY` accepts a `normalize` callable that pre-applies to each
universe element:

```python
kquery(['Q89', 'Q90'], ['q89', 'Q91'], normalize=str.upper)
# → {'00': [], '01': ['Q91'], '10': ['Q90'], '11': ['Q89']}
```

`'Q89'` and `'q89'` agree under case-folding. Useful for
identifier canonicalisation, lineage projection, etc.

### Why the four-cell view matters

A KQUERY isn't just a richer diff. It's a *complete classification*
of the universe. Every conventional read selects from these four
cells. The methodology's commitment is that you should always have
all four available — not just the two that conventional diff tools
expose.

This is most useful for *structural-consistency checks*. Example:
"Of all specs that have frame_format declared (universe), which are
paged (A), and which have restart-suitable frames (B)?" The cell
breakdown tells you:

- `11` — paged AND restart-suitable: virtual memory works.
- `10` — paged but not restart-suitable: Q92 violation.
- `01` — restart-suitable but not paged: pre-VM specs (fine).
- `00` — neither: structurally interesting (e.g., 80286).

## 10. The retroactive-attribution case

This is the methodology's central demonstration. Watch what happens
when you add a chronologically-earlier object to a break that's
already attributed.

### Setup

```python
cat = SymmetryCatalogue(':memory:')
cat.introduce_object('newer', 'Newer (1990)', year=1990)
cat.introduce_break('Q-test', 'Test break', axes=['spatial'])
cat.witness('newer', 'Q-test', 'origin')
cat.witness('newer', 'Q-test', 'catalogue-introduces')

print(cat.origin('Q-test'))
# → {'originator_name': 'Newer (1990)', 'originated_year': 1990, ...}
```

### Add an earlier object

```python
cat.introduce_object('older', 'Older (1980)', year=1980)
cat.witness('older', 'Q-test', 'origin')   # ← just an additional witness

print(cat.origin('Q-test'))
# → {'originator_name': 'Older (1980)', 'originated_year': 1980, ...}
```

The originator changed automatically. No `RETRO` verb. No
correction step. The view's `MIN(year)` over `origin`-class
witnesses naturally picked up the earlier year.

### What didn't change

```python
print(cat.first_seen('Q-test'))
# → {'first_seen_at_name': 'Newer (1990)', 'first_seen_year': 1990, ...}

print(cat.retroactive_gap('Q-test'))
# → 10  (1990 - 1980)
```

`first_seen` still points to `newer` (because `catalogue-introduces`
is still on `newer`). The retroactive gap is `first_seen.year -
origin.year = 10`.

### Why this matters

This is the trace-thickening pattern (see `theory.md` § 11). The
prior reading wasn't *false* — it was what the trace-set then
licensed. The new reading isn't a *correction* — it's what the
trace-set *now* licenses. Both are valid relative to their
trace-sets.

The catalogue's value comes from being able to keep adding witnesses
without ever invalidating prior derivations. *History is preserved
by trace-thickening, not by versioning.*

## 11. Detecting drift via wedge audits

When the catalogue has multiple representations (prose + SQL,
annotated source code + structured data, prior version + current
version), they can drift apart. Wedge audits surface drift.

### A simple wedge

Suppose you have two source-of-truth claims:

```python
prose_breaks = ['Q74', 'Q75', 'Q76', 'Q89', 'Q-x']      # from prose doc
sql_breaks   = ['Q74', 'Q75', 'Q76', 'Q89', 'Q-y']      # from SQL

from v4cat import wedge
result = wedge(prose_breaks, sql_breaks)
# → {'in_a_not_b': ['Q-x'],   # ← prose mentions Q-x; SQL doesn't
#    'in_b_not_a': ['Q-y'],   # ← SQL has Q-y; prose doesn't
#    'in_both':    ['Q74', 'Q75', 'Q76', 'Q89']}
```

The drift is real and named. Either:

- prose mentions Q-x but it was never structurally adopted (delete
  from prose, or run `introduce_break('Q-x', ...)` to add)
- SQL has Q-y but prose doesn't reflect it (update prose)

Either way, the audit surfaces something to address.

### Bounded-universe drift

Sometimes drift is more subtle: items in the *universe of
discourse* that *neither* representation mentions.

```python
all_breaks_we_care_about = ['Q74', 'Q75', 'Q76', 'Q89', 'Q90', 'Q91',
                             'Q92', 'Q93']

from v4cat import kquery
result = kquery(prose_breaks, sql_breaks,
                universe=all_breaks_we_care_about)
# → {'00': ['Q90', 'Q91', 'Q92', 'Q93'],   # ← SHARED BLINDNESS
#    '01': ['Q-y'],
#    '10': ['Q-x'],
#    '11': ['Q74', 'Q75', 'Q76', 'Q89']}
```

The 00 cell tells you *both representations are missing four
breaks* that the universe of discourse expects. This is information
that ordinary diff hides.

### Audit a representation against the catalogue

A common application: audit a prose document against the live
catalogue.

```python
mentioned_in_prose = parse_prose_for_break_numbers('my_doc.md')
in_catalogue       = [b['number'] for b in cat.all_breaks()]

result = wedge(mentioned_in_prose, in_catalogue)
print(f"In prose but missing from catalogue: {result['in_a_not_b']}")
print(f"In catalogue but missing from prose: {result['in_b_not_a']}")
```

The MCP server's `audit_md_vs_sql` prompt automates this for the
common case.

## 12. A small worked example

Let's tie it all together with a small linguistic-domain example.
Three fictitious programming languages, two breaks, lineage,
refinements, and the retroactive-attribution case.

### Setup

```python
from v4cat import SymmetryCatalogue, kquery

cat = SymmetryCatalogue('/tmp/lang-tutorial.db')
```

### Introduce objects with year + lineage

```python
cat.introduce_object('alpha-lang', 'Alpha', year=1980,
                     attrs={'vendor': 'AlphaCorp'})

cat.introduce_object('beta-lang', 'Beta',  year=1985,
                     attrs={'vendor': 'AlphaCorp'},
                     lineage=[('alpha-lang', 'descended-from')])

cat.introduce_object('gamma-lang', 'Gamma', year=1990,
                     attrs={'vendor': 'AlphaCorp'},
                     lineage=[('beta-lang', 'descended-from')])
```

### Introduce two structural breaks

```python
cat.introduce_break('LANG-A', 'Static type system',
                    axes=['equivalential'])
cat.introduce_break('LANG-B', 'Lazy evaluation',
                    axes=['temporal'])
```

### Witness contributions

```python
# alpha-lang originated static typing
cat.witness('alpha-lang', 'LANG-A', 'origin')
cat.witness('alpha-lang', 'LANG-A', 'catalogue-introduces')

# beta-lang refined static typing with row polymorphism
cat.witness('beta-lang', 'LANG-A', 'refines')
cat.refine('LANG-A', 'beta-lang', 'row-polymorphism',
           description='Records can be subtyped by row width')

# beta-lang originated lazy evaluation
cat.witness('beta-lang', 'LANG-B', 'origin')
cat.witness('beta-lang', 'LANG-B', 'catalogue-introduces')

# gamma-lang inherits both from its lineage
# (no explicit witness needed; inherited_breaks() picks them up
# via lineage closure)

cat.commit()
```

### Read the derived structure

```python
# Originator queries (tropical MIN-year over origin-class)
print(cat.origin('LANG-A'))
# → originator: alpha-lang, year: 1980

print(cat.origin('LANG-B'))
# → originator: beta-lang, year: 1985

# Lineage chain
print(cat.lineage('gamma-lang'))
# → [{'ancestor': 'beta-lang',  'depth': 1, ...},
#    {'ancestor': 'alpha-lang', 'depth': 2, ...}]

# Inherited breaks (transitive)
print(cat.inherited_breaks('gamma-lang'))
# → [{'break_number': 'LANG-A', 'via_ancestor': 'beta-lang',  'depth': 1, ...},
#    {'break_number': 'LANG-B', 'via_ancestor': 'beta-lang',  'depth': 1, ...},
#    {'break_number': 'LANG-A', 'via_ancestor': 'alpha-lang', 'depth': 2, ...}]
```

### Now add a retroactive ancestor

Suppose later research reveals that an even-earlier language,
`proto-lang` (year 1975), introduced static typing first. We
*don't* correct alpha-lang's witness; we *add* a new origin
witness:

```python
cat.introduce_object('proto-lang', 'Proto', year=1975,
                     attrs={'vendor': 'ProtoCorp'})

cat.witness('proto-lang', 'LANG-A', 'origin',
            notes='Discovered in archival research')
cat.commit()

print(cat.origin('LANG-A'))
# → originator: proto-lang, year: 1975  ← changed automatically

print(cat.first_seen('LANG-A'))
# → first_seen_at: alpha-lang  ← unchanged

print(cat.retroactive_gap('LANG-A'))
# → 5  (1980 - 1975)
```

The catalogue thickened forward. Prior readings remain valid
relative to their trace-sets; the current reading derives from the
current trace-set.

### A KQUERY audit

Suppose someone claims our catalogue should also cover
`call-by-need-evaluation` (which is structurally a flavour of
LANG-B). Wedge that:

```python
expected_breaks    = ['LANG-A', 'LANG-B', 'LANG-call-by-need']
catalogue_breaks   = [b['number'] for b in cat.all_breaks()]

result = kquery(catalogue_breaks, expected_breaks)
print(f"In catalogue but not expected: {result['10']}")  # → []
print(f"Expected but missing:          {result['01']}")  # → ['LANG-call-by-need']
print(f"Both:                          {result['11']}")  # → ['LANG-A', 'LANG-B']
```

The drift is named. Decision: either treat
`call-by-need-evaluation` as a refinement of LANG-B (call
`refine('LANG-B', 'beta-lang', 'call-by-need-variant', ...)`) or
introduce it as a separate break.

## 13. What to do next

You've now operated every primitive in the framework. The natural
follow-ups:

- **Read `methodology.md`** — the full design, including the MCP
  server's tools/resources/prompts.
- **Read `theory.md`** — the foundations: shadow architecture,
  temporal axis, Klein-four core, Yoneda + Derrida, magma +
  pointfree topology, recursive schema, convergence, trace-
  thickening.
- **Read `examples.md`** — domain templates beyond processors.
- **Look at the parent repo's `symmetries.md` and
  `symmetries.sql`** — the processor catalogue is the framework's
  most extensively-developed application. ~24 specs, ~53 named
  breaks, full retroactive-attribution example, Q92 consistency
  rule.
- **Explore the MCP resources**:
  - `catalogue://breaks` — inventory
  - `catalogue://retroactive` — retroactive cases
  - `catalogue://q92_violations` — paged-spec consistency
  - `catalogue://lineages/{id}` — descent chain
  - `catalogue://docs` — list of available documentation

The framework's value compounds the more you put into it. A
catalogue with 5 objects is informative; with 50 it surfaces
patterns; with 500 it converges into a metamodel for the domain.

---

*See also: `methodology.md` (operational design),
`theory.md` (foundations), `examples.md` (domain templates),
`README.md` (quick-start).*
