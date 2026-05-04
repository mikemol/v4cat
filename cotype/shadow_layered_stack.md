# Shadow: Layered deliverable stack (L0 → L7)

## Form

v4cat's deliverable is an 8-layer entailment chain. Each layer
depends only on layers below it.

| L | Layer | Module(s) | Depends on |
|---|-------|-----------|------------|
| L0 | Klein-four read primitive | [views.py](../views.py) (`kquery`) | — |
| L1 | Schema (S0–S11 framework breaks) | [schema.sql](../schema.sql) | L0 |
| L2 | ISA (verbs) | [catalogue.py](../catalogue.py) (`SymmetryCatalogue`) | L1 |
| L3 | Analytic views | [views.py](../views.py) (named selections) | L0, L1, L2 |
| L4 | MCP server (transport) | [mcp_server.py](../mcp_server.py), [sandbox.py](../sandbox.py) | L2, L3 |
| L5 | Closure check | [bootstrap.py](../bootstrap.py), [cells.py](../cells.py), [theory.py](../theory.py) | L0–L3 |
| L6 | Self-cataloguing seed | [framework_seed.sql](../framework_seed.sql) | L1, L5 |
| L7 | Documentation | [README.md](../README.md), [tutorial.md](../tutorial.md), [methodology.md](../methodology.md), [theory.md](../theory.md), [examples.md](../examples.md) | L0–L6 |

## Realisations

The directory layout mirrors the stack: 9 source files at the
project root, ~one per layer (with L5 and L7 spread across
multiple files). Tests are layered correspondingly:
[tests/test_isa.py](../tests/test_isa.py) covers L0–L3,
[tests/test_mcp.py](../tests/test_mcp.py) covers L4,
[tests/test_sandbox.py](../tests/test_sandbox.py) covers L4's
slot validator,
[tests/test_self_hosting.py](../tests/test_self_hosting.py)
covers L5+L6.

## Property

Each layer's contract is satisfied iff the layers below pass
their tests. The test suite respects the stratification: failing
L0 fails L3+; failing L1 fails L2+; etc.

## Composition

Layered re-export plus dependency injection. `__init__.py`
re-exports L0+L3 (`kquery`, `wedge`, `agree`, ...) and L2
(`SymmetryCatalogue`); L4 imports L2 directly; L5 takes a
catalogue (L2) as input and reads from L1+L6.

## Entailment

```
L0 sound ⟹ L1 readable
L0,L1 sound ⟹ L2 sound (verbs are kquery-mediated reads/writes)
L2 sound ⟹ L3 derivable (named selections of kquery)
L2,L3 sound ⟹ L4 sound (MCP just exposes them)
L0–L3 sound + L6 loaded ⟹ L5 passes ⟹ self-hosting
```

The tests verify each implication independently. The CI gate is
that all four test files pass — currently 36+38+28+16 = 118
tests at commit `7e02713`.

## Reuse evidence

The layering pattern recurs in any *domain extension* of the
framework: the user's domain schema is a parallel L1', the
domain views are a parallel L3', and the closure check still
runs at L5 because supported_kinds is data, not code.
[README.md:144-152](../README.md#L144-L152) describes this
extension protocol.

## Algebraic anchor (2026-05-04 cont'd)

Re-read under
[shadow_assertion_history_group.md](shadow_assertion_history_group.md):
L0 (kquery) is the **V₄-coordinate-chart layer** of the
observer-pair group action; everything above L0 is a downstream
projection or further-quotient of that chart. L1 (schema.sql)
admits the basis `𝔄_node ⊔ 𝔄_edge` over which `H = ℤ^𝔄` is
constructed; L2 (ISA verbs) is the forward-monotone facet of
group translation; L5 (closure check) is the V₄-coordinate audit
of the framework's own self-hosting orbit (Theorem 14.5
strengthens to: gap = ∅ iff the framework's assertion-history is
visible under its own observer-coordinate action). See
[theory.md § 15](../src/v4cat/theory.md), especially § 15.5 and § 15.15.F.
