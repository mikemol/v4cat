# Shadow: v4cat-octave VCIF-profiles gap (promissory cell)

**Tracking**: [v4cat-oss/v4cat-octave#4](https://github.com/v4cat-oss/v4cat-octave/issues/4) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_v4cat_octave_distribution.md](shadow_v4cat_octave_distribution.md)).
> Region **#4** (S2G alone -- pure cataloguing).*

## Form

VCIF defines six profile schemas (`v4cat.snapshot`,
`v4cat.patch`, `v4cat.vocabulary`, `v4cat.recognizer-package`,
`v4cat.closure-report`, `v4cat.residue-report`) -- see
[`vcif/docs/spec.md`](https://github.com/v4cat-oss/vcif/blob/main/docs/spec.md).
`v4cat-octave` v0.1 implements `vcif_import.m` / `vcif_export.m`
for the **snapshot profile only** -- the load-bearing core
needed for kernel-parity.

This shadow names the surface for extending VCIF round-trip to
the other five profiles.

## What to extract per profile

| Profile | Octave entry points | What it carries beyond snapshot |
| --- | --- | --- |
| `v4cat.patch` | `vcif_import_patch.m`, `vcif_export_patch.m` | Operation-log: ordered list of additive RISC writes (group-faithful root of the projection-depth axis) |
| `v4cat.vocabulary` | `vcif_import_vocab.m`, `vcif_export_vocab.m` | node_kinds + edge_kinds only (no nodes/edges); used for cross-document type-system pin |
| `v4cat.recognizer-package` | `vcif_import_recognizer.m`, `vcif_export_recognizer.m` | tensions + cell actions + parameter declarations; v4cat-octave's QueryDAG is the natural run-target |
| `v4cat.closure-report` | `vcif_import_closure.m`, `vcif_export_closure.m` | covers + cells + expectations; v4cat-octave's `kquery` produces the cells natively |
| `v4cat.residue-report` | `vcif_import_residue.m`, `vcif_export_residue.m` | residues from prior closure runs; cell-mask projection |

The vcif library's [Python importer/exporter][vcif-py] is the
reference; matching its semantics is the bar.

[vcif-py]: https://github.com/v4cat-oss/vcif/tree/main/src/vcif

## Why deferred from v0.1

`snapshot` is the only profile needed for the kernel-parity
invariant. The other five profiles are useful for richer
inter-distribution interchange (e.g., a vcif-rdf carrier writing
a `closure-report` and v4cat-octave reading + verifying it) but
not on the load-bearing critical path of v0.1.

The recognizer-package profile is particularly meaningful: VCIF's
recognizers are tensions with cell-actions; v4cat-octave's
QueryDAG is a near-isomorphic data-shape for the same concept.
The future fire makes the isomorphism explicit by adding a
recognizer-package import that compiles directly to a QueryDAG.

## Future fire

`v4cat-octave-vcif-profiles` (single sub-fire spanning all five
remaining profiles, since they share importer infrastructure).

## Closure

Closes when v4cat-octave ≥ v0.x:

1. Imports + exports each of the six profiles.
2. Round-trips a fixture document for each profile.
3. Cross-substrate-parity tests against v4cat (Python) for each
   profile's `kquery`-shaped invariants.
