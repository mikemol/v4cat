# v4cat — Hosted skills

> *Grade: hosted-framework design.
> Companion to [hosted_skill_usage.md](hosted_skill_usage.md) (the operating
> manual) and [rigorous_use.md](rigorous_use.md) (the user-facing
> covenant). This document specifies how the four shadow-architecture
> skills (DBE, RFS, S2G, shadow-architecture) become v4cat-hosted
> framework objects whose claims, firing rules, intervention steps,
> products, residues, and closure obligations are themselves
> catalogued and kquery-auditable.*

The correct move is to make the skills into **hosted framework objects** inside v4cat, not merely documents *about* skills.

The task is region **#8: DBE + RFS + S2G**. The uploaded `shadow-architecture` skill explicitly defines the three-skill lattice, with DBE as forward "intact goal → shadows," RFS as sideways "existing artefact → shadows + recomposition," and S2G as backward "accumulated shadows → goal"; it also names the eight lattice regions, including two discipline-forbidden regions.

The formulation target is:

```text
Make shadow-architecture, decomposable-by-entailment,
regroup-from-shadows, and snap-to-grid into v4cat-hosted frameworks
whose claims, firing rules, intervention steps, products, residues,
and closure obligations are themselves catalogued and kquery-auditable.
```

## 1. DBE pass: name the costructure

The repeated form across the skills is not "a skill document." It is:

```text
HostedFramework
```

A `HostedFramework` is a v4cat object whose prose specification, runtime discipline, catalogue representation, and closure checks are compared by the same V₄ read.

Concretely:

```text
HostedFramework(F) =
  declared framework F
  + skill-document claims
  + v4cat nodes/edges representing those claims
  + tensions/kqueries that audit agreement
  + residues classified as promote / defer / boundary / out-of-scope
```

The composition operation is:

```text
host(F₁) ⊕ host(F₂) ⊕ ... ⊕ host(Fₙ)
  → hosted shadow-architecture
```

The entailment is:

```text
If each component skill is hosted as a framework,
and the lattice edges between skills are hosted,
and the closure queries show no unaccounted residues,
then the shadow-architecture itself is hosted.
```

This mirrors DBE's own rule: substantive work should first name a reusable costructure, name the composition, and name the entailment before proceeding. The DBE text says the skill produces "shadows" as named externalized substructures that survive context loss, and requires naming the costructure, composition operation, and entailment before implementation resumes.

So the first hosted object is:

```text
HF-HostedFrameworkContract
```

with this invariant:

```text
A hosted framework is valid only when every important claim in its
specification is represented as a v4cat node/edge/tension or explicitly
classified as out-of-scope.
```

## 2. RFS pass: extract the shadows from the existing skill bundle

The existing artifact is `shadow-architecture skill.md`. RFS applies because the artifact already contains several working protocols and cross-protocol patterns. RFS is defined as the sideways move that takes an existing artifact, extracts reusable substructures as named shadows, abstracts them where possible, and recomposes the artifact while preserving behavior.

The extracted shadows are these:

```text
Skill
FireCondition
NonFireCondition
InterventionStep
ExternalizedShadow
CompositionOperation
EntailmentClaim
Cotype
Quotient
SnapEvent
Recomposition
BehaviorPreservation
LatticeRegion
ForbiddenRegion
RegionTransition
SymmetryDiscovery
OperationalRole
ArcPhase
DisciplineRule
WarningSign
SuccessOutcome
ResidueAction
ClosureQuery
```

These shadows quotient into seven framework-level abstractions:

```text
1. FrameworkDeclaration
   What the skill claims to be.

2. FiringProtocol
   When the skill must, may, or must not fire.

3. InterventionProtocol
   The ordered procedure the skill executes.

4. ArtifactFlow
   What artifacts the skill consumes and produces.

5. ResidueDiscipline
   What happens to incomplete, ambiguous, forbidden, or drifting cases.

6. CompositionSemantics
   How the skill composes with the others.

7. ClosureObligation
   What query proves the hosted representation agrees with the source.
```

This is the regrouping: each skill document is no longer a blob of prose; it becomes an instance of the same hosted-framework schema.

## 3. S2G pass: snap the shadows onto the v4cat grid

S2G says the cotype accumulates shadows, forms useful quotients, and detects when the accumulated contents become consistent with the original request. It explicitly treats the cotype as the arena where shadows land, quotients form, structure accumulates, and snap-to-grid occurs when the entailment is consistent and sufficiently populated.

Here, the snap is:

```text
The three skills are not merely related documents.
They are orbit-elements of a single HostedFramework protocol.
```

The v4cat grid should therefore have these hosted node types:

```text
node-type: hosted-framework
node-type: framework-claim
node-type: firing-condition
node-type: intervention-step
node-type: produced-shadow
node-type: consumed-shadow
node-type: lattice-region
node-type: discipline-rule
node-type: closure-obligation
node-type: tension
node-type: residue-action
```

