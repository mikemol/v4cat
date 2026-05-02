# Shadow: kquery as universal read primitive

## Form

```
kquery(A, B, universe=U) → { '11': [...], '10': [...],
                              '01': [...], '00': [...] }
```

Klein-four classifier: every element of `U` lands in exactly one
of four cells per its membership in `A` and `B`. The four cells
are the V₄ group elements; every named read in v4cat is a
selection of one or more cells.

## Realisations

- Implementation: [views.py](../views.py) (the file's primary
  export).
- Cell entry: `Cell('kquery', Kind.K, ...)` in
  [theory.py:70-71](../theory.py#L70-L71).
- Catalogue row: `Q-kquery` in
  [framework_seed.sql:68-69](../framework_seed.sql#L68-L69).

## Named call sites (≥7)

The reuse evidence — kquery is the form, these are the instances:

1. **`agree`** (cell 11) — set intersection.
2. **`left_residue`** (cell 10) — A \ B.
3. **`right_residue`** (cell 01) — B \ A.
4. **`blind`** (cell 00) — universe minus (A ∪ B).
5. **`coverage`** (cells 11+10+01) — union, "anything seen by
   either side."
6. **`wedge`** (cells 10+01) — symmetric difference.
7. **`closure_status`** ([bootstrap.py:206-227](../bootstrap.py#L206-L227))
   — kquery(IMPL, CAT, IMPL ∪ CAT) — the framework reads itself.

Plus inside the closure check: `check_closure` raises iff cells
`10` or `01` are non-empty — also a kquery-result inspection.

## Composition

Each named selection is `kquery(A, B, U)` followed by a fixed
projection onto a subset of the four cells. The projection is the
composition operation; kquery itself is the costructure.

## Entailment

Lemma 14.1 (level-blindness): kquery does not consult `tag`.
Therefore *every* read at any level of the framework — the
catalogue's own data, the framework's self-cataloguing, and the
domain extension's data — uses the same primitive. There is no
level-2 read that doesn't reduce to a level-0 kquery on a
sub-universe.

This is what licenses calling kquery the *universal* read primitive.

## Reuse evidence

7 named selections + 1 closure-check site + every domain query
written by users via the MCP server's `kquery_tool`. Strong
multi-site reuse; satisfies the costructure-without-reuse warning.
