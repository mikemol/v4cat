# Shadow: geometric currying — v4cat-octave role matrices (promissory)

**Tracking**: [v4cat-oss/v4cat-octave#7](https://github.com/v4cat-oss/v4cat-octave/issues/7) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_geometric_currying.md](shadow_geometric_currying.md)).
> Region **#4** (S2G alone — pure cataloguing).*

## Form

`v4cat-octave` (the algebraic reference carrier) currently
implements `edge` with the **geometric currying invariant
already explicit** ([its v0.1 distribution
shadow](shadow_v4cat_octave_distribution.md) names this as the
load-bearing observation). What's *not* yet explicit is the
**role-matrix encoding** that makes role closure visible as
sparse-matrix algebra.

This sub-fire adds it — making boundary closure not just an
invariant but a *computation* in the carrier substrate.

## What to extract

### Three role matrices

For an edge-cell index space of size `P`:

```octave
S = sparse (P, N);   % S(e, s) = 1 if e has source s
K = sparse (P, N);   % K(e, k) = 1 if e has kind k
T = sparse (P, N);   % T(e, t) = 1 if e has target t
```

where `N = numel(cat.nodes)` is the node universe size.

### Saturating closure

```octave
edge_closed = any (S, 2) & any (K, 2) & any (T, 2);
% edge_closed(e) is true iff e has at least one occupant in each role.
```

This is the **saturating-mode** closure: the geometric-currying
invariant.

### Strict closure (with `edge_strict` from
[shadow_v4cat_octave_edge_strict.md](shadow_v4cat_octave_edge_strict.md))

```octave
edge_closed_strict = sum (S, 2) == 1 ...
                   & sum (K, 2) == 1 ...
                   & sum (T, 2) == 1;
% Each role bound exactly once -- no overloads, no gaps.
```

This pairs cleanly with the existing `edge_strict` promissory
shadow for v4cat-octave (already catalogued; this sub-fire is
the *role-matrix* half of the strict-mode operationalisation).

### Visibility benefit

Making the role matrices first-class gives v4cat-octave's role
as the *algebraic reference carrier* a cleaner expression:

```octave
% Boundary closure as sparse matrix algebra:
boundary_closed_per_edge = full (any (S, 2) & any (K, 2) & any (T, 2));

% Role-occupant count per cell -- the reverse direction:
source_occupants_per_cell = sum (S, 2);
kind_occupants_per_cell   = sum (K, 2);
target_occupants_per_cell = sum (T, 2);

% Cells with multiply-bound roles (a closure violation in strict mode):
overloaded_cells = source_occupants_per_cell > 1 ...
                 | kind_occupants_per_cell   > 1 ...
                 | target_occupants_per_cell > 1;
```

These are **trivial sparse-matrix expressions**. The geometric
substrate becomes inspectable in the same way the kquery cells
already are.

### Pairing with existing v4cat-octave promissories

This sub-fire pairs naturally with two existing v4cat-octave
promissories:

- [`shadow_v4cat_octave_edge_strict.md`](shadow_v4cat_octave_edge_strict.md)
  — strict-mode edge. The role matrices are the *substrate* of
  strict-mode operationalisation.
- [`shadow_v4cat_octave_framework_seed.md`](shadow_v4cat_octave_framework_seed.md)
  — framework-seed equivalent. Once both land, the full
  type-strict mode is reachable in the algebraic carrier.

The recommended joint v0.x sub-fire bundle is:

```text
gc-octave-role-matrices  (this sub-fire)
+ v4cat-octave-edge-strict
+ v4cat-octave-bootstrap (framework_seed equivalent)
```

These three together produce a v4cat-octave that has the full
geometric-currying substrate operational as algebraic data —
an unusually strong reference for the new substrate.

## Why deferred from the substrate-naming fire

v4cat-octave is independent of v4cat (Python) — they're peer
kernel implementations. The role-matrix sub-fire can land
*before* `gc-v4cat-core` if v4cat-octave wants to be the
operational reference for the substrate. (This is even
methodologically interesting: the algebraic reference carrier
proves the substrate works *before* the systems kernel
implements it.)

## Future fire

`gc-octave-role-matrices`. Region #6 expected (DBE+S2G).
Closure-scope: single-repo (writes only land in
`v4cat-oss/v4cat-octave`).

Ordering recommendation: this sub-fire is *independent* of
ordering with respect to the v4cat-Python migration. It can
land first, last, or in parallel.

## Closure path

Closes when v4cat-octave ≥ v0.x ships:

1. `inst/+v4cat/role_matrices.m` building `S`, `K`, `T` sparse
   matrices from the catalogue's edge structure-of-arrays.
2. `inst/+v4cat/edge_closed.m` returning the saturating closure
   logical vector.
3. `inst/+v4cat/edge_closed_strict.m` returning the strict-mode
   closure logical vector (paired with the existing
   `edge_strict` promissory).
4. Tests asserting:
   - `edge_closed` agrees with `edge_live` on saturating-mode
     catalogues (the v0.1 default).
   - `edge_closed_strict` rejects overloaded cells.
   - Cross-substrate parity (kernel-parity test) continues to
     produce identical V₄ cells.
5. Documentation extension in `v4cat-octave/docs/spec.md`
   demonstrating role-matrix computations as worked examples.

## Closure trail (2026-05-05 — fire #15)

**Closed** by [v4cat-octave 8582d70](https://github.com/v4cat-oss/v4cat-octave/commit/8582d70)
landing under [v4cat-octave#7](https://github.com/v4cat-oss/v4cat-octave/issues/7)
within fire #15.

What shipped:

- `inst/+v4cat/role_matrices.m` — returns sparse `[S, K, T]`
  matrices over a catalogue: `S(e,s) = 1` iff edge `e` has
  source `s`; analogously `K`, `T`.
- `inst/+v4cat/edge_closed.m` — saturating-mode closure,
  `closed = full(any(S, 2) & any(K, 2) & any(T, 2))`.
- `inst/+v4cat/edge_closed_strict.m` — strict closure rejecting
  overloaded role-bindings, `sum(S, 2) == 1 & sum(K, 2) == 1 & sum(T, 2) == 1`.
- `test/test_role_matrices.m` — 5 assertions validating shape,
  saturation, and strict mode.

Cross-substrate parity (`tools/parity-check.sh`) continues to
produce identical V₄ classifications against the Python
reference. The role-matrix layer composes with the existing
catalogue without modifying the saturated-edge projection that
legacy consumers see.

Deferred to a follow-on fire (per shadow §"Closure path",
item 5): the documentation extension in `docs/spec.md`
demonstrating role-matrix computations as worked examples.
