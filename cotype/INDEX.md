# cotype/ — accumulated shadows of v4cat-as-deliverable

This directory accumulates externalised shadows of v4cat itself,
treated as a self-hosted artefact (Theorem 14.5). Produced by the
`decomposable-by-entailment` fire of 2026-05-02; updated by
`regroup-from-shadows` and `snap-to-grid` fires thereafter.

A shadow here is a *named substructure of v4cat-as-goal* that
survives session boundaries. Each shadow entry states: (1) the
form, (2) where the form is realised in the repo, (3) the
composition operation that assembles instances into the whole, and
(4) the entailment claim that licenses the composition.

The fact that this directory is itself a v4cat-shaped artefact
(named substructures + closure claim) is the framework's design
intent at theory.md § 14: v4cat's deliverable IS the application
of v4cat to v4cat.

## Shadows (DBE fire, 2026-05-02)

- [shadow_cell.md](shadow_cell.md) — the unit of decomposition;
  every primitive is a `Cell(id, kind, desc)`.
- [shadow_dual_representation.md](shadow_dual_representation.md) —
  every primitive has paired IMPL (theory.py) and CAT
  (framework_seed.sql) realisations.
- [shadow_kind_stratification.md](shadow_kind_stratification.md) —
  the 8-way `O,B,W,R,E,A,K,X` partition (Definition 14.1) plus the
  `supported_kinds` refinement that carves scope.
- [shadow_kquery_universal_read.md](shadow_kquery_universal_read.md)
  — kquery as the level-0 read primitive; ≥7 named call sites.
- [shadow_layered_stack.md](shadow_layered_stack.md) — the L0→L7
  entailment chain from kquery up to docs.
- [shadow_docs_quartet.md](shadow_docs_quartet.md) — the
  README/tutorial/methodology/theory progression plus examples.

## Findings (RFS fire, 2026-05-02)

- [rfs_findings.md](rfs_findings.md) — sideways read against the
  six DBE shadows. Four findings, classified per
  shadow-architecture's orbit-saturation rule. One acted-on (RFS
  extraction: views.py duplication removed); three deferred to S2G.

## Shadows + classifications (S2G fire, 2026-05-02)

- [shadow_kquery_orbit.md](shadow_kquery_orbit.md) — the 6 named
  selections of kquery as orbit positions of a saturated orbit;
  Kind.K, not Kind.A.
- [s2g_classifications.md](s2g_classifications.md) — resolutions
  for the three RFS deferrals. Notably *corrects* RFS's "Kind.A
  vestigial" reading: theory.md reserves Kind.A for the
  bicategorical 2-cell lift (§14.6.5) and as the under-promising
  example (§14.6.1), so the slot is deliberately empty, not dead.
- [snap_report.md](snap_report.md) — snap-to-grid check against
  the 2026-05-02 user request. Snap occurred; deliverable
  readable.

## Composition

The shadows compose under **Theorem 14.5's preservation theorem**:

> Additive schema moves on K preserve `ClosureKQ(K, scope).gap = ∅`.

Operationally, the four-step move from `theory.py`'s docstring:
implement → add Cell → catalogue → run closure check. Anything
landing in v4cat passes through this composition or it isn't part
of v4cat.

## Entailment

```text
∀ cells c in scope. (IMPL(c) ↔ CAT(c))
  ⟹ check_closure(cat) returns gap = ∅
  ⟹ v4cat is self-hosting at scope
```

Verified by `tests/test_self_hosting.py::test_closure_check_passes_on_fresh_catalogue`.
118 tests green at 7e02713.
