# v4cat — Python API discipline

> *Grade: API guide.
> Companion to [rigorous_use.md](rigorous_use.md) (the operating covenant)
> and [methodology.md](methodology.md) (the operational design).
> Read this when you want to drive the non-MCP API in the same
> spirit the framework drives itself.*

The non-MCP API should be used as a **local proof discipline**:

```text
write only through catalogue verbs;
read serious comparisons through kquery/tensions;
derive status/origin/gaps through views;
treat raw SQL as extension substrate, not ordinary use.
```

The API already has the right strata.

```text
RISC mutation:
  SymmetryCatalogue.introduce_node
  SymmetryCatalogue.edge

RISC read:
  v4cat.kquery

Reusable reads:
  v4cat.curry.Tension
  SymmetryCatalogue.evaluate_tension

CISC convenience:
  introduce_object
  introduce_break
  witness
  refine
  defer
  promote
  boundary
  tropical_min / tropical_max

Self-audit:
  v4cat.bootstrap.check_closure
  v4cat.bootstrap.closure_status
  v4cat.bootstrap.check_risc_discipline

Legacy / substrate:
  query
  load_extension
  conn.execute
```

## 1. Default to self-hosted catalogue opens

For serious use, open with the default constructor:

```python
from v4cat import SymmetryCatalogue

with SymmetryCatalogue("domain.v4cat.db") as cat:
    ...
```

Do **not** use this for serious catalogues unless you intentionally want an empty, non-self-hosted test fixture:

```python
SymmetryCatalogue(":memory:", check_self_hosting=False)
```

The default path loads the framework seed, loads the self-cataloguing data, and runs the self-hosting closure check. That is what lets the rest of the RISC surface work.

Practical rule:

```text
Production / research catalogue:
  check_self_hosting=True

Unit tests needing a blank database:
  check_self_hosting=False

Migration debugging:
  maybe False, but only temporarily
```

## 2. Prefer `introduce_node` and `edge` when defining serious structure

The rigorous form is:

```python
cat.introduce_node("B-claim", "Claimed structural break", "break")
cat.introduce_node("paper-1", "Paper 1", "spec", attrs={"year": 2024})
cat.edge("paper-1", "B-claim", "origin")
```

That is the canonical shape:

```text
node
node
typed edge
```

The CISC helpers are acceptable, but you should remember their reduction:

```python
cat.introduce_break("B-claim", "Claimed structural break")
cat.introduce_object("paper-1", "Paper 1", year=2024)
cat.witness("paper-1", "B-claim", "origin")
```

This is fine for ordinary domain work. But when you are trying to use v4cat "as rigorously as itself," the mental model should still be:

```text
introduce_object  ≃ introduce_node(type='spec')
introduce_break   ≃ introduce_node(type='break')
witness           ≃ edge(spec, break, kind)
lineage_witness   ≃ edge(spec, spec, kind)
refine            ≃ introduce_node(child break) + edge(origin) + edge(refines)
defer/promote     ≃ witness constructors
boundary          ≃ witness(kind='sibling-boundary')
```

## 3. Introduce domain vocabulary before using it

A rigorous catalogue should not invent edge kinds implicitly. If your domain needs a new edge relation, catalogue it first.

Example:

```python
with SymmetryCatalogue("domain.db") as cat:
    # Domain node type. Physically these still live in specs,
    # but they are typed as "paper".
    cat.introduce_node("paper", "Paper", "node-type")

    # Domain edge kind: paper/spec-like node to break.
    cat.introduce_node(
        "literature-supports",
        "literature-supports",
        "edge-kind",
        attrs={
            "source-type": "paper",
            "target-type": "break",
        },
    )

    cat.introduce_node("P1", "Some Prior Paper", "paper", attrs={"year": 1998})
    cat.introduce_node("B1", "Residue-aware four-cell comparison", "break")

    cat.edge("P1", "B1", "literature-supports")
```

Current `edge()` dispatch supports target types `'break'` and `'spec'`, because those map to the existing `witnesses` and `lineages` tables. Domain node types are still physically spec-like, so `source-type` is mostly a catalogued declaration today; the implementation validates target type more strongly than source type. Treat that as a known current limitation, not as a reason to skip declaring source type.

## 4. Use `kquery` directly for every serious boundary audit

Do not use `wedge()` as your primary rigorous read. `wedge()` is legacy/selection sugar and does not preserve `00`.

Use:

```python
from v4cat import kquery

U = {
    "claim-a",
    "claim-b",
    "claim-c",
    "claim-d",
}

implemented = {
    "claim-a",
    "claim-b",
}

catalogued = {
    "claim-b",
    "claim-c",
}

cells = kquery(implemented, catalogued, universe=U)

assert cells == {
    "00": ["claim-d"],
    "01": ["claim-c"],
    "10": ["claim-a"],
    "11": ["claim-b"],
}
```

Interpretation:

```text
11: implemented and catalogued
10: implemented but not catalogued
01: catalogued but not implemented
00: in scope but seen by neither
```

The discipline is:

```text
always pass universe=... when 00 matters;
treat normalize=... as an explicit quotient;
treat emit=... as an explicit projection.
```

