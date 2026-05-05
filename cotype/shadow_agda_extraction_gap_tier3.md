# Shadow: Agda extraction gap (Tier 3, promissory cell)

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> **At orbit-position 1** of the Tier-3 expansion; per discipline
> rule 6, S2G to catalogue the gap. Each Tier-3 item is a candidate
> for a future small fire that adds it to the extractor.*

## Form

agda2v4cat v0.1 covers Tiers 1 + 2 of the kquery 10-cell against
vcif's existing `agda-import.json` fixture — 15 of 25 named items.
This shadow names the **10 deferred Tier-3 items** so future fires
can pick them up from named substructure.

## The 10 deferred items

Each item names what to extract, where it lives in Agda, and the
node-kind / edge-kind it would emit when implemented.

### 14. Pragmas

- **Source**: `Agda.Syntax.Concrete.Pragma` (`COMPILE`, `INLINE`,
  `NO_POSITIVITY_CHECK`, `NON_TERMINATING`, `STATIC`, `DISPLAY`,
  `FOREIGN`, `BUILTIN`, `OPTIONS`, …).
- **Emits**: node-kind `agda-pragma`; edge-kind `has-pragma`
  (def → pragma) plus per-pragma payload edges.

### 15. Termination metadata

- **Source**: `Agda.Termination.TerminationCheck` output;
  `funTerminates` flag in `FunctionData`.
- **Emits**: node-kind `agda-termination-status` (`Terminating`,
  `MaybeTerminating`, `NonTerminating`, `Inlined`); edge-kind
  `has-termination-status`.

### 16. Coverage check status

- **Source**: `funCovering` flag.
- **Emits**: node-kind `agda-coverage-status`; edge-kind
  `has-coverage-status`.

### 17. Polarity / variance

- **Source**: `defPolarity` per definition.
- **Emits**: node-kind `agda-polarity` (`Covariant`, `Contravariant`,
  `Invariant`, `Nonvariant`); edge-kind
  `has-polarity` (def-arg-position → polarity).

### 20. Foreign declarations

- **Source**: `Agda.TypeChecking.Monad.Base.Foreign` block.
- **Emits**: node-kind `agda-foreign-block`; edge-kind
  `has-foreign-binding`.

### 21. Open / using / hiding / renaming

- **Source**: `Agda.Syntax.Concrete.ImportDirective`.
- **Emits**: node-kinds `agda-import`, `agda-renaming`; edge-kinds
  `imports-module`, `renames-name`, `hides-name`.

### 22. Pattern synonyms

- **Source**: `PatternSynDefn` in the `Definition`'s `theDef`.
- **Emits**: node-kind `agda-pattern-synonym`; edge-kind
  `has-pattern-synonym-arg`.

### 23. Generalizable variables

- **Source**: `GeneralizableVar` in `Defn`.
- **Emits**: node-kind `agda-generalizable-var`; edge-kind
  `is-generalizable`.

### 24. Where-clause local definitions

- **Source**: nested anonymous `QName`s inside `Clause` /
  `clauseTel`.
- **Emits**: node-kind `agda-where-defn`; edge-kind `has-where-defn`
  (clause → where-defn).

### 25. Mutual blocks

- **Source**: Agda's mutual-info attribution; defs sharing a
  `MutualId`.
- **Emits**: node-kind `agda-mutual-block`; edge-kind
  `in-mutual-block`.

## Why deferred

Each Tier-3 item requires walking a different part of Agda's AST
(pragmas via concrete syntax; termination via the termination
checker's output; mutual blocks via mutual-info attribution).
Collectively too much for v0.1. Each is small enough to be its own
v0.x fire.

## Lattice classification

Region **#4 (S2G alone — pure cataloguing)**, by exception.
Registers the 10-item structural design space; no implementation.

## Closure

Each Tier-3 item closes incrementally as v0.x fires implement it.
Recommended grouping for future fires:

| Future fire | Items |
| --- | --- |
| `agda2v4cat-pragmas` (v0.2 sub-fire) | 14 (pragmas) |
| `agda2v4cat-termination` | 15, 16 (termination + coverage) |
| `agda2v4cat-modalities-deeper` | 17 (polarity) |
| `agda2v4cat-foreign-and-imports` | 20, 21 |
| `agda2v4cat-advanced-defs` | 22, 23, 24 |
| `agda2v4cat-mutual` | 25 |

When all are closed, this shadow is annotated with the closure
trail per the catalogue-thickens-forward discipline.

## Tier-3 design surface preserved

By naming each item's expected node-kind and edge-kind here, a
future fire picks up from named substructure rather than
re-deriving the design. This is the DBE skill's "shadow as
context-loss residue" working at meta-level: even if no v0.2 fire
happens for years, the design space is captured.
