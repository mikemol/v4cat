# Shadow: geometric currying — vcif-hlo carrier (promissory)

**Tracking**: [v4cat-oss/vcif-hlo#4](https://github.com/v4cat-oss/vcif-hlo/issues/4) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_geometric_currying.md](shadow_geometric_currying.md)).
> Region **#4** (S2G alone — pure cataloguing).*

## Form

`vcif-hlo` (the tensor / OpenHLO substrate column) currently
encodes edges as a structure-of-arrays:

```text
edge_rows : tensor<P × 3 × Id>  -- (source_idx, kind_idx, target_idx) per edge
edge_live : tensor<P × Bool>
```

Each row is a saturated edge. Geometric currying says each row
is a **projection** of three role-closure masks. The tensor
substrate gains the masks as first-class arrays; the saturated
form remains as a derived view.

## What to extract

### Three role-closure tensors

```text
role_source_closed : tensor<P × Bool>
role_kind_closed   : tensor<P × Bool>
role_target_closed : tensor<P × Bool>
```

Each is `True` at edge index `e` iff the corresponding role of
edge-cell `e` has been closed. The saturated mask follows:

```text
edge_closed = role_source_closed
            & role_kind_closed
            & role_target_closed
```

### Path-advancement mask

```text
advance_mask = scheduled_mask & edge_closed
```

Where `scheduled_mask : tensor<P × Bool>` indicates cells
scheduled for the path under consideration. The `advance_mask`
is the V₄ cover's `c11` cell (closed AND presented) reduced to
a Bool tensor.

This is **fusion-friendly**: the per-cell predicate is a
broadcast-elementwise AND, which compiles cleanly to OpenHLO /
StableHLO / XLA ops.

### Carrier-grid impact

vcif-hlo already operationalises kquery as `cell_code = 2 *
A_live + B_live` ([per theory.md § 15][theory15]). The
geometric-currying tensors give a finer denominator:

[theory15]: https://github.com/v4cat-oss/v4cat/blob/main/src/v4cat/theory.md

```text
A_live = role_source_closed & role_kind_closed & role_target_closed
       = edge_closed
B_live = scheduled_mask
```

Then `cell_code = 2 * edge_closed + scheduled_mask`:

```text
0 (=00):  unscheduled and unclosed cell (open frontier)
1 (=01):  scheduled but boundary not closed (presentation-without-substrate)
2 (=10):  closed but not scheduled in this path (silent closure)
3 (=11):  scheduled and closed (honest path advancement)
```

This is the **path-advancement cover** from the central shadow,
operationalised in the tensor substrate.

### Existing tests

`vcif-hlo/src/vcif_hlo/tests/test_parity.py` (the cross-
substrate parity test that closed G1) needs no change to the
parity *invariant*; it gains additional fixtures exercising the
geometric tensors.

## Why deferred from the substrate-naming fire

The tensor extensions touch `vcif_hlo`'s data layout, kquery
operationalisation, and bridge layer (`bridge_v4cat`). Each of
those is its own design surface; bundling into the substrate-
naming fire would over-scope.

## Future fire

`gc-vcif-hlo-carrier`. Region #6 expected (DBE+S2G). Closure-
scope: single-repo (writes only land in `v4cat-oss/vcif-hlo`).

Best landed in any order with respect to the other carriers; all
three carriers ultimately produce identical V₄ classifications,
so a partial-migration state is testable via cross-substrate
parity.

## Closure path

Closes when vcif-hlo ≥ v0.x ships:

1. Three role-closure Bool tensors as first-class data.
2. Derived `edge_closed` = elementwise AND.
3. Path-advancement mask in terms of role tensors.
4. Updated `bridge_v4cat.apply_derive_mask` (or successor) to
   propagate role-closure events from the v4cat-core cell layer
   to the role tensors.
5. Cross-substrate parity tests (existing 8 tests in
   `test_parity.py`) extended to exercise the role tensors.
6. Recommended: a fusion-friendliness benchmark showing
   `edge_closed` compiles to a single XLA op rather than three
   sequential ones (this is *aspirational* and is a follow-on
   sub-sub-fire).
