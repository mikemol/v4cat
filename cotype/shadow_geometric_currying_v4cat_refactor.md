# Shadow: geometric currying — v4cat-core refactor (promissory)

**Tracking**: [v4cat-oss/v4cat#5](https://github.com/v4cat-oss/v4cat/issues/5) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_geometric_currying.md](shadow_geometric_currying.md)).
> Region **#4** (S2G alone — pure cataloguing). The v4cat-side
> half of the seven-repo migration; the load-bearing one — when
> this lands, the substrate is operational.*

## Form

`v4cat` (Python) currently implements the RISC ISA as flat
operations on the `specs`, `breaks`, `witnesses`, `lineages`,
and `node_attrs` tables. `edge()` validates that the kind is
catalogued, then `INSERT OR IGNORE`s into the dispatch table
([catalogue.py lines 474–524][edge-py]).

[edge-py]: https://github.com/v4cat-oss/v4cat/blob/main/src/v4cat/catalogue.py#L474-L524

The geometric-currying substrate ([`shadow_geometric_currying.md`](shadow_geometric_currying.md))
requires an internal layer underneath the existing public API:

```text
introduce_cell(cell_id, cell_kind)
bind_role(cell_id, role, occupant_id)
close_boundary(cell_id)
close_cell(cell_id)
advance_path(path_id, cell_id)
```

The existing `introduce_node` and `edge` redirect to this layer.
**Public API is unchanged for v0.x compatibility.**

## What to extract

### Internal-layer functions (under `v4cat/src/v4cat/cells.py`, new module)

| Function | Purpose |
| --- | --- |
| `introduce_cell(cell_id, cell_kind)` | introduce a cell of stated kind (`NodeCell` or `EdgeCell`); idempotent |
| `bind_role(cell_id, role, occupant_id)` | record a role-binding `ρ_r(e, x)`; one of three for each EdgeCell |
| `close_boundary(cell_id)` | check that all three role-bindings are present + closed; if so, mark the boundary as closed |
| `close_cell(cell_id)` | mark a cell as closed (precondition: boundary is closed) |
| `advance_path(path_id, cell_id)` | append a step to a path; precondition: cell is closed |

### Existing public API redirects

```python
def introduce_node(self, id, name, type, attrs=None):
    introduce_cell(id, "NodeCell")
    bind_role(id, "self", id)
    close_cell(id)                          # 0-cells close trivially
    materialize_legacy_node_projection(id, name, type, attrs)

def edge(self, src, tgt, kind):
    cell = edge_cell_id(src, kind, tgt)     # H(s, k, t) — content-addressed
    introduce_cell(cell, "EdgeCell")
    bind_role(cell, "source", src)
    bind_role(cell, "kind",   kind)
    bind_role(cell, "target", tgt)
    close_boundary(cell)                    # closes if all three bind
    close_cell(cell)                        # closes if boundary is closed
    materialize_legacy_edge_projection(cell, src, tgt, kind)
```

The legacy `witnesses` / `lineages` rows are kept as **saturated
projections** of closed edge-cells. Old consumers continue to
work; new consumers can query the cell layer directly.

### Schema additions (`v4cat/src/v4cat/schema.sql`)

```sql
CREATE TABLE IF NOT EXISTS cells (
  id            TEXT PRIMARY KEY,
  cell_kind     TEXT NOT NULL,            -- NodeCell | EdgeCell | ...
  closure_state TEXT NOT NULL DEFAULT 'open'  -- open | boundary-closed | closed
);

CREATE TABLE IF NOT EXISTS role_bindings (
  cell_id       TEXT NOT NULL,
  role          TEXT NOT NULL,            -- source | kind | target | self
  occupant_id   TEXT NOT NULL,
  closure_state TEXT NOT NULL DEFAULT 'open',
  PRIMARY KEY (cell_id, role)
);

CREATE TABLE IF NOT EXISTS path_steps (
  path_id     TEXT NOT NULL,
  step_index  INTEGER NOT NULL,
  cell_id     TEXT NOT NULL,
  PRIMARY KEY (path_id, step_index)
);
```

The legacy `witnesses` / `lineages` tables remain. New schemas
are additive, not replacements.

### Vocabulary extensions (`v4cat/src/v4cat/framework_seed.sql`)

Catalogue 11 new node-kinds + 17 new edge-kinds per
`shadow_geometric_currying.md`'s "New self-hosted vocabulary"
section. Each is an ordinary spec/edge-kind row in
`framework_seed.sql` so the bootstrap ships HF-GeometricCurrying
on first load.

### Bootstrap closure recognizers (also in `framework_seed.sql`)

Four T-* tensions:

```text
T-edge-boundary-closure
  Detect EdgeCells whose boundary is not closed (cell-closure cover, c01 cell)

T-edge-projection-backed-by-cell
  Detect saturated edge-projections (witnesses / lineages rows) without backing cells
  (path-advancement cover, c01 cell — presentation-without-substrate)

T-path-advance-only-through-closed-cells
  Detect path-steps that advance through unclosed cells
  (path-advancement cover, c01 cell, oriented for path scope)

T-path-presentation-closure
  Detect path-presentations whose underlying path lacks closed cells
```

Each compiles to a `KqueryNode` AST in the existing curry-spec
algebra ([`curry.py`](https://github.com/v4cat-oss/v4cat/blob/main/src/v4cat/curry.py)).

### Referent renames (in `curry.py`)

```text
CellReferent  ->  KqueryCellReferent      (existing — clarified by rename)
                  EventCellReferent       (new)
                  RoleHornReferent        (new)
                  BoundaryClosureReferent (new)
```

The rename is a backward-incompatible API change to a non-public
class. Mitigation: keep `CellReferent` as a deprecated alias for
`KqueryCellReferent` in v0.x, remove in v1.0.

### New ISA verbs (eventually)

`record / replay / invert` for path operations — closing the
[event-log gap](shadow_event_log_gap.md). These can land in this
sub-fire or in a follow-up; if deferred, they get their own
sub-shadow.

## Why deferred from this fire

This fire is **substrate-naming-only** (S₀ from the user's
brief). The actual implementation of the cell layer + schema
additions + vocabulary seed + closure recognizers + referent
renames is substantial work; bundling it into the
substrate-naming fire would land in region #5 (DBE+RFS without
adequate S2G granularity).

Per the agda2v4cat-Tier-3 + v4cat-octave-promissory precedent:
one shadow per future fire keeps closure trails clean.

## Future fire

`gc-v4cat-core`. Region #8 expected (DBE-led with substantive
RFS — the existing tables become projections of the new cell
substrate; the existing `EdgeReferent` becomes a saturated-edge
projection; the existing curry algebra extends). Closure-scope:
single-repo (writes only land in `v4cat-oss/v4cat`).

Recommended ordering within the migration: this sub-fire **first**
(the substrate is operational) before the carriers and the
reference carriers consume it.

## Closure path

Closes when v4cat ≥ v0.x ships:

1. `cells.py` module with the five internal-layer functions.
2. Schema additions (`cells`, `role_bindings`, `path_steps`
   tables).
3. Public API redirects (`introduce_node` / `edge` go through
   the cell layer; legacy projections continue to materialise).
4. Vocabulary extensions (HF-GeometricCurrying nodes + 17
   edge-kinds in `framework_seed.sql`).
5. Four T-* closure recognizers as bootstrap tensions.
6. `curry.py` rename: `CellReferent` → `KqueryCellReferent`;
   new `EventCellReferent`, `RoleHornReferent`,
   `BoundaryClosureReferent`.
7. Test coverage: every closure rule in the substrate has a
   matching pytest assertion.

Verification: kernel-parity tests (against
[v4cat-octave](https://github.com/v4cat-oss/v4cat-octave) once
*its* sub-fire lands) continue to produce identical V₄ cells.
