# v4cat — Symmetry-break cataloguing framework

> *Grade: quick-start (one-page survey).
> Deeper: [tutorial.md](src/v4cat/tutorial.md) (worked walk-through), then [methodology.md](src/v4cat/methodology.md) (operational design), then [theory.md](src/v4cat/theory.md) (foundations).
> Operating: [rigorous_use.md](src/v4cat/rigorous_use.md) (the user-facing covenant), [python_api.md](src/v4cat/python_api.md) (non-MCP API discipline).
> Hosted skills: [hosted_skills.md](src/v4cat/hosted_skills.md) (DBE/RFS/S2G/shadow-architecture as v4cat-hosted frameworks), [hosted_skill_usage.md](src/v4cat/hosted_skill_usage.md) (per-region operating manual).
> Architectural detail: [cotype/](cotype/).*

A Python ISA + SQLite schema for accumulating named structural
distinctions about a domain. The structural core is **three RISC
primitives** — `introduce_node`, `edge`, `kquery` — plus a small
declarative-artifact set (breaks, specs, tensions); every other
verb in the ISA is documented sugar that reduces to these three.
The strengthened self-hosting closure check (`theory.md` § 14.5.8)
verifies the reductions on every catalogue open.

An MCP (Model Context Protocol) presentation of the same ISA lives
in a separate distribution, [v4cat-mcp][mcp]. Install it when you
want to drive the catalogue from an LLM client; the catalogue
itself is independent of any presentation layer.

[mcp]: https://github.com/v4cat-oss/v4cat-mcp

The framework is **domain-agnostic**. The same primitives and
analytic views work whether the witness objects are programming
languages, processors, cryptographic primitives, file systems,
formal systems, ML architectures, or anything else with structure
worth cataloguing. See [examples.md](examples.md) for domain
templates.

See [methodology.md](methodology.md) for the operational design,
[tutorial.md](tutorial.md) for an LLM-friendly walk-through, and
[cotype/](cotype/) for the architectural shadow library —
including [cotype/shadow_risc_core.md](cotype/shadow_risc_core.md)
which is the authoritative source for the RISC reframe.

## Layout

```text
v4cat/
├── __init__.py              public API
├── catalogue.py             SymmetryCatalogue class (the ISA)
├── views.py                 kquery + analytic queries
├── schema.sql               generic framework schema (S0-S11)
├── cells.py                 Cell tagged union + Kinds enum (theory.md § 14.5.1)
├── theory.py                framework signature, the IMPL referent (§ 14.5.2)
├── bootstrap.py             closure check (§ 14.5.4); SelfHostingViolation
├── framework_seed.sql       framework self-cataloguing seed data (§ 14.5.5)
├── methodology.md           operational design — ISA, schema, KQUERY, MCP
├── theory.md                foundations — shadow architecture, Klein-four, Yoneda+Derrida, magma+pointfree, Theorem 14.5
├── tutorial.md              LLM-friendly walk-through, empty → small worked domain
├── examples.md              domain templates (languages, processors, crypto, …)
├── rigorous_use.md          user-facing operating covenant — using v4cat as rigorously as v4cat uses itself
├── python_api.md            non-MCP API discipline — RISC/CISC strata, kquery + tension patterns
├── hosted_skills.md         hosting the four shadow-architecture skills (DBE/RFS/S2G/shadow-architecture) as v4cat-framework objects
├── hosted_skill_usage.md    per-region operating manual for the hosted skills — fire classification, kquery audit, residue actions
├── README.md                this file
├── pyproject.toml           pip-installable package metadata
└── tests/
    ├── test_isa.py          framework tests, synthetic data
    └── test_self_hosting.py regression test for Theorem 14.5
```

The MCP server (formerly `mcp_server.py`, `mcp_setup.md`,
`tests/test_mcp.py`) is now in its own distribution at
[v4cat-oss/v4cat-mcp][mcp].

## Documentation

The framework is documented at five levels of depth, plus four
operational guides (Python API discipline, rigorous use,
hosted-skills design, hosted-skill usage). MCP-server setup lives
in the [v4cat-mcp][mcp] repository.

- **`README.md`** (this file): quick start. Installation, layout,
  first commands.
- **`tutorial.md`**: walk-through from empty catalogue to a small
  worked domain. Best first read for an LLM operating the
  catalogue.
- **`methodology.md`**: full operational design — ISA, schema
  breaks, the Klein-four read primitive, MCP interface,
  philosophical lineage.
- **`theory.md`**: foundations — shadow architecture, the
  temporal axis as normal to symmetry planes, magma + pointfree
  topology, Yoneda + Derrida, the recursive schema, convergence,
  trace-thickening, plus § 15's group-theoretic reading
  (RISC writes as translations; kquery as the V₄ coordinate
  chart of the observer-pair group action).
- **`examples.md`**: domain templates — programming languages,
  cryptographic primitives, databases, file systems, network
  protocols, mathematical structures, OS designs, ML architectures.
- **`rigorous_use.md`**: the user-facing operating covenant —
  declaring `U`, treating every claim as needing a carrier,
  preserving the four cells, and using v4cat as rigorously as v4cat
  uses itself.
- **`python_api.md`**: non-MCP API discipline — RISC/CISC strata,
  `kquery` + `Tension` patterns, lifecycle as witnesses,
  `load_extension()` shape, snapshot comparisons.
- **`hosted_skills.md`**: the hosted-framework contract — making
  the four shadow-architecture skills (DBE, RFS, S2G,
  shadow-architecture) into v4cat objects whose claims, firing
  rules, intervention steps, products, residues, and closure
  obligations are themselves catalogued and kquery-auditable.
