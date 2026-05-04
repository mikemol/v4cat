# Shadow: v4cat as free-abelian assertion-history group action

> *DBE+RFS+S2G fire of 2026-05-04 (cont'd). Region #8 of the
> shadow-architecture lattice; **RFS-dominant** (this reading
> retroactively regroups large swaths of existing material). The
> structural shadow companion to [theory.md § 15](../src/v4cat/theory.md#15-group-theoretic-reading-v4cat-as-free-abelian-assertion-history-group-action).*

## Form

The universal at the assertion-axis is the **free-abelian
assertion-history group action**:

```text
H = ℤ^(𝔄)         (assertion-history space)
G_mut = ℤ^(𝔄_node ⊔ 𝔄_edge)   (translations by RISC generators)
G_query(U) = V₄^U                (observer-toggle group per universe)
```

The visible catalogue is the support / projection:

```text
π : H → CatalogueState
π(h) ∋ a   iff   h(a) > 0
```

`kquery(A, B; U)` is the V₄-equivariant observer-coordinate chart of
the observer-pair group action:

```text
χ₍A,B₎ : U → V₄
χ₍A,B₎(u) = (χ_A(u), χ_B(u))
```

The four cells are fibers of `χ`:

```text
χ⁻¹(11) = A ∩ B          χ⁻¹(10) = A ∖ B
χ⁻¹(01) = B ∖ A          χ⁻¹(00) = U ∖ (A ∪ B)
```

## Where realised

- **Algebraic exposition**: [theory.md § 15](../src/v4cat/theory.md#15-group-theoretic-reading-v4cat-as-free-abelian-assertion-history-group-action)
  (16 sub-sections, with the compact formal statement at § 15.14 and
  the slogan at § 15.16).
- **Forward modal facet** (the publicly-exposed monotone facet of the
  group action):
  - `cat.introduce_node` ([catalogue.py:348](../src/v4cat/catalogue.py#L348))
    — translates by `Nₓ`.
  - `cat.edge` ([catalogue.py:474](../src/v4cat/catalogue.py#L474))
    — translates by `Eₛ,ₖ,ₜ`.
  - `kquery` ([views.py:42](../src/v4cat/views.py#L42)) —
    materializes the V₄ coordinate decomposition over a universe.
- **Cell + Kind machinery** ([cells.py](../src/v4cat/cells.py)) —
  the typed-tagged-union substrate the action operates over.
- **Forward-monotone discipline** (no public deletion, no public
  retraction) — the methodology's append-only / additive
  commitments are consequences of `π` being a support map, not
  primitive axioms.

## Composition operation

The slogan is the composition operation:

> **RISC writes are translations; kquery is the V₄ coordinate chart.**

Concretely: a v4cat run is a composition of left-translations in
`H` interspersed with V₄-coordinate observations. The visible
catalogue at any moment is the support `π(h)` of the cumulative
left-translated history.

For materialized kqueries (vcif `v4cat.closure-report` profile, `cat`
side cover-cell tables) the materialization is itself a translation
by the assertion payload `Q₍U,A,B₎(π(h))`, with the inverse retained
as a modal/history-level operation along the query-event axis.

## Entailment

Six load-bearing entailments, each with a concrete operational
consequence:

| # | Entailment | Operational consequence |
|---|---|---|
| A | Idempotence is a quotient artefact, not primitive | The append-only schema discipline is *derived* from `π`'s support-map shape; no separate idempotence axiom needed |
| B | Deletion is not required | `defer/promote/boundary` are modal moves on the history axis, not destructive mutations |
| C | Kinds and properties are not special | They are nodes acted on by the same group; carriers (RDF/SHACL/SPARQL, JSON Schema) must *never* introduce a first-class property layer |
| D | `kquery` is not a diff | It is the V₄-coordinate chart; symmetric difference (`10 ∪ 01`) is one named *projection* of it |
| E | Recognizers must preserve equivariance | A recognizer that fails `recognize(σ · C) = σ · recognize(C)` is smuggling in non-structural information |
| F | Self-hosting is group-completion closure | Theorem 14.5's `ClosureKQ(K, scope).gap = ∅` is the V₄-coordinate check on the framework's own assertion-history orbit |

## Lattice classification

Region **#8 (DBE + RFS + S2G — substantive structural arc)**, with the
**heaviest RFS pass we've seen**. The reading regroups the following
existing artefacts (without modifying their prior content):

| Existing material | Re-read as |
|---|---|
| methodology.md "every read is a comparison" | kquery is the V₄ coordinate chart of `O_U = V₄^U` acting on observer pairs |
| theory.md § 4 (Klein-four read core) | `𝒫(U) × 𝒫(U) ≅ V₄^U` under symmetric difference; cells are fibers, not buckets |
| theory.md § 12 (trace-thickening) | visible state = π(h); inverses live at the history level, not the visible level |
| theory.md § 14.5 (self-hosting closure) | self-hosting is group-completion closure of the framework's own assertion atoms |
| methodology.md additive-only schema | a formal consequence of `H = ℤ^𝔄` plus `π` being a support map |
| The "append-only / no-RETRO" discipline | forward-modal facet of group translation; inverses retained but not exposed publicly |
| vcif's `v4cat.patch` profile | the operation-log carrier — `h ∈ H` itself, group-faithful |
| vcif's `v4cat.snapshot` profile | `π(h)` — the support quotient |
| vcif's `v4cat.closure-report` profile | `χ_{A,B}(π(h))` — the V₄ coordinate decomposition |
| v4cat-mcp's monotone tools | forward modal facet of the assertion-translation group |
| Carrier-vs-object discipline (RDF carrier writeup) | visible-quotient vs history-fiber distinction at the kernel level |
| The kernel-cell reading (prior turn) | the assertion-history group action *itself*, with monotone facet exposed |
| Carriers as co-projections (prior turn) | carriers are projections of `H` at various projection depths |

## Trace-integrity

Per methodology.md's catalogue-thickens-forward commitment, prior
shadows are **not** invalidated. They are re-derived through this
algebraic lens:

- [shadow_kquery_universal_read.md](shadow_kquery_universal_read.md)
  acquires a clearer joint origin: kquery is the V₄ coordinate chart.
- [shadow_kquery_orbit.md](shadow_kquery_orbit.md) — the 6 named
  selections are projections of the V₄ fiber cover, not independent
  ops.
- [shadow_layered_stack.md](shadow_layered_stack.md) — L0 (kquery) is
  the V₄-coordinate-chart layer; everything above is a projection.
- [shadow_distribution_seam_mcp.md](shadow_distribution_seam_mcp.md)
  — MCP is the forward-modal facet of the assertion-translation
  group, exposed over RPC.
- [shadow_vcif_distribution.md](shadow_vcif_distribution.md) — vcif
  carriers are projections of `H` at depths {operation-log,
  snapshot, V₄-cover, residue}; the six profiles factor along this
  depth axis, with `v4cat.patch` at the group-faithful bottom.
- [shadow_risc_core.md](shadow_risc_core.md) — the three RISC
  primitives are the generators of the assertion-translation group
  plus the V₄-coordinate-chart action.

Each prior shadow gains a one-paragraph "Algebraic anchor" footer
pointing here. The cotype thickens forward; nothing is overwritten.

## Snap-to-grid check

User's request (across the latest several turns): "We should land
this; I think it clarifies/formalizees a lot."

Cotype's entailment after this lands: "v4cat is a free-abelian
assertion-history group action whose observable states are V₄-audited
quotients; the three RISC primitives are translations + a coordinate
chart." Many implicit framings get explicit anchoring; many prior
shadows snap into focus around the slogan.

Snap valid; the formal statement at § 15.14 *generalises* the
user's request — it gives a precise object the prior reading was
groping toward. Bonus deliverable, not drift.

## Predicted-vs-observed cadence

Plan predicted **sequential rotation** with Stage 1 (this fire) being
doc-heavy and Stage 2 (vcif-rdf build) following. Observed for Stage 1:
one large theory.md § 15 append + this shadow + cross-reference inserts
+ six soft-correction footers + INDEX.md update + vcif spec.md polish,
landing as a single coherent commit. Stage 2 builds on top.

## Discipline check — region #5 forbidden?

If we did DBE+RFS without S2G we would land in region #5 (forbidden
by the snap-at-session-end discipline). Concretely: write theory.md §
15 + soft-correct prior shadows, but skip *this* file. Writing this
file is what converts the fire to region #8. Required, not optional.

## The slogan, repeated

> **v4cat is a free assertion-history group action whose observable
> states are V₄-audited quotients.**

Tighter:

> **RISC writes are translations; kquery is the V₄ coordinate chart.**
