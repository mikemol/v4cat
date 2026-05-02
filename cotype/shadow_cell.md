# Shadow: Cell-as-unit-of-decomposition

## Form

```python
@dataclass(frozen=True)
class Cell:
    id: str
    kind: Kind         # one of O, B, W, R, E, A, K, X
    description: str = ''
```

The atomic unit of v4cat's self-cataloguing. Two Cells are equal
iff `(id, kind)` match; description is informational. Cells are
hashable, frozen, JSON-friendly via `Kind(str, Enum)`.

## Realisations

- Type definition: [cells.py:38-56](../cells.py#L38-L56).
- Instance enumeration (15 cells): [theory.py:28-90](../theory.py#L28-L90).
- Tag projection: `tag(c) = c.kind`, level-blindness per
  Lemma 14.1 ([cells.py:59-66](../cells.py#L59-L66)).

## Property

`P(c) := IMPL(c) ↔ CAT(c)` — the cell is implemented in code AND
catalogued in the framework seed. This is what `check_closure`
audits cell-by-cell.

## Composition

Cells compose by **set union** under the supported-kinds filter:

```
impl_ids = { _catalogue_id_for(c) | c ∈ SIGNATURE, c.kind ∈ supported_kinds }
cat_ids  = { break_number | (spec, break_number) ∈ witnesses, spec='framework' }
```

The composition is implemented in
[bootstrap.py:enumerate_supported_cells](../bootstrap.py#L143-L177).

## Entailment

```
P(c) for every c in scope ⟹ kquery(IMPL, CAT, IMPL ∪ CAT).gap = ∅
                          ⟹ self-hosting closure (Theorem 14.5)
```

## Reuse evidence

15 instances in `SIGNATURE` (theory.py); 13 paired catalogue rows
in `framework_seed.sql`; 8 kinds in `Kind`. The Cell-as-unit
pattern recurs every time the framework adds a primitive — that
recurrence is the costructure's reuse and the reason it qualifies
as a shadow rather than a one-off type.
