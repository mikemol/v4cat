# Shadow: agda2v4cat — first instance of catalogue-source role

> *DBE+RFS+S2G fire of 2026-05-04. Region #8 of the
> shadow-architecture lattice. **DBE-led** (substantial new
> Haskell-side costructure). Algebraic anchor:
> [shadow_assertion_history_group.md](shadow_assertion_history_group.md).
> Operationalised at [v4cat-oss/agda2v4cat](https://github.com/v4cat-oss/agda2v4cat).*

## Form

The **first instance** of a new role in the v4cat-oss workspace:
**catalogue source**. Where the carriers
([vcif](https://github.com/v4cat-oss/vcif),
[vcif-rdf](https://github.com/v4cat-oss/vcif-rdf),
[vcif-hlo](https://github.com/v4cat-oss/vcif-hlo)) *transport*
catalogue content across substrates, agda2v4cat *produces* it from a
domain — Agda's typechecked internal representation.

```text
                  agda2v4cat            ← catalogue source (NEW role)
                      │ produces
                      ▼
                  VCIF JSON
                      │ ingested by
                      ▼
            {vcif, vcif-rdf, vcif-hlo}  ← carriers
                      │ pulls in
                      ▼
                    v4cat              ← kernel
```

## Where realised

- **Repo**: [v4cat-oss/agda2v4cat](https://github.com/v4cat-oss/agda2v4cat) v0.1.
- **Implementation**: Haskell (cabal-built); Agda backend via the
  `Agda.Compiler.Backend.Backend` typeclass. Toolchain pinned via
  `mise.toml`: `cabal 3.10.3.0` (latest 3.10.x with prebuilt binary
  on haskell.org; cabal 3.16 broke Agda's custom `Setup.hs`),
  *system* `/usr/bin/ghc-9.6.6` (GHC pinned through mise/ghcup
  pipe-deadlocks during doc-install when stdout is not a TTY), Agda
  library `>=2.6.3 && <2.6.4` from Hackage (forced upstream by
  agda2train 0.0.3.0).
- **Extraction scope (v0.1)**: Tier 1 + Tier 2 of the kquery 10-cell
  against vcif's hand-crafted `agda-import.json` fixture (15 of 25
  items). Emitted vocabulary: 19 node-kinds, 18 edge-kinds (one each
  added beyond the original plan: `agda-arg-position` /
  `has-arg-position`, so per-arg edges fan out from per-arg nodes
  rather than collapsing onto the def — required for vcif's
  edge-uniqueness rule). Tier 3 deferred via
  `shadow_agda_extraction_gap_tier3.md`.
- **Output**: per-module VCIF JSON files (`v4cat.snapshot` profile);
  each validates against vcif's schema. `vcif.apply` ingests with a
  workspace-side bootstrap workaround tracked in
  [shadow_v4cat_vcif_bootstrap_gap.md](shadow_v4cat_vcif_bootstrap_gap.md).
- **Bijection invariant**: the slug encoding from arbitrary Agda
  identifiers / type-strings / modality tuples into vcif's ID
  alphabet is bijective (`+XX`-hex of UTF-8 bytes); `unslug . slug =
  id`. Round-trip from emitted JSON back to original Agda strings is
  a pure decode. Exercised by `Test.Vcif.bijectiveSlug`.

## Composition operation

`agda2v4cat <Agda flags>` wraps Agda's typechecker. After
typechecking, the backend walks every typechecked `QName`, builds an
`ExtractedDef` record, and serialises a per-module
`v4cat.snapshot` document.

Pipeline:

```text
.agda → typecheck → extract → buildSnapshot → JSON file → vcif.apply → v4cat catalogue
```

## Entailment

```text
∀ typechecked Agda program P. agda2v4cat(P) is a VCIF document whose
nodes/edges are domain-faithful to P's internal AST under v0.1's
Tier-1+2 extraction surface (15 named items from the kquery 10-cell).
```

Equivalent to: **after agda2v4cat runs, the Agda program is
queryable via kquery in the v4cat catalogue at the granularity v0.1
documents.**

## Lattice classification

Region **#8** (DBE + RFS + S2G — substantive structural arc).

- **DBE (heavy)**: forward design of the Agda backend, the
  `ExtractedDef` costructure (Tier-1+2 fields), the 19-node-kind /
  18-edge-kind VCIF vocabulary, per-arg-position fan-out shape (so
  each (arg, modality) edge is unique), bijective slug encoding,
  one-shot BUILTIN-registry walk threaded through `env`, and the
  per-module emission. ~600 lines of Haskell across Backend.hs,
  Extract.hs, Vcif.hs.
- **RFS**: regroups vcif's hand-crafted `agda-import.json` fixture
  as a *minimal point* in a much larger structural surface — the
  fixture under-demands by ≈4× per the kquery analysis at orbit
  position 1 of "domain extractor for v4cat".
- **S2G**: this file. Plus
  [shadow_agda_ffi_gap.md](shadow_agda_ffi_gap.md) and
  [shadow_agda_extraction_gap_tier3.md](shadow_agda_extraction_gap_tier3.md)
  as promissory companions.

### Discipline rule 6 (orbit-saturation) check

Orbit position **1** of "domain extractor for v4cat":

| Instance | Source language | Realised in |
| --- | --- | --- |
| **agda2v4cat** | Agda | v4cat-oss/agda2v4cat |

Below the C7 ≥3 threshold; orbit-driven recurrence (parameterised by
source language); **S2G to catalogue, no `DomainExtractor` wrapper
extracted**. v4cat itself remains the universal at the kernel-cell.

A future second instance (e.g., coq2v4cat, rust2v4cat,
typescript2v4cat) would be the second orbit-element. At three the
C7 threshold tips toward RFS-eligible.

## Trace-integrity

Prior shadows preserved:

- [shadow_carrier_grid.md](shadow_carrier_grid.md) — three substrate
  columns unchanged. agda2v4cat is **not a fourth carrier**; it's a
  different role (catalogue source) producing across the existing
  three.
- [vcif/docs/examples/agda-import.json](https://github.com/v4cat-oss/vcif/blob/main/docs/examples/agda-import.json)
  — the hand-crafted fixture is NOT replaced; it remains as a
  schema-validation demo + a cross-substrate parity fixture in
  vcif/vcif-rdf/vcif-hlo. agda2v4cat's actual output is a strict
  superset.
- [audit_workspace_2026_05_04.md](audit_workspace_2026_05_04.md) — gains
  agda2v4cat as the seventh distribution; trajectory gains fire #10.
- [shadow_workspace_certification.md](shadow_workspace_certification.md)
  — v4cat-certify could grow a `claim:agda2v4cat-emits-valid-vcif`
  workspace-claim in a future fire; for v0.1 the cotype simply
  registers the new distribution.

## Snap-to-grid check

User's request: "Now, the next thing I want is an agda extension
that uses v4cat as an FFI and as a way to fully export agda data
(akin to agda2train, but less ML-specific)."

User's follow-up: "what possible information could we further
extract from agda that isn't already described in the hand-crafted
agda-import fixture? (what is the klein4 between what's available
and what the fixture demands?)"

Cotype's entailment after this fire lands: "agda2v4cat is the first
catalogue source for v4cat. Its v0.1 extracts 15 of 25 named items
in the kquery 10-cell against vcif's existing fixture. Tier 3 (10
items) is registered as a v0.2 promissory cell. The FFI (Agda code
calling into v4cat) is also a v0.2 promissory cell."

Snap valid. The fire produces a working extractor *and* exposes the
full structural design space (Tiers 1-3 named in the spec) so the
v0.2 follow-up has named substructure to pick up from.

## What this fire does NOT extract

Per discipline rule 6:

- No `DomainExtractor` wrapper above {agda2v4cat}.
- No "ExtractorCarrier" abstraction above {extractor produces JSON;
  carrier transports JSON}.
- No fourth substrate column. agda2v4cat *consumes the existing
  three* via its Python smoke-test pipeline.

## The slogan, applied at the source level

> v4cat audits its own framework via Theorem 14.5.
> v4cat-certify audits the workspace via the same V₄ pattern.
> agda2v4cat sources the workspace from a domain via the same V₄
> coordinate chart applied to "extractable vs demanded".

Same observer-pair group action; new orbit (extraction).
