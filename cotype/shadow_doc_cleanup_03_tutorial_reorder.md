# Shadow: D₃ — tutorial.md reorder

> Per [shadow_doc_cleanup_plan.md](shadow_doc_cleanup_plan.md).

## Form

§ 2 reframed from "The seven verbs and one classifier" to
"Three RISC primitives + named conveniences." The new section
leads with the three RISC primitives (INTRODUCE_NODE, EDGE,
KQUERY) as the structural core, then a CISC sugar table
documenting the existing verbs and their reductions. The section
notes that §§ 3–13 walk through CISC sugar (the ergonomic path)
and § 14 shows the RISC equivalent.

§ 14 (formerly "— added 2026-05-03" appendage) is retained but
reframed: it is now a legitimate deep section in the tutorial's
arc, not an appendage. The lead paragraph turns the walkthrough
inside-out — same operations, RISC expression. § 14.1's title
changes from "RISC equivalents of the CISC walkthrough" to
"Side-by-side: CISC sugar and RISC primitives" so neither side
reads as derivative of the other.

§§ 3–13 (the CISC walkthrough) are unchanged. The reader who
follows the linear flow gets ergonomic CISC verbs first; § 14
provides the structural translation for readers who want it.

The TOC is updated to include § 14.

## Realisations

| Site | Change |
|------|--------|
| TOC item 2 | "The seven verbs and one classifier" → "Three RISC primitives + named conveniences" |
| TOC item 14 | added |
| § 2 | replaced with RISC primitives table + CISC sugar table + reduction column |
| § 14 heading | "— added 2026-05-03" suffix removed |
| § 14 lead paragraph | rewritten to frame § 14 as a natural deep section |
| § 14.1 heading | "RISC equivalents of the CISC walkthrough" → "Side-by-side: CISC sugar and RISC primitives" |

## Step-witness

- ✓ TOC items 2 + 14 valid
- ✓ § 2 leads with 3 RISC primitives
- ✓ CISC sugar documented with `derives_from`-style reductions
- ✓ § 14 retained but reframed
- ✓ No "added 2026-05-03" markers remain in tutorial.md
- ✓ §§ 3–13 walkthrough preserved (reader experience intact)
- ✓ Tables aligned
