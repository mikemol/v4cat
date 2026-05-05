# Shadow: geometric currying — vcif carrier (promissory)

**Tracking**: [v4cat-oss/vcif#1](https://github.com/v4cat-oss/vcif/issues/1) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_geometric_currying.md](shadow_geometric_currying.md)).
> Region **#4** (S2G alone — pure cataloguing).*

## Form

`vcif` (the JSON Schema substrate column of the carrier grid)
currently encodes edges as compact saturated triples:

```json
{"source": "s", "kind": "k", "target": "t"}
```

Geometric currying says this triple is the **saturated projection
of a closed event-cell**. The full geometric form has explicit
cells, role-bindings, and boundaries.

## What to extract

### New top-level sections in the snapshot profile

```json
{
  "cells":             [{"id": "...", "cell_kind": "EdgeCell", "closure": "closed"}],
  "role_bindings":     [{"cell": "...", "role": "source", "occupant": "..."}],
  "boundaries":        [{"cell": "...", "closed": true}],
  "path_presentations":[{"path": "...", "steps": [...]}]
}
```

These extend the existing `nodes` and `edges` arrays. The
`edges[]` array remains as the saturated-projection form (back-
compatible); a snapshot can carry **both** the geometric form
and the projection, and the schema enforces consistency.

### Schema-level invariant

> Every `edges[i]` entry must correspond to a cell in `cells[]`
> whose `cell_kind == "EdgeCell"` and whose `closure == "closed"`,
> and whose three `role_bindings` for `source`, `kind`, `target`
> match the edge's three fields.

Implemented as a JSON-Schema cross-reference rule plus a
semantic-validator pass in `vcif/src/vcif/semantic.py` (current
14-rule pipeline gains a 15th rule).

### Backward compatibility

Existing snapshots without `cells[]` are valid: the importer
auto-derives one EdgeCell per entry in `edges[]`. The validator
emits a deprecation warning encouraging explicit cell shapes.

### Profile-by-profile impact

| Profile | Geometric impact |
| --- | --- |
| `v4cat.snapshot` | gains `cells`, `role_bindings`, `boundaries` (described above) |
| `v4cat.patch` | additive operation log gains operation types `introduce_cell`, `bind_role`, `close_boundary`, `close_cell`, `advance_path` |
| `v4cat.vocabulary` | gains the 11 new node-kinds + 17 new edge-kinds from HF-GeometricCurrying |
| `v4cat.recognizer-package` | T-edge-boundary-closure et al. become canonical recognizer fixtures |
| `v4cat.closure-report` | covers gain `cell-closure` and `path-advancement` cover-kinds in addition to the existing v4cat covers |
| `v4cat.residue-report` | residues from open boundaries become a first-class category alongside the existing kquery-cell residues |

## Why deferred from the substrate-naming fire

vcif's schema additions are substantial (~6 new top-level
sections, 1 new semantic-validator rule, 6 profile updates).
Bundling them into the substrate-naming fire would land in
region #5 (DBE+RFS without adequate per-distribution S2G).

## Future fire

`gc-vcif-carrier`. Region #6 expected (DBE+S2G — adds the
geometric sections, no major RFS internal to vcif). Closure-scope:
single-repo (writes only land in `v4cat-oss/vcif`).

Best landed *after* `gc-v4cat-core` so vcif's schema reflects
the operational substrate rather than a candidate one.

## Closure path

Closes when vcif ≥ v0.x ships:

1. JSON Schema additions for `cells`, `role_bindings`,
   `boundaries`, `path_presentations`.
2. Updated `semantic.py` rule 15 enforcing
   edges-projection-backed-by-cell.
3. Updated profile schemas (snapshot / patch / vocabulary /
   recognizer-package / closure-report / residue-report).
4. Importer back-compat: derives cells from legacy edges.
5. Tests for round-trip: snapshot with explicit cells round-
   trips losslessly; snapshot with only legacy `edges[]` imports
   into v4cat with cells auto-derived.

Cross-substrate parity (against vcif-rdf and vcif-hlo, once
*their* sub-fires land) continues to produce identical V₄
classifications.
