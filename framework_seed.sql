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
INSERT OR IGNORE INTO breaks (number, name, short_desc) VALUES
    -- Object-introduction operations (kind O)
    ('Q-introduce_object',  'introduce_object operation',
     'Object-introduction primitive'),
    ('Q-introduce_tension', 'introduce_tension operation',
     'Tension-introduction primitive'),

    -- Break-introduction (kind B)
    ('Q-introduce_break',   'introduce_break operation',
     'Break-introduction primitive'),

    -- Witness operations (kind W)
    ('Q-witness',           'witness operation',
     'Typed-edge introduction primitive'),
    ('Q-defer',             'defer operation',
     'Witness-shorthand for kind=deferred-candidate'),
    ('Q-promote',           'promote operation',
     'Witness-shorthand for kind=confirms (promotion)'),
    ('Q-boundary',          'boundary operation',
     'Witness-shorthand for kind=sibling-boundary'),

    -- Refinement (kind R)
    ('Q-refine',            'refine operation',
     'Refinement-introduction primitive'),

    -- Schema-extension (kind E)
    ('Q-load_extension',    'load_extension operation',
     'Domain-extension loading primitive'),

    -- Read primitives (kind K)
    ('Q-kquery',            'kquery operation',
     'Klein-four read classifier (the universal read primitive)'),
    ('Q-tropical_min',      'tropical_min operation',
     'Generic tropical-MIN over an ordered column'),
    ('Q-tropical_max',      'tropical_max operation',
     'Generic tropical-MAX over an ordered column'),

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
    ('framework', 'Q-introduce_object',  'catalogue-introduces', NULL),
    ('framework', 'Q-introduce_tension', 'catalogue-introduces', NULL),
    ('framework', 'Q-introduce_break',   'catalogue-introduces', NULL),
    ('framework', 'Q-witness',           'catalogue-introduces', NULL),
    ('framework', 'Q-defer',             'catalogue-introduces', NULL),
    ('framework', 'Q-promote',           'catalogue-introduces', NULL),
    ('framework', 'Q-boundary',          'catalogue-introduces', NULL),
    ('framework', 'Q-refine',            'catalogue-introduces', NULL),
    ('framework', 'Q-load_extension',    'catalogue-introduces', NULL),
    ('framework', 'Q-kquery',            'catalogue-introduces', NULL),
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