- **`hosted_skill_usage.md`**: the per-region operating manual for
  the hosted skills — work-fire as the unit of use, eight worked
  examples (one per lattice region, including the two forbidden
  ones), and the orbit-saturation guard.
- **`cotype/`**: the shadow library — the authoritative source for
  architectural commitments (RISC reframe, migration history,
  doc-discipline, RFS findings, snap reports). Deep readers should
  follow this thread; the user-facing docs above reference it where
  architectural detail exceeds doc grade.

When the [v4cat-mcp][mcp] server is running, all ten user-facing
files are exposed as MCP resources at `catalogue://readme`,
`catalogue://mcp_setup`, `catalogue://tutorial`,
`catalogue://methodology`, `catalogue://theory`,
`catalogue://examples`, `catalogue://rigorous_use`,
`catalogue://python_api`, `catalogue://hosted_skills`, and
`catalogue://hosted_skill_usage`. There's also `catalogue://docs`
— an index resource that lists everything available, suitable as
the entry point for an LLM encountering the framework.

## Quick start

```python
from v4cat import SymmetryCatalogue, kquery, agree, blind

with SymmetryCatalogue('/tmp/cat.db') as cat:
    # Introduce objects with year + lineage
    cat.introduce_object('alpha', 'Alpha', year=1980)
    cat.introduce_object('beta',  'Beta',  year=1985,
                         lineage=[('alpha', 'descended-from')])

    # Introduce a break with axis classification
    cat.introduce_break('F1', 'My first break', axes=['spatial'])

    # Witness and refine
    cat.witness('alpha', 'F1', 'origin')
    cat.witness('alpha', 'F1', 'catalogue-introduces')
    cat.witness('beta',  'F1', 'inherits')
    cat.refine('F1', 'beta', 'extension', description='details')

    # Derived attribution (always a query, never stored)
    print(cat.origin('F1'))            # → originator: alpha
    print(cat.lineage('beta'))         # → ancestor chain
    print(cat.inherited_breaks('beta'))  # → F1 inherited from alpha

# Klein-four read primitive: every read is a comparison
result = kquery(['a', 'b'], ['b', 'c'], universe=['a', 'b', 'c', 'd'])
# {
#   '11': ['b'],     # both — agreement
#   '10': ['a'],     # left only
#   '01': ['c'],     # right only
#   '00': ['d']      # shared blindness
# }
```

## MCP server

The MCP (Model Context Protocol) presentation of the catalogue
ships as a separate distribution: [v4cat-mcp][mcp]. Install it
when you want to drive the catalogue from an MCP-aware client
(VS Code, Claude Desktop, Claude Code, Codex CLI, custom agents).

```sh
pip install v4cat-mcp        # pulls v4cat as a dependency
v4cat-mcp --db /path/to/cat.db
```

See the [v4cat-mcp setup guide][mcp-setup] for per-client wiring.
The catalogue file produced by `SymmetryCatalogue` is exactly the
file the MCP server reads; nothing about persistence changes when
you add the presentation layer.

[mcp-setup]: https://github.com/v4cat-oss/v4cat-mcp/blob/main/src/v4cat_mcp/setup.md

## Loading a domain on top

The framework schema (`schema.sql`) is generic. Domain-specific
schema extensions (per-break detail tables, per-domain views, seed
data) load via `load_extension`:

```python
cat = SymmetryCatalogue('/tmp/proc.db')
cat.load_extension('path/to/my_domain.sql')
```

Domain extensions are responsible for their own idempotence
(`CREATE TABLE IF NOT EXISTS`, `INSERT OR IGNORE`).

## Run the tests

```sh
python -m v4cat.tests.test_isa
```

Tests use synthetic data only and don't depend on any specific
domain. (MCP-server tests live in the [v4cat-mcp][mcp] repo.)

## Methodology

The brief version:

1. **Identity is relational** (Yoneda). An object is its
   participation in the witness graph; nothing more.
2. **Time and lineage are breaks-themselves.** A metric field
   (e.g. year) and lineage are recorded once per object as primary
   data; *attribution emerges* via tropical MIN over the chosen
   axis, restricted to origin-class edges. There's no `RETRO` verb.
3. **Every read is a comparison** (Klein-four). `kquery(A, B; U)`
   classifies the universe into four cells (`11`, `10`, `01`, `00`).
   `query`, `wedge`, `coverage`, `blind` are named selections.
4. **Schema breaks are additive.** Don't drop columns; add new
   ones. The schema's own evolution mirrors the methodology.
5. **Global structure is always derived, never imposed.** Status,
   origin, retroactive gaps, consistency violations — all live in
   views.

The full case for these commitments — and their alignment with
Derridean traces, Yoneda relationality, and pointfree topology —
is in [methodology.md](methodology.md).

## Naming

The package is **`v4cat`** — "the category of V₄-equipped domain
catalogues." The name is licensed by Theorem 14.5 (theory.md § 14)
being operative *by default*: ``SymmetryCatalogue(...)`` runs the
closure check on every open, and the regression test in
``tests/test_self_hosting.py`` passes against every shipped
catalogue. The renaming was *triggered by a runtime invariant*,
not by an act of nomination — see theory.md § 14.8.

Earlier candidate names from the lifting work, kept here for
reference:

- `kfour/` — earlier name committing only to V₄ as the read
  primitive at level 0, used while the closure check was opt-in.
- `sbc/` — Symmetry-Break Cataloguing (descriptive but generic).
- `traces/` — Derridean reading.
- `cotype/` — after the snap-to-grid accumulator concept.

The MCP URI scheme (`catalogue://...`) is unchanged: it identifies
addressable catalogue resources by purpose, not by package name.

## License

MIT. See [LICENSE](../../LICENSE) at the repo root.