For rigorous audits, do not write:

```python
kquery(A, B)
```

unless you are intentionally saying:

```text
U = A ∪ B
therefore 00 is forced empty
```

Better:

```python
kquery(A, B, universe=declared_scope)
```

## 5. Wrap repeated `kquery` shapes as tensions

When a comparison matters more than once, turn it into a `Tension`.

That is how you prevent "analysis" from becoming ad hoc Python code.

```python
from v4cat.curry import (
    Tension,
    KqueryNode,
    EdgeReferent,
    AxisCutReferent,
    Param,
)

origin_before = Tension(
    id="Q-origin-before",
    name="Origin witnesses before threshold",
    description="Compare origin-class witnesses of break B against specs before time t.",
    disposition="audit",
    parameters=("B", "t"),
    shape=KqueryNode(
        a=EdgeReferent(
            pivot=Param("B"),
            kinds=("origin", "catalogue-introduces"),
            pivot_role="target",
            return_role="source",
        ),
        b=AxisCutReferent(
            axis_column="year",
            op="<=",
            threshold=Param("t"),
        ),
    ),
)

with SymmetryCatalogue("domain.db") as cat:
    cells = cat.evaluate_tension(origin_before, B="B1", t=2000)
```

That gives you a reusable arrow:

```text
χ : U → V₄
```

rather than a one-off report.

Use `disposition` honestly:

```text
concern     — something unresolved
utility     — regular derived read
diagnostic  — detects a condition
audit       — verifies a boundary/invariant
```

## 6. Let lifecycle methods create witnesses, not statuses

Use these as witness constructors:

```python
cat.defer("B1", by="P1", reason="Candidate break, insufficient independent support.")
cat.promote("B1", by="P2", reason="Independent confirmation.")
cat.boundary("B1", by="P3", reason="Adjacent but intentionally non-merged distinction.")
```

Do **not** treat them as imperative state transitions.

The rigorous reading is:

```text
defer   → witness(kind='deferred-candidate')
promote → witness(kind='confirms')
boundary→ witness(kind='sibling-boundary')
status  → derived view
```

So this is good:

```python
status = cat.status("B1")
```

This is bad as a practice:

```sql
UPDATE breaks SET status = 'active' ...
```

The status should be a derived consequence of the witness graph.

## 7. Use tropical queries for ordered attribution, not hand-written origin fields

Origin and first-seen should remain derived.

```python
origin = cat.origin("B1")
first_seen = cat.first_seen("B1")
gap = cat.retroactive_gap("B1")
```

For non-year axes, use the generic ordered query:

```python
rows = cat.tropical_min(
    axis_column="year",
    witness_kinds=("origin", "catalogue-introduces"),
    break_="B1",
)

recent = cat.tropical_max(
    axis_column="year",
    witness_kinds=("confirms",),
    break_="B1",
)
```

This is the right pattern:

```text
store witnesses;
derive attribution;
derive gap;
do not store conclusion as primary fact.
```

## 8. Use `load_extension()` only for additive schema and named views

`load_extension()` is the right place for domain-specific tables, indexes, views, and consistency rules.

A good extension SQL file looks like this:

```sql
CREATE TABLE IF NOT EXISTS literature_sources (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER
);

CREATE VIEW IF NOT EXISTS unsupported_claim_violations AS
SELECT b.number AS break_number, b.name AS break_name
FROM breaks b
WHERE NOT EXISTS (
    SELECT 1
    FROM witnesses w
    WHERE w.break_number = b.number
      AND w.kind IN ('origin', 'catalogue-introduces', 'confirms', 'literature-supports')
);
```

Then:

```python
from v4cat import SymmetryCatalogue, consistency

with SymmetryCatalogue("domain.db") as cat:
    cat.load_extension("literature_extension.sql")
    violations = consistency(cat, "unsupported_claim")
```

The convention is important:

```text
<rule>_violations
```

because `consistency(cat, "unsupported_claim")` reads:

```sql
SELECT * FROM unsupported_claim_violations
```

So a domain consistency rule is a materialized `10`-style violation view.

## 9. Treat `query()` as read-only unless you are writing framework/extension code

The API exposes:

```python
cat.query(sql, *params)
```

Use it for SELECTs:

```python
rows = cat.query(
    "SELECT * FROM witnesses WHERE break_number = ? ORDER BY kind",
    "B1",
)
```

Avoid using it for ordinary mutation, even though SQLite would allow mutation through `conn.execute`.

Good mutation path:

```python
cat.introduce_node(...)
cat.edge(...)
cat.witness(...)
cat.refine(...)
```

Bad ordinary-use path:

```python
cat.query("INSERT INTO witnesses ...")
cat.conn.execute("UPDATE ...")
```

Reserve `conn.execute` and mutation SQL for:

```text
schema extensions
migrations
indexes
materialized domain views
repair scripts with explicit audit
```

## 10. After significant changes, run the same checks the framework runs

For framework-level closure:

```python
from v4cat.bootstrap import check_closure, closure_status, check_risc_discipline

with SymmetryCatalogue("domain.db") as cat:
    check_risc_discipline()
    result = check_closure(cat)
```

