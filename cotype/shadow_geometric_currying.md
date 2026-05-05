# Shadow: geometric currying — edge as closed event-cell

**Tracking**: closed-fire trajectory entry at [v4cat-oss/v4cat#4](https://github.com/v4cat-oss/v4cat/issues/4); migration epic at [v4cat-oss/methodology#10](https://github.com/v4cat-oss/methodology/issues/10) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *DBE+RFS+S2G fire of 2026-05-05. Region **#8** of the
> [shadow-architecture lattice](https://github.com/v4cat-oss/methodology/blob/main/shadow-architecture.md#the-lattice),
> recognition-led. Algebraic anchor:
> [shadow_assertion_history_group.md](shadow_assertion_history_group.md).
> Names a new semantic substrate beneath the existing RISC
> projection ([shadow_risc_core.md](shadow_risc_core.md)).*

## Form

The existing v4cat treats an edge as a **typed relation row**:
validated against a catalogued edge-kind, dispatched to a
`witnesses` or `lineages` table by the kind's `target-type`,
recorded permissively via `INSERT OR IGNORE` (see
[`v4cat/src/v4cat/catalogue.py` lines 474–524](https://github.com/v4cat-oss/v4cat/blob/main/src/v4cat/catalogue.py#L474-L524)).

Geometric currying treats an edge as a **closed event-cell whose
boundary contains three role obligations** (source / kind /
target). The current permissiveness becomes *intentional* rather
than *accidental*; boundary closure becomes the load-bearing
semantic.

> **Decisive distinction.** The existing implementations treat an
> edge as a *typed relation assertion*. The geometric-currying
> implementation treats an edge as a *closed event-cell whose
> boundary contains three role obligations*.

This is a different semantic foundation. It does not change
v4cat's public RISC API in v0.x; it changes what's *underneath*
the API.

## Where realised

- **In this shadow**: documentation only. The substrate is
  named; the migration is named in seven per-repo promissory
  shadows (see "Migration plan" below).
- **In future v0.x fires**: a coordinated cross-repo migration
  rebases the existing edge implementation, the three carrier
  substrates, the catalogue source, the certification suite, and
  the reference carrier on the new substrate.

## Formal object definitions

Let `Id` be the universe of v4cat identities. Let the role set be:

```text
Role₃ = { source, kind, target }
```

An **edge-cell** is a tuple:

```text
e = ⟨s, k, t⟩ ∈ Id × Id × Id
```

but the tuple is not merely data — it determines a **boundary**:

```text
∂e = { ρ_source(e, s), ρ_kind(e, k), ρ_target(e, t) }
```

where each `ρ_r(e, x)` is a **role-binding event**:

```text
ρ_source(e, s) = "edge-cell e has source role filled by s"
ρ_kind(e, k)   = "edge-cell e has kind role filled by k"
ρ_target(e, t) = "edge-cell e has target role filled by t"
```

Three closure predicates:

```text
Closed₀(x)            x is closed as a 0-cell / node-like referent
ClosedRole(e, r, x)   role r of edge-cell e is closed by identity x
ClosedEdge(e)         saturated edge-cell e is closed
```

Two entailment rules:

**Role closure entails node closure.**

```text
ClosedRole(e, r, x)
─────────────────────
     Closed₀(x)
```

**Edge closure requires all three role closures.**

```text
ClosedRole(e, source, s)
ClosedRole(e, kind,   k)
ClosedRole(e, target, t)
─────────────────────────
   ClosedEdge(⟨s,k,t⟩)
```

No order is imposed among the three role closures. **Boundary
closure is unordered**; higher-path advancement is ordered only
*after* boundary closure.

## Dimensional time

The chronological-event-log intuition flattens too aggressively.
Geometric currying replaces it with **graded closure**:

```text
grade 0: close source / kind / target identities (0-cells)
grade 1: close role bindings of an edge-cell (1-horns)
grade 2: close saturated edge-cell (2-cell)
grade n+1: advance path containing the edge-cell
```

The ordering law:

> A higher-n path may not advance through a cell until the
> lower-n boundary of that cell is closed.

But within the lower boundary:

> Source, kind, target may close in any order.

The chronological order in any current event-log presentation
is a **vector traversal** of the closure geometry, not its
defining structure.

## Edge as curry construct

For the ternary edge constructor:

```text
Edge : Id × Id × Id → EventCell
```

the three role-oriented partials are:

```text
SourceGivenKindTarget(k, t) = { s | ClosedEdge(⟨s,k,t⟩) }
KindGivenSourceTarget(s, t) = { k | ClosedEdge(⟨s,k,t⟩) }
TargetGivenSourceKind(s, k) = { t | ClosedEdge(⟨s,k,t⟩) }
```

These are all referent universes. They feed into `kquery`:

```text
kqueryΩ(SourceGivenKindTarget(k,t), CataloguedSourcesFor(k,t))
kqueryΩ(KindGivenSourceTarget(s,t), ObservedKindsBetween(s,t))
```

So edge currying does not replace the existing curry-spec
currying ([`v4cat/src/v4cat/curry.py`](https://github.com/v4cat-oss/v4cat/blob/main/src/v4cat/curry.py)).
It gives `kquery` richer referent universes to compare. The two
curryings compose: edge-role currying produces referent
universes; curry-spec currying compares them under the V₄
coordinate chart.

## Contrast table

| Axis | Existing implementations | Geometric currying |
| --- | --- | --- |
| Edge meaning | Typed relation row | Saturated event-cell |
| Endpoint status | Often pre-validated (or assumed) by storage layer; v4cat's `edge()` is **accidentally** permissive (`INSERT OR IGNORE`, no FK enforcement) | Entailed as boundary obligations; permissiveness is *intentional* |
| `kind` field | Catalogued edge-kind dispatch key | Role occupant of edge-cell, itself introduced/closed like any other identity |
| Event log | Chronological append presentation | Path through closed cells; vector is only a traversal rendering |
| Currying | Mainly `kquery` / tension currying | Also edge-role currying: source/kind/target partials |
| Failure mode | Missing node / invalid FK / unknown kind | Open boundary / unclosed role / unsupported closure |
| Closure | Type-system + claim closure | Boundary closure plus type/claim closure |
| CISC interpretation | CISC redirects to RISC calls | CISC composes cell/horn closures before path advancement |

## New self-hosted vocabulary: HF-GeometricCurrying

The substrate names a new self-hosted framework. All entries are
ordinary v4cat nodes; per the carrier-vs-object discipline they
occupy node positions or edge-kind positions, never
first-class-property positions.

### 11 new node-kinds

```text
kind:Cell                a cell at any grade
kind:NodeCell            grade-0 cell (node-like 0-cell)
kind:EdgeCell            grade-2 cell with three role-boundaries
kind:RoleBinding         grade-1 role-binding event ρ_r(e, x)
kind:Boundary            collection of role-bindings forming a cell's ∂
kind:Path                an oriented traversal through closed cells
kind:PathStep            one step within a Path
kind:PathPresentation    a vector or chronological rendering of a Path
kind:PathSnapshot        a presentation pinned to a state-snapshot
kind:ClosureObligation   a not-yet-discharged closure requirement
kind:RoleHorn            a partial boundary (two of three roles closed)
```

### 17 new edge-kinds

```text
has-cell-kind                cell → cell-kind
has-boundary                 cell → boundary
has-role-binding             cell → role-binding
role-of-cell                 role-binding → cell (inverse)
role-name                    role-binding → role-token (source/kind/target)
role-occupant                role-binding → identity
source-role                  edge-cell → its source role-binding
kind-role                    edge-cell → its kind role-binding
target-role                  edge-cell → its target role-binding
boundary-of                  boundary → cell
closes-role                  closure-event → role-binding
closes-cell                  closure-event → cell
path-advances-through        path-step → cell
blocked-by-boundary          path-step → open boundary that prevents advance
presents-path                path-presentation → path
snapshot-of                  path-snapshot → path-presentation
projects-as-edge             closed edge-cell → its saturated edge projection
```

`framework_seed.sql` currently catalogues 21 edge-kinds; this
extends to **38** (21 + 17). The new edge-kinds are added; the
existing 21 are unchanged.

## New closure covers

Each cover names a `(Ω, A, B)` triple. **Cell orientation is
significant**: reversing the role of `A` and `B` swaps the `10`
and `01` cells. Each cover documents its orientation explicitly.

### Boundary-closure cover

For an edge-cell `e = ⟨s,k,t⟩`:

```text
Ω = required role bindings of e
A = role bindings observed/introduced
B = role bindings required by EdgeCell schema

kqueryΩ(A, B)
```

Cells (left=observed, right=required):

```text
11 = required and observed role binding
10 = observed but not required (extra role-binding; usually a bug)
01 = required but not observed (open boundary; closure obligation)
00 = in Ω but neither observed nor required
```

`01` empty ⟺ the edge-cell's boundary is closed.

### Cell-closure cover

```text
Ω = edge-cells in current path frontier
A = cells with closed boundary
B = cells marked closed

kqueryΩ(A, B)
```

Cells (left=boundary-closed, right=marked-closed):

```text
11 = boundary closed and cell marked closed
10 = boundary closed but cell not yet marked closed (derivation opportunity)
01 = cell marked closed without boundary evidence (unsupported closure claim)
00 = frontier cell neither boundary-closed nor marked closed (open frontier)
```

### Path-advancement cover

```text
Ω = cells scheduled for path P
A = cells closed
B = cells presented in P's vector / path rendering

kqueryΩ(A, B)
```

Cells (left=closed, right=presented):

```text
11 = presented and closed (honest)
10 = closed but not presented (silent closure)
01 = presented before closure evidence (presentation-without-substrate)
00 = scheduled but neither closed nor presented (unfilled frontier)
```

The path-advancement cover is the V₄ classifier the
[event-log gap shadow](shadow_event_log_gap.md) was missing —
see the next section.

## Path identity has its missing substrate

The
[event-log gap shadow](shadow_event_log_gap.md) (formerly
`shadow_event_log_gap.md`'s open promissory) records that v4cat
has no operation-log API satisfying the assertion-history-group
specification (record / replay / invert). The structural gap
isn't *just* the API — the gap was that **path identity** had
no defining primitive.

Closure-before-traversal supplies the primitive:

```text
A path is identified by its sequence of closed cells.
A vector is a presentation of that sequence.
Identity: two paths are the same if they traverse the same
          sequence of closed cells, in the same order, under the
          same orientation.
```

The path-advancement cover above is the V₄ classifier of
"closed vs presented", and the event log's `record / replay /
invert` operations become well-typed under it:

```text
record  := append a step (cell_id) to a path; precondition: cell is closed
replay  := re-derive the cell sequence from the closure history
invert  := reverse traversal under boundary closure (ordered
           because cells are 2-cells, but reversal is well-defined
           because each cell's three role closures are unordered)
```

The remaining work to close the event-log-gap is the **per-repo
migration** (especially v4cat-core: introducing the cell layer
and surfacing path operations as ISA verbs). The substrate is
named here; the API operationalisation is named in
[`shadow_geometric_currying_v4cat_refactor.md`](shadow_geometric_currying_v4cat_refactor.md).

## Disambiguation: "cell"

The word "cell" is now overloaded:

| Usage | Meaning | Where |
| --- | --- | --- |
| **kquery cell** | One of `00 / 01 / 10 / 11` — a coordinate of the V₄ chart | [`curry.py:104-110`](https://github.com/v4cat-oss/v4cat/blob/main/src/v4cat/curry.py#L104) (`CellReferent`) |
| **event cell** | A graded geometric object with a boundary | this shadow |

These are different. The kquery cell is a 2-bit coordinate
label; the event cell is a structural object with a boundary
and closure obligations. Both will coexist after the migration.

The migration recommends the rename:

```text
CellReferent (existing)  →  KqueryCellReferent
                            EventCellReferent (new)
                            RoleHornReferent (new)
                            BoundaryClosureReferent (new)
```

This rename lands in the v4cat-core sub-fire (see
[`shadow_geometric_currying_v4cat_refactor.md`](shadow_geometric_currying_v4cat_refactor.md)),
not here.

## The accidental permissiveness — surfaced

The existing `edge()` in
[`catalogue.py` lines 474–524](https://github.com/v4cat-oss/v4cat/blob/main/src/v4cat/catalogue.py#L474-L524)
issues `INSERT OR IGNORE` against the `witnesses` or `lineages`
table without enforcing foreign-key existence on `src` or `tgt`
(SQLite's `PRAGMA foreign_keys=OFF` is the default). An edge
to a non-existent node is silently recorded.

In the typed-relation reading, this is a **bug or laxity**. In
the geometric-currying reading, it is **the saturating-mode
half of the strict/saturating dichotomy**:

```text
saturating mode:
  edge() introduces source / kind / target as needed
  (boundary closure obligation discharged on first use)

strict mode:
  edge() emits residue if source / kind / target are not already
  closed
  (boundary closure obligation surfaces as residue)
```

The current behaviour is approximately *saturating-mode-without-
the-explicit-introduce*. The migration's v4cat-core sub-fire
(see promissory shadow) makes the saturating-vs-strict choice
explicit and adds the strict mode as an opt-in.

This recognition is **load-bearing**: it is the empirical
observation in the existing code that licenses the
geometric-currying reading as already-applicable, not as
hypothetical-future-semantics.

## Lattice classification

Region **#8** (DBE+RFS+S2G), recognition-led.

- **DBE**: forward design of the new substrate — 11 node-kinds +
  17 edge-kinds + boundary-closure law + 4 closure recognizers.
- **RFS**: regroups existing `EdgeReferent` as a saturated
  projection over closed edge-cells; regroups
  `shadow_event_log_gap.md`'s path-identity gap as having its
  missing substrate; regroups the accidental permissiveness as
  intentional saturating-mode.
- **S2G**: this file + 7 per-repo promissory shadows + the
  closure-trail update on `shadow_event_log_gap.md`.

### Discipline rule 6 (orbit-saturation) check

| Orbit | Position after this fire | Wrapper extracted? |
| --- | --- | --- |
| "geometric semantic substrate" | 1 (this fire) | no — orbit position 1, name without abstracting |
| "carrier-vs-projection regroupings" | 2 (carrier-vs-object discipline @ position 1; edge-as-cell-vs-edge-as-projection @ position 2) | no — below the C7 ≥3 threshold |
| "self-hosted vocabulary expansion" | n+1 (HF-GeometricCurrying joins the existing framework seed) | no — vocabulary is data, not abstraction |

A future "geometric currying for higher-cells" (n-ary edges,
2-cells whose boundaries are themselves cells) would be orbit
position 2 of "geometric semantic substrate". At three a
`CellFramework` wrapper would be RFS-eligible.

## Migration plan

The cross-repo migration is named here as **seven per-repo
promissory shadows** (one per repo affected), each catalogued as
its own future v0.x sub-fire. This mirrors the
agda2v4cat-Tier-3 + v4cat-octave-promissory conventions: one
shadow per future fire, so closure trails are clean.

| Sub-fire | Shadow |
| --- | --- |
| `gc-v4cat-core` | [shadow_geometric_currying_v4cat_refactor.md](shadow_geometric_currying_v4cat_refactor.md) |
| `gc-vcif-carrier` | [shadow_geometric_currying_vcif_carrier.md](shadow_geometric_currying_vcif_carrier.md) |
| `gc-vcif-rdf-carrier` | [shadow_geometric_currying_vcif_rdf_carrier.md](shadow_geometric_currying_vcif_rdf_carrier.md) |
| `gc-vcif-hlo-carrier` | [shadow_geometric_currying_vcif_hlo_carrier.md](shadow_geometric_currying_vcif_hlo_carrier.md) |
| `gc-agda2v4cat-permissive` | [shadow_geometric_currying_agda2v4cat_permissive.md](shadow_geometric_currying_agda2v4cat_permissive.md) |
| `gc-certify-checks` | [shadow_geometric_currying_certify_checks.md](shadow_geometric_currying_certify_checks.md) |
| `gc-octave-role-matrices` | [shadow_geometric_currying_octave_role_matrices.md](shadow_geometric_currying_octave_role_matrices.md) |

Recommended order: v4cat-core first (so the substrate is
operational), then carriers (vcif → vcif-rdf → vcif-hlo) in any
order, then catalogue source (agda2v4cat) + reference carrier
(v4cat-octave) + certification (v4cat-certify) in any order. The
order is recommended but not strict; sub-fires are cataloged
independently.

## The new formal invariant

> Every saturated edge assertion must be the projection of a
> closed edge-cell whose source, kind, and target role-boundaries
> are closed. No higher path may advance through an edge-cell
> until that cell is closed. The order in which the
> role-boundaries close is not semantically significant; only
> the closure of the boundary is significant.

Equivalently:

> `edge(s, k, t)` is not the primitive insertion of a relation
> row; it is the projection of the closed filler of the horn
> `{source=s, kind=k, target=t}`.

## Compact theorem shape

> Given identities `s, k, t`, the edge event `E(s, k, t)` is
> licensed iff there exists a closed role-boundary consisting of
> `source=s`, `kind=k`, and `target=t`. The saturated edge
> assertion is the projection of that closed event-cell. Any path
> containing `E(s, k, t)` may advance past it only after
> `E(s, k, t)` is closed. Since boundary closure is unordered,
> edge construction is geometrically curried by any of its three
> roles.

## Trace integrity

Prior structural content unchanged:

- The four-cell V₄ partition algebra ([`views.py:42-97`](https://github.com/v4cat-oss/v4cat/blob/main/src/v4cat/views.py#L42-L97))
  is unchanged. What changes is what referent universes feed it.
- The carrier-vs-object discipline is unchanged. The new
  self-hosted vocabulary nodes are nodes, not first-class
  properties.
- The existing 21 edge-kinds in `framework_seed.sql` are
  unchanged. The 17 new edge-kinds extend the seed; they don't
  replace.
- [shadow_risc_core.md](shadow_risc_core.md),
  [shadow_dual_representation.md](shadow_dual_representation.md),
  [shadow_kquery_universal_read.md](shadow_kquery_universal_read.md),
  [shadow_layered_stack.md](shadow_layered_stack.md) remain
  valid; this shadow names a *deeper substrate* beneath their
  RISC projection, not a replacement.
- [shadow_event_log_gap.md](shadow_event_log_gap.md) is annotated
  with a "Substrate update" pointer to this shadow; the gap
  itself remains promissory until the per-repo migration lands.

## Snap-to-grid check

User's request (with the load-bearing recognition surfaced
explicitly): *"Yes. This should be formalized as a new shadow,
because it changes the semantic substrate beneath the existing
RISC projection. ... The new thing is not 'edge as ternary
tuple.' The new thing is: edge as geometric curry cell."*

Cotype's entailment after this shadow lands:

> The v4cat-oss workspace's RISC projection is a *projection* of
> a richer geometric substrate in which edges are closed event-
> cells with three role-boundaries. The substrate is named by
> HF-GeometricCurrying (11 node-kinds + 17 edge-kinds +
> boundary-closure law + closure recognizers). The migration to
> realise the substrate across the seven distributions is named
> as seven sub-fires, each with its own promissory shadow. The
> path-identity primitive is supplied by closure-before-traversal,
> giving the previously-unsubstrated event-log gap its missing
> structural ground.

Snap valid. The fire produces a substrate-recognition + a clean
migration-design surface; the migration itself is paced over
seven follow-on fires.

## Slogan

```text
Current v4cat:
  edge writes a typed relation.

Geometric-currying v4cat:
  edge closes a boundary.

Current v4cat:
  nodes precede edges operationally.

Geometric-currying v4cat:
  edges entail their boundary nodes dimensionally.

Current v4cat:
  event log is mostly chronological presentation.

Geometric-currying v4cat:
  chronology is a path rendering of closure geometry.
```
