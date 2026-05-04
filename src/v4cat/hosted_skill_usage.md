# v4cat — Hosted skill usage

> *Grade: operating manual.
> Companion to [hosted_skills.md](hosted_skills.md) (the design /
> hosted-framework contract) and [python_api.md](python_api.md) (the
> non-MCP API discipline). This document is the runtime discipline
> for actually using the four hosted shadow-architecture skills
> (DBE, RFS, S2G, shadow-architecture) under v4cat — every fire is
> classified, represented, audited, and closed.*

The hosted skill should be used as a **runtime discipline for making skill-use itself cataloguable**.

Not:

```text
"I used DBE/RFS/S2G."
```

But:

```text
"This work-fire occupies lattice region R.
These framework claims were active.
These shadows were produced or consumed.
These catalogue nodes/edges represent them.
This kquery audits source-skill claims vs hosted representation.
These residues remain."
```

The uploaded skill says the shadow-architecture meta-skill fires when classifying the 8-region lattice, detecting region transitions, auditing discipline, and seeing DBE/RFS/S2G as a coherent system rather than independent firings. It also defines DBE as forward goal → shadows, RFS as sideways artifact → shadows + recomposition, and S2G as backward accumulated shadows → goal.

So the hosted use-protocol is:

```text
1. Classify the fire.
2. Name the active framework(s).
3. Represent the active claims as v4cat nodes.
4. Represent products/residues as v4cat nodes.
5. Connect them with typed edges.
6. Run kquery over source claims vs catalogued claims.
7. Act on every 10 / 01 / 00 residue.
8. Close or re-enter with a sharper region.
```

## 0. The operating object

The unit of use is not a whole session. It is a **fire**.

A fire is one coherent work-move:

```text
fire :=
  request or subtask
  + active skill-region
  + source obligations
  + produced shadows
  + catalogue representation
  + closure query
```

In v4cat terms:

```python
cat.introduce_node("FIRE-001", "Host DBE as v4cat framework", "work-fire")
cat.edge("FIRE-001", "REG-111", "belongs-to-region")
```

Every fire should answer:

```text
Which region?
Which skill claims?
Which shadows?
Which cotype entries?
Which closure query?
Which residues?
```

## 1. Basic invocation pattern

At the beginning of a substantive move:

```text
A. Classify
   Is this DBE, RFS, S2G, DBE+S2G, RFS+S2G, or all three?

B. Bind
   Create a work-fire node and attach it to a lattice-region node.

C. Execute
   Run the component protocol(s).

D. Catalogue
   Add nodes/edges for claims, shadows, steps, residues.

E. Audit
   kquery(source_claims, catalogued_claims, universe=accountable_claims)

F. Close
   Promote, defer, boundary-mark, exclude, or extend scope.
```

The important inversion is that the skill is not merely "applied." It is **hosted as an auditable object**.

## 2. Example: DBE alone — pure scoping memo

### Situation

User says:

```text
Design the hosted-framework contract for v4cat skills.
```

No existing artifact is being refactored yet. No accumulated cotype needs recovery. This is DBE alone: the skill text identifies DBE alone as a pure scoping memo region, and DBE itself fires before substantive implementation/proof/formalization to avoid monolithic attack.

### Region

```text
REG-100 = DBE alone
```

### DBE execution

Name the target:

```text
Target:
  Define HostedFrameworkContract for representing skills under v4cat.
```

Name the costructure:

```text
Costructure:
  HostedFrameworkClaim
```

Signature:

```text
HostedFrameworkClaim :=
  id
  framework_id
  claim_text
  claim_kind
  source_anchor
  represented_by_node?
  audited_by_tension?
```

Name the composition:

```text
compose_claims:
  HostedFrameworkClaim* → HostedFramework
```

Name the entailment:

```text
If every normative source claim of a skill is represented as a
HostedFrameworkClaim, and each HostedFrameworkClaim is attached to
a v4cat node/edge/tension or explicit out-of-scope residue, then the
skill is hosted.
```

### v4cat representation

```python
cat.introduce_node("FIRE-001", "Scope HostedFrameworkContract", "work-fire")
cat.edge("FIRE-001", "REG-100", "belongs-to-region")

cat.introduce_node(
    "SHADOW-HostedFrameworkClaim",
    "HostedFrameworkClaim",
    "produced-shadow",
)

cat.introduce_node(
    "CLAIM-DBE-names-costructure",
    "DBE requires naming the repeatable costructure before implementation",
    "framework-claim",
)

cat.edge("FIRE-001", "SHADOW-HostedFrameworkClaim", "produces")
cat.edge("CLAIM-DBE-names-costructure", "SHADOW-HostedFrameworkClaim", "supports")
```

