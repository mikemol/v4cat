# Shadow: workspace certification — V₄-closure-check at workspace scope

> *DBE+RFS+S2G fire of 2026-05-04 (G2 closure). Region #8 of the
> shadow-architecture lattice. Algebraic anchor:
> [shadow_assertion_history_group.md](shadow_assertion_history_group.md).
> Operationalised at [v4cat-oss/v4cat-certify](https://github.com/v4cat-oss/v4cat-certify).*

## Form

The **second instance** of v4cat's self-hosting closure pattern,
lifted from framework-internal scope to workspace-wide scope. Where
Theorem 14.5 ([theory.md § 14][theory14]) checks that the framework's
own primitives are honest, **v4cat-certify** checks that the
workspace's structural commitments are honest.

[theory14]: ../src/v4cat/theory.md

```text
                     U = declared workspace claims
                          │
            kquery        ▼            kquery
            (V₄ chart, theory.md § 15.5)
   ┌──────────────────┬──────────────────┐
   │                  │                  │
   ▼                  ▼                  ▼
   A = implemented    B = catalogued     U = declared
   (check passes)     (witness exists)
            │                  │
            └──────────────────┴───────► χ_{A,B}: U → V₄
                                          │
                                          ▼
                              {00, 01, 10, 11} cells
                                          │
                                          ▼
                              PASS iff 10 = 01 = 00 = ∅
```

## Where realised

- **Repo**: [v4cat-oss/v4cat-certify](https://github.com/v4cat-oss/v4cat-certify) v0.1.
- **WorkspaceClaim** type + **WORKSPACE_CLAIMS** list in
  `src/v4cat_certify/claim.py`. Eight initial claims.
- **Implementation checks**: `src/v4cat_certify/checks.py`. Eight
  functions, one per claim.
- **V₄ runner**: `src/v4cat_certify/runner.py`. Computes
  `kquery(implemented, catalogued; declared)`.
- **Three-substrate emitters**: `src/v4cat_certify/reports.py`.
  Emits the closure-report in vcif JSON, vcif-rdf Turtle, and
  vcif-hlo JSON tensor dump simultaneously.
- **CLI**: `v4cat-certify {run, report, claims, status}`.
- **Tests**: 37 green; including 4 cross-substrate parity tests
  verifying the three emissions classify identically.

## Composition operation

`certify(workspace_root) → CertificationResult`. The result carries:

- `universe`: declared claim ids.
- `cells`: per-V₄-cell list of claim ids.
- `passing`: bool (True iff cells 10, 01, 00 are all empty).

The all-three-substrate emission is the meta-level cross-substrate
parity check: the certification suite is itself certified across
substrates.

## Entailment

```text
∀ workspace W. certify(W).passing
  ⟺
  every declared structural commitment of W
  has a working implementation_check AND a catalogue_witness file.
```

Equivalent to: **the workspace honors every structural commitment it
claims**. This is the workspace-scope analogue of Theorem 14.5's
gap-empty closure invariant.

## Lattice classification

Region **#8 (DBE + RFS + S2G — substantive structural arc)**.

- **DBE (heavy)**: forward design of `WorkspaceClaim`,
  closure-report-generation in three substrates, the certification
  CLI surface. New costructure with no parallel in existing repos.
- **RFS**: regroups two existing patterns:
  - Manual audit (`audit_workspace_*.md` shadows) → automated
    closure-check.
  - The V₄-closure-check pattern from Theorem 14.5 → applied at
    workspace scope.
- **S2G**: this file. Plus G2 marked closed in
  [audit_workspace_2026_05_04.md](audit_workspace_2026_05_04.md).

### Discipline rule 6 (orbit-saturation) check

The V₄-closure-check pattern now has **2 instances**:

| Instance | Scope X | Realised in |
|---|---|---|
| Theorem 14.5 | framework-internal — own primitives | [v4cat/src/v4cat/bootstrap.py](../src/v4cat/bootstrap.py) |
| **v4cat-certify** | workspace-wide — workspace claims | [v4cat-oss/v4cat-certify](https://github.com/v4cat-oss/v4cat-certify) |

Below the C7 ≥3 threshold for free-duplication extraction. The
recurrence is **orbit-driven** (parameterised by scope X). Per
discipline rule 6: **S2G to catalogue, no `ClosureCheck` wrapper
extracted**. v4cat itself remains the universal at the kernel-cell.

A future third instance (e.g., closure check over user-domain
claims when a user deploys v4cat in production) would tip this into
RFS-eligible territory. For now, two parallel rows.

## Trace-integrity

Prior shadows preserved:

- [shadow_assertion_history_group.md](shadow_assertion_history_group.md)
  — algebraic universal unchanged. The certification is one more
  application of `kquery_U(A, B)` per theory.md § 15.5.
- [shadow_carrier_grid.md](shadow_carrier_grid.md) — three
  substrate columns unchanged. v4cat-certify is **not** a fourth
  column; it's a different role (workspace audit) that *emits
  across* the existing three.
- [audit_workspace_2026_05_04.md](audit_workspace_2026_05_04.md) —
  G2 marked closed; gap registry now reads "G2 closed; G3, G4 open".
  Trajectory table gains fire #9.

## Snap-to-grid check

User's request: "Sounds like g2 should land as a certification suite."

Cotype's entailment after this fire lands: "v4cat-oss is now a
self-certifying workspace. The framework certifies itself
internally (Theorem 14.5); the workspace certifies itself externally
(v4cat-certify). Both run the same V₄ pattern at different scopes;
both emit the same shape of closure-report."

Snap valid. The certification suite framing closes G2 *and* makes
the placement structurally honest *and* generalises the V₄-closure-
check pattern to a second instance — three deliverables from one
fire.

## What this fire does NOT extract

Per discipline rule 6:

- No `ClosureCheck` wrapper above {Theorem 14.5, v4cat-certify}.
- No `Audit` wrapper above {manual `audit_*.md`, automated
  v4cat-certify}.
- No fourth substrate column. v4cat-certify *consumes* the three
  existing substrates; it does not extend the carrier grid.

## The slogan, applied at the workspace level

> v4cat audits its own framework via Theorem 14.5.
> v4cat-certify audits the workspace via the same V₄ pattern.
> Same observer-pair group action, different scope.

Tighter:

> The workspace knows what it knows; certification verifies what it has.
