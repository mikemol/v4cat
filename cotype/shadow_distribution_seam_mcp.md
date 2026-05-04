# Shadow: distribution seam between v4cat (core) and v4cat-mcp

> *DBE+RFS+S2G fire of 2026-05-04. Region #8 of the
> shadow-architecture lattice.*

## Form

A **distribution-seam** shadow: a structural commitment about where
the v4cat catalogue ends and the MCP presentation begins. Two pip
distributions, one runtime dependency edge:

```text
┌────────────────────┐         ┌────────────────────────┐
│ v4cat              │ ◄────── │ v4cat-mcp              │
│ (catalogue ISA,    │ depends │ (MCP server presenting │
│  schema, kquery,   │   on    │  the v4cat ISA over    │
│  views, sandbox)   │         │  stdio MCP)            │
└────────────────────┘         └────────────────────────┘
```

The seam runs **at the import boundary**: `v4cat_mcp.server`
imports `v4cat.{catalogue,sandbox,views,bootstrap}` and
nothing else from v4cat's internals. The catalogue does not
import anything from v4cat-mcp.

## Where realised

- Repos: `v4cat-oss/v4cat` (core) and `v4cat-oss/v4cat-mcp` (this
  shadow's other half).
- Files moved out of v4cat into v4cat-mcp:
  - `src/v4cat/mcp_server.py`     → `src/v4cat_mcp/server.py`
  - `src/v4cat/mcp_setup.md`      → `src/v4cat_mcp/setup.md`
  - `src/v4cat/tests/test_mcp.py` → `src/v4cat_mcp/tests/test_server.py`
  - MCP-side block (lines 742–1077) of `tests/test_branch_coverage.py`
    → `src/v4cat_mcp/tests/test_branch_coverage.py`
- Files updated on the v4cat side:
  - `pyproject.toml`: drops `mcp>=1.0` dep and the `v4cat-mcp`
    console-script entry; URLs retargeted to `v4cat-oss`.
  - `src/v4cat/README.md`: drops "Run the MCP server" section,
    layout list, and resource list; adds pointer to v4cat-mcp.
  - `src/v4cat/theory.py`: docstring step-1 of the four-step move
    notes that MCP-side primitives land in `v4cat_mcp.server`.

## Composition operation

`pip install v4cat-mcp` resolves to both distributions; the
console-script `v4cat-mcp` and `python -m v4cat_mcp` both land in
`v4cat_mcp.server:main`, which calls the same `FastMCP` instance
that the in-process tests exercise. The catalogue file produced by
`SymmetryCatalogue` is bit-identical to the one the MCP server reads
— there is no schema or serialisation translation across the seam.

The MCP-exposed `catalogue://` URI scheme is unchanged. The ten
documentation resources are served via `importlib.resources.files()`:
nine read from the `v4cat` package, one (`setup.md`) reads from the
`v4cat_mcp` package.

## Entailment

```text
v4cat is identity-preserving under presentation:
∀ catalogue file f. SymmetryCatalogue(f).<API> ≡
  v4cat_mcp.server.<MCP-tool/resource> over f
```

The catalogue's identity is the witness graph; the MCP interface is
one *witness of* that identity, not a constituent of it. Removing
the MCP server (e.g., installing v4cat without v4cat-mcp) does not
shrink the catalogue's content; the catalogue is fully usable from
Python code alone (`python_api.md`).

Verified by:
- `v4cat`: `tests/test_isa.py`, `test_branch_coverage.py`,
  `test_risc.py`, `test_sandbox.py`, `test_self_hosting.py` all
  pass with `mcp` not installed.
- `v4cat-mcp`: `tests/test_server.py`, `tests/test_branch_coverage.py`
  pass against the installed v4cat package.

## Lattice classification

Region #8 of the shadow-architecture 8-region lattice:

| Skill | Active | Move |
|---|---|---|
| DBE  | ✓ | Forward design of the v4cat-mcp package skeleton, dep edge, console script |
| RFS  | ✓ | Sideways extraction of the MCP-shadow from the existing v4cat artefact |
| S2G  | ✓ | This file — registering the seam in the cotype |

The fire was **sequential rotation** (per shadow-architecture's
prediction): commit-then-verify cadence rather than one synchronized
commit. Three commits across two repos:

1. `v4cat`: pre-split commit completing the doc-set-of-ten.
2. `v4cat-mcp`: extract + restructure (filter-repo + rename + import
   rewrite + importlib.resources fix).
3. `v4cat`: strip MCP files/deps + update docs + register this shadow.

## Why this is not a forbidden region #5 (DBE+RFS without S2G)

The snap-at-session-end discipline requires that any extraction be
catalogued. Without this shadow file, the split would be a region-#5
violation — extraction completed without being registered. Writing
this file converts the fire to region #8.

## Consequences for prior cotype shadows

The existing shadows in this directory remain valid with one
re-derivation:

- `shadow_layered_stack.md` — the L0→L7 entailment chain still
  holds, but levels involving the MCP presentation now span two
  distributions. The chain is preserved across the seam by the
  identity-preservation entailment above.
- `rfs_findings_risc_projection.md` finding "MCP wrappers
  already-aligned" is unchanged; the wrappers still simply call
  the SymmetryCatalogue methods, only now from a different package.

No prior shadow is invalidated; the catalogue thickens forward.

## Algebraic anchor (2026-05-04 cont'd)

Re-read under
[shadow_assertion_history_group.md](shadow_assertion_history_group.md):
v4cat-mcp is the **forward-modal facet of the assertion-translation
group, exposed over RPC**. Each MCP tool is a single ◇⁺ move on `H`
(introduce_node/edge translations) or a V₄-chart read (kquery
tools). The catalogue's identity is preserved across the seam
*because* the seam runs at the public-monotone facet — the same
facet v4cat itself exposes — not at a deeper layer that would
require access to history-modal inverses. The "presentations are
identity-preserving" entailment is the operational consequence of
identity (E) in shadow_assertion_history_group.md (recognizers
preserve equivariance; presentations preserve identity). See
[theory.md § 15.13](../src/v4cat/theory.md) on modal time axes.