For inspection without raising:

```python
from v4cat.bootstrap import closure_status

status = closure_status(cat)
if status is not None:
    print(status["10"], status["01"], status["00"], status["11"])
```

For domain-level rigor, define your own analogue:

```python
from v4cat import kquery

def domain_claim_closure(cat):
    implemented = {
        row["id"]
        for row in cat.query("SELECT id FROM implementation_claims")
    }
    catalogued = {
        row["break_number"]
        for row in cat.query(
            "SELECT DISTINCT break_number FROM witnesses "
            "WHERE kind = 'catalogue-introduces'"
        )
    }
    universe = {
        row["id"]
        for row in cat.query("SELECT id FROM accountable_claim_universe")
    }
    return kquery(implemented, catalogued, universe=universe)
```

That is the pattern you want:

```text
make each serious domain define its own ClosureKQ.
```

## 11. Use snapshots as comparisons, not replacements

The API does not yet provide a formal snapshot abstraction, but you can already do this with `query()` + `kquery`.

```python
def break_set(cat):
    return {
        row["number"]
        for row in cat.query("SELECT number FROM breaks")
    }

before = break_set(cat)

# perform additions
cat.introduce_break("B-new", "New distinction")
cat.witness("source-1", "B-new", "catalogue-introduces")

after = break_set(cat)

cells = kquery(before, after, universe=before | after)
```

Interpretation:

```text
10 old-only: removed / lost claims
01 new-only: added claims
11 stable: preserved claims
00 impossible here unless universe wider than before∪after
```

For a real audit, use a wider declared universe.

## 12. Recommended usage skeleton

This is the practical pattern I would use for every serious catalogue.

```python
from v4cat import SymmetryCatalogue, kquery, consistency
from v4cat.bootstrap import check_closure, check_risc_discipline
from v4cat.curry import Tension, KqueryNode, EdgeReferent, LiteralReferent

DB = "research.v4cat.db"

with SymmetryCatalogue(DB) as cat:
    # 1. Framework self-discipline.
    check_risc_discipline()
    check_closure(cat)

    # 2. Domain vocabulary.
    cat.introduce_node("paper", "Paper", "node-type")
    cat.introduce_node(
        "literature-supports",
        "literature-supports",
        "edge-kind",
        attrs={"source-type": "paper", "target-type": "break"},
    )

    # 3. Domain objects and breaks.
    cat.introduce_node("P-belnap", "Belnap 1977", "paper", attrs={"year": 1977})
    cat.introduce_node("B-four-cell", "Four-cell comparison cover", "break")

    # 4. Witness edges, not conclusion fields.
    cat.edge("P-belnap", "B-four-cell", "literature-supports")
    cat.witness("P-belnap", "B-four-cell", "catalogue-introduces")

    # 5. Direct V₄ audit with explicit universe.
    artifact_claims = {"B-four-cell", "B-arrow-category", "B-self-hosting"}
    literature_claims = {"B-four-cell"}
    universe = {
        "B-four-cell",
        "B-arrow-category",
        "B-self-hosting",
        "B-provenance",
    }

    audit = kquery(
        artifact_claims,
        literature_claims,
        universe=universe,
    )

    # 6. Interpret every residue.
    for claim in audit["10"]:
        cat.defer(claim, by="P-belnap", reason="Artifact-only until independently witnessed.")

    for claim in audit["00"]:
        cat.boundary(claim, by="P-belnap", reason="In declared scope but untreated by both sides.")
```

## 13. The API discipline in one table

| Need                         | Use                                      | Avoid                          |
| ---------------------------- | ---------------------------------------- | ------------------------------ |
| Add a real entity            | `introduce_node`                         | raw `INSERT`                   |
| Add a relation               | `edge`                                   | untyped prose                  |
| Add ordinary object/break    | `introduce_object`, `introduce_break`    | manual table writes            |
| Add support/claim/refinement | `witness`, `refine`                      | status flags                   |
| Mark lifecycle               | `defer`, `promote`, `boundary`           | direct status mutation         |
| Compare two observers        | `kquery(..., universe=U)`                | `wedge()` as primary audit     |
| Reuse a comparison           | `Tension` + `evaluate_tension`           | repeated ad hoc SQL            |
| Domain consistency           | `<rule>_violations` + `consistency()`    | prose-only checklist           |
| Framework integrity          | `check_closure`, `check_risc_discipline` | trusting docs                  |
| Domain extension             | `load_extension()` with idempotent SQL   | non-repeatable migration blobs |
| Inspection                   | `query(SELECT ...)`                      | mutation through `query()`     |

## 14. The strict operating rule

A rigorous v4cat client should satisfy this invariant:

```text
Every mutation is a node or edge introduction.

Every serious read is a kquery, a named selection from kquery,
or a tension that evaluates to kquery.

Every conclusion is derived from witnesses.

Every quotient is named.

Every blind spot requires an explicit universe.

Every extension adds checks, not just tables.
```

That is how the non-MCP API supports using v4cat the way v4cat uses itself.
