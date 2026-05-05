# Shadow: vcif/v4cat bootstrap gap (G5)

**Tracking**: [v4cat-oss/methodology#1](https://github.com/v4cat-oss/methodology/issues/1) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-04. **Region #4** (S2G alone — pure
> cataloguing). Surfaced during agda2v4cat v0.1's end-to-end smoke
> test: an integration mismatch between vcif's `apply` and v4cat's
> bootstrap state. Companion to the existing G1–G4 gap shadows
> registered in [audit_workspace_2026_05_04.md](audit_workspace_2026_05_04.md).*

## Form

`vcif.apply(doc, catalogue)` walks `doc.vocabulary.node_kinds` and
calls `catalogue.introduce_node(id, label, kind='node-kind')` for
each entry — i.e. it registers each declared node-kind as a *node
of kind* `'node-kind'`. Same shape for edge-kinds with
`kind='edge-kind'`.

But:

1. v4cat's `framework_seed.sql` does **not** pre-register
   `'node-kind'` (or `'edge-kind'`) as a *node-type*. The seed
   declares `'node-type'`, `'break'`, `'spec'`, `'tension'`,
   `'edge-kind'` as node-types — `'node-kind'` is conspicuously
   absent. The asymmetry between `'node-kind'` and `'edge-kind'`
   here is itself a bug (one is a node-type, the other isn't).
2. v4cat's `introduce_node` is *strict*: any value passed in the
   type slot must already be a registered node-type, or the call
   raises
   `ValueError: unknown node-type '<X>'`.
3. So `vcif.apply` against a freshly-bootstrapped v4cat catalogue
   immediately fails at the first vocabulary entry, regardless of
   what document is being applied. The same failure reproduces on
   vcif's own `agda-import.json` fixture.

The integration is in a "carrier knows about catalogue but
catalogue doesn't carry the carrier's typing assumptions" state.

## Where realised

- Trigger: any `vcif.apply(doc, SymmetryCatalogue(':memory:'))`.
- Workaround in agda2v4cat's smoke test
  ([tests/python/end_to_end.py][st]): introduce `'node-kind'`,
  `'edge-kind'`, and every per-document vocabulary entry as a
  node-type before invoking `vcif.apply`.
- Affected symmetric pair: vcif (apply) ↔ v4cat (framework seed).

[st]: https://github.com/v4cat-oss/agda2v4cat/blob/main/tests/python/end_to_end.py

## Decomposition by entailment

The carrier-vs-object discipline (`theory.md` § 15.10,
`shadow_kquery_orbit.md`) says: object-language *kinds* are
ordinary nodes, not first-class predicates / types. vcif's
`apply` honours that — vocabulary entries become nodes. But
v4cat's `introduce_node` then enforces that the *kind slot* of a
node refer to an already-declared node-type. Together, applying
vcif documents through `apply` requires:

```text
∀ kind k declared in doc.vocabulary.node_kinds:
  catalogue declares k as a node-type before any node of kind k is introduced
```

That precondition is not currently enforced or established by
either side:

- vcif's `apply` could **dual-register** — first introduce the
  vocabulary entry as a node-type, then as a node-of-kind
  `'node-kind'`. This is the natural fix on the carrier side.
- v4cat could **relax** `introduce_node`'s strict check, e.g.
  treat unknown node-types as deferred-introduction. This is the
  natural fix on the kernel side.
- `framework_seed.sql` could pre-declare `'node-kind'` as a
  node-type alongside `'edge-kind'` — closes the asymmetry but
  doesn't address the per-vocabulary auto-registration need.

The right fix per carrier-vs-object discipline is the carrier-side
dual-registration: vcif knows what kinds the document declares, so
vcif should establish the precondition before ingesting the rest
of the document.

## Lattice classification

Region **#4** (S2G alone — pure cataloguing). No new costructure
yet; this shadow names the gap and the entailed fix surface so a
future small fire can close it.

## Closure path

A single fire on vcif's `importer.py`:

```python
# vcif.importer.apply, vocabulary loop:
for nk in doc.get('vocabulary', {}).get('node_kinds', []):
    # NEW: pre-register the kind as a node-type so subsequent
    # nodes-of-kind=<X> are accepted by v4cat's introduce_node.
    _idempotent_introduce_node(
        catalogue, nk['id'], nk.get('label', nk['id']),
        kind='node-type', attrs=None, report=report,
    )
    # existing call (now a no-op for already-declared id):
    _idempotent_introduce_node(
        catalogue, nk['id'], nk.get('label', nk['id']),
        kind='node-kind', attrs=None, report=report,
    )
```

…plus an analogous tweak for `edge_kinds`, and the
`'node-kind'` ↔ `'edge-kind'` asymmetry in
`framework_seed.sql` corrected so `'node-kind'` is also
pre-declared as a node-type.

After closure, agda2v4cat's smoke test loses its workaround block
and `vcif.apply` works against a default-bootstrap v4cat catalogue
without preliminaries — for any document, not just agda2v4cat's.

## Trace-integrity

This gap was **discovered** by agda2v4cat v0.1's end-to-end smoke
test. Reproducing on vcif's own fixture confirmed the issue is
upstream of agda2v4cat — agda2v4cat is the messenger, not the
cause. Per the catalogue-thickens-forward discipline, the gap is
catalogued where it surfaced (here) and the upstream fix surface
is named (`vcif/src/vcif/importer.py` apply-vocabulary loop +
`v4cat/src/v4cat/framework_seed.sql`).

## Snap-to-grid check

Cotype after this shadow lands: "the v4cat/vcif integration has a
known bootstrap gap (G5): `vcif.apply` requires every declared
node-kind to be pre-registered as a v4cat node-type, but neither
vcif (auto-register) nor v4cat (framework seed pre-declare)
establishes that precondition. Consumers work around it by
manually introducing the missing node-types. Closure is a small
focused fire on vcif.importer + framework_seed.sql."

Snap valid. The user's existing G1–G4 gap shadows already
demonstrate the precedent for cataloguing integration-gaps as
named v0.x-promissory cells; G5 fits that orbit at position 5.
