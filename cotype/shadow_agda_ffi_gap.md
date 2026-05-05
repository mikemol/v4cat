# Shadow: Agda FFI gap (promissory cell)

> *S2G fire of 2026-05-04 (companion to
> [shadow_agda2v4cat_distribution.md](shadow_agda2v4cat_distribution.md)).
> **At orbit-position 1**; per discipline rule 6, S2G to catalogue
> the gap, NOT RFS to extract a wrapper. v0.2 closes this.*

## Form

A promissory cell: **Agda code calling into v4cat at runtime via FFI**.

The user's original request was for "an Agda extension that uses
v4cat as an FFI and as a way to fully export Agda data". v0.1
shipped the export half (agda2v4cat). The FFI half — Agda code
that *interacts with a running v4cat catalogue at runtime* — is
deferred.

## What's missing

Three components of an FFI:

1. **Agda postulates** declaring v4cat operations:

   ```agda
   postulate
     introduce-node : Id → Label → Kind → IO ⊤
     edge           : Id → Kind → Id → IO ⊤
     kquery         : Set → Set → Set → IO Cells
   ```

2. **Haskell foreign bindings** that implement the postulates by
   talking to v4cat. The architecturally honest path: bind via
   v4cat-mcp's MCP-over-stdio protocol.

   ```text
   Agda postulate → ghc-compile-pragma → Haskell IO action
                                           │
                                           ▼
                                       MCP client
                                           │ stdio
                                           ▼
                                  v4cat-mcp server process
                                           │
                                           ▼
                                       v4cat catalogue
   ```

3. **An Agda library** (`V4cat.Catalogue`, `V4cat.Kquery`) that
   re-exports the postulates with an ergonomic API.

## Why deferred to v0.2

- v0.1 already covers ~900-1100 lines of Haskell for the export
  pipeline.
- FFI design has architectural choices (sync vs async; one MCP
  process per Agda compile vs per call; how IO threading interacts
  with Agda's typechecker). Each warrants its own DBE pass.
- The export use case unblocks "kquery on Agda code"; the FFI use
  case is more niche (interactive tactic that queries v4cat
  mid-typecheck).

## What this shadow does NOT do

Per discipline rule 6:

- Does not introduce an `AgdaFFI` abstract class.
- Does not pre-commit to MCP as the only path (a pure-Haskell
  binding to a SQLite-shaped v4cat is also possible if v4cat
  publishes a stable wire format).
- Does not modify agda2v4cat v0.1 in any way.

## Lattice classification

Region **#4 (S2G alone — pure cataloguing)**.

## Promissory cell — what would close it

A future agda2v4cat ≥ v0.2 ships with:

1. New module `Agda2V4cat.FFI` with Haskell foreign-call bindings.
2. A small Agda library at `agda2v4cat/lib/V4cat.agda` exposing the
   postulates.
3. Tests demonstrating an Agda program that introduces nodes and
   queries them in v4cat at compile time (via a Haskell rewrite
   rule or REWRITE pragma) or at runtime (via a Haskell main
   harness compiled by Agda's GHC backend).
4. Documentation in `docs/spec.md` covering FFI semantics +
   threading model.
5. A workspace-claim in v4cat-certify
   (`claim:agda2v4cat-ffi-roundtrips`) verifying a complete
   round-trip.

## Closure

When agda2v4cat v0.2 ships the FFI, this shadow is annotated with
"closed at agda2v4cat 0.2 (commit X)" per the
catalogue-thickens-forward discipline.

Until then, this shadow stands as a registered structural
commitment the framework has *named* but not yet *executed*.
