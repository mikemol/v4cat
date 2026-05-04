# Shadow: missing v4cat event-log API (promissory cell)

> *S2G fire of 2026-05-04 (Stage 2 of the algebraic-foundations arc).
> **At orbit-position 1** (just v4cat itself); per discipline rule 6,
> S2G to catalogue the gap, NOT RFS to extract a wrapper. Algebraic
> anchor: [shadow_assertion_history_group.md](shadow_assertion_history_group.md).*

## Form

A **promissory cell** in the framework's self-hosting closure: v4cat
does not yet expose an explicit operation-log API. The patch profile
(in vcif and vcif-rdf) is *theoretically* group-faithful but
*operationally* downgraded.

Per [theory.md § 15][theory15] the assertion-history group is `H =
ℤ^𝔄`; an operation-log carrier is `h ∈ H` itself, an ordered sequence
of left-translations. v4cat currently exposes only the **forward
modal facet** — `cat.introduce_node` and `cat.edge` mutate the
visible catalogue (`π(h)`) directly, without writing to any
order-preserving event log.

[theory15]: ../src/v4cat/theory.md

## What's missing

A `v4cat.events` API surface that records, for each RISC call:

```text
event:
  index           : int           # ordering within a session
  timestamp       : datetime      # wall clock
  generator       : str           # 'introduce_node' | 'edge'
  args            : dict          # call arguments
  input_state_hash: hash          # sha256 of (π(h_prev))
  output_state_hash: hash         # sha256 of (π(h_after))
```

Plus three operations:

```python
cat.events.append(generator, args, ...)   # auto-called by ISA
cat.events.replay(start, end)             # produce h ∈ H from a subrange
cat.events.invert(event_id)               # modal inverse along event axis
```

With this:

- The `v4cat.patch` profile (in both vcif and vcif-rdf) becomes
  **truly group-faithful**: a patch dump captures `h` exactly, and
  `apply(patch)` to a fresh catalogue replays the translations in
  order, producing the same `π(h)`.
- Materialized kqueries (per § 15.6) can be inverted by replaying
  the prior state hash and removing exactly the cover-cell payload
  that was added.
- The "deletion is not required" entailment from § 15.15.B becomes
  *operationally* available — modal inverses live in the event log,
  not in the public mutating API.

## What this shadow does NOT do

Following discipline rule 6: **at orbit-position 1 (just v4cat), the
move is S2G — catalogue the gap, do not extract a wrapper.**
Specifically:

- Does not introduce an "event-log carrier" abstract base class
  above v4cat.
- Does not modify v4cat's existing API.
- Does not deprecate or downgrade the current
  `introduce_node`/`edge` surface.
- Does not commit to a particular implementation (could be SQLite
  trigger-based, could be Python-decorator-based, could be a
  separate event-store table).

The shadow simply names the gap so the catalogue thickens forward,
and so future fires that touch v4cat's storage layer have a stable
reference point.

## Promissory cell — what would close it

A future `v4cat>=0.6` (or similar) ships with:

1. A new SQL table `events(index INTEGER PRIMARY KEY, timestamp,
   generator, args_json, input_state_hash, output_state_hash)`.
2. SymmetryCatalogue's RISC verbs append to `events` before/after
   their existing mutations (atomic transaction).
3. `cat.events.replay(...)` and `cat.events.invert(...)` exposed as
   public methods.
4. The existing schema-bootstrap check is extended to verify
   `events`-table presence as part of the closure check.
5. v4cat's regression test `test_self_hosting.py` gains a
   round-trip test: dump events → fresh catalogue → replay → verify
   `π(h)` matches.

This would close the cell. The vcif and vcif-rdf patch profiles then
become operationally what they're already documented to be.

## Lattice classification

Region **#4 (S2G alone — pure cataloguing)**, by exception. Per
shadow-architecture's lattice, S2G-alone fires are the small minority
of work — typically cotype refreshes, audit-memo regenerations, or
gap-registration. This is exactly the latter: register the gap, no
forward design (DBE) or extraction (RFS) yet.

The accompanying shadows in this Stage 2 fire
([shadow_carrier_grid.md](shadow_carrier_grid.md) and the vcif-rdf
build) are region #8; this one is region #4 because there's no v4cat
code change and no shadow-extraction at orbit-position 1.

## Trace-integrity

Prior shadows are unaffected:

- The patch profile in [shadow_vcif_distribution.md](shadow_vcif_distribution.md)'s
  algebraic-anchor footer is correctly named as "operation-log
  carrier — `h ∈ H`, group-faithful, invertible". The promissory
  status (operationally downgraded until the event-log API ships)
  is registered *here*, not *there*; the prior shadow's claim
  remains honest at the theoretical level.
- [shadow_assertion_history_group.md](shadow_assertion_history_group.md)
  § 15.15.B ("deletion is not required") is preserved; this shadow
  notes that the modal inverse exists in the event log even before
  the event-log API is exposed.

## When this shadow closes

When v4cat ships an event-log API satisfying the promissory-cell
list above, this shadow can be retired (or, more honestly per the
catalogue-thickens-forward discipline, annotated with a "closed at
v4cat 0.X" footer). At that point the carrier-grid shadow's
operation-log row becomes operationally as well as theoretically
filled.

Until then, this shadow stands as a registered structural commitment
the framework has *named* but not yet *implemented*.
