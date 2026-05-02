# Shadow: Dual representation (IMPL ↔ CAT)

## Form

Every primitive of v4cat is realised at *two* aligned sites:

1. **IMPL site** — a `Cell` entry in `theory.py:SIGNATURE`.
2. **CAT site** — a `(breaks row, witnesses row)` pair in
   `framework_seed.sql`, addressed by `Q-{cell.id}` (or by
   `cell.id` directly when it already starts with `Q-`).

Linked by [bootstrap._catalogue_id_for](../bootstrap.py#L61-L69).

## Realisations

- The two predicates: [bootstrap.IMPL](../bootstrap.py#L72-L79)
  and [bootstrap.CAT](../bootstrap.py#L82-L103).
- The naming convention: `_catalogue_id_for` — drops a leading
  `Q-` if present, else prepends one. This *is* the dual-rep
  morphism; it has only this one mathematical role.
- 15 paired instances at [framework_seed.sql:38-98](../framework_seed.sql#L38-L98).

## Property

`P(c) := IMPL(c) ∧ CAT(c)` — cell exists at both sites. The
asymmetric failures are named:

- **gap.10 (implicit)**: IMPL holds, CAT fails — code without
  catalogue. The framework is doing something it hasn't told the
  catalogue about.
- **gap.01 (promissory)**: CAT holds, IMPL fails — catalogue
  without code. The framework promised something it hasn't
  delivered.

Both are surfaced in `SelfHostingViolation`'s payload
([bootstrap.py:36-54](../bootstrap.py#L36-L54)) — Corollary 14.5.1's
constructive to-do list.

## Composition

The composition operation is the **four-step move** from
[theory.py:9-13](../theory.py#L9-L13):

```
add_primitive(impl, cell, seed_rows):
    1. Implement impl in catalogue.py / views.py / mcp_server.py
    2. Add Cell to SIGNATURE
    3. Add (breaks, witnesses) rows to framework_seed.sql
    4. Run check_closure; if green, commit
```

Steps 1+3 alone (no Cell) → implicit. Steps 2+3 alone (no impl) →
promissory. Only the full four-step move preserves self-hosting.

## Entailment

The four-step move preserves `ClosureKQ(K, scope).gap = ∅`. This
is the preservation theorem catalogued at
`Q-bootstrap-closure.preservation_theorem` — itself a refinement
inside the framework, so the entailment is reflectively
catalogued ([framework_seed.sql:107-108](../framework_seed.sql#L107-L108)).

## Reuse evidence

15 paired sites. The morphism `_catalogue_id_for` is the only
function in the codebase whose sole purpose is to mediate this
duality — its existence is structural evidence the dual-rep
pattern is the canonical home of these 15 alignments.