### Closure query

```python
source_claims = {
    "CLAIM-DBE-names-target",
    "CLAIM-DBE-names-costructure",
    "CLAIM-DBE-names-composition",
    "CLAIM-DBE-names-entailment",
}

catalogued_claims = {
    "CLAIM-DBE-names-costructure",
}

universe = source_claims

kquery(source_claims, catalogued_claims, universe=universe)
```

Expected residue:

```text
11:
  CLAIM-DBE-names-costructure

10:
  CLAIM-DBE-names-target
  CLAIM-DBE-names-composition
  CLAIM-DBE-names-entailment

01:
  ∅

00:
  ∅
```

Action:

```text
10 means source-required DBE claims are not yet hosted.
Add the missing claim nodes before treating DBE as hosted.
```

That is "using v4cat as v4cat uses itself."

## 3. Example: S2G alone — pure catalogue refresh

### Situation

You already have shadows:

```text
SHADOW-HostedFrameworkClaim
SHADOW-FiringCondition
SHADOW-InterventionStep
SHADOW-ResidueAction
```

The goal is not to design anything new, only to register them in the cotype and refresh the audit memo.

The shadow-architecture table marks S2G alone as "pure cataloguing," and S2G is the backward skill that consumes accumulated shadows into a cotype and reads their entailment.

### Region

```text
REG-001 = S2G alone
```

### S2G execution

Cotype entry:

```text
Cotype:
  hosted-skill-framework-cotype

Shadows:
  HostedFrameworkClaim
  FiringCondition
  InterventionStep
  ResidueAction

Current entailment:
  These shadows specify a minimal hosted-framework schema.
```

### v4cat representation

```python
cat.introduce_node("FIRE-002", "Refresh hosted-skill cotype", "work-fire")
cat.edge("FIRE-002", "REG-001", "belongs-to-region")

cat.introduce_node(
    "COTYPE-hosted-skill-framework",
    "Hosted skill framework cotype",
    "cotype",
)

for shadow in [
    "SHADOW-HostedFrameworkClaim",
    "SHADOW-FiringCondition",
    "SHADOW-InterventionStep",
    "SHADOW-ResidueAction",
]:
    cat.edge("COTYPE-hosted-skill-framework", shadow, "accumulates")
```

### Closure query

```python
source_shadows = {
    "SHADOW-HostedFrameworkClaim",
    "SHADOW-FiringCondition",
    "SHADOW-InterventionStep",
    "SHADOW-ResidueAction",
}

catalogued_shadows = shadows_accumulated_by("COTYPE-hosted-skill-framework")

cells = kquery(source_shadows, catalogued_shadows, universe=source_shadows)
```

Interpretation:

```text
10 = shadows known from the work but not in the cotype
01 = cotype shadows not licensed by current work
11 = correctly registered shadows
00 = scoped shadow slots still empty
```

If `10` is empty, the cotype refresh is clean.

## 4. Example: DBE + S2G — sideways grid projection

### Situation

You have already hosted DBE. Now you want to host RFS using the same hosted-framework schema.

There is no extraction from three repeated instances yet. You are copying a pattern from one parallel row to another:

```text
HF-DBE row → HF-RFS row
```

The skill document identifies DBE+S2G as "sideways grid projection": build a new grid cell by copying a pattern from a parallel row at the same grade, with no shadow absorption because fewer than three instances exist yet.

### Region

```text
REG-101 = DBE + S2G
```

### Move

Use DBE to name the entailment:

```text
If DBE can be hosted by FrameworkDeclaration + FiringProtocol +
InterventionProtocol + ArtifactFlow + ClosureObligation, then RFS can
be hosted by the same schema with different claim instances.
```

Use S2G to place it in the same grid:

```text
same grade:
  hosted-framework

different axis-value:
  role = sideways / existing-artifact-to-shadows
```

### v4cat representation

