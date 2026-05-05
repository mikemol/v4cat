# Shadow: v4cat-octave — algebraic reference carrier (NEW role)

**Tracking**: closed-fire trajectory entry at [v4cat-oss/methodology#9](https://github.com/v4cat-oss/methodology/issues/9) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *DBE+RFS+S2G fire of 2026-05-05. Region **#8** of the
> shadow-architecture lattice. Algebraic anchor:
> [shadow_assertion_history_group.md](shadow_assertion_history_group.md).
> Operationalised at
> [v4cat-oss/v4cat-octave](https://github.com/v4cat-oss/v4cat-octave).*

## Form

The **first instance** of a new role in the v4cat-oss workspace:
**reference carrier**. Where the data-at-rest carriers
([vcif](https://github.com/v4cat-oss/vcif),
[vcif-rdf](https://github.com/v4cat-oss/vcif-rdf),
[vcif-hlo](https://github.com/v4cat-oss/vcif-hlo)) *transport*
catalogue content across substrates, and the catalogue source
([agda2v4cat](https://github.com/v4cat-oss/agda2v4cat))
*produces* it from a domain, the reference carrier
**re-implements the kernel itself** in a substrate where the
finite incidence geometry is painfully visible.

```text
v4cat-octave         ← reference carrier (NEW role)
                       (algebraic, sparse-matrix-native,
                        slow-but-inspectable kernel
                        re-implementation)

v4cat                ← systems kernel (Python, fast)
{vcif, vcif-rdf,
 vcif-hlo}           ← data-at-rest carriers (substrate columns)
v4cat-certify        ← workspace certification suite
agda2v4cat           ← catalogue source (Agda → VCIF)
v4cat-mcp            ← RPC presentation (MCP)
methodology          ← public methodology + workspace-level issues
```

The reference-carrier role is **not** a fourth substrate column.
The substrate columns transport VCIF documents in different
syntactic substrates; v4cat-octave is a *full implementation* of
the v4cat semantics (RISC ISA + kquery + QueryDAGs + self-hosting
closure) in Octave's algebra. It produces VCIF, consumes VCIF,
and computes V₄ classifications -- the same kernel API surface
as `v4cat` (Python), in a different language with different
performance characteristics.

## Where realised

- **Repo**: [v4cat-oss/v4cat-octave](https://github.com/v4cat-oss/v4cat-octave) v0.1.
- **Implementation**: GNU Octave (developed against 9.4.0; works on
  any 6.x+). No mise pin -- system Octave from the distribution
  package manager is enough.
- **Layout**: `inst/+v4cat/` package directory (Octave's namespacing
  convention; every function callable as `v4cat.<name>`).
- **Test count**: 7 tests + 3 worked examples; parity-check shell
  script runs the kernel-parity invariant.

## Composition operation

```text
.agda or .ttl or .json --> vcif_import.m --> v4cat-octave catalogue
                                              |
                                              | kquery, edge_select,
                                              | incidence_for_kind, ...
                                              v
                                          V_4 cells
                                              |
                                              | vcif_export.m
                                              v
                                          .json
```

Plus self-hosting closure: `self_closure(cat)` catalogues 9 claims
about the package and applies `kquery` to them. The closure check
**is** kquery -- which is the v4cat-octave point.

## Entailment

```text
∀ VCIF snapshot S.
  v4cat_octave.kquery(import(S)) and v4cat_python.kquery(import(S))
  produce identical V_4 cell membership (kernel-parity invariant).
```

Verified end-to-end by [tools/parity-check.sh][parity], using a
shared fixture document at [tools/parity-fixture.json][fixture].

[parity]: https://github.com/v4cat-oss/v4cat-octave/blob/main/tools/parity-check.sh
[fixture]: https://github.com/v4cat-oss/v4cat-octave/blob/main/tools/parity-fixture.json

This is **kernel-parity** -- a sibling of carrier-parity
([vcif-hlo's test_parity.py][carrier-parity], which checks
identical V_4 cells across {vcif, vcif-rdf, vcif-hlo}). Together
the two parities cover the workspace's kernel × carrier matrix.

[carrier-parity]: https://github.com/v4cat-oss/vcif-hlo/blob/main/src/vcif_hlo/tests/test_parity.py

## Lattice classification

Region **#8** (DBE+RFS+S2G).

- **DBE (heavy)**: forward design of the Octave RISC ISA, sparse
  incidence carrier, kquery as four logical/sparse formulas,
  QueryDAG evaluator, self-hosting closure check, VCIF
  import/export, kernel-parity orchestration. ~600 lines of
  Octave + 100 lines of Python + a shell driver.
- **RFS** (substantive): regroups the existing v4cat (Python) as
  *orbit-position-1* of "v4cat kernel implementation" -- the
  Python implementation, formerly *the* kernel, becomes one
  *instance* among potentially many. Also: the existing
  cross-substrate parity discipline (carrier-parity) is
  recognised as one of two parity species; **kernel-parity**
  (v4cat-octave ↔ v4cat-python on the same VCIF input) is the
  new species, surfaced at orbit position 1 of "kernel-parity".
- **S2G**: this file, plus 5 per-future-fire promissory shadows
  for the deferred ISA + bootstrap + VCIF profiles + classdef
  wrapper + edge_strict mode.

### Discipline rule 6 (orbit-saturation) check

Two simultaneous orbit recognitions:

| Orbit | Position after this fire | C7 ≥3 met? | Wrapper extracted? |
| --- | --- | --- | --- |
| v4cat kernel implementation | 2 (Python + Octave) | no | no |
| reference-carrier role | 1 (Octave) | no | no |
| kernel-parity recognition | 1 (octave ↔ python) | no | no |
| carrier-parity recognition | 3 (vcif × vcif-rdf × vcif-hlo) | yes | no -- the carriers don't unify under a `Carrier` wrapper because v4cat itself is the universal at the kernel-cell |

A future second instance of "reference-carrier role" (e.g.
v4cat-coq, v4cat-lean) would parameterise the orbit. At three
the C7 threshold tips toward RFS-eligible.

## The geometric-currying observation

The defining recognition that makes v4cat-octave's RISC ISA
distinct from v4cat (Python)'s: **`edge` may introduce its
boundary nodes if they do not yet exist**.

```octave
[cat, ~] = v4cat.edge(cat, "alice", "knows", "bob");
% Lands "alice", "knows", "bob" as nodes plus one edge.
```

This is the load-bearing observation. The strict-mode complement
(`edge_strict`, which would emit residue when any boundary isn't
already closed) is promissory; see
[shadow_v4cat_octave_edge_strict.md](shadow_v4cat_octave_edge_strict.md).
The Python kernel is closer to strict-mode in its split between
`introduce_node` and `edge` -- the geometric-currying recognition
makes explicit that an edge structurally entails its three
boundary nodes, regardless of which mode the kernel chooses.

## Trace integrity

Prior shadows preserved:

- [shadow_carrier_grid.md](shadow_carrier_grid.md) -- three
  substrate columns unchanged. v4cat-octave is **not** a fourth
  substrate column; it's a different role (reference carrier).
- [shadow_assertion_history_group.md](shadow_assertion_history_group.md)
  -- the algebraic substrate is unchanged. The Octave package's
  `kquery` is the same V_4 coordinate chart, executed in a
  different language.
- vcif-hlo's `test_parity.py` -- carrier-parity is unchanged.
  Kernel-parity is added as a sibling species of parity, not a
  replacement.

## Snap-to-grid check

User's request (with the load-bearing recognition surfaced
explicitly): "An Octave implementation of v4cat should be the
**algebraic reference carrier**: not the fastest backend, not the
systems kernel, but the place where the finite incidence
geometry is painfully visible. ... Notice the **geometric
currying** improvement: `edge` may introduce its boundary nodes
if they do not yet exist."

Cotype's entailment after this shadow lands:

> v4cat-octave is the first instance of a new workspace role:
> reference carrier. It re-implements the v4cat RISC ISA in
> Octave with sparse incidence matrices and logical-vector
> referent universes. The geometric-currying invariant is named
> as a load-bearing observation about edges and their boundary
> nodes. Kernel-parity (v4cat-octave ↔ v4cat-python) is added as
> a sibling of carrier-parity. v0.1 covers the RISC core +
> kquery + sparse incidence + QueryDAGs + self-closure + VCIF
> snapshot round-trip; the 16 CISC sugar verbs, framework_seed
> equivalent, other VCIF profiles, classdef wrapper, and
> edge_strict mode are each catalogued as named promissory
> cells.

Snap valid. The fire produces a working reference kernel **and**
the structural recognitions (geometric currying, kernel-parity)
that make the role first-class in the cotype.

## What this fire does NOT extract

Per discipline rule 6:

- No `KernelImplementation` wrapper above {v4cat, v4cat-octave}.
  At 2 instances the C7 threshold is not met. v4cat (Python)
  remains the systems kernel; v4cat-octave is the algebraic
  peer.
- No `ReferenceCarrier` wrapper above {v4cat-octave}. At 1
  instance the orbit is named, not abstracted.
- No `Parity` wrapper above {kernel-parity, carrier-parity}. The
  parity-discipline orbit is named here so a future third
  parity-species (e.g., MCP-presentation-parity for v4cat-mcp)
  would parameterise it; at three the C7 threshold tips
  toward RFS-eligible.

## The slogan, applied at the kernel level

> v4cat (Python) makes the kernel terrifyingly fast.
> v4cat-octave makes the kernel painfully visible.
> Together they pin down the same algebraic reference -- and
> kernel-parity proves it.