And these hosted edge kinds:

```text
declares
fires-on
does-not-fire-on
has-step
produces
consumes
composes-with
belongs-to-region
forbids-region
transitions-to
records-residue-as
audited-by
implemented-by
catalogued-by
projects-to
quotients-with
preserves
```

The hosted-framework grid is the `Cat`; the V₄ comparison is the audit.

## 4. The core v4cat hosting pattern

Each skill gets four layers.

### Layer A — source document claims

For DBE:

```text
DBE claims:
  - fires before substantive implementation/proof/formalisation
  - produces shadows
  - names target, costructure, composition, entailment
  - uses multi-angle attack when no substructure is visible
  - externalizes residue for S2G
```

For RFS:

```text
RFS claims:
  - fires on existing working artifacts
  - inventories commitments
  - extracts candidate shadows
  - abstracts across candidates
  - recomposes behavior-preservingly
  - documents the structural change
```

For S2G:

```text
S2G claims:
  - consumes accumulated shadows
  - maintains cotype
  - forms quotients
  - reads current entailment
  - checks consistency with original request
  - snaps when populated enough
```

For Shadow Architecture:

```text
Shadow Architecture claims:
  - orchestrates DBE/RFS/S2G
  - classifies 2³ = 8 regions
  - forbids R-only and D+R-without-S by discipline
  - treats region transitions as symmetry discoveries
  - recognizes DBE as carrier, S2G as sampler, RFS as burst
```

### Layer B — v4cat catalogue representation

Each claim becomes a `framework-claim` node.

Each skill becomes a `hosted-framework` node.

Each procedural step becomes an `intervention-step` node.

Each relation becomes an edge.

Example:

```python
from v4cat import SymmetryCatalogue

with SymmetryCatalogue("shadow_architecture.v4cat.db") as cat:
    cat.introduce_node(
        "HF-DBE",
        "decomposable-by-entailment",
        "hosted-framework",
        attrs={"role": "forward", "direction": "goal-to-shadows"},
    )

    cat.introduce_node(
        "C-DBE-produces-shadows",
        "DBE produces named externalized shadows",
        "framework-claim",
    )

    cat.edge("HF-DBE", "C-DBE-produces-shadows", "declares")

    cat.introduce_node(
        "STEP-DBE-name-costructure",
        "Name the repeatable costructure",
        "intervention-step",
        attrs={"ordinal": "3"},
    )

    cat.edge("HF-DBE", "STEP-DBE-name-costructure", "has-step")
    cat.edge("STEP-DBE-name-costructure", "C-DBE-produces-shadows", "supports")
```

### Layer C — closure query

For each hosted framework:

```text
A = claims extracted from SKILL.md
B = claims represented in v4cat
U = accountable framework-claim universe
```

Then:

```python
from v4cat import kquery

cells = kquery(
    extracted_claim_ids,
    catalogued_claim_ids,
    universe=accountable_claim_ids,
)
```

Interpretation:

```text
11 = source claim represented in v4cat
10 = source claim not yet represented
01 = catalogue claim not licensed by source
00 = accountable claim absent from both
```

This is the direct analogue of v4cat's own IMPL/CAT closure.

### Layer D — residue action

Every non-empty residue gets an action:

```text
10 → add missing node/edge/tension or explicitly defer
01 → mark as promissory, speculative, or unsupported
00 → either narrow U or add source/catalogue coverage
11 → stable hosted claim
```

No prose-only explanations.

## 5. The hosted lattice

Represent the 8-region lattice directly.

```python
REGIONS = [
    ("REG-000", "empty", False, False, False, "no-work"),
    ("REG-100", "DBE alone", True, False, False, "pure-scoping-memo"),
    ("REG-010", "RFS alone", False, True, False, "forbidden"),
    ("REG-001", "S2G alone", False, False, True, "pure-cataloguing"),
    ("REG-110", "DBE+RFS", True, True, False, "forbidden"),
    ("REG-101", "DBE+S2G", True, False, True, "sideways-grid-projection"),
    ("REG-011", "RFS+S2G", False, True, True, "mechanical-helper-promotion"),
    ("REG-111", "All three", True, True, True, "substantive-structural-arc"),
]
```

Then catalogue:

```python
with SymmetryCatalogue("shadow_architecture.v4cat.db") as cat:
    for rid, name, dbe, rfs, s2g, mode in REGIONS:
        cat.introduce_node(
            rid,
            name,
            "lattice-region",
            attrs={
                "DBE": str(dbe),
                "RFS": str(rfs),
                "S2G": str(s2g),
                "mode": mode,
            },
        )

    cat.edge("HF-shadow-architecture", "REG-111", "classifies")
    cat.edge("HF-shadow-architecture", "REG-010", "forbids-region")
    cat.edge("HF-shadow-architecture", "REG-110", "forbids-region")
```