```python
cat.introduce_node("FIRE-003", "Project hosted-framework schema from DBE to RFS", "work-fire")
cat.edge("FIRE-003", "REG-101", "belongs-to-region")

cat.introduce_node(
    "HF-RFS",
    "regroup-from-shadows",
    "hosted-framework",
    attrs={"direction": "existing-artifact-to-shadows-plus-recomposition"},
)

cat.edge("HF-RFS", "SHADOW-HostedFrameworkClaim", "uses-schema-shadow")
cat.edge("HF-RFS", "SHADOW-FiringCondition", "uses-schema-shadow")
cat.edge("HF-RFS", "SHADOW-InterventionStep", "uses-schema-shadow")
cat.edge("HF-RFS", "SHADOW-ResidueAction", "uses-schema-shadow")
```

### kquery

Compare projected schema slots vs filled RFS slots:

```python
required_slots = {
    "FrameworkDeclaration",
    "FiringProtocol",
    "InterventionProtocol",
    "ArtifactFlow",
    "ResidueDiscipline",
    "ClosureObligation",
}

rfs_filled_slots = {
    "FrameworkDeclaration",
    "FiringProtocol",
}

cells = kquery(required_slots, rfs_filled_slots, universe=required_slots)
```

Residue:

```text
10:
  InterventionProtocol
  ArtifactFlow
  ResidueDiscipline
  ClosureObligation
```

Action:

```text
Continue filling RFS hosted slots.
Do not claim RFS is fully hosted yet.
```

## 5. Example: RFS + S2G — mechanical helper promotion

### Situation

You discover three nearly identical closure-query helpers:

```text
dbe_claim_closure()
rfs_claim_closure()
s2g_claim_closure()
```

No design question remains. They should all become:

```text
hosted_framework_closure(framework_id)
```

The skill document calls RFS+S2G "mechanical helper promotion": near-identical duplicate atoms are extracted into a canonical home, with trivial DBE because there is no design question.

### Region

```text
REG-011 = RFS + S2G
```

### RFS execution

Inventory commitments:

```text
Each helper returns kquery(source_claims(F), catalogued_claims(F), U_F).
```

Candidate shadow:

```text
HostedFrameworkClosureQuery
```

Recomposition:

```text
dbe_claim_closure() = hosted_framework_closure("HF-DBE")
rfs_claim_closure() = hosted_framework_closure("HF-RFS")
s2g_claim_closure() = hosted_framework_closure("HF-S2G")
```

### S2G execution

Register the promoted helper in the cotype:

```python
cat.introduce_node(
    "SHADOW-HostedFrameworkClosureQuery",
    "Generic closure query for any hosted framework",
    "produced-shadow",
)

cat.edge("COTYPE-hosted-skill-framework", "SHADOW-HostedFrameworkClosureQuery", "accumulates")
```

### v4cat representation

```python
cat.introduce_node("FIRE-004", "Promote repeated closure helpers", "work-fire")
cat.edge("FIRE-004", "REG-011", "belongs-to-region")

for helper in [
    "HELPER-dbe-claim-closure",
    "HELPER-rfs-claim-closure",
    "HELPER-s2g-claim-closure",
]:
    cat.edge(helper, "SHADOW-HostedFrameworkClosureQuery", "quotients-with")

cat.edge("FIRE-004", "SHADOW-HostedFrameworkClosureQuery", "produces")
```

### kquery

```python
duplicate_helpers = {
    "HELPER-dbe-claim-closure",
    "HELPER-rfs-claim-closure",
    "HELPER-s2g-claim-closure",
}

canonical_helpers = {
    "SHADOW-HostedFrameworkClosureQuery",
}

# The universe here is not "same type of node";
# it is "closure-query implementations accountable in this refactor."
```

The actual preservation audit should compare behavior before/after:

```text
A = results of old helpers
B = results of generic helper instantiated three times
U = all tested hosted frameworks
```

Expected:

```text
11 = every framework closure result agrees
10 = old-only behavior lost
01 = new-only behavior introduced
00 = untested framework slots
```

If `10` and `01` are empty, behavior preservation holds for the declared test universe.

## 6. Example: all three — substantive structural arc

### Situation

You want to host the entire shadow-architecture meta-skill under v4cat.

This is the full triple:

```text
DBE:
  define the target and hosted-framework costructure

RFS:
  extract common framework shadows from the existing skill bundle

S2G:
  register them into the hosted-skill cotype and lattice grid
```

The skill document identifies all-three fires as substantive structural arcs involving design work, shadow recognition/extraction, and grid placement/cataloguing.

