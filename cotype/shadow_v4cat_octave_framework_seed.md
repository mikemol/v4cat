# Shadow: v4cat-octave framework_seed gap (promissory cell)

**Tracking**: [v4cat-oss/v4cat-octave#3](https://github.com/v4cat-oss/v4cat-octave/issues/3) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_v4cat_octave_distribution.md](shadow_v4cat_octave_distribution.md)).
> Region **#4** (S2G alone -- pure cataloguing).*

## Form

v4cat (Python) auto-bootstraps a self-cataloguing **framework
seed** at every catalogue open: the 5 node-types (`node-type`,
`break`, `spec`, `tension`, `edge-kind`) plus 18 schema-witness
edge-kinds plus 10 K-ATTR-* attribute breaks. This is what makes
v4cat's `introduce_node` / `edge` operations *type-strict*: they
validate against schema-witnessed type-system seed before
writing.

`v4cat-octave` v0.1 has no equivalent. Its `node` + `edge`
primitives are *saturating-only*: anything goes, by name. The
geometric-currying invariant means edges introduce their boundary
nodes; type-checking is absent.

This shadow names the design surface for porting the framework
seed to Octave so type-strict mode becomes reachable.

## What to extract

Source: [`v4cat/src/v4cat/framework_seed.sql`](https://github.com/v4cat-oss/v4cat/blob/main/src/v4cat/framework_seed.sql)
(350+ lines).

| Section | Octave equivalent |
| --- | --- |
| 5 node-type tokens (`node-type` self-typed, `break`, `spec`, `tension`, `edge-kind`) | rows in a `cat.node_types` struct-of-arrays |
| 18 schema-witness edge-kinds (incl. `K-SOURCE-TYPE`, `K-TARGET-TYPE`, `requires-attr`, `admits-attr`, plus the witness-graph + lineage-graph kinds) | introduced as nodes via `v4cat.node(cat, "K-...")` and recognised by name in introduce-time validators |
| 10 K-ATTR-* attribute breaks (K-ATTR-NUMBER / NAME / YEAR / CATALOGUE-ORDER / NOTES / ID / DISPOSITION / PARAMETERS / SHAPE / SHORT-DESC) | similar; their names anchor schema validation |
| 19 `Q-prefixed` ISA-operation breaks (Q-introduce_node, Q-edge, Q-kquery, etc.) | catalogued for self-hosting closure (some already implicit in v4cat-octave's 9-claim self_closure; the full Q-prefix surface is broader) |
| Bootstrap `framework` spec + Q-supported-claims + Q-bootstrap-closure | a single `bootstrap_seed.m` that calls the appropriate `node`/`edge` operations on a fresh catalogue |

## Why deferred from v0.1

The framework seed is only meaningful in *type-strict* mode. v4cat-octave
v0.1 is saturating-only by design (the geometric-currying
invariant is the explicit choice). Type-strict mode is the
complement, named separately in
[shadow_v4cat_octave_edge_strict.md](shadow_v4cat_octave_edge_strict.md).

The framework seed is the *data half* of type-strict mode; the
edge_strict primitive is the *operation half*. Both need to land
together to produce a meaningful type-strict mode.

## Future fire

`v4cat-octave-bootstrap`. Likely paired with the
`v4cat-octave-edge-strict` sub-fire so type-strict mode is
end-to-end usable when both close.

## Closure

Closes when v4cat-octave ≥ v0.x ships:

1. A `bootstrap_seed.m` that lands the 5 node-types + 18
   schema-witness edge-kinds + 10 K-ATTR-* breaks on a fresh
   catalogue.
2. Validation hooks in `node` / `edge` that consult the seed
   (only when type-strict mode is enabled; saturating remains
   the default for the geometric-currying mode).
3. A test that imports v4cat (Python)'s framework_seed.sql
   equivalent and asserts the resulting Octave catalogue passes
   the same `check_closure` predicate (bootstrapping = no gap).
