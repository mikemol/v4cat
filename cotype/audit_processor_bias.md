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

## Deferred

The following remain processor-flavoured but their bias is
example-heavy rather than structural. Listed in
priority-of-update order:

1. **`tutorial.md`** (~21 mentions). User-facing walk-through.
   Should be next when this audit continues.
2. **`methodology.md`** (~85 mentions). The bias is mostly in
   running examples that explain the design with processor
   specifics. The structural arguments are already domain-
   agnostic; rewriting the examples is mechanical but voluminous.
3. **`theory.md`** (~38 mentions). Similar — the abstract
   arguments are clean, but the worked examples (and the running
   case study in § 14) lean on processor names. Structurally
   sound; cosmetically biased.
4. **`examples.md`** (~10 mentions). This file's purpose is
   domain templates, so processor mentions here are
   *contextually correct* — processors are ONE of the templates,
   not privileged. The remaining mentions are likely fine as-is;
   a quick read should confirm.

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
