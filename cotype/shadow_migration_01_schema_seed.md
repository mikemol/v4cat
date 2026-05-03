# Shadow: Migration step S₁ — schema columns + type-system seed

> **Forward shadow, generated at S₁ implementation start.**
> Per [shadow_migration_plan.md](shadow_migration_plan.md)'s
> DBE-Step-7 discipline: each step gets its own
> Form/Realisations/Composition/Entailment shadow as
> implementation begins.

## Form

S₁ adds the **declarative substrate** for the RISC reframe:
schema columns on `tensions` to store curry-spec ASTs, plus
type-system seed rows in `framework_seed.sql` that catalogue
the framework's own primitive vocabulary as data. No new tables;
no new schema constraints beyond CHECK on the `disposition`
column; no validation hooks (those land in S₂ with `edge` /
`introduce_node`).

```sql
-- Schema (schema.sql) additive deltas:
ALTER TABLE tensions ADD COLUMN disposition TEXT
    DEFAULT 'concern'
    CHECK (disposition IN ('concern','utility','diagnostic','audit'));
ALTER TABLE tensions ADD COLUMN parameters_json TEXT;
ALTER TABLE tensions ADD COLUMN shape_json TEXT;

-- Seed (framework_seed.sql) additive INSERTs:
specs:                          5 node-type tokens + 17 edge-kind tokens
breaks:                         10 attribute-schema breaks (K-ATTR-*)
spec_attributes:                type, source-type, target-type entries
witnesses:                      requires-attr / admits-attr edges
                                (using existing witnesses table; new
                                 kind labels added to vocabulary)
```

## Realisations

| Form element | Target file | Position |
|--------------|-------------|----------|
| Schema deltas | [schema.sql](../src/v4cat/schema.sql) | new section after S11 lineages, before VIEWS |
| Seed type-tokens | [framework_seed.sql](../src/v4cat/framework_seed.sql) | new section after the existing INSERTs |
| Seed attribute-breaks | [framework_seed.sql](../src/v4cat/framework_seed.sql) | same section |
| Seed type-relations | [framework_seed.sql](../src/v4cat/framework_seed.sql) | same section |
| Documentation | inline SQL comments noting "S₁ — type-system seed" header |

The type-tokens use `catalogue_order = NULL` and `year = NULL`
to mark them as system specs outside catalogue exposition order
and outside any temporal axis. Tropical-MIN queries filter NULLs
already (`AND s2.{axis_column} IS NOT NULL` in
[catalogue.py:321](../src/v4cat/catalogue.py#L321)) so this
won't perturb existing tropical results.

## Composition (with the migration plan)

S₁ is the *first* element of the ordered additive composition
defined in
[shadow_migration_plan.md](shadow_migration_plan.md). It enables
S₂ by providing:

- **Schema columns** that S₂'s `Tension` AST persistence will
  populate (`shape_json`, `parameters_json`, `disposition`).
- **Type-system seed data** that S₂'s `introduce_node` and
  `edge` validators will read via `kquery` to verify type
  conformance.

S₁ does *not* enable validation by itself; it only stages the
data. Validation engages in S₂ when the RISC verbs run their
type-checks against the seeded type-system.

## Entailment

```text
ALTER TABLE ADD COLUMN with DEFAULT (or NULL-allowed)
  + INSERT OR IGNORE rows that don't witness via 'framework' spec
  ⟹ no change to (impl_ids, cat_ids) sets used by check_closure
  ⟹ ClosureKQ(K, scope).gap = ∅ preserved
```

The closure check
([bootstrap.py:enumerate_supported_cells](../src/v4cat/bootstrap.py#L143-L177))
computes:

- `impl_ids` = cells from `SIGNATURE` whose kind ∈ `supported_kinds`
- `cat_ids` = `SELECT DISTINCT break_number FROM witnesses WHERE spec_id = 'framework'`

S₁ doesn't modify `SIGNATURE` (S₄ does) and doesn't add witnesses
where `spec_id = 'framework'`. The new specs are *not* `framework`;
the new breaks are *not* witnessed by `framework`. Therefore both
`impl_ids` and `cat_ids` remain unchanged, and the closure check
result is unchanged.

This is the additive-monoid property in action: the migration
substrate's invariants stay green because S₁'s delta lies entirely
outside the closure check's input domain.

## External commitments preserved

Per [rfs_findings_risc_projection.md](rfs_findings_risc_projection.md)'s
inventory:

| Commitment | Mechanism |
|------------|-----------|
| 169 tests pass | `ALTER TABLE ADD COLUMN` with default/NULL preserves all existing rows; new specs use `INSERT OR IGNORE` (idempotent); no SQL view definitions touched |
| Public `SymmetryCatalogue` API | No method signatures change in S₁ |
| MCP tool surface | Unchanged in S₁ |
| Closure check passes | New seed rows fall outside `(impl_ids, cat_ids)` (above entailment) |
| Anti-pattern (no drops) | All deltas are `ADD COLUMN` and `INSERT`; no `DROP`, no `DELETE`, no `ALTER TABLE` modifications other than additions |
| Database compatibility | `ALTER TABLE ADD COLUMN` with `DEFAULT` is non-breaking on SQLite for existing databases; reading old DBs at the new schema yields the default value for the new columns |
| IMPL ↔ CAT pairings | Existing pairings unchanged (S₁ doesn't touch `SIGNATURE`) |

## Step-witness (the green-light criterion)

Implementation of S₁ is complete iff:

1. `schema.sql` has the 3 `ALTER TABLE` deltas.
2. `framework_seed.sql` has the new INSERT blocks documented as
   "S₁ — type-system seed" header.
3. The full test suite (169 tests across 5 files) passes
   without modification.
4. Importing `SymmetryCatalogue` into a Python session and
   opening a fresh `:memory:` catalogue with `bootstrap=True,
   check_self_hosting=True` succeeds without raising
   `SelfHostingViolation`.

If any of (1)–(4) fail, the additive-move discipline has been
violated and the step rolls back via `git checkout -- <files>`.

## Cross-references

- [shadow_risc_core.md](shadow_risc_core.md) — the parent target
  architecture; this step delivers the seed declared in the
  "Self-hosted type system / Bootstrap floor" section.
- [shadow_migration_plan.md](shadow_migration_plan.md) — the
  ordered composition; this step is S₁ of 5.
- [rfs_findings_risc_projection.md](rfs_findings_risc_projection.md)
  — Finding 6 (tensions schema delta) and the type-system seed
  discussion under S₁ in the Extraction Queue.
