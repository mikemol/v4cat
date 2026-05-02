# Shadow: kquery orbit (saturated)

## Form

The 6 named-selection functions in [views.py](../views.py) are
**orbit-elements of kquery under fixed `emit`-mask + projection**:

| Named selection | kquery generator |
|-----------------|------------------|
| `agree(a, b)`         | `kquery(a, b, emit={11})['11']` |
| `left_residue(a, b)`  | `kquery(a, b, emit={10})['10']` |
| `right_residue(a, b)` | `kquery(a, b, emit={01})['01']` |
| `blind(a, b, U)`      | `kquery(a, b, U, emit={00})['00']` |
| `coverage(a, b)`      | `kquery(a, b, emit={10,01,11})` flattened |
| `wedge(a, b)`         | `kquery(a, b, emit={10,01,11})` reformatted |

Each named selection is `kquery` applied with a particular `emit`
subset of `2^{00,01,10,11} = 16` possible cell-projections. The
orbit's *generator* is kquery; the orbit's *positions* are choices
of `emit`.

## Property

The orbit is **saturated** for the named-selection use cases the
framework currently exposes: every named selection corresponds to
a non-empty subset of the four V₄ cells, and the 6 functions cover
the practically-meaningful subsets.

The orbit could grow if new emit-subsets become useful (e.g.,
"only the asymmetric cells" = `{10,01}` is *exactly* `wedge`'s
cell selection; "everything but blindness" = `{10,01,11}` =
`coverage`). The 6 currently-named selections + the universal
4-cell `kquery` itself = 7 orbit positions out of 16.

## Composition

Composition is **kquery itself with parameter substitution**:

```
named_selection(a, b, ...) := postprocess ∘ kquery(a, b, ..., emit=mask)
```

Where `postprocess` is `flatten`, `reformat`, or `pick(cell)`
depending on the named selection.

## Entailment

**Per orbit-saturation discipline (rule 6 of `shadow-architecture`):**
the named selections quotient under "instances of kquery at fixed
mask." Extracting them into separate Cells under their own kind
would be **wrapper-extraction of an existing operator** (the
operator already serves as the universal). They are correctly
classified as `Kind.K` (kquery instances), not `Kind.A` or any
new kind.

This is the case where C7's "≥3 instances → universal record"
threshold misfires: the recurrence is orbit-driven, not free
duplication.

## Catalogue position

`Q-kquery` is the orbit generator. The 6 named selections are
implicit orbit positions of `Q-kquery` — they need not be
catalogued as separate breaks. The MCP server's
`catalogue://wedges`-style resources, if added later, should
expose them as *projections* of the kquery resource, not as
peer breaks.

## Reuse evidence

7 functions in views.py (kquery + 6 named selections); used at
≥1 closure-check call site (`closure_status`); plus every domain
query a user writes via the MCP `kquery_tool`. The orbit is the
shape; each call is a position.

## Origin

This shadow was identified during the S2G fire of 2026-05-02 in
response to RFS's Finding 3 (Kind.A vestigial slot). RFS deferred
the orbit classification to S2G; S2G externalised it.
