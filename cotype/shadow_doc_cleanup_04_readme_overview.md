# Shadow: D₄ — README.md overview

> Per [shadow_doc_cleanup_plan.md](shadow_doc_cleanup_plan.md).

## Form

First paragraph rewritten to lead with the RISC core
(`introduce_node`, `edge`, `kquery`) and reference the
strengthened closure check at theory.md § 14.5.8. Cross-refs to
methodology.md, tutorial.md, and the cotype/ shadow library now
appear in the second paragraph as the natural deeper reads.

The Documentation section gains a `cotype/` entry pointing at
the architectural shadow library. The MCP-resource list and
quick-start example are unchanged — the quick-start uses CISC
verbs (introduce_object, introduce_break, witness, refine) which
remain ergonomic and are now documented as sugar in tutorial § 2.

## Realisations

| Site | Change |
|------|--------|
| First paragraph | Rewritten to lead with RISC core + closure-check reference |
| Second paragraph (cross-refs) | New paragraph pointing at methodology, tutorial, and cotype/ |
| Documentation list | New `cotype/` entry as the architectural source-of-truth |
| Quick-start example | Unchanged (CISC verbs are valid sugar) |
| Layout block | Unchanged (file listing stays accurate) |

## Step-witness

- ✓ First paragraph mentions (β) RISC core
- ✓ cotype/ pointer present and labeled as architectural source
- ✓ theory.md § 14.5.8 referenced for the closure-check strengthening
- ✓ Layout block unchanged (still accurate)
- ✓ Quick-start CISC example preserved (valid sugar)
- ✓ No "added 2026-05-03" markers introduced
