# v4cat — Symmetry-break cataloguing framework

A Python ISA + SQLite schema + MCP server for accumulating named
structural distinctions ("breaks") about a domain, with witnesses,
refinements, lineage edges, and the Klein-four read primitive.

The framework is **domain-agnostic**. The ISA's `introduce_object`,
`introduce_break`, `witness`, `refine` verbs and the analytic views
work the same whether the witness objects are programming languages,
processors, cryptographic primitives, file systems, formal systems,
ML architectures, or anything else with structure worth cataloguing.
See [examples.md](examples.md) for domain templates.

See [methodology.md](methodology.md) for the design.

## Layout

```text
v4cat/
├── __init__.py              public API
├── catalogue.py             SymmetryCatalogue class (the ISA)
├── views.py                 kquery + analytic queries
├── mcp_server.py            FastMCP server exposing tools/resources/prompts
├── schema.sql               generic framework schema (S0-S11)
├── cells.py                 Cell tagged union + Kinds enum (theory.md § 14.5.1)
├── theory.py                framework signature, the IMPL referent (§ 14.5.2)
├── bootstrap.py             closure check (§ 14.5.4); SelfHostingViolation
├── framework_seed.sql       framework self-cataloguing seed data (§ 14.5.5)
├── methodology.md           operational design — ISA, schema, KQUERY, MCP
├── theory.md                foundations — shadow architecture, Klein-four, Yoneda+Derrida, magma+pointfree, Theorem 14.5
├── tutorial.md              LLM-friendly walk-through, empty → small worked domain
├── examples.md              domain templates (languages, processors, crypto, …)
├── README.md                this file
├── pyproject.toml           pip-installable package metadata
└── tests/
    ├── test_isa.py          framework tests, synthetic data
    ├── test_mcp.py          MCP server tests, synthetic data
    └── test_self_hosting.py regression test for Theorem 14.5
```

## Documentation

The framework is documented at four levels of depth:

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
  trace-thickening.
- **`examples.md`**: domain templates — programming languages,
  cryptographic primitives, databases, file systems, network
  protocols, mathematical structures, OS designs, ML architectures.

All five files are exposed as MCP resources at `catalogue://readme`,
`catalogue://tutorial`, `catalogue://methodology`,
`catalogue://theory`, and `catalogue://examples`. There's also
`catalogue://docs` — an index resource that lists everything
available, suitable as the entry point for an LLM encountering
the framework.

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

## Run the MCP server

Two persistence modes, mutually exclusive:

```sh
# Pinned-file: server pinned to one SQLite file. Slot tools error;
# the LLM has no string to redirect.
python -m v4cat.mcp_server --db /path/to/cat.db

# Named-slot: server confined to a sandbox directory. Slot tools
# become available; clients address catalogues by slug, never path.
python -m v4cat.mcp_server --root /path/to/dir [--default mydomain]
```

In named-slot mode the server only ever opens files matching
`<root>/<slug>.db`, where `<slug>` is `[A-Za-z0-9][A-Za-z0-9_-]{0,63}`.
The slug regex rules out `..`, `/`, `\`, leading dots, and NUL bytes;
post-resolve the parent must equal the resolved root, catching
symlink-escape attempts. See [v4cat/sandbox.py](sandbox.py) for the
validation.

Connects via stdio (the standard MCP transport). Configure your
MCP-aware client (Claude Desktop, Claude Code, custom agents) to
talk to it.

The server exposes:

- **tools**: every ISA verb (`introduce_break`, `introduce_object`,
  `witness`, `refine`, `defer`, `promote`, `boundary`, `kquery`,
  `query_origin`, `query_lineage`, etc.) plus, in named-slot mode,
  `list_catalogues`, `open_catalogue`, `create_catalogue`.
- **resources**: addressable views (`catalogue://breaks`,
  `catalogue://objects/{id}`, `catalogue://retroactive`,
  `catalogue://axes`, `catalogue://lineages/{id}`,
  `catalogue://self_hosting`, ...)
- **prompts**: workflow templates (`analyze_new_object`,
  `audit_md_vs_sql`, `next_object`, `snap_to_grid_check`)

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
python -m v4cat.tests.test_mcp
```

Both use synthetic data only and don't depend on any specific
domain. 50 tests; all green on Python 3.13.

## Methodology

The brief version:

1. **Identity is relational** (Yoneda). An object is its
   participation in the witness graph; nothing more.
2. **Time and lineage are breaks-themselves.** Year and lineage
   are recorded once per object as primary data; *attribution
   emerges* via tropical MIN-year over origin-class edges.
   There's no `RETRO` verb.
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

(Inherits from parent repo.)
