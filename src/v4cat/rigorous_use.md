# v4cat — Rigorous use

> *Grade: operating covenant.
> Companion to [methodology.md](methodology.md) (the operational design)
> and [python_api.md](python_api.md) (the Python API discipline).
> Read this when you want to use v4cat **as rigorously as v4cat
> uses itself**.*

To use `v4cat` as rigorously as `v4cat` uses itself, treat every catalogue as needing its own **self-hosting analogue**.

The core rule:

```text
Nothing important may remain merely said.

It must be one of:
  node,
  edge,
  kquery,
  named tension,
  explicit projection,
  declared out-of-scope residue.
```

Or, in the system's own shape:

```text
Every serious use of v4cat should define its own:

  IMPL-like side:      what the domain artifact actually contains
  CAT-like side:       what the catalogue claims it contains
  ◇C-like scope:       the bounded universe of accountable claims
  ClosureKQ-like read: the V₄ comparison of the two
```

## 1. Always begin by declaring the universe `U`

The most important practical discipline is: **never run a meaningful `kquery` without knowing what universe it is over.**

A `kquery(A, B)` without `U` can still compare visible material, but it cannot make the `00` cell epistemically meaningful.

The rigorous form is:

```text
Given:
  U = bounded universe of accountable items
  A = left observer / left representation / implementation predicate
  B = right observer / right representation / catalogue predicate

Return:
  χ₍A,B₎ : U → V₄
```

where:

```text
11 = U ∩ A ∩ B
10 = U ∩ A ∩ ¬B
01 = U ∩ ¬A ∩ B
00 = U ∩ ¬A ∩ ¬B
```

So before cataloguing a domain, write a small **scope charter**:

```text
This catalogue is accountable for:
  - these object classes
  - these break classes
  - these witness kinds
  - these source classes
  - these comparison axes
  - these named projections

This catalogue is not accountable for:
  - ...
```

If there is no bounded `U`, the `00` cell is not a blind spot; it is just an unearned absence.

## 2. Treat every claim as requiring a carrier

When you say:

```text
X originated Y.
X refines Y.
X confirms Y.
X inherits Y.
X is a better attribution than Z.
This document supports that break.
This break is active.
This concern is resolved.
```

ask immediately:

```text
What is the node?
What is the edge?
What is the witness kind?
What query would observe this?
What gap would falsify it?
```

A rigorous v4cat use should not contain important free-floating prose such as:

```text
Rust refines the C++ ownership model.
```

It should become something like:

```text
object: Rust
object: C++
break: affine/ownership discipline
edge: Rust --origin/confirms/refines--> break
edge: C++ --prior-art/contrast/boundary--> break
kquery: Rust ownership witnesses vs C++ ownership witnesses over declared U
```

The sentence can remain in a report, but the report should be a rendering of the catalogue, not the place where the claim lives.

## 3. Never collapse `10` and `01` silently

The most common misuse will be treating `kquery` as ordinary diff.

That loses the thing v4cat exists to preserve.

Bad:

```text
A differs from B by {x, y, z}.
```

Better:

```text
A-left residue:  {x, y}
B-right residue: {z}
shared seen:     {...}
shared blind:    {...}
```

You may project:

```text
10 ∪ 01
```

but the projection must be named.

For example:

```text
ordinary_diff = 10 ∪ 01
agreement     = 11 ∪ 00
coverage      = 11 ∪ 10 ∪ 01
left_claims   = 11 ∪ 10
right_claims  = 11 ∪ 01
```

A projection is a quotient. In v4cat usage, quotienting should be explicit, named, and preferably catalogued as a tension or view.

## 4. Use `kquery` at every boundary

v4cat uses `kquery` to audit itself. You should use it to audit every serious boundary in the domain.

Good comparison pairs include:

```text
implementation claims     vs catalogue claims
documentation claims      vs schema facts
test coverage             vs declared ISA
paper claims              vs artifact behavior
README claims             vs tutorial claims
historical attribution    vs evidence attribution
old catalogue snapshot    vs new catalogue snapshot
LLM-produced summary      vs source-backed witness graph
domain extension schema   vs generic framework contract
```

For each boundary, define:

```text
U = accountable claim universe
A = source 1 predicate
B = source 2 predicate
χ = kquery(A, B; U)
```

Then inspect all four cells.

The rigorous report form is:

```text
11: aligned claims
10: source-A-only residue
01: source-B-only residue
00: declared-scope blind spot
projection used: if any
action taken: promote / defer / boundary / refine / out-of-scope
```

## 5. Promote only by witness, not by confidence

A candidate break should not become active because it "feels right."

Use a promotion ladder:

```text
candidate
  → deferred-candidate
  → boundary
  → confirms
  → origin/refines/inherits/etc.
```

A practical rule:

```text
No break may be promoted unless there is:
  1. a named partition or distinction,
  2. at least one positive witness,
  3. at least one boundary or contrast witness,
  4. a query that would observe its absence or misclassification.
```

This prevents the catalogue from becoming a bag of attractive abstractions.

## 6. Do not store derived facts as primary facts

v4cat is already disciplined about this: origin, first-seen, retroactive gap, status, and lineage-derived views should be queried, not hand-written as authoritative facts.

Follow the same rule in domain use.

Do not store:

```text
originator = X
status = retroactive
Y inherited break Z
```

unless the system requires a cache.

Instead store:

```text
X --origin--> break
Y --inherits/descended-from--> X
catalogue-introduces edge
year/version/publication axis
```

Then derive the attribution.

A rigorous catalogue is not a notebook of conclusions. It is a graph from which conclusions are reproducible.

## 7. Treat every CISC convenience as suspicious until reduced

