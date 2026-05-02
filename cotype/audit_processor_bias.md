# Audit: removing CPU-ISA bias from v4cat

Session of 2026-05-02. The framework was lifted from a parent
processor catalogue (`mikemol/sixfiveohtwo`); this audit removes
bias toward processors so the framework presents as
domain-agnostic, with processors as one of several legitimate
example domains rather than the privileged one.

## Done in this audit

### Code (structural bias — fully removed)

- **`__init__.py`** — quick-start example replaced with synthetic
  `alpha`/`beta`/`F1` objects; module docstring now states the
  framework is domain-agnostic and points at examples.md.
- **`views.consistency()`** — was hardcoded to a single `'q92'`
  rule with processor-specific docstring. Now parametric over any
  rule name; validates the rule against
  `[A-Za-z][A-Za-z0-9_]*` to prevent SQL injection at the
  resource boundary; reads `<rule>_violations` from whatever
  domain extension is loaded.
- **`mcp_server.py`**:
  - Module docstring now references `analyze_new_object` and
    `next_object` instead of `analyze_new_processor` /
    `next_processor`.
  - Server `instructions=` block: removed "specs (witness objects:
    processors, formal systems)" → "specs (witness objects of any
    kind a domain extension introduces)".
  - `catalogue://q92_violations` resource → parametric
    `catalogue://violations/{rule}`. Returns `{'error': ...}` JSON
    on invalid rule names.
  - `introduce_object` tool docstring: example now uses synthetic
    data; the long list of domain types is generic.
  - `witness` tool: `scope='agent'` docstring no longer references
    8087/Q87 specifically — describes the structural condition
    (one named witness containing multiple distinguishable
    contributors).
  - `agent_witnesses` resource docstring: same generalisation.
  - **Prompts renamed**: `analyze_new_processor` →
    `analyze_new_object`, `next_processor` → `next_object`. Bodies
    rewritten to remove processor-specific phrasing while
    preserving the workflow structure (the heuristics and
    methodological reminders still apply to any domain).
  - `catalogue://docs` index: removed "non-processor domains"
    framing; added the parametric violations resource; updated
    agent-witnesses description.
- **`schema.sql`** — comments scrubbed of "Q72 in the processor
  catalogue" and "8087 forced agent-level Q87" historical
  references; replaced with the structural conditions the
  comments were trying to convey.
- **Tests** — `test_branch_coverage.py` and `test_mcp.py` updated
  to match the new API:
  - `test_consistency_q92_branch_taken` →
    `test_consistency_with_valid_rule_reads_violations_view`
    (uses `'demo'` instead of `'q92'`).
  - New `test_consistency_rejects_invalid_rule_name` covers the
    SQL-injection guard.
  - `test_q92_violations_resource` →
    `test_violations_resource_with_valid_rule` plus
    `test_violations_resource_rejects_bad_rule_name`.
  - `test_analyze_new_processor_prompt` →
    `test_analyze_new_object_prompt`.
  - `test_next_processor_prompt_uses_current_catalogue` →
    `test_next_object_prompt_uses_current_catalogue`.

### Surface docs (user-facing genericisation)

- **README.md** — opening paragraph rewritten to lead with
  domain-agnostic framing; "processor catalogue in the parent
  repo" reference removed; layout-table examples line updated;
  prompt names corrected.

## Deferred work — completed in v0.2.1

The deferred doc rewrites listed in v0.2.0's audit are done in
v0.2.1:

1. **`tutorial.md`** — generic alpha/beta/F1 examples now
   throughout the wedge audit; processor-catalogue parenthetical
   ("Q81 — multi-CPU shared-memory") removed; closing references
   to the parent repo's `symmetries.md` / `q92_violations`
   replaced with the parametric `catalogue://violations/{rule}`
   resource and a list of domain templates from `examples.md`.
   Three remaining processor mentions are list items where
   processor sits alongside other domains.

