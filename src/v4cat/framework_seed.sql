-- =============================================================================
-- catalogue/framework_seed.sql — the framework's self-cataloguing.
--
-- Loaded after schema.sql when the catalogue is opened with
-- check_self_hosting=True. Adds rows that make the framework's own
-- primitives addressable as catalogue cells, satisfying the CAT
-- predicate (theory.md § 14.5.5).
--
-- This file is *seed data*, not schema. It uses INSERT OR IGNORE so
-- it's idempotent across re-opens. The corresponding IMPL referent
-- is catalogue/theory.py's SIGNATURE.
--
-- After loading both, ``bootstrap.check_closure()`` should pass.
-- =============================================================================

-- The framework as a witness-object. Year 2026 is the development
-- year for this catalogue lineage; catalogue_order=0 places it at
-- the seed of the catalogue's exposition.
INSERT OR IGNORE INTO specs (id, name, year, catalogue_order, notes) VALUES
    ('framework', 'symmetry-break cataloguing framework',
     2026, 0,
     'The framework cataloguing itself. Required for the closure check (Theorem 14.5).');

-- The bootstrap breaks: scope declaration + preservation theorem.
-- Both have cell.id starting with Q-, so they catalogue under that
-- exact id (no Q- prefix added — see _catalogue_id_for).
INSERT OR IGNORE INTO breaks (number, name, short_desc) VALUES
    ('Q-supported-claims',
     'Supported claims (scope of closure check)',
     'Refinement enumerates kinds in the closure scope (Definition 14.7 cond. 3)'),
    ('Q-bootstrap-closure',
     'Bootstrap closure preservation theorem',
     'Additive moves on K preserve gap=empty (Theorem 14.5)');

-- One break per primitive operation in catalogue/theory.py SIGNATURE.
-- Naming convention: catalogue id is 'Q-' + cell.id (per
-- bootstrap._catalogue_id_for).
--
-- S₄ reclassification (cotype/shadow_migration_04_signature_reclassify.md):
-- the (β) RISC core is {Q-introduce_node, Q-edge, Q-kquery}; everything
-- else is CISC sugar with documented derives_from chains in theory.py.
INSERT OR IGNORE INTO breaks (number, name, short_desc) VALUES
    -- RISC core (β) — derives_from=None in SIGNATURE
    ('Q-introduce_node',    'introduce_node operation',
     'RISC primitive: universal node introduction'),
    ('Q-edge',              'edge operation',
     'RISC primitive: universal typed-edge introduction'),
    ('Q-kquery',            'kquery operation',
     'RISC primitive: Klein-four read classifier (universal read)'),

    -- CISC sugar (object-introduction, kind O)
    ('Q-introduce_object',  'introduce_object operation',
     'CISC sugar: introduce_node(type=spec) + edge for lineage'),
    ('Q-introduce_tension', 'introduce_tension operation',
     'CISC sugar: introduce_node(type=tension)'),

    -- CISC sugar (break-introduction, kind B)
    ('Q-introduce_break',   'introduce_break operation',
     'CISC sugar: introduce_node(type=break)'),

    -- CISC sugar (witness operations, kind W)
    ('Q-witness',           'witness operation',
     'CISC sugar: edge(...) with default scope=spec'),
    ('Q-lineage_witness',   'lineage_witness operation',
     'CISC sugar: edge(...) for spec-spec graph'),
    ('Q-defer',             'defer operation',
     'Orbit-element of witness with kind=deferred-candidate'),
    ('Q-promote',           'promote operation',
     'Orbit-element of witness with kind=confirms (promotion)'),
    ('Q-boundary',          'boundary operation',
     'Orbit-element of witness with kind=sibling-boundary'),

    -- CISC sugar (refinement, kind R)
    ('Q-refine',            'refine operation',
     'CISC sugar: introduce_node(child-break) + edge(origin) + edge(refines)'),

    -- Schema-extension (kind E) — substrate-coupled, not RISC-reducible
    ('Q-load_extension',    'load_extension operation',
     'Domain-extension loading primitive'),

    -- CISC sugar (read primitives, kind K) — orbit-elements of kquery
    ('Q-tropical_min',      'tropical_min operation',
     'Orbit-element of kquery: sweep over ordered axis (MIN)'),
    ('Q-tropical_max',      'tropical_max operation',
     'Orbit-element of kquery: sweep over ordered axis (MAX)'),

    -- Closure check (kind X)
    ('Q-check_closure',     'check_closure operation',
     'Self-hosting closure check (Theorem 14.5)');

