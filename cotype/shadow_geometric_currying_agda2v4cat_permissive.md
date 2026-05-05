# Shadow: geometric currying — agda2v4cat permissive importer (promissory)

**Tracking**: [v4cat-oss/agda2v4cat#12](https://github.com/v4cat-oss/agda2v4cat/issues/12) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_geometric_currying.md](shadow_geometric_currying.md)).
> Region **#4** (S2G alone — pure cataloguing).*

## Form

`agda2v4cat` (the catalogue source extracting Agda definitions to
VCIF) currently emits edges that pre-suppose every endpoint
exists. Concretely, the v0.1 importer ([Vcif.hs][vcif-hs]) emits:

[vcif-hs]: https://github.com/v4cat-oss/agda2v4cat/blob/main/src/Agda2V4cat/Vcif.hs

```haskell
-- Each definition first emits its kind anchor + name anchor + def node,
-- then emits relationship edges to those anchors.
[ nodeJson "kind:AgdaFunction" ...
, nodeJson "name:foo" ...
, nodeJson "def:foo" ...
, edgeJson "def:foo" "name:foo"          "defines-name"
, edgeJson "def:foo" "kind:AgdaFunction" "has-kind"
]
```

The order is enforced by the importer: anchor-introductions
before relationship edges. This is *operational discipline* in
the absence of geometric currying.

Under geometric currying, **the order doesn't matter**. The
importer can emit edges first; the boundary nodes close as the
catalogue receives them. Validation shifts from
"endpoint pre-existence" to "boundary closure."

## What to extract

### Permissive emission order

The importer emits every relationship edge as soon as the
relationship is *known*, without first ensuring the endpoint
nodes are emitted. The receiving v4cat catalogue's
geometric-currying layer (shipped via
[`shadow_geometric_currying_v4cat_refactor.md`](shadow_geometric_currying_v4cat_refactor.md))
introduces missing nodes via `bind_role` as needed.

This makes the importer code substantially simpler:

```haskell
-- Before (current v0.1):
ensureKindAnchor "kind:AgdaFunction"
ensureNameAnchor "name:foo"
introduceDef "def:foo"
edge "def:foo" "name:foo"          "defines-name"
edge "def:foo" "kind:AgdaFunction" "has-kind"

-- After (geometric currying):
edge "def:foo" "name:foo"          "defines-name"
edge "def:foo" "kind:AgdaFunction" "has-kind"
-- That's it. Endpoint nodes are introduced as boundary closures.
```

The reduction is real: the entire `ensureKindAnchor` /
`ensureNameAnchor` ceremony goes away, replaced by trust in the
receiver's geometric-currying semantics.

### Validation invariant

The importer becomes a **boundary-closure-discharger**. For
every edge it emits, the receiver's cell layer:

1. Introduces the edge-cell.
2. Binds three role-bindings (source, kind, target).
3. Closes the boundary (since all three role-occupants are now
   identifiable by name).
4. Closes the cell.

The importer's correctness criterion is:

> Every edge it emits has a closeable boundary in the receiving
> catalogue.

Unclosed boundaries are residue — the receiver flags them via
`T-edge-boundary-closure` (one of the four bootstrap closure
recognizers from the v4cat-core sub-fire).

### v0.1 promissory: Tier-3 items

agda2v4cat's existing 10 Tier-3 promissory shadows
([per the agda2v4cat fire](shadow_agda2v4cat_distribution.md))
become *more* feasible under geometric currying: extracting a
new Agda construct now means emitting the edges; the cell
boundaries close as the catalogue receives them.

This sub-fire is therefore a *prerequisite* for the
agda2v4cat-Tier-3 sub-fires landing cleanly — they should land
*after* this one.

## Why deferred from the substrate-naming fire

agda2v4cat is downstream of v4cat-core. This sub-fire is a
relatively small change (delete pre-emission ceremony; trust
geometric currying); it's deferred because it depends on
`gc-v4cat-core` shipping the cell layer first.

## Future fire

`gc-agda2v4cat-permissive`. Region #6 expected (DBE+S2G — adds
the permissive emission code path; removes the pre-emission
ceremony as RFS regrouping). Closure-scope: single-repo (writes
only land in `v4cat-oss/agda2v4cat`).

Strict ordering: lands **after** `gc-v4cat-core`; lands
**before** any of the 10 agda2v4cat-Tier-3 sub-fires.

## Closure path

Closes when agda2v4cat ≥ v0.x ships:

1. Permissive emission order in `Vcif.hs` (no
   `ensureKindAnchor` / `ensureNameAnchor`).
2. End-to-end smoke test using a v4cat-core build with the
   geometric-currying layer, confirming all boundaries close.
3. Promissory annotation on each of the 10 Tier-3 shadows
   updated to reflect that the simpler permissive emission is
   the path forward.
