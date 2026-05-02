# Shadow: Kind stratification (8-way partition)

## Form

`Kind` is an `enum.Enum` with exactly 8 single-letter values
([cells.py:22-35](../cells.py#L22-L35)):

| Code | Meaning |
|------|---------|
| `O`  | objects (and object-introduction operations) |
| `B`  | breaks |
| `W`  | witnesses |
| `R`  | refinements |
| `E`  | schema extensions |
| `A`  | wedge audits |
| `K`  | kquery instances / read operators |
| `X`  | closure-check instances |

The 8 kinds are the codomain of `tag : Cell → Kind`.

## Realisations

- Enum: [cells.py:22-35](../cells.py#L22-L35).
- Cell-distribution under SIGNATURE: O×2, B×3, W×4, R×1, E×1,
  K×3, X×1, A×0 (15 total).
- The scope filter: `Q-supported-claims.supported_kinds`,
  currently `'O,B,W,R,E,K,X'` ([framework_seed.sql:104-106](../framework_seed.sql#L104-L106)).
  Note: `A` (audits) is in the type but not in scope of the
  default closure check — a kind-shaped *shadow gap* worth
  flagging to RFS.

## Property

`P(c) := c.kind ∈ supported_kinds` — the cell's kind is in the
declared closure scope. Cells outside scope are filtered out of
both IMPL and CAT before the kquery runs.

## Composition

```python
universe = ⋃ { c | c ∈ SIGNATURE, c.kind ∈ supported_kinds }
```

Implemented in [bootstrap.enumerate_supported_cells](../bootstrap.py#L143-L177)
and [bootstrap.supported_kinds](../bootstrap.py#L110-L140). The
composition is a *set union over kind-filtered subsets* — which
makes scope a refinement, not a hard constraint.

## Entailment

Restricting to a smaller `supported_kinds` is a *refinement of
scope*. The closure check still runs; gap is computed only over
the filtered universe. This is exactly Definition 14.7 clause 3
(the recursion clause) — scope is itself catalogued and editable
from data, so domain-extension catalogues can opt out of full
self-hosting by leaving `Q-supported-claims` un-witnessed.

## Reuse evidence

8 kinds × any number of cells per kind. Used at every
`enumerate_supported_cells` call (the closure check), and at
every Cell construction (the Kind tag is mandatory). The 8-way
stratification recurs at `theory.py`'s comment-banded sections
(one band per kind), at `framework_seed.sql`'s comment bands,
and implicitly at the directory layout (catalogue.py = O+B+W+R,
views.py = K, bootstrap.py = X, etc.).

## Open question for RFS

Kind `A` (wedge audit) is declared in the type but no SIGNATURE
cell uses it, and `wedge` lives in [views.py](../views.py) without
a corresponding Cell entry. Either (a) wedge should be added to
SIGNATURE as `Kind.A`, (b) `A` should be removed from `Kind` and
from the supported_kinds list (currently it isn't there), or
(c) the asymmetry is intentional and should be documented. RFS
should classify which.