### Region

```text
REG-111 = DBE + RFS + S2G
```

### DBE layer

Target:

```text
Host shadow-architecture as a v4cat framework.
```

Costructure:

```text
LatticeRegionClaim
```

Composition:

```text
compose_regions:
  8 LatticeRegionClaim → ShadowArchitectureLattice
```

Entailment:

```text
If all 8 lattice regions are represented,
and forbidden/productive/trivial classifications are represented,
and fire observations can be kqueried against allowed regions,
then the shadow-architecture lattice is hosted.
```

### RFS layer

Extract from the source skill:

```text
REG-000 empty
REG-100 DBE alone
REG-010 RFS alone forbidden
REG-001 S2G alone
REG-110 DBE+RFS forbidden
REG-101 DBE+S2G
REG-011 RFS+S2G
REG-111 all three
```

Extract common abstraction:

```text
LatticeRegion :=
  id
  DBE_active
  RFS_active
  S2G_active
  discipline_class
  characteristic_move
```

### S2G layer

Register all eight regions:

```python
REGIONS = [
    ("REG-000", False, False, False, "trivial", "no-work"),
    ("REG-100", True,  False, False, "productive", "pure-scoping-memo"),
    ("REG-010", False, True,  False, "forbidden", "rfs-alone"),
    ("REG-001", False, False, True,  "productive", "pure-cataloguing"),
    ("REG-110", True,  True,  False, "forbidden", "dbe-rfs-without-s2g"),
    ("REG-101", True,  False, True,  "productive", "sideways-grid-projection"),
    ("REG-011", False, True,  True,  "productive", "mechanical-helper-promotion"),
    ("REG-111", True,  True,  True,  "productive", "substantive-structural-arc"),
]

for rid, dbe, rfs, s2g, discipline, move in REGIONS:
    cat.introduce_node(
        rid,
        rid,
        "lattice-region",
        attrs={
            "DBE": str(dbe),
            "RFS": str(rfs),
            "S2G": str(s2g),
            "discipline": discipline,
            "move": move,
        },
    )

cat.edge("HF-shadow-architecture", "REG-010", "forbids-region")
cat.edge("HF-shadow-architecture", "REG-110", "forbids-region")
```

### Discipline audit

```python
all_regions = {r[0] for r in REGIONS}

allowed_regions = {
    rid for rid, _, _, _, discipline, _ in REGIONS
    if discipline in {"productive", "trivial"}
}

observed_regions = {
    "REG-100",
    "REG-101",
    "REG-111",
}

cells = kquery(
    observed_regions,
    allowed_regions,
    universe=all_regions,
)
```

Interpretation:

```text
11:
  observed and allowed

10:
  observed but not allowed
  → discipline violation or deliberate relaxation

01:
  allowed but unobserved
  → available productive mode not seen in this trace

00:
  neither observed nor allowed
  → forbidden and absent, which is good
```

If `REG-010` or `REG-110` appears in `10`, the system detected a forbidden-region fire.

## 7. Example: forbidden RFS alone

### Situation

You notice:

```text
"These three routines look similar."
```

But you do not analyze the common structure and do not register the observation.

That is RFS alone.

The skill explicitly says RFS alone is forbidden by discipline because spotting a shadow without analyzing it or recording it wastes the recognition.

### Region

```text
REG-010 = forbidden
```

### Correct response

Do not proceed as pure RFS. Immediately add DBE or S2G.

Two legal repairs:

```text
RFS + S2G:
  "These are byte-identical helpers; promote to canonical helper and register."

DBE + RFS + S2G:
  "These are similar but not identical; analyze the abstraction,
   extract it, then register the new shadow."
```

### v4cat residue

```python
cat.introduce_node("FIRE-005", "Observed similar routines without action", "work-fire")
cat.edge("FIRE-005", "REG-010", "belongs-to-region")
cat.edge("FIRE-005", "RESIDUE-unrecorded-shadow", "produces")
```

Then run:

```python
cells = kquery(
    observed_regions={"REG-010"},
    allowed_regions={"REG-000", "REG-100", "REG-001", "REG-101", "REG-011", "REG-111"},
    universe={"REG-000","REG-100","REG-010","REG-001","REG-110","REG-101","REG-011","REG-111"},
)
```

Result:

```text
10:
  REG-010
```

Action:

