# Shadow: Documentation depth-quartet (+1)

## Form

The five documentation files form a graded entailment ladder.
Each level expands a step taken at the level above it.

| Doc | Role | Audience | Depth |
|-----|------|----------|-------|
| [README.md](../README.md) | Quick start; one-page survey | First-time reader | Glance |
| [tutorial.md](../tutorial.md) | Worked walk-through, empty → small domain | LLM operator | Hands-on |
| [methodology.md](../methodology.md) | Operational design — ISA, schema, KQUERY, MCP | Implementer | Reference |
| [theory.md](../theory.md) | Foundations — shadow architecture, V₄, Yoneda+Derrida, Theorem 14.5 | Theorist | Proof |
| [examples.md](../examples.md) | Domain templates beyond processors | Adopter | Application |

The README explicitly enumerates this ladder at
[README.md:42-58](../README.md#L42-L58); each subsequent doc
extends what the prior level introduced.

## Realisations

All five are exposed as MCP resources at `catalogue://readme`,
`catalogue://tutorial`, `catalogue://methodology`,
`catalogue://theory`, `catalogue://examples`, plus an index
resource `catalogue://docs` listing them all
([README.md:60-65](../README.md#L60-L65)). The MCP layer is the
externalised re-statement of the depth-quartet as an addressable
resource grid.

## Property

`P(d) := d entails the document above it without contradicting
the document below it`. Concretely: tutorial's worked example
must use only operations introduced in README; methodology's
spec must align with what tutorial demonstrates; theory's
formalism must justify methodology's design; examples must apply
methodology's rules to new domains.

## Composition

`docs := README ⋃ tutorial ⋃ methodology ⋃ theory ⋃ examples`
served by the MCP `catalogue://docs` index. Composition is
**graded re-statement** — each level says the same thing, just
at a different depth.

## Entailment

The graded re-statement is what licenses an LLM (the primary
audience) to enter at any level and still arrive at a coherent
mental model. README + tutorial alone is sufficient for a basic
operator; methodology + theory together is sufficient for a
maintainer; all five together is sufficient for an extender.

## Reuse evidence

5 files + 1 index resource. The depth-grading recurs as the MCP
prompt set: `analyze_new_processor` (tutorial-grade workflow),
`audit_md_vs_sql` (methodology-grade reconciliation),
`snap_to_grid_check` (theory-grade self-audit). Prompts inherit
the depth-quartet structure from the docs.

## Open question for RFS

Are there genuine ≥3-instance patterns being repeated *across*
docs that should be extracted into a shared snippet? Candidates:
the V₄/kquery cell table; the four-step move from theory.py;
the gap.10/gap.01 vocabulary. RFS should classify whether these
are duplications (extract) or graded re-statements (correct).
