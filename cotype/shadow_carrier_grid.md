# Shadow: the (depth × substrate) carrier grid

> *DBE+RFS+S2G fire of 2026-05-04 (Stage 2 of the algebraic-foundations
> arc). Region #8 of the shadow-architecture lattice. Algebraic anchor:
> [shadow_assertion_history_group.md](shadow_assertion_history_group.md).*

## Form

Carriers of v4cat factor along **two orthogonal axes**:

```text
                JSON-Schema    RDF/SHACL/SPARQL    (future substrate)
              ┌─────────────┬──────────────────┬───────────────────
                JSON-Schema    RDF/SHACL/SPARQL    Tensor (NumPy/JAX/StableHLO)
operation-log │ vcif/patch  │ vcif-rdf/patch   │ vcif-hlo/op-log     │
state-snapshot│ vcif/snap   │ vcif-rdf/snap    │ vcif-hlo/U-tensors  │
V₄-cover      │ vcif/closur │ vcif-rdf/closur  │ vcif-hlo/CoverTens  │
residue       │ vcif/resid  │ vcif-rdf/resid   │ vcif-hlo/cell-mask  │
─────────────┴─────────────┴──────────────────┴─────────────────────┴
recognizer    │ vcif/recog  │ vcif-rdf/recog   │ vcif-hlo/QueryDAG   │   (operator
vocabulary    │ vcif/vocab  │ vcif-rdf/vocab   │ vcif-hlo/IdDict     │    axis, not depth)
```

The **vertical axis** is *projection-depth*. From `shadow_assertion_history_group.md`:

```text
operation-log         h ∈ H = ℤ^𝔄                  group-faithful, invertible
   │ π
state-snapshot        π(h) ⊆ 𝔄                     idempotent quotient
   │ χ_{A,B}
V₄-cover              χ_{A,B}: π(h) → V₄           coordinate chart
   │ project-cells
residue-report        Cells₁₀ ∪ Cells₀₁ ∪ ...      further quotient
```

The **horizontal axis** is *substrate*. JSON, RDF, future Protobuf /
CBOR / etc. Each substrate brings its own native tooling:

| Substrate | Validator | Query language | Idempotence model |
|---|---|---|---|
| JSON | JSON Schema 2020-12 (jsonschema) | Python set_expr eval | dict-key uniqueness + content hash |
| RDF/Turtle | SHACL Core + SHACL-SPARQL (pyshacl) | SPARQL 1.1 (rdflib) | triple-set uniqueness + URI canonicalisation |
| Tensor | tensor-shape checks (numpy/jax) | branchless mask algebra (`2·A_live + B_live`) | row-equality + first-free padding occupancy |
| (Protobuf) | protoc-gen + custom validator | (no native) | message-equality + content hash |

A specific carrier instance is a *cell* `(depth, substrate)` of this
grid.

## Where realised

- Vertical axis (depth) — registered in
  [shadow_assertion_history_group.md](shadow_assertion_history_group.md);
  the four state-carrying VCIF profiles factor along it.