-- The framework witnesses each of its own breaks as
-- catalogue-introduces. This is the CAT side of the closure check.
INSERT OR IGNORE INTO witnesses (spec_id, break_number, kind, notes) VALUES
    ('framework', 'Q-supported-claims',  'catalogue-introduces',
     'Scope declaration; recursion clause 3 of Def 14.7'),
    ('framework', 'Q-bootstrap-closure', 'catalogue-introduces',
     'Preservation theorem; theorem 14.5'),
    -- RISC core (β)
    ('framework', 'Q-introduce_node',    'catalogue-introduces', NULL),
    ('framework', 'Q-edge',              'catalogue-introduces', NULL),
    ('framework', 'Q-kquery',            'catalogue-introduces', NULL),
    -- CISC sugar
    ('framework', 'Q-introduce_object',  'catalogue-introduces', NULL),
    ('framework', 'Q-introduce_tension', 'catalogue-introduces', NULL),
    ('framework', 'Q-introduce_break',   'catalogue-introduces', NULL),
    ('framework', 'Q-witness',           'catalogue-introduces', NULL),
    ('framework', 'Q-lineage_witness',   'catalogue-introduces', NULL),
    ('framework', 'Q-defer',             'catalogue-introduces', NULL),
    ('framework', 'Q-promote',           'catalogue-introduces', NULL),
    ('framework', 'Q-boundary',          'catalogue-introduces', NULL),
    ('framework', 'Q-refine',            'catalogue-introduces', NULL),
    ('framework', 'Q-load_extension',    'catalogue-introduces', NULL),
    ('framework', 'Q-tropical_min',      'catalogue-introduces', NULL),
    ('framework', 'Q-tropical_max',      'catalogue-introduces', NULL),
    ('framework', 'Q-check_closure',     'catalogue-introduces', NULL);

-- Refinements: the data carrying the actual scope and theorem.
-- Q-supported-claims's `supported_kinds` is read by
-- bootstrap.supported_kinds(); change here to extend or restrict
-- the closure scope.
INSERT OR IGNORE INTO refinements (break_number, spec_id, name, description) VALUES
    ('Q-supported-claims', 'framework', 'supported_kinds',
     'O,B,W,R,E,K,X'),
    ('Q-bootstrap-closure', 'framework', 'preservation_theorem',
     'Additive schema moves on K preserve ClosureKQ(K, scope).gap = empty.'),

    -- Q-kquery's orbit: the named selections in views.py are
    -- orbit-positions of kquery under fixed emit-mask + projection.
    -- All six remain Kind.K (kquery instances), not their own kind —
    -- per orbit-saturation discipline (shadow-architecture rule 6),
    -- they are NOT separate universal records. See
    -- cotype/shadow_kquery_orbit.md.
    ('Q-kquery', 'framework', 'named_selections',
     'agree:{11}; left_residue:{10}; right_residue:{01}; blind:{00}; coverage:{10,01,11}/flat; wedge:{10,01,11}/legacy'),
    ('Q-kquery', 'framework', 'orbit_saturation',
     '7 of 16 emit-subsets named (kquery itself + 6 named selections); saturated for current named-read use cases.');

-- Axes and (partition, preservation-theorem) on the bootstrap break.
INSERT OR IGNORE INTO break_axes (break_number, axis) VALUES
    ('Q-supported-claims',  'meta'),
    ('Q-bootstrap-closure', 'meta');

INSERT OR IGNORE INTO break_invariants
    (break_number, partition_desc, preservation_claim, temporal_axis_kind)
VALUES
    ('Q-bootstrap-closure',
     'Cells in scope partitioned by (IMPL, CAT) into Klein-four cells',
     'Additive schema moves preserve gap=empty (Theorem 14.5)',
     'analysis_step');

