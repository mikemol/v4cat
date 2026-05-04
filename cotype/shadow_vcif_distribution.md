# Shadow: VCIF distribution seam — data-at-rest presentation

> *DBE+RFS+S2G fire of 2026-05-04 (cont'd). Region #8 of the
> shadow-architecture lattice. The first **data-at-rest carrier** to
> be extracted (parallel to [shadow_distribution_seam_mcp.md](shadow_distribution_seam_mcp.md),
> which is on a different orbit — RPC presentations).
> Subsequently joined by [shadow_vcif_rdf_distribution.md][vcif-rdf-shadow]
> and [shadow_vcif_hlo_distribution.md][vcif-hlo-shadow] as the second
> and third substrate columns of the carrier grid; see
> [shadow_carrier_grid.md][grid] for the (depth × substrate)
> framing in which all three sit.*

[grid]: shadow_carrier_grid.md
[vcif-rdf-shadow]: shadow_carrier_grid.md
[vcif-hlo-shadow]: shadow_vcif_hlo_distribution.md

## Form

A second **distribution-seam** shadow, parallel to the MCP seam. v4cat
ships in three distributions; this shadow registers the third row:

```text
┌────────────────────┐         ┌────────────────────────┐
│ v4cat              │ ◄────── │ v4cat-mcp              │
│ (catalogue ISA,    │ depends │ (RPC presentation —     │
│  schema, kquery,   │   on    │  Model Context Protocol)│
│  views, sandbox)   │         │                        │
└────────────────────┘         └────────────────────────┘
        ▲
        │ depends on
        │
┌────────────────────────────────────┐
│ vcif                                │
│ (data-at-rest presentation —       │
│  JSON-Schema-enforced interchange) │
└────────────────────────────────────┘
```

The seam runs **at the import boundary**: `vcif` imports v4cat's
public ISA (`introduce_node`, `edge`, `defer/promote/boundary`,
`SymmetryCatalogue`) and nothing internal. v4cat does not import
anything from vcif. The 14-rule semantic validator in
`vcif.semantic` is implemented entirely on top of dict-shape checks;
it doesn't poke v4cat's tables directly.

## Where realised

- New repo: [v4cat-oss/vcif](https://github.com/v4cat-oss/vcif).
- Schemas (Apache-2.0, language-agnostic):
  - [`src/vcif/schemas/vcif-1.0.schema.json`](https://github.com/v4cat-oss/vcif/blob/main/src/vcif/schemas/vcif-1.0.schema.json)
    — core schema with all `$defs`.
  - Six profile schemas in `src/vcif/schemas/profiles/` for
    `v4cat.snapshot`, `v4cat.patch`, `v4cat.vocabulary`,
    `v4cat.recognizer-package`, `v4cat.closure-report`,
    `v4cat.residue-report`.
- Python tooling (MIT) in `src/vcif/`:
  `validator.py`, `semantic.py`, `importer.py`, `tensions.py`,
  `relations.py`, `cli.py`.
- Spec: [`docs/spec.md`](https://github.com/v4cat-oss/vcif/blob/main/docs/spec.md).
- Examples: `docs/examples/agda-import.json` (snapshot),
  `docs/examples/hf-dbe-closure.json` (closure-report).

v4cat-side touch-points (this commit):

- [`src/v4cat/methodology.md`](../src/v4cat/methodology.md)
  § "Document store (JSON-shaped)" updated to point at VCIF as the
  canonical interchange; the prior break-centric example kept as
  non-canonical illustrative.
- This file (registers the shadow).
- [`cotype/INDEX.md`](INDEX.md) indexes this shadow.

## Composition operation

`pip install vcif` resolves both v4cat and vcif. The CLI subcommands
(`vcif validate`, `vcif inspect`, `vcif dry-run`, `vcif import`) all
run the two-pass validator (JSON Schema 2020-12 + 14 catalogue-native
rules). Apply mode mutates the catalogue solely through public ISA
verbs.

## Entailment

```text
v4cat is identity-preserving under presentation:
∀ presentation P. P.depends-on(v4cat) ∧ ¬v4cat.depends-on(P)
  ⟹ catalogue.identity ≡ identity-of(catalogue accessed through P)
```

VCIF-specific instance:

```text
∀ vcif_doc d. validate(d) ∧ apply(d, cat)
  ⟹ cat.state-after ≡ cat.state-after-equivalent-ISA-calls
```

That is, VCIF is a serialization, not a side channel.

## Lattice classification

Region #8 of the shadow-architecture 8-region lattice. Same region as
the MCP seam; *different operational mix*:

| Skill | Active | What it did |
|---|---|---|
| DBE  | ✓ | Forward design of the new package skeleton, schema files, validator/importer code paths. Heavy. |
| RFS  | ✓ | Re-grouped methodology.md's existing JSON example as non-canonical illustrative against VCIF's flat canonical form. Light. |
| S2G  | ✓ | This file — registering the second seam. Confirms the orbit position; does *not* yet extract a universal record (≥3 instances required). |

### Discipline rule 6 check (orbit-saturation)

Two presentation seams now exist (MCP, VCIF). C7 threshold is ≥3
instances → universal record. We are at 2 — **below threshold**. The
move at 2 instances is to *catalogue the orbit position*, not extract
a wrapper.

The generating symmetry is already visible:

> v4cat-as-carrier ≢ v4cat-as-presentation. The catalogue's identity
> is constituted by its witness graph; presentations are functions
> from that graph to a target shape (RPC-call surface, on-disk JSON,
> a future query response, etc.).

A third presentation (VQL? federation protocol? web UI? GraphQL
gateway?) would tip into RFS-extraction of this universal. For now,
two parallel rows are the structure.

## Predicted vs observed cadence

Plan predicted **sequential rotation** (multi-step build with
intermediate verification) per shadow-architecture's empirical 8-of-11
prevalence. Observed:

1. vcif initial commit (722ed04 in vcif): all-in-one package
   skeleton + Stage A/B/C schemas + Python tooling + tests + examples
   + spec.
2. v4cat-side methodology pointer + cotype shadow (this commit).

Two commits across two repos. Less granular than the 3+1 plan
sketched, but the test suite (43 tests) gates the all-in-one shape,
so the *internal* sequential discipline (Stage A → B → C with each
compiling+passing) was preserved within the single commit.

## Consequences for prior cotype shadows

- [shadow_distribution_seam_mcp.md](shadow_distribution_seam_mcp.md)
  — unchanged. Now part of a pair witnessing the
  presentation-distribution pattern.
- [shadow_layered_stack.md](shadow_layered_stack.md) — the L0→L7
  entailment chain is preserved across this seam by VCIF's
  identity-preservation entailment. VCIF's schemas describe L0
  (kquery covers via `set_expr`/`relation_expr`) up through L4 (MCP-equivalent
  workflow surface via tensions + cell actions). VCIF is the *file
  format* presentation of L0–L4; v4cat-mcp is the *RPC* presentation
  of the same range.
- [methodology.md's JSON example](../src/v4cat/methodology.md) — now
  re-framed as non-canonical illustrative; VCIF is the contract.

No prior shadow is invalidated.

## Trace integrity

The catalogue thickens forward (per methodology.md). This shadow is
the second of a pair. Future fires on a third presentation would:

1. Land their own shadow (e.g., `shadow_vql_distribution.md`).
2. Trigger an RFS extraction: a universal record
   `shadow_presentation_pattern.md` quotienting the three rows.
3. The three individual shadows then become orbit-instance witnesses
   of the universal pattern.

The catalogue knows in advance what the universal *will* look like:
"P depends-on v4cat; v4cat does not depend on P; identity preserved."
What it doesn't know is how many such P will exist. Three filled
substrate columns at time of next-fire registration; the orbit is
parameterised by substrate and remains open-ended. Per the
re-reading in the algebraic-anchor footer below + discipline rule 6,
no `Carrier` wrapper is extracted at any number of filled columns.
See [shadow_carrier_grid.md](shadow_carrier_grid.md) for the
multi-column grid framing.

## Algebraic anchor (2026-05-04 cont'd)

Re-read under
[shadow_assertion_history_group.md](shadow_assertion_history_group.md):
**vcif's six profiles factor along a projection-depth axis** rooted
in the assertion-history group `H = ℤ^𝔄`. The profiles, ordered by
distance from `H`:

| Profile | Group-theoretic content |
|---|---|
| `v4cat.patch` | `h ∈ H` itself — the operation-log carrier; group-faithful, invertible |
| `v4cat.snapshot` | `π(h)` — the visible support quotient; idempotent |
| `v4cat.closure-report` | `χ_{A,B}(π(h))` — the V₄ coordinate decomposition |
| `v4cat.residue-report` | a further named projection of cell members |

The two operator/signature profiles (`v4cat.vocabulary` declaring
`𝔄` and `v4cat.recognizer-package` declaring tensions) are not on
the projection-depth axis; they declare the basis and the
recognizer-action layer. Carriers (vcif, vcif-rdf, future) are
**substrate columns** — each substrate replicates the same
projection-depth axis. The "siblings, not parent/child" reading
above is correct in the sense that JSON is not canonical; the
"co-projections sharing a kernel" reading is correct in the sense
that every carrier pulls in v4cat. Both are subsumed by the
algebraic reading: carriers are projections of `H` at various
depths, instantiated in various substrates. See
[theory.md § 15](../src/v4cat/theory.md), § 15.4, and § 15.13.