2. **`methodology.md`** — opening section rewritten to lead with
   domain-agnostic framing instead of "the processor catalogue is
   one application." The "How `symmetries.md` and `symmetries.sql`
   map onto the ISA" section, which detailed the parent repo's
   commit history, replaced with a generic worked example
   ("adding an object that forces a new break"). The K_QUERY paging
   example reframed as a generic A/B consistency rule with a
   parenthetical note that processor catalogues bind A=paged,
   B=restart-suitable. The MCP example dialogue now uses
   omega/F-new/synthetic data instead of z16/Q94/mainframe. The
   open-questions section's Q89-paging cross-domain example
   reframed generically.

3. **`theory.md`** — § 2's preservation-theorem examples flagged
   as processor-catalogue context; § 3's "Q72 in the processor
   catalogue" reduced to an ordinary structural claim; § 4's K_QUERY
   `00`-cell paging example reframed as a generic
   "rule-of-the-form-A-requires-B" schematic with a parenthetical
   processor illustration. § 5's StepRule examples list processor
   alongside lambda calculus and Brainfuck. § 8's Derridean
   commitment list (no foundational break / origin / schema /
   object) now uses generic phrasing. § 11's convergence section's
   long enumeration of x86 / 68k / mainframe processor history
   replaced with a generic "in a processor catalogue's growth
   history" sketch that names the same convergence shape without
   the specific year/break tuples. § 12's retroactive-attribution
   example now uses α/β with the processor catalogue's
   80386/System/360/67 case as a parenthetical illustration.
   § 13's `Q81 (multi-CPU sibling-framework boundary)` framing
   replaced with a discussion of the `BOUNDARY` verb's general
   stance.

4. **`examples.md`** — opening rewritten to lead with
   domain-agnostic framing. Section 1 renamed from "Processor
   architectures (the canonical case)" to just "Processor
   architectures." The processor section's parent-repo references
   removed, the Q-numbered break enumeration replaced with a
   list of *kinds of breaks* (paging, interrupts, vector facility,
   ...) so the section reads as a domain template like the
   others. Closing reference to the parent repo's
   `symmetries.md` / `symmetries.sql` removed.

5. **`README.md`** — license note updated from "(Inherits from
   parent repo.)" to "MIT. See [LICENSE](../../LICENSE)."

Verification: 160 tests pass; 100% statement and branch coverage
holds (no code changed). Released as v0.2.1.

## What's NOT bias

- The repo is named `v4cat` and the term "Symmetry-break
  cataloguing" is the methodology's name. Neither implies
  processors.
- The framework's claim that *every* read is a kquery is
  domain-neutral.
- The 8 cell kinds (`O,B,W,R,E,A,K,X`) are domain-neutral.
- The closure check (Theorem 14.5) is domain-neutral.
- The `framework_seed.sql` self-cataloguing data is domain-
  neutral (it catalogues v4cat's own primitives, which are
  about cataloguing, not about processors).

## Verification

After all code changes: 160 tests pass (was 159; +2 from
splitting `test_consistency_unknown_rule_raises` into the two
parametric versions, and the new
`test_violations_resource_rejects_bad_rule_name`); 100% branch
coverage holds (572 stmts → 577 stmts due to the new regex
match + ValueError raise; all branches covered).

API breakage from this audit:

- **`consistency(cat, rule)`** now accepts any valid identifier
  and reads `<rule>_violations` instead of dispatching on
  `'q92'`. Existing callers that passed `'q92'` will continue
  to work IFF a `q92_violations` view is present in the
  catalogue's loaded schema.
- **`catalogue://q92_violations`** is gone. Replaced by
  parametric **`catalogue://violations/{rule}`** — clients should
  request `catalogue://violations/q92` instead.
- **MCP prompts renamed**: `analyze_new_processor` →
  `analyze_new_object`, `next_processor` → `next_object`.

This is `0.1.0` → `0.2.0` material. Nothing in the parent repo's
processor catalogue depends on these specific names; updates
there can use the new generic forms.