-- =============================================================================
-- S12: type-system seed — bootstrap floor for the (β) RISC reframe
--
-- Catalogues the framework's own primitive vocabulary as data: node-types,
-- edge-kinds, attribute-schemas, and the schema-witness edges binding them.
-- This is the *bootstrap-mode pass* — INSERTs land directly without going
-- through validation (validation engages in S₂ when introduce_node and edge
-- exist as RISC primitives that read this seed via kquery).
--
-- All seed rows use catalogue_order=NULL and year=NULL, marking them as
-- system specs outside catalogue exposition order and outside any temporal
-- axis. Tropical-MIN queries already filter NULLs, so this won't perturb
-- existing tropical results. None of these specs are 'framework', so the
-- closure check's (impl_ids, cat_ids) sets are unchanged.
--
-- See cotype/shadow_risc_core.md (Self-hosted type system / Bootstrap floor)
-- and cotype/shadow_migration_01_schema_seed.md.
-- =============================================================================

-- ----- Node-type tokens (specs of type 'node-type') --------------------------
-- 'node-type' is self-typed; a Smalltalk-style fixpoint at the type-system's
-- floor.

INSERT OR IGNORE INTO specs (id, name, year, catalogue_order, notes) VALUES
    ('node-type', 'Node Type', NULL, NULL,
     'Type-token: kinds of nodes the catalogue holds. Self-typed.'),
    ('break',     'Break',     NULL, NULL,
     'Type-token: a named structural distinction.'),
    ('spec',      'Spec',      NULL, NULL,
     'Type-token: a witness object of any kind a domain extension introduces.'),
    ('tension',   'Tension',   NULL, NULL,
     'Type-token: a named curry-spec AST over kquery (S12 reframe).'),
    ('edge-kind', 'Edge Kind', NULL, NULL,
     'Type-token: a label for a typed edge in the witness or lineage graph.');

-- ----- Edge-kind tokens (specs of type 'edge-kind') --------------------------
-- The framework-canonical edge-kind vocabulary. Each token is a spec; under
-- (β) S₂'s introduce_node will validate that an edge's kind is catalogued
-- here. The schema-witness kinds (K-SOURCE-TYPE, K-TARGET-TYPE, requires-
-- attr, admits-attr) are themselves edge-kinds — they're the kinds the
-- type-system uses to describe itself.

INSERT OR IGNORE INTO specs (id, name, year, catalogue_order, notes) VALUES
    -- Witness-graph kinds (spec → break, populated by witness())
    ('origin',                'origin',                NULL, NULL,
     'Edge-kind: chronologically first articulation.'),
    ('catalogue-introduces',  'catalogue-introduces',  NULL, NULL,
     'Edge-kind: catalogue''s first analysis of this break.'),
    ('confirms',              'confirms',              NULL, NULL,
     'Edge-kind: additional witness; no structural change.'),
    ('refines',               'refines',               NULL, NULL,
     'Edge-kind: extends with new attributes / cardinality.'),
    ('first-witness',         'first-witness',         NULL, NULL,
     'Edge-kind: concrete instance of a previously-deferred break.'),
    ('precedes',              'precedes',              NULL, NULL,
     'Edge-kind: surfaces an abstract pattern at a different scope.'),
    ('cross-vendor',          'cross-vendor',          NULL, NULL,
     'Edge-kind: independent confirmation in another lineage.'),
    ('inherits',              'inherits',              NULL, NULL,
     'Edge-kind: successor retains an ancestor''s contribution.'),
    ('deferred-candidate',    'deferred-candidate',    NULL, NULL,
     'Edge-kind: named the candidate but not yet adopted.'),
    ('sibling-boundary',      'sibling-boundary',      NULL, NULL,
     'Edge-kind: deliberate metamodel non-extension.'),
    ('gates-with-fault',      'gates-with-fault',      NULL, NULL,
     'Edge-kind: reveals structural inadequacy.'),

    -- Lineage-graph kinds (spec → spec, populated by lineage edges)
    ('descended-from',        'descended-from',        NULL, NULL,
     'Edge-kind: direct architectural / lineal descent.'),
    ('family-member',         'family-member',         NULL, NULL,
     'Edge-kind: same family, no specific descent.'),
    ('inherits-from',         'inherits-from',         NULL, NULL,
     'Edge-kind: generic inheritance.'),

    -- Schema-witness kinds (used by the type-system to describe itself)
    ('K-SOURCE-TYPE',         'K-SOURCE-TYPE',         NULL, NULL,
     'Schema-witness edge-kind: declares the source-type of an edge-kind.'),
    ('K-TARGET-TYPE',         'K-TARGET-TYPE',         NULL, NULL,
     'Schema-witness edge-kind: declares the target-type of an edge-kind.'),
    ('requires-attr',         'requires-attr',         NULL, NULL,
     'Schema-witness edge-kind: a node-type''s required attribute.'),
    ('admits-attr',           'admits-attr',           NULL, NULL,
     'Schema-witness edge-kind: a node-type''s optional attribute.');

