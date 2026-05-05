# Shadow: geometric currying — vcif-rdf carrier (promissory)

**Tracking**: [v4cat-oss/vcif-rdf#1](https://github.com/v4cat-oss/vcif-rdf/issues/1) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_geometric_currying.md](shadow_geometric_currying.md)).
> Region **#4** (S2G alone — pure cataloguing).*

## Form

`vcif-rdf` (the RDF/SHACL/SPARQL substrate column) currently
encodes edges using fixed carrier predicates:

```turtle
:e1 a vc:EdgeAssertion ;
   vc:source     :term1 ;
   vc:edgeKind   :hasKind ;
   vc:target     :kindDef .
```

This is the **compact saturated form**. Geometric currying
adds the explicit cell + role-binding form:

```turtle
:e1 a vc:CellAssertion ;
   vc:cellKind   :EdgeCell .

:rb1 a vc:RoleBinding ;
   vc:role       :source ;
   vc:occupant   :term1 ;
   vc:roleOfCell :e1 .

:rb2 a vc:RoleBinding ;
   vc:role       :kind ;
   vc:occupant   :hasKind ;
   vc:roleOfCell :e1 .

:rb3 a vc:RoleBinding ;
   vc:role       :target ;
   vc:occupant   :kindDef ;
   vc:roleOfCell :e1 .
```

The compact `vc:source / vc:edgeKind / vc:target` triples
**remain** as a SHACL-validated projection. The RDF carrier
gains the *underlying* cell shape; both shapes are accepted; the
validator enforces their consistency.

## What to extract

### New carrier predicates (carrier slots, fixed)

| New predicate | Type signature | Purpose |
| --- | --- | --- |
| `vc:cellKind` | `CellAssertion → NodeAssertion` | the cell's kind anchor (`EdgeCell`, `NodeCell`, …) |
| `vc:role` | `RoleBinding → NodeAssertion` | the role-token anchor (`source`, `kind`, `target`) |
| `vc:occupant` | `RoleBinding → NodeAssertion` | the identity filling the role |
| `vc:roleOfCell` | `RoleBinding → CellAssertion` | back-pointer from role-binding to its cell |
| `vc:closureState` | `CellAssertion → NodeAssertion` | one of `open`, `boundary-closed`, `closed` |

These are **carrier predicates**, not object-language nodes
(per the carrier-vs-object discipline in
[vcif-rdf/docs/spec.md][vcif-rdf-spec]). They join the existing
8 carrier slots (`vc:source`, `vc:edgeKind`, …).

[vcif-rdf-spec]: https://github.com/v4cat-oss/vcif-rdf/blob/main/docs/spec.md

### New carrier classes

```text
vc:CellAssertion        the full geometric edge
vc:RoleBinding          one of three role-bindings
```

Both are catalogued in `carrier.ttl` alongside the existing
`vc:NodeAssertion`, `vc:EdgeAssertion`, `vc:CoverAssertion`,
`vc:CellAssertion` (oh — collision; see below).

### "CellAssertion" name collision

vcif-rdf already has `vc:CellAssertion` for the kquery cell-
classification record (one of the existing 9 carrier classes).
Geometric currying introduces an `EventCellAssertion`-shaped
concept; reusing the name `CellAssertion` would be wrong.

Resolution (per the central shadow's "Disambiguation: cell"
section):

```text
existing vc:CellAssertion  ->  vc:KqueryCellAssertion
                               vc:EventCellAssertion (new)
```

The rename is backward-incompatible at the RDF level. Mitigation:
ship `vc:CellAssertion` as a deprecated alias for
`vc:KqueryCellAssertion`; SHACL warns rather than rejects on
the legacy name; full removal in a future major version.

### SHACL Layer 2 (self-hosting closure) extension

The existing two-layer SHACL enforcement gains a third rule at
Layer 2: **every saturated `vc:EdgeAssertion` must be backed by
a `vc:EventCellAssertion` whose three role-bindings match the
edge's source / edgeKind / target**. This makes the geometric-
projection consistency machine-checkable at validation time.

```sparql
# Layer 2 extension: edge-backed-by-cell closure
ASK WHERE {
  ?edge a vc:EdgeAssertion ;
        vc:source ?s ;
        vc:edgeKind ?k ;
        vc:target ?t .
  FILTER NOT EXISTS {
    ?cell a vc:EventCellAssertion ;
          vc:closureState ?cs .
    FILTER (?cs IN (vc:closed))
    ?rb1 vc:roleOfCell ?cell ; vc:role :source ; vc:occupant ?s .
    ?rb2 vc:roleOfCell ?cell ; vc:role :kind ;   vc:occupant ?k .
    ?rb3 vc:roleOfCell ?cell ; vc:role :target ; vc:occupant ?t .
  }
}
# returns true ⟺ at least one edge is unbacked
```

### Importer impact

`vcif_rdf.importer.apply` already does a boring loop. The
geometric-importer extension processes `vc:EventCellAssertion` +
`vc:RoleBinding` records first, then `vc:EdgeAssertion` records
as projections. Idempotent; matches the existing import shape.

## Why deferred from the substrate-naming fire

The carrier extension touches `carrier.ttl`,
`shapes/carrier-form.ttl`, `shapes/carrier-self-hosting.ttl`,
the importer, and the SHACL Layer 2 closure check. Substantial
work; deserves its own sub-fire.

## Future fire

`gc-vcif-rdf-carrier`. Region #6 expected (DBE+S2G — adds the
new carrier classes + predicates; the rename is RFS-flavoured
but small). Closure-scope: single-repo (writes only land in
`v4cat-oss/vcif-rdf`).

Best landed *after* `gc-vcif-carrier` so the JSON-substrate
schema additions are reflected in the RDF substrate.

## Closure path

Closes when vcif-rdf ≥ v0.x ships:

1. New carrier predicates + classes in `carrier.ttl`.
2. Existing `vc:CellAssertion` renamed to
   `vc:KqueryCellAssertion`, with deprecated alias.
3. SHACL Layer 2 extended with the
   edge-projection-backed-by-cell closure rule.
4. Importer extended to process geometric records first, then
   saturated projections.
5. Cross-substrate parity tests against vcif and vcif-hlo
   continue to produce identical V₄ cells.
