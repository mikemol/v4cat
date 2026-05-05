# Shadow: v4cat-octave edge_strict (promissory cell)

**Tracking**: [v4cat-oss/v4cat-octave#6](https://github.com/v4cat-oss/v4cat-octave/issues/6) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_v4cat_octave_distribution.md](shadow_v4cat_octave_distribution.md)).
> Region **#4** (S2G alone -- pure cataloguing).*

## Form

The user's brief surfaces a structurally important pair:

> The stricter version can separate:
>
> ```text
> edge_saturating:
>   introduces source, kind, target as needed
>
> edge_strict:
>   emits residue if source/kind/target are not already closed
> ```
>
> For Octave, start saturating.

`v4cat-octave` v0.1 ships only the **saturating** mode -- the
geometric-currying invariant. The strict-mode complement is
catalogued here.

## What to implement

A new `+v4cat/edge_strict.m` function with the same signature as
`edge` but different behaviour:

```octave
function [cat, eid, residue] = edge_strict (cat, source_name, kind_name, target_name)
  ## If any of source / kind / target is not already a node, do
  ## NOT introduce it. Instead, return the missing names in the
  ## residue list and refuse to record the edge.
  ...
endfunction
```

Returns:

| Return | Meaning |
| --- | --- |
| `cat` | unchanged on residue; updated on success |
| `eid` | `uint64(0)` on residue; the edge index on success |
| `residue` | cell array of names that weren't pre-introduced (empty on success) |

Conversely, the existing `edge.m` (geometric currying) can be
renamed `edge_saturating.m` with `edge.m` becoming a thin alias
that calls into the saturating form (preserving v0.1 callers).
That rename is part of this future fire.

## Pairing with the framework_seed shadow

`edge_strict` is meaningful only when there's something to be
strict against. The natural pairing is with the framework_seed
shadow ([shadow_v4cat_octave_framework_seed.md](shadow_v4cat_octave_framework_seed.md)):

- Saturating mode: useful for prototyping, geometric-currying,
  ingesting unstructured input. v0.1 default.
- Strict mode + framework seed: useful for type-checked workflows
  where every node-kind / edge-kind must be pre-declared.

The two future fires are best landed together as a single
`v4cat-octave-strict-mode` sub-fire that introduces both pieces.

## Why deferred from v0.1

The geometric-currying invariant is the v0.1 disposition. Strict
mode is an opt-in alternate, not a default replacement. v0.1
should be **fluid** -- the brief's slogan emphasizes obviousness
of geometry, which is best-served by saturating defaults.

## Future fire

`v4cat-octave-edge-strict` (paired with
`v4cat-octave-bootstrap` per [shadow_v4cat_octave_framework_seed.md](shadow_v4cat_octave_framework_seed.md)).

## Closure

Closes when v4cat-octave ≥ v0.x:

1. Adds `+v4cat/edge_strict.m`.
2. Adds an opt-in mode flag on the catalogue (e.g.
   `cat.strict_mode = true`) that makes `node` and `edge`
   default to the strict variant.
3. Has a test asserting that strict mode emits residue (rather
   than introducing nodes) on `edge(cat, "unknown_a",
   "unknown_k", "unknown_b")` when none of the three has been
   pre-introduced.
4. Documents the saturating ↔ strict choice in README + `docs/spec.md`.