-- ----- Attribute-schema breaks ----------------------------------------------
-- Each K-ATTR-* break names an attribute that node-types may require or
-- admit. Node-types witness against these via 'requires-attr' / 'admits-
-- attr' edges below. Attribute-schemas use the existing breaks table; option
-- (2a) per shadow_risc_core.md.

INSERT OR IGNORE INTO breaks (number, name, short_desc) VALUES
    ('K-ATTR-NUMBER',          'has number attribute',
     'Schema break: node admits/requires a number attribute (e.g., breaks.number).'),
    ('K-ATTR-NAME',            'has name attribute',
     'Schema break: node admits/requires a name attribute.'),
    ('K-ATTR-YEAR',            'has year attribute',
     'Schema break: node admits/requires a year attribute (the default tropical-MIN axis).'),
    ('K-ATTR-CATALOGUE-ORDER', 'has catalogue-order attribute',
     'Schema break: node admits/requires a catalogue_order attribute.'),
    ('K-ATTR-NOTES',           'has notes attribute',
     'Schema break: node admits/requires a notes attribute.'),
    ('K-ATTR-ID',              'has id attribute',
     'Schema break: node admits/requires an id attribute.'),
    ('K-ATTR-DISPOSITION',     'has disposition attribute',
     'Schema break: node admits/requires a disposition attribute (tensions).'),
    ('K-ATTR-PARAMETERS',      'has parameters attribute',
     'Schema break: node admits/requires a parameters list attribute (tensions).'),
    ('K-ATTR-SHAPE',           'has shape attribute',
     'Schema break: node admits/requires a curry-spec AST shape attribute (tensions).'),
    ('K-ATTR-SHORT-DESC',      'has short-desc attribute',
     'Schema break: node admits/requires a short-description attribute.');

-- ----- Type-relation spec_attributes ----------------------------------------
-- For each type-token, record its node-type. For each edge-kind, record its
-- node-type plus its (source-type, target-type). These attributes are how
-- S₂'s validation will look up type information without needing additional
-- tables.

