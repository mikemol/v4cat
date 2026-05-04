# Shadow: StableHLO export gap (promissory cell)

> *S2G fire of 2026-05-04 (Stage 3 of the algebraic-foundations arc).
> **At orbit-position 1** (just vcif-hlo's NumPy backend); per discipline
> rule 6, S2G to catalogue the gap, NOT RFS to extract a wrapper.
> Companion to [shadow_vcif_hlo_distribution.md](shadow_vcif_hlo_distribution.md).*

## Form

A **promissory cell** in vcif-hlo's substrate column. v0.1 ships
with NumPy as the default backend; JAX is optional. The OpenHLO/
StableHLO export path *exists in principle* — any JAX function
compiles to StableHLO MLIR via `jax.export.export(...).serialize()`
— but is **not yet exercised** in v0.1.

## What's missing

Three components of an end-to-end vcif-hlo → StableHLO pipeline:

1. **Backend parameterisation.** The tensor kernels in
   `vcif_hlo.kernels` are written in NumPy-API style and work
   transparently under `jax.numpy` (duck-typing on `broadcast_to`,
   `where`, `logical_and`, `astype`, etc.). What's missing: explicit
   `xp` parameter passing through the QueryDAG executor, plus a
   pytest-parametrize over both backends.

2. **`jax.export` integration.** A `vcif_hlo.compile_to_stablehlo(dag)
   → str` function that:
   - Takes a `QueryDAG`.
   - Wraps it as a JAX-traceable function (placeholder shapes for
     each `UniverseConstructor` / `MaskBuilder` input).
   - Calls `jax.jit` to trace.
   - Calls `jax.export.export(...).serialize()` to dump StableHLO.
   - Returns the MLIR text.

3. **Round-trip validation.** A test that takes a `QueryDAG`, exports
   to StableHLO MLIR, parses it back (via `xla.compile_mlir_to_hlo`
   or equivalent), and confirms the cell-classification matches the
   eager-NumPy execution on the same inputs.

## What this shadow does NOT do

Per discipline rule 6: **at orbit-position 1 (just vcif-hlo's
NumPy backend), the move is S2G — catalogue the gap, do not
extract a wrapper.** Specifically:

- Does not introduce a "compile target" abstract base class.
- Does not parameterise vcif-hlo's kernel module signature beyond
  duck-typing.
- Does not commit to JAX as the *only* path to StableHLO; a future
  fire could also use the `mlir-python-bindings` directly to write
  StableHLO MLIR text.

The shadow simply names the gap so the catalogue thickens forward.

## Promissory cell — what would close it

A future `vcif-hlo>=0.2` ships with:

1. `pip install vcif-hlo[jax]` pulls in `jax>=0.4` as a real
   optional dep.
2. Kernels accept an optional `xp` parameter (`numpy` by default,
   `jax.numpy` when JAX is present).
3. New module `vcif_hlo.compile.stablehlo` with
   `compile_to_stablehlo(dag, *, abstract_inputs) → str`.
4. New CLI subcommand `vcif-hlo compile <recognizer> --to=stablehlo`.
5. A test that exports the resolve_references DAG to StableHLO,
   inspects the MLIR text, and confirms it contains `stablehlo.add`
   (for `2 * A_live + B_live`) plus `stablehlo.compare` (for the
   per-row equality checks in `introduce_node` / `edge`).
6. The `vcif-hlo` README's "Backend" section is updated to
   describe StableHLO export as a first-class path.

This would close the cell. The OpenHLO-target framing in the
writeup ("OpenHLO supplies the carrier: branchless tensor
execution") becomes operationally what it's already documented to
be at the spec level.

## Lattice classification

Region **#4 (S2G alone — pure cataloguing)**, by exception. Per
shadow-architecture's lattice, S2G-alone fires are the small
minority of work — typically cotype refreshes, audit-memo
regenerations, or gap-registration. This is exactly the latter:
register the promissory cell, no code change yet.

The accompanying shadows in this Stage 3 fire
([shadow_vcif_hlo_distribution.md](shadow_vcif_hlo_distribution.md)
plus the carrier-grid extension) are region #8; this one is
region #4 because the gap is at orbit-position 1.

## Trace-integrity

Prior shadows are unaffected:

- [shadow_event_log_gap.md](shadow_event_log_gap.md) — the v4cat
  side's event-log gap is structurally analogous: vcif-hlo's
  StableHLO export is to *the JAX/XLA tooling target* what v4cat's
  event-log API is to *the operation-log carrier*. Both are
  promissory cells registered at orbit-position 1; both name a
  concrete future fire that would close them.
- [shadow_carrier_grid.md](shadow_carrier_grid.md) — the tensor
  substrate column is filled; the StableHLO sub-target within that
  column is the next refinement.

## When this shadow closes

When vcif-hlo ships a `compile_to_stablehlo` function with the
promissory-cell list above satisfied, this shadow can be retired
(or annotated with "closed at vcif-hlo 0.X" per the
catalogue-thickens-forward discipline). At that point, the writeup's
phrase "OpenHLO supplies the carrier" becomes an operative
guarantee, not just a design intent.

Until then, this shadow stands as a registered structural commitment
the framework has *named* but not yet *executed*.
