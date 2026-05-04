# Shadow: vcif-hlo distribution — third substrate column (tensor/OpenHLO)

> *DBE+RFS+S2G fire of 2026-05-04 (Stage 3 of the algebraic-foundations
> arc). Region #8 of the shadow-architecture lattice; **DBE-heavy**
> (the tensor types are genuinely new costructure with no parallel in
> vcif/vcif-rdf). Algebraic anchor:
> [shadow_assertion_history_group.md](shadow_assertion_history_group.md);
> grid placement: [shadow_carrier_grid.md](shadow_carrier_grid.md).*

## Form

The third substrate column in v4cat's (depth × substrate) carrier
grid. v4cat's RISC operations compile to **branchless tensor DAGs
over interned identity IDs**:

```text
ReferentUniverseTensor[K]:
  rows : tensor<P × K × Id>      universe-shaped tensor
  live : tensor<P × Bool>         per-row liveness mask
  arity: int                      K (1=node, 2=binary, 3=edge-triple, ...)

CoverTensor:
  frame_rows : tensor<P × K × Id>
  cell       : tensor<P × UInt2>  V₄ coordinate ∈ {0, 1, 2, 3}
  live       : tensor<P × Bool>
```

The kquery kernel is the V₄-equivariant coordinate chart of the
observer-pair group, realised branchlessly:

```text
cell_code = 2 · A_live + B_live ∈ {0, 1, 2, 3}
```

Strings exist only at the dictionary boundary (`IdDictionary`).
OpenHLO/StableHLO/JAX/NumPy never see strings; only `Id` tensors
flow inside the kernels.

## Where realised