- Horizontal axis (substrate) — currently filled at three columns:
  - JSON column: [v4cat-oss/vcif](https://github.com/v4cat-oss/vcif)
    — six profiles in `src/vcif/schemas/profiles/`.
  - RDF column: [v4cat-oss/vcif-rdf](https://github.com/v4cat-oss/vcif-rdf)
    — six profiles in `src/vcif_rdf/ontology/profiles/`.
  - Tensor column: [v4cat-oss/vcif-hlo](https://github.com/v4cat-oss/vcif-hlo)
    — branchless tensor algebra over interned IDs;
    `ReferentUniverseTensor` + `CoverTensor` + RISC kernels +
    `QueryDAG` for CISC composition. NumPy backend in v0.1; JAX +
    StableHLO export available via `[jax]` extra (export path
    promissory — see [shadow_stablehlo_export_gap.md](shadow_stablehlo_export_gap.md)).

## Composition operation

`fill(depth, substrate, h)` — given a projection depth, a substrate,
and a history element `h ∈ H`, produces a carrier document at that
grid cell. Composition rules:

- Vertical (depth): `fill(d', s, h) = project_{d→d'}(fill(d, s, h))`
  for `d` shallower than `d'`. Information loss flows downward.
- Horizontal (substrate): `fill(d, s', h) = transcribe_{s→s'}(fill(d, s, h))`.
  Lossless across substrates *at the same depth* — a snapshot in JSON
  and a snapshot in RDF carry the same `π(h)`.

## Entailment

The **cross-substrate parity invariant**: round-tripping a snapshot
from one substrate to another (via v4cat as the kernel) preserves
the visible-state quotient. Concretely, for substrates `s₁` and `s₂`
at the same depth `d`:

```text
import_{s₂}(transcribe_{s₁→s₂}(fill(d, s₁, h)))
  ≡_v4cat
import_{s₁}(fill(d, s₁, h))
```

up to v4cat's catalogue identity.

The **cross-depth visibility invariant**: shallower depths are
quotients of deeper depths (within a substrate). The patch profile
(operation-log) is the deepest — anything in snapshot/closure-report/
residue-report can be derived from it given `π` and the V₄ chart.

## Lattice classification

Region **#8 (DBE + RFS + S2G — substantive structural arc)**.

- **DBE**: forward design of the second substrate column (vcif-rdf).
- **RFS** (light): the JSON column's existing six profiles re-read
  along the depth axis (shallow regrouping; documented in
  shadow_vcif_distribution.md's algebraic-anchor footer).
- **S2G**: this file. Names the orbit-position (the grid). Per
  discipline rule 6, **does not extract a `Carrier` universal** — the
  v4cat RISC ISA is already the universal at the kernel-cell, and
  carriers are co-projections of it parameterised by `(depth,
  substrate)`. The grid is the catalogue position; the universal is
  v4cat itself.

## Trace-integrity

Prior shadows are re-read through this grid framing without removal:

- [shadow_distribution_seam_mcp.md](shadow_distribution_seam_mcp.md) —
  v4cat-mcp lives on a *different* axis: not the carrier grid (which
  is data-at-rest) but the RPC-presentation orbit. Distinct generating
  symmetry: `expose(v4cat-ISA, protocol-X)` rather than
  `co-project(v4cat-ISA, syntax-X)`.
- [shadow_vcif_distribution.md](shadow_vcif_distribution.md) — the
  "vcif as the second presentation" reading is preserved; this shadow
  refines it: vcif is one *column* of the carrier grid, vcif-rdf is
  the second column, the four state-carrying profiles within each
  column are *rows* on the depth axis.

## Snap-to-grid check

User's request: "We should land [the group-theoretic reading] too;
I think it clarifies/formalizees a lot."

Cotype's entailment after this shadow lands: "v4cat carriers factor
along (projection-depth × substrate); two substrate columns now
filled (JSON, RDF), four projection-depth rows populated in each.
The kernel — v4cat's RISC ISA + V₄ coordinate chart — is the
universal at the grid centre; columns and rows are co-projections of
it."

Snap valid; the formal grid framing operationalises the prior turns'
discussion of "carriers as projections of an orbit" and "the kernel
cell". Bonus deliverable, not drift.

## What this shadow does NOT extract

Per discipline rule 6, no `Carrier` wrapper class is defined. v4cat
is the universal at the kernel-cell; lifting a Python `Carrier`
abstract base class above vcif and vcif-rdf would produce a wrapper-
of-an-operator (the operator already serves as the universal). At
even three or thirty filled substrate columns, the move would still
be S2G — register the orbit position, do not extract.

## The slogan, filed at this grid level

> The carriers form a (depth × substrate) grid;
> v4cat sits at the centre as the universal;
> every cell of the grid is a co-projection of v4cat parameterised
> by `(depth, substrate)`.