```text
Convert to REG-011 or REG-111.
```

## 8. Example: forbidden DBE + RFS without S2G

### Situation

You design an abstraction and extract it, but do not register it in the cotype or catalogue.

The skill marks DBE+RFS without S2G as forbidden in practice because extraction should be catalogued by snap-at-session-end discipline.

### Bad fire

```text
REG-110 = DBE + RFS, no S2G
```

### Repair

Add S2G:

```text
Register extracted shadow.
Attach it to cotype.
Run closure kquery.
Now the fire becomes REG-111.
```

### v4cat move

```python
cat.edge("FIRE-006", "REG-110", "initially-belonged-to")
cat.edge("FIRE-006", "REG-111", "reclassified-as")
cat.edge("FIRE-006", "TRANSITION-110-to-111", "records-region-transition")
```

And classify the transition as a symmetry discovery, not a mistake. The uploaded skill explicitly says mid-session region transitions are productive symmetry discoveries and should be recorded as such rather than treated as errors.

## 9. Example: orbit-saturation guard

### Situation

You see three instances:

```text
HostedDBEClosure
HostedRFSClosure
HostedS2GClosure
```

Temptation:

```text
Extract a universal wrapper above them.
```

But they may be orbit-elements of an existing operator:

```text
hosted_framework_closure(F)
```

The shadow-architecture discipline warns that before extracting a universal record from three recurring instances, you must ask whether a generating symmetry already produces them as orbit-elements; if so, classification is S2G, not RFS, and the correct move is to catalogue orbit position rather than extract a wrapper.

### Correct use

Ask:

```text
Are these free duplicates, or are they generated by applying one
operator to three framework arguments?
```

If generated:

```text
REG-001 or REG-101, not RFS.
```

v4cat representation:

```python
cat.introduce_node(
    "OP-hosted-framework-closure",
    "hosted_framework_closure(F)",
    "operator",
)

for fw in ["HF-DBE", "HF-RFS", "HF-S2G"]:
    cat.edge("OP-hosted-framework-closure", fw, "has-orbit-element")
```

The residue is the symmetry generator, not a missing abstraction.

## 10. The usable checklist

Before acting:

```text
1. What fire is this?
2. Which region is active?
3. Is the region allowed?
4. What source claims are active?
5. What shadows are produced or consumed?
6. What v4cat nodes/edges record them?
7. What kquery audits them?
8. What residues remain?
```

During action:

```text
DBE active:
  name target, costructure, composition, entailment

RFS active:
  inventory existing artifact, extract shadows, recompose, verify preservation

S2G active:
  add shadows to cotype, form useful quotients, read entailment, check snap
```

At closure:

```text
kquery(source, catalogue, universe)

11:
  stable hosted claim

10:
  source claim not represented
  → add node/edge/tension or explicitly defer

01:
  catalogue claim not licensed by source
  → mark speculative, unsupported, or remove from hosted core

00:
  accountable scope seen by neither
  → narrow U, extend source extraction, or declare out-of-scope
```

## 11. The canonical examples in one table

| Situation                                                  |    Region | Use                                            |
| ---------------------------------------------------------- | --------: | ---------------------------------------------- |
| Design the hosted-framework contract before implementation | `REG-100` | DBE scoping memo                               |
| Refresh cotype/audit memo from existing shadows            | `REG-001` | S2G cataloguing                                |
| Copy hosted schema from DBE to RFS                         | `REG-101` | DBE+S2G sideways projection                    |
| Promote three duplicate helpers into one canonical helper  | `REG-011` | RFS+S2G mechanical promotion                   |
| Host the whole shadow-architecture lattice                 | `REG-111` | DBE+RFS+S2G substantive arc                    |
| Notice a pattern but neither analyze nor record it         | `REG-010` | Forbidden; repair to `REG-011` or `REG-111`    |
| Extract after designing but fail to catalogue              | `REG-110` | Forbidden; add S2G and reclassify to `REG-111` |

## Bottom line

The skill is used by making every application of the skills itself pass through v4cat's discipline:

```text
classify the fire;
represent the active claims;
record the shadows;
audit source-vs-catalogue with kquery;
act on every residue.
```

The moment you can ask:

```text
Which V₄ comparison licensed this skill-fire?
```

and answer with actual nodes, edges, fibers, and residue actions, the skill is being used as a hosted framework rather than as prompt folklore.