INSERT OR IGNORE INTO spec_attributes (spec_id, name, value) VALUES
    -- Node-type tokens declare themselves as type='node-type' (incl. self-typing)
    ('node-type', 'type', 'node-type'),
    ('break',     'type', 'node-type'),
    ('spec',      'type', 'node-type'),
    ('tension',   'type', 'node-type'),
    ('edge-kind', 'type', 'node-type'),

    -- Witness-graph edge-kinds: type='edge-kind', source-type='spec', target-type='break'
    ('origin',               'type',        'edge-kind'),
    ('origin',               'source-type', 'spec'),
    ('origin',               'target-type', 'break'),
    ('catalogue-introduces', 'type',        'edge-kind'),
    ('catalogue-introduces', 'source-type', 'spec'),
    ('catalogue-introduces', 'target-type', 'break'),
    ('confirms',             'type',        'edge-kind'),
    ('confirms',             'source-type', 'spec'),
    ('confirms',             'target-type', 'break'),
    ('refines',              'type',        'edge-kind'),
    ('refines',              'source-type', 'spec'),
    ('refines',              'target-type', 'break'),
    ('first-witness',        'type',        'edge-kind'),
    ('first-witness',        'source-type', 'spec'),
    ('first-witness',        'target-type', 'break'),
    ('precedes',             'type',        'edge-kind'),
    ('precedes',             'source-type', 'spec'),
    ('precedes',             'target-type', 'break'),
    ('cross-vendor',         'type',        'edge-kind'),
    ('cross-vendor',         'source-type', 'spec'),
    ('cross-vendor',         'target-type', 'break'),
    ('inherits',             'type',        'edge-kind'),
    ('inherits',             'source-type', 'spec'),
    ('inherits',             'target-type', 'break'),
    ('deferred-candidate',   'type',        'edge-kind'),
    ('deferred-candidate',   'source-type', 'spec'),
    ('deferred-candidate',   'target-type', 'break'),
    ('sibling-boundary',     'type',        'edge-kind'),
    ('sibling-boundary',     'source-type', 'spec'),
    ('sibling-boundary',     'target-type', 'break'),
    ('gates-with-fault',     'type',        'edge-kind'),
    ('gates-with-fault',     'source-type', 'spec'),
    ('gates-with-fault',     'target-type', 'break'),

    -- Lineage-graph edge-kinds: type='edge-kind', source-type='spec', target-type='spec'
    ('descended-from',       'type',        'edge-kind'),
    ('descended-from',       'source-type', 'spec'),
    ('descended-from',       'target-type', 'spec'),
    ('family-member',        'type',        'edge-kind'),
    ('family-member',        'source-type', 'spec'),
    ('family-member',        'target-type', 'spec'),
    ('inherits-from',        'type',        'edge-kind'),
    ('inherits-from',        'source-type', 'spec'),
    ('inherits-from',        'target-type', 'spec'),

    -- Schema-witness edge-kinds (used internally by the type-system)
    ('K-SOURCE-TYPE',        'type',        'edge-kind'),
    ('K-SOURCE-TYPE',        'source-type', 'edge-kind'),
    ('K-SOURCE-TYPE',        'target-type', 'spec'),
    ('K-TARGET-TYPE',        'type',        'edge-kind'),
    ('K-TARGET-TYPE',        'source-type', 'edge-kind'),
    ('K-TARGET-TYPE',        'target-type', 'spec'),
    ('requires-attr',        'type',        'edge-kind'),
    ('requires-attr',        'source-type', 'spec'),
    ('requires-attr',        'target-type', 'break'),
    ('admits-attr',          'type',        'edge-kind'),
    ('admits-attr',          'source-type', 'spec'),
    ('admits-attr',          'target-type', 'break');

-- ----- Attribute-schema witnesses (which node-type requires/admits which attr)
-- These use the existing witnesses table with the new edge-kinds 'requires-
-- attr' and 'admits-attr'. The spec_id is a node-type token (e.g., 'break'),
-- the break_number is a K-ATTR-* break, and the kind declares whether the
-- attribute is required or optional. None of these spec_ids are 'framework'
-- so the closure check is unaffected.

INSERT OR IGNORE INTO witnesses (spec_id, break_number, kind, notes) VALUES
    -- 'break' node-type: requires number, name; admits short-desc
    ('break',   'K-ATTR-NUMBER',          'requires-attr', NULL),
    ('break',   'K-ATTR-NAME',            'requires-attr', NULL),
    ('break',   'K-ATTR-SHORT-DESC',      'admits-attr',   NULL),

    -- 'spec' node-type: requires id, name; admits year, catalogue-order, notes
    ('spec',    'K-ATTR-ID',              'requires-attr', NULL),
    ('spec',    'K-ATTR-NAME',            'requires-attr', NULL),
    ('spec',    'K-ATTR-YEAR',            'admits-attr',   NULL),
    ('spec',    'K-ATTR-CATALOGUE-ORDER', 'admits-attr',   NULL),
    ('spec',    'K-ATTR-NOTES',           'admits-attr',   NULL),

    -- 'tension' node-type: requires id, name, disposition; admits shape,
    -- parameters, notes (shape admitted-not-required because legacy
    -- concern-disposition tensions exist without curry-spec ASTs)
    ('tension', 'K-ATTR-ID',              'requires-attr', NULL),
    ('tension', 'K-ATTR-NAME',            'requires-attr', NULL),
    ('tension', 'K-ATTR-DISPOSITION',     'requires-attr', NULL),
    ('tension', 'K-ATTR-SHAPE',           'admits-attr',   NULL),
    ('tension', 'K-ATTR-PARAMETERS',      'admits-attr',   NULL),
    ('tension', 'K-ATTR-NOTES',           'admits-attr',   NULL);
