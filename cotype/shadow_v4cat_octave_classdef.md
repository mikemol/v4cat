# Shadow: v4cat-octave classdef wrapper (promissory cell)

**Tracking**: [v4cat-oss/v4cat-octave#5](https://github.com/v4cat-oss/v4cat-octave/issues/5) (status canonical there per [shadow_workspace_project_tracking.md](shadow_workspace_project_tracking.md)).

> *S2G fire of 2026-05-05 (companion to
> [shadow_v4cat_octave_distribution.md](shadow_v4cat_octave_distribution.md)).
> Region **#4** (S2G alone -- pure cataloguing).*

## Form

`v4cat-octave` v0.1 ships a **function/struct API**: every
operation is a function in the `+v4cat/` package; state is
threaded as the first argument (`cat`) and returned as the first
output. The user's brief explicitly chose this:

> Octave supports `classdef`, but Octave's own docs still
> describe support as limited relative to MATLAB, so I would
> make the core implementation function/struct based, with an
> optional class wrapper later.

This shadow names the design surface for the optional `classdef`
wrapper.

## What to design

A `Catalogue` classdef wrapper that holds the underlying struct
internally and exposes the operations as methods:

```matlab
cat = v4cat.Catalogue();
cat.edge("alice", "knows", "bob");        % no need to thread state
M = cat.incidence_for_kind("knows");
C = cat.kquery(Omega, A, B);
```

The wrapper does **not** replace the function API. Both must
coexist. The wrapper merely sugars the state-threading by
holding the struct in an instance field.

Per Octave's own
[classdef docs][classdef], support is improving but not yet at
MATLAB parity. The wrapper should avoid any classdef feature
known-broken in current Octave (no `protected` access modifiers
in inheritance, careful with `handle` semantics, etc.).

[classdef]: https://docs.octave.org/latest/classdef-Classes.html

## Why deferred from v0.1

The brief is explicit: "make the core implementation
function/struct based, with an optional class wrapper later."
The classdef wrapper is downstream of API stability; v0.1 may
still iterate the function signatures as more verbs land
(especially the CISC sugar in
[shadow_v4cat_octave_cisc_sugar.md](shadow_v4cat_octave_cisc_sugar.md)).

## Future fire

`v4cat-octave-classdef`. Single sub-fire; once API stabilises
the wrapper is mostly mechanical.

## Closure

Closes when v4cat-octave ≥ v0.x:

1. Ships `inst/v4cat/Catalogue.m` (a classdef class).
2. Has a test asserting that the classdef-wrapper code is
   semantically equivalent to the function-API code on a
   fixture (same final V_4 cell membership for the same
   sequence of operations).
3. README documents both APIs and explains when each is
   preferred (function API for terse one-shot scripts, classdef
   for longer interactive sessions / pipelines).