- **Repo**: [v4cat-oss/vcif-hlo](https://github.com/v4cat-oss/vcif-hlo).
  v0.1 ships with NumPy backend (light dependency); JAX optional.
- **Tensor types**: `src/vcif_hlo/tensors.py` —
  `ReferentUniverseTensor`, `CoverTensor`.
- **RISC kernels**: `src/vcif_hlo/kernels.py` —
  `introduce_node`, `edge`, `kquery`. Each is branchless,
  group-faithful at the tensor level.
- **CISC composition**: `src/vcif_hlo/dag.py` — `QueryDAG` typed
  composition of universe / mask / kquery / projection nodes.
- **Recognizers**: `src/vcif_hlo/recognizers.py` — the writeup's
  ResolveReferencesForName (§ 6) and recursive_definition (§ 7)
  worked examples.
- **Bridges**: `src/vcif_hlo/bridge_v4cat.py` (load/apply with a
  SymmetryCatalogue), `src/vcif_hlo/bridge_vcif.py` (load from vcif
  JSON or vcif-rdf RDF graphs).
- **Tests**: 50 green; cross-substrate parity demonstrated against
  vcif's agda-import.json fixture.

## Composition operation

`compile(QueryDAG, dictionary) → tensor program`, optionally
exportable to StableHLO via `jax.export.export(...).serialize()`
(the export path is currently a promissory cell — see
[shadow_stablehlo_export_gap.md](shadow_stablehlo_export_gap.md)).

The composition rule: every CISC recognizer is a typed DAG of
universe-shaped tensor transformations; every kquery gate is a
branchless `2·A_live + B_live`; every wire is universe-shaped.

## Entailment

If a DAG honours the carrier-vs-object discipline (no strings inside
kernels; only `Id` tensors), and if every comparison node is kquery,
and if every wire is universe-shaped, then the DAG is **v4cat-native
and OpenHLO-fusable**. Concretely: a CISC recognizer expressed as a
`QueryDAG` lowers to a sequence of NumPy / JAX broadcast-mask-reduce
operations with no Python-level branching.

The cross-substrate parity invariant: a snapshot loaded from vcif
(JSON), vcif-rdf (RDF), or a v4cat catalogue, when run through the
same kquery in tensor form, yields **identical V₄ cell membership**.
Demonstrated by `test_parity.py` against vcif's agda-import fixture.

## Lattice classification

Region **#8 (DBE + RFS + S2G — substantive structural arc)** with a
**DBE-dominant mix**, distinct from prior fires:

- **DBE (heavy)**: the tensor types (ReferentUniverseTensor,
  CoverTensor) are genuinely new — no parallel in vcif or vcif-rdf,
  which carry only declarative data. The kernel design is
  forward-original.
- **RFS (light)**: regroups VCIF's `recognizer-package` profile
  against the QueryDAG framing. The writeup makes operational what
  recognizer-package gestured at declaratively.
- **S2G**: this file. Snaps onto the carrier-grid as the third
  substrate column.

### Discipline rule 6 check

At three substrate columns, do we *now* extract a `Carrier` wrapper?

**No.** Per the orbit-projection reading from prior turns, v4cat is
the universal at the kernel-cell; the substrate-axis is parameterised
by the choice of execution-or-serialization syntax. Any number of
further substrate columns (Protobuf, CBOR, Arrow, ...) would be
additional orbit-elements, not triggers for wrapper-extraction. The
C7 ≥3 threshold *applies to free duplication*, not to orbit-element
enumeration.

What changes at three filled columns: the catalogue's entailment
generalises further from "v4cat ships with a couple of substrate
columns" to "v4cat is substrate-agnostic; carriers are
co-projections parameterised by `(depth, substrate)`, with
arbitrarily many substrate-options living in the same equivalence
class under `apply(_, v4cat_catalogue)`-equality."

## Trace-integrity

Prior shadows are preserved and re-read through this addition:

- [shadow_carrier_grid.md](shadow_carrier_grid.md) — extended to
  three columns. The grid table is widened; vcif-hlo joins as the
  third filled cell across all four projection-depth rows.
- [shadow_assertion_history_group.md](shadow_assertion_history_group.md)
  — the algebraic universal is unchanged; vcif-hlo is one more
  co-projection of the same `(H, π, V₄^U)` structure.
- [shadow_kquery_universal_read.md](shadow_kquery_universal_read.md)
  — kquery's "universal read primitive" status is now operationalised
  *as a branchless tensor kernel*, not just as a logical pattern.
  The shadow's algebraic-anchor footer extends naturally.
- [shadow_distribution_seam_mcp.md](shadow_distribution_seam_mcp.md)
  and [shadow_vcif_distribution.md](shadow_vcif_distribution.md) —
  not affected; vcif-hlo is parallel to vcif (same projection-depth
  axis, different substrate column), not in the RPC orbit.

No prior shadow is invalidated.

## Snap-to-grid check

User's request: "Apply the four skills to the system, with this
OpenHLO perspective landed, and land it."

Cotype's entailment after this fire lands: "v4cat is realised
across three substrate columns now — JSON (vcif), RDF (vcif-rdf),
tensor (vcif-hlo). The operation-log row is fundamental in all three
substrates; the V₄-cover row is realised most efficiently in the
tensor substrate via branchless cell-code arithmetic. v4cat sits at
the kernel-cell as the universal across all three columns."

Snap valid; substrate column #3 generalises the prior reading from
"two substrate options" to "the substrate axis is open-ended." Bonus
deliverable: the recognizer-package profile becomes operationally
*executable* (not just declarative) in the tensor substrate.

## What this shadow does NOT extract

Per discipline rule 6:

- No `Carrier` abstract base class above vcif / vcif-rdf / vcif-hlo.
- No `Profile` abstract base class above the {snapshot, patch,
  vocabulary, recognizer-package, closure-report, residue-report}
  set.
- No "tensor-carrier" abstraction above NumPy/JAX/StableHLO; those
  are *backends* of the same tensor carrier, all duck-typed against
  the array-API surface.

The orbit is parameterised; v4cat IS the universal; wrapper
extraction would just produce a wrapper-of-an-operator.

## The slogan, operationalised

> v4cat supplies the ontology.
> VCIF / VCIF-RDF supply the interchange.
> vcif-hlo supplies the carrier — branchless tensor execution over
> interned identity IDs.
> Shadow-architecture supplies the discipline.

Tighter:

> Strings name the world outside.
> IDs carry it inside.
> kquery splits it into V₄ fibers.
> CISC is just a fused DAG of those splits.
> v4cat audits the whole carrier against itself.
