# Shadow: Agda extraction gap — open / using / hiding / renaming (Tier 3, item 21)

**Tracking**: [v4cat-oss/agda2v4cat#7](https://github.com/v4cat-oss/agda2v4cat/issues/7) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> One of ten per-item Tier-3 promissory shadows. Region **#4** (S2G
> alone — pure cataloguing).*

## Form

Item **21** of the agda2v4cat extraction kquery 10-cell. agda2v4cat
v0.1 extracts cross-module `references-def` edges but does not
preserve the **import directives** (`open M using (foo); rename
(bar to baz); hiding (quux)`) that govern how a name is brought
into scope. The design surface is named here.

## What to extract

- **Source in Agda**: `Agda.Syntax.Concrete.ImportDirective`. Lives
  in the *concrete* syntax (not `Agda.Syntax.Internal`), so the
  walk has to grab the per-module `ImportDirective`s before they
  are scope-checked away. They are preserved on the typechecked
  Interface.
- **Per-directive content**: the imported module's name, plus the
  using/hiding/renaming clauses.

## Expected emission

| Slot | Identifier |
| --- | --- |
| Node-kinds | `agda-import`, `agda-renaming` |
| Edge-kinds | `imports-module`, `renames-name`, `hides-name` |

`agda-import` is one node per `import` statement; its outgoing
edges (`imports-module`, `renames-name`, `hides-name`) attach the
imported module + per-directive specifications.

## Why deferred from v0.1

Import-directives are concrete-syntax data, distinct from v0.1's
`Defn`-internal walks. Captures the *scoping* dimension that v0.1
elides. Small enough to share a v0.2 sub-fire with item 20
(foreign declarations).

## Future fire

`agda2v4cat-foreign-and-imports` (v0.2 sub-fire — shared with
item 20).

## Closure

Closes when agda2v4cat ≥ v0.2 emits at least one `agda-import`
node per `open M ...` statement on the existing fixture modules,
with appropriate `imports-module` edges and any `renames-name` /
`hides-name` edges per directive clause.