Then define the current task:

```python
cat.introduce_node(
    "TASK-host-skills-under-v4cat",
    "Host shadow-architecture skills as v4cat frameworks",
    "task",
)

cat.edge("TASK-host-skills-under-v4cat", "REG-111", "belongs-to-region")
```

Because this task requires DBE design, RFS extraction from existing skill documents, and S2G registration into the v4cat grid.

## 6. The hosted framework contract

The most useful artifact is this contract.

```text
HostedFrameworkContract

A framework F is hosted under v4cat iff:

1. F has a hosted-framework node.
2. Every source-level normative claim has a framework-claim node,
   or is explicitly out-of-scope.
3. Every firing condition is represented as a firing-condition node.
4. Every intervention step is represented as an intervention-step node.
5. Every product/residue type is represented as a produced-shadow,
   consumed-shadow, cotype, quotient, or residue-action node.
6. Every relation among those objects is represented by typed edges.
7. F has at least one closure-obligation node.
8. The closure-obligation is implemented as a kquery/tension.
9. Non-empty 10, 01, or 00 cells are assigned residue actions.
10. The framework can be compared against its own hosted representation.
```

This is the point where the system uses v4cat as v4cat uses itself.

## 7. The closure tensions

Define one generic tension shape:

```text
T-hosted-framework-closure(F)

A = source_claims(F)
B = catalogued_claims(F)
U = accountable_claims(F)

Return kquery(A, B, U).
```

Then instances:

```text
T-DBE-closure
T-RFS-closure
T-S2G-closure
T-shadow-architecture-closure
```

And one lattice-specific tension:

```text
T-region-discipline

A = observed region fires
B = allowed productive regions
U = all eight lattice regions

Expected:
  10 = observed forbidden-region fires
  01 = allowed-but-unobserved regions
  11 = observed allowed regions
  00 = neither observed nor allowed
```

This gives the discipline teeth.

A forbidden region is not merely a warning in prose. It becomes a non-empty `10` cell under the region-discipline query.

## 8. The regrouped schema extension

The v4cat extension should be additive.

```sql
CREATE TABLE IF NOT EXISTS hosted_frameworks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    direction TEXT,
    source_doc TEXT
);

CREATE TABLE IF NOT EXISTS framework_claims (
    id TEXT PRIMARY KEY,
    framework_id TEXT NOT NULL,
    claim_text TEXT NOT NULL,
    claim_kind TEXT NOT NULL,
    source_anchor TEXT,
    FOREIGN KEY(framework_id) REFERENCES hosted_frameworks(id)
);

CREATE TABLE IF NOT EXISTS framework_obligations (
    id TEXT PRIMARY KEY,
    framework_id TEXT NOT NULL,
    obligation_kind TEXT NOT NULL,
    description TEXT NOT NULL,
    tension_id TEXT,
    FOREIGN KEY(framework_id) REFERENCES hosted_frameworks(id)
);

CREATE VIEW IF NOT EXISTS hosted_framework_unrepresented_claims_violations AS
SELECT c.*
FROM framework_claims c
WHERE NOT EXISTS (
    SELECT 1
    FROM witnesses w
    WHERE w.break_number = c.id
       OR w.spec_id = c.id
);
```

But the key is: do **not** let these tables become a second system. They are indexing substrate. The authoritative structural relations should still be visible through v4cat nodes, edges, witnesses, and kqueries.

## 9. The snap result

The snap-to-grid event is this recognition:

```text
DBE, RFS, and S2G are themselves three hosted frameworks,
and shadow-architecture is the fourth hosted framework that classifies
their joint firing lattice.
```

So the final hosted structure is:

```text
HF-DBE
HF-RFS
HF-S2G
HF-shadow-architecture

HF-shadow-architecture --orchestrates--> HF-DBE
HF-shadow-architecture --orchestrates--> HF-RFS
HF-shadow-architecture --orchestrates--> HF-S2G

HF-DBE --produces--> ExternalizedShadow
HF-RFS --extracts--> ExternalizedShadow
HF-S2G --accumulates--> ExternalizedShadow
HF-S2G --forms--> Quotient
HF-S2G --detects--> SnapEvent

HF-shadow-architecture --classifies--> REG-000 ... REG-111
HF-shadow-architecture --forbids-region--> REG-010
HF-shadow-architecture --forbids-region--> REG-110
```

## 10. Terminal rule

The whole formulation can be reduced to one invariant:

```text
A skill is hosted under v4cat only when its own claims are no longer
privileged prose: they are catalogue objects whose agreement with the
source skill, implementation behavior, and discipline rules is tested
by V₄ comparison.
```

Or more compactly:

```text
The skill earns hosted-framework status when it can be kqueried against
itself.
```

That is the exact analogue of the `kfour → v4cat` licensing move: the framework is not licensed by being named; it is licensed when its own representation is inside the comparison category and its closure residue is observable.