If you add a new verb, view, report, MCP tool, or workflow, ask:

```text
Does this reduce to introduce_node, edge, and kquery?
```

If yes, document the reduction.

If no, classify it honestly:

```text
risc primitive
cisc sugar
schema substrate
bootstrap/meta root
external effect
unsafe convenience
```

Do not let new verbs quietly become new foundations.

For example:

```text
"mark_resolved"
```

should probably not be primitive. It should reduce to something like:

```text
edge(tension, resolution_witness, kind="resolved-by")
kquery(prior_gap, current_gap, U=declared_scope)
```

A resolution is not a flag. It is an observed change in a comparison cover.

## 8. Make extensions additive, idempotent, and checkable

Every domain extension should behave like a disciplined schema migration.

A rigorous extension should satisfy:

```text
additive:
  it does not rewrite the generic framework meaning

idempotent:
  loading twice does not duplicate facts or corrupt state

typed:
  new tables/views correspond to declared node/edge/witness kinds

observable:
  its claims appear in some closure or consistency query

reversible in interpretation:
  even if SQL migration is not reversible, the semantic delta is named
```

Minimum extension checklist:

```text
CREATE TABLE IF NOT EXISTS ...
CREATE VIEW IF NOT EXISTS ...
INSERT OR IGNORE ...
declared new breaks
declared witness kinds
declared tensions
post-load closure check
domain-specific kquery audit
```

If an extension cannot explain how its new structure is visible through `kquery`, it is probably not yet v4cat-native.

## 9. Use tensions as named reusable reads

Do not let important queries remain ad hoc SQL.

If a query matters repeatedly, turn it into a named tension.

A tension should say:

```text
name:
  what structural concern or utility this read addresses

disposition:
  concern / utility / diagnostic / audit

left predicate:
  what A means

right predicate:
  what B means

universe:
  what U means

projection:
  whether the full V₄ cover is preserved or projected

resolution:
  what action each non-empty cell implies
```

This is how you prevent "analysis" from drifting away from the catalogue.

## 10. Preserve the arrow, not just the result

The most rigorous category-theoretic usage is to treat each comparison as an object:

```text
χ₍A,B₎ : U → V₄
```

Then reports, views, refinements, and summaries are morphisms or projections of that arrow.

So instead of saying:

```text
The result is this set.
```

say:

```text
This set is the 10-fiber of χ₍A,B₎ over U.
```

Instead of saying:

```text
We summarized the gap.
```

say:

```text
We projected χ through q_gap : V₄ → 𝟚, where 10 and 01 map to 1.
```

This is the discipline that keeps the arrow-category reading real rather than decorative.

## 11. For literature or prior-art work, use v4cat as a four-cell audit machine

For a paper, system, method, or invention claim, define:

```text
U = claim universe
A = claims made by the artifact
B = claims supported by literature
```

Then:

```text
11 = artifact claims with literature support
10 = artifact-only claims: possible novelty or overclaim
01 = literature-only claims: missed precedent
00 = scoped but untreated claim space
```

This is exactly the review shape you keep asking for:

```text
What is novel?
What is not novel?
What is supported?
What is unsupported?
What academic precedent exists?
What precedent did we miss?
```

v4cat can make that review shape mechanical.

## 12. Maintain a "no silent residue" rule

Every non-empty `10`, `01`, or `00` should end in one of a few actions:

```text
promote:
  turn residue into a confirmed break/witness

defer:
  preserve as candidate without claiming resolution

boundary:
  mark as contrastive edge requiring care

refine:
  split an overbroad break into sharper child breaks

exclude:
  explicitly remove from U with justification

extend:
  widen U because the blind spot exposed a bad scope

project:
  knowingly quotient the residue for a named purpose
```

The anti-rigorous move is to observe residue and then merely explain it away in prose.

## 13. Version the catalogue by comparison, not replacement

When the catalogue evolves, do not treat the new version as "the corrected one."

Compare snapshots:

```text
old catalogue claims vs new catalogue claims
old witness graph    vs new witness graph
old U                vs new U
old tensions         vs new tensions
```

The rigorous question is not:

```text
What changed?
```

but:

```text
Which V₄ fibers did the change move through?
```

For example:

```text
10 old-only:
  removed claims

01 new-only:
  added claims

11 stable:
  preserved claims

00 still blind:
  known scope not covered by either snapshot
```

That gives you a migration audit instead of a changelog.

## 14. Use reports as renderings, not sources of truth

A report should be generated from:

```text
nodes
edges
witnesses
tensions
kquery results
projection declarations
```

The report may be beautiful, but it should not be authoritative.

A rigorous report includes its own audit footer:

```text
source catalogue:
scope U:
queries rendered:
non-empty residues:
projections used:
unresolved 10:
unresolved 01:
unresolved 00:
```

This is how you keep prose subordinate to the graph without making the prose sterile.

## 15. The practical operating covenant

I would use this covenant every time:

```text
Before asserting a distinction, define its carrier.

Before comparing carriers, declare the universe.

Before reporting a result, preserve the four cells.

Before collapsing cells, name the quotient.

Before promoting a claim, attach a witness.

Before adding a verb, reduce it to the RISC core or classify it as meta/substrate.

Before trusting a catalogue, run its closure query.

Before publishing a conclusion, show which cell licensed it.
```

## The strongest single discipline

The strongest advice is this:

```text
Use v4cat by making every important statement answerable as:

  Which arrow χ : U → V₄ produced this?
  Which fiber of χ am I talking about?
  Which witness licenses the observer predicate?
  Which projection, if any, did I apply?
  What remains in 10, 01, and 00?
```

That is what it means to use v4cat as rigorously as v4cat uses itself.
