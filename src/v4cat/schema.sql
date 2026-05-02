-- =============================================================================
-- catalogue/schema.sql — generic schema for the symmetry-break cataloguing
-- methodology. Domain-agnostic.
--
-- The schema evolves through documented breaks (S0 through S11) — each
-- adds raw structure that some domain pressure forced into view. The
-- shape mirrors the methodology described in methodology.md.
--
-- This file contains *only* the framework's generic core. Per-break-family
-- detail tables (halt modes, page tables, atomic ops, etc.) are
-- domain-specific extensions and live outside the framework — load them
-- as additional schema after this file.
--
-- Re-runnable via SQLite: `sqlite3 my.db < schema.sql`.
-- =============================================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- S0: breaks — the table of symmetry planes (the seed)
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS breaks (
    number      TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    short_desc  TEXT
);

-- -----------------------------------------------------------------------------
-- S1 + S2: specs — the witness vocabulary, framework-minimal
--
-- The framework's `specs` table contains *only* attributes that are
-- load-bearing for framework views. Each column has a documented
-- structural purpose:
--
--   id:              identity (primary key); needed by every relation
--   name:            human-readable label; needed by reports, prompts
--   year:            tropical-MIN axis for the break_origin view;
--                    structurally privileged by the temporal-axis
--                    commitment (Q72 in the processor catalogue, the
--                    universal-temporal-axis claim in theory.md § 3)
--   catalogue_order: tropical-MIN axis for the break_first_seen view;
--                    distinct from year because catalogue exposition
--                    order isn't always chronological
--   notes:           free-form annotation; any catalogue benefits
--
-- Domain-specific attributes (vendor, family, register widths, ...)
-- are *not* baked in. They belong in `spec_attributes` (S2b below)
-- as (name, value) pairs, OR in a domain-extension's own ALTER
-- TABLE if the attribute is queried frequently enough to justify a
-- typed column.
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS specs (
    id               TEXT PRIMARY KEY,
    name             TEXT NOT NULL,
    year             INTEGER,
    catalogue_order  INTEGER,
    notes            TEXT
);

-- -----------------------------------------------------------------------------
-- S2b: spec_attributes — domain-specific (name, value) pairs on specs
--
-- A first-class place for any attribute that isn't framework-load-
-- bearing. Each row is a (spec, attribute_name, value) triple — the
-- same trace structure the methodology uses everywhere else.
--
-- Values are stored as TEXT; callers cast at query time. This is the
-- minimum-commitment shape: domains that need typed access can
-- ALTER spec_attributes ADD COLUMN value_int / value_float / etc.,
-- or define a domain-specific extension table that subclasses or
-- replaces this one.
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS spec_attributes (
    spec_id  TEXT NOT NULL REFERENCES specs(id),
    name     TEXT NOT NULL,
    value    TEXT,
    PRIMARY KEY (spec_id, name)
);

-- -----------------------------------------------------------------------------
-- S3: witnesses — the bipartite contribution graph
--
-- Witness kinds (documented vocabulary):
--   * 'origin'             — chronologically first articulation
--   * 'catalogue-introduces' — catalogue's first analysis of this break
--   * 'confirms'           — additional witness; no structural change
--   * 'refines'            — extends with new attributes / cardinality
--   * 'first-witness'      — concrete instance of a previously-deferred break
--   * 'precedes'           — surfaces an abstract pattern at a different scope
--   * 'cross-vendor'       — independent confirmation in another lineage
--   * 'inherits'           — successor retains an ancestor's contribution
--   * 'deferred-candidate' — named the candidate but not yet adopted
--   * 'sibling-boundary'   — deliberate metamodel non-extension
--   * 'gates-with-fault'   — reveals structural inadequacy
-- -----------------------------------------------------------------------------

-- Includes the S8 `scope` column (originally added later for agent vs
-- spec distinction). Consolidated for re-runnability.
CREATE TABLE IF NOT EXISTS witnesses (
    spec_id       TEXT NOT NULL REFERENCES specs(id),
    break_number  TEXT NOT NULL REFERENCES breaks(number),
    kind          TEXT NOT NULL,
    notes         TEXT,
    scope         TEXT NOT NULL DEFAULT 'spec',
    PRIMARY KEY (spec_id, break_number, kind)
);

-- -----------------------------------------------------------------------------
-- S4: refinements — per-spec named attribute additions
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS refinements (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    break_number  TEXT NOT NULL REFERENCES breaks(number),
    spec_id       TEXT NOT NULL REFERENCES specs(id),
    name          TEXT NOT NULL,
    description   TEXT
);

-- -----------------------------------------------------------------------------
-- S5: (omitted from framework)
--
-- Per-break-family detail tables (e.g., halt_modes, aliases, page_tables,
-- atomic_ops, frame_formats, modes, privilege_levels) are domain-specific
-- and live in extension files, not in the framework's schema.
-- -----------------------------------------------------------------------------

-- -----------------------------------------------------------------------------
-- S6: break_axes — per-break axis classification (Q71's 4-axis tuple)
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS break_axes (
    break_number  TEXT NOT NULL REFERENCES breaks(number),
    axis          TEXT NOT NULL,
    description   TEXT,
    PRIMARY KEY (break_number, axis)
);

-- -----------------------------------------------------------------------------
-- S7: tensions — structural concerns about implementation alignment
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tensions (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    description     TEXT,
    status          TEXT,
    addressing_stage TEXT
);

CREATE TABLE IF NOT EXISTS tension_breaks (
    tension_id     TEXT NOT NULL REFERENCES tensions(id),
    break_number   TEXT NOT NULL REFERENCES breaks(number),
    note           TEXT,
    PRIMARY KEY (tension_id, break_number)
);

-- -----------------------------------------------------------------------------
-- S8: scope on witnesses — already inlined above (agent vs spec).
-- This break corresponds to adding the `scope` column when 8087
-- forced agent-level Q87 to be distinguished from spec-level.
-- -----------------------------------------------------------------------------

-- -----------------------------------------------------------------------------
-- S9: spec_axes + spaces — the 5-axis Spec record
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS spec_axes (
    spec_id      TEXT NOT NULL REFERENCES specs(id),
    axis         TEXT NOT NULL,
    declaration  TEXT NOT NULL,
    PRIMARY KEY (spec_id, axis)
);

CREATE TABLE IF NOT EXISTS spaces (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    spec_id        TEXT NOT NULL REFERENCES specs(id),
    name           TEXT NOT NULL,
    addr_dtype     TEXT,
    val_dtype      TEXT,
    size           INTEGER,
    cell_overflow  TEXT,
    blocking_io    INTEGER,
    access_class   TEXT,
    write_class    TEXT,
    mount_at       TEXT,
    description    TEXT
);

-- -----------------------------------------------------------------------------
-- S10: break_invariants — Z78's (partition, preservation-theorem) decomp
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS break_invariants (
    break_number       TEXT PRIMARY KEY REFERENCES breaks(number),
    partition_desc     TEXT NOT NULL,
    preservation_claim TEXT NOT NULL,
    temporal_axis_kind TEXT,
    notes              TEXT
);

-- -----------------------------------------------------------------------------
-- S11: lineages — (descendant, ancestor) edges between objects
--
-- Forced by methodology.md's commitment that lineage is a break-on-objects
-- (a partition by descent). Edges admit multiple kinds:
--   'descended-from'   — direct architectural / lineal descent
--   'family-member'    — same family, no specific descent
--   'inherits-from'    — generic inheritance
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS lineages (
    descendant_id  TEXT NOT NULL REFERENCES specs(id),
    ancestor_id    TEXT NOT NULL REFERENCES specs(id),
    kind           TEXT NOT NULL,
    notes          TEXT,
    PRIMARY KEY (descendant_id, ancestor_id, kind)
);

-- =============================================================================
-- VIEWS — derived properties (the methodology's "global structure is
-- always derived" commitment in action)
-- =============================================================================

DROP VIEW IF EXISTS break_origin;
CREATE VIEW break_origin AS
SELECT DISTINCT
    b.number  AS break_number,
    b.name    AS break_name,
    s.id      AS originator_id,
    s.name    AS originator_name,
    s.year    AS originated_year
FROM breaks b
JOIN witnesses w ON w.break_number = b.number
JOIN specs     s ON w.spec_id      = s.id
WHERE w.kind IN ('origin', 'catalogue-introduces')
  AND s.year = (
    SELECT MIN(s2.year)
    FROM witnesses w2
    JOIN specs s2 ON w2.spec_id = s2.id
    WHERE w2.break_number = b.number
      AND w2.kind IN ('origin', 'catalogue-introduces')
      AND s2.year IS NOT NULL
  );

DROP VIEW IF EXISTS break_first_seen;
CREATE VIEW break_first_seen AS
SELECT
    b.number  AS break_number,
    s.id      AS first_seen_at_id,
    s.name    AS first_seen_at_name,
    s.catalogue_order AS first_seen_order,
    s.year    AS first_seen_year
FROM breaks b
JOIN witnesses w ON w.break_number = b.number
JOIN specs     s ON w.spec_id      = s.id
WHERE w.kind = 'catalogue-introduces'
  AND s.catalogue_order = (
    SELECT MIN(s2.catalogue_order)
    FROM witnesses w2
    JOIN specs s2 ON w2.spec_id = s2.id
    WHERE w2.break_number = b.number
      AND w2.kind = 'catalogue-introduces'
      AND s2.catalogue_order IS NOT NULL
  );

DROP VIEW IF EXISTS break_status;
CREATE VIEW break_status AS
SELECT
    b.number AS break_number,
    CASE
        WHEN EXISTS (
            SELECT 1 FROM witnesses w
            WHERE w.break_number = b.number AND w.kind = 'sibling-boundary'
        ) THEN 'sibling-boundary'
        WHEN EXISTS (
            SELECT 1 FROM witnesses w
            WHERE w.break_number = b.number AND w.kind = 'deferred-candidate'
        ) AND NOT EXISTS (
            SELECT 1 FROM witnesses w
            WHERE w.break_number = b.number
              AND w.kind IN ('origin','catalogue-introduces','first-witness','confirms')
              AND w.spec_id NOT IN (
                  SELECT w2.spec_id FROM witnesses w2
                  WHERE w2.break_number = b.number AND w2.kind = 'deferred-candidate'
              )
        ) THEN 'deferred'
        ELSE 'active'
    END AS status
FROM breaks b;

DROP VIEW IF EXISTS breaks_with_origin;
CREATE VIEW breaks_with_origin AS
SELECT
    b.number,
    b.name,
    bs.status,
    bo.originator_name,
    bo.originated_year,
    bf.first_seen_at_name,
    bf.first_seen_year,
    CASE
        WHEN bo.originated_year < bf.first_seen_year THEN 1
        ELSE 0
    END AS is_retroactive,
    (bf.first_seen_year - bo.originated_year) AS retroactive_gap_years
FROM breaks b
LEFT JOIN break_origin     bo ON bo.break_number = b.number
LEFT JOIN break_first_seen bf ON bf.break_number = b.number
LEFT JOIN break_status     bs ON bs.break_number = b.number;

DROP VIEW IF EXISTS retroactive_attributions;
CREATE VIEW retroactive_attributions AS
SELECT
    number,
    name,
    originator_name,
    originated_year,
    first_seen_at_name,
    first_seen_year,
    retroactive_gap_years
FROM breaks_with_origin
WHERE is_retroactive = 1
ORDER BY retroactive_gap_years DESC;

DROP VIEW IF EXISTS spec_contributions;
CREATE VIEW spec_contributions AS
SELECT
    s.id              AS spec_id,
    s.name            AS spec_name,
    s.catalogue_order AS catalogue_order,
    s.year            AS spec_year,
    w.break_number,
    b.name            AS break_name,
    w.kind,
    w.scope,
    w.notes
FROM witnesses w
JOIN specs  s ON w.spec_id      = s.id
JOIN breaks b ON w.break_number = b.number
ORDER BY s.catalogue_order, w.break_number, w.kind;

DROP VIEW IF EXISTS new_breaks_per_spec;
CREATE VIEW new_breaks_per_spec AS
SELECT
    s.id    AS spec_id,
    s.name  AS spec_name,
    s.year  AS spec_year,
    COUNT(DISTINCT bo.break_number) AS breaks_originated
FROM specs s
LEFT JOIN break_origin bo ON bo.originator_id = s.id
GROUP BY s.id, s.name, s.year
ORDER BY s.year;

DROP VIEW IF EXISTS breaks_by_axis;
CREATE VIEW breaks_by_axis AS
SELECT
    ba.axis,
    COUNT(DISTINCT ba.break_number) AS break_count,
    GROUP_CONCAT(ba.break_number, ', ') AS break_numbers
FROM break_axes ba
GROUP BY ba.axis
ORDER BY break_count DESC;

DROP VIEW IF EXISTS mixed_breaks;
CREATE VIEW mixed_breaks AS
SELECT
    b.number,
    b.name,
    GROUP_CONCAT(ba.axis, ', ') AS axes
FROM breaks b
JOIN break_axes ba ON ba.break_number = b.number
GROUP BY b.number, b.name
HAVING COUNT(ba.axis) > 1
ORDER BY b.number;

DROP VIEW IF EXISTS agent_level_witnesses;
CREATE VIEW agent_level_witnesses AS
SELECT
    s.name AS spec_name,
    w.break_number,
    b.name AS break_name,
    w.kind,
    w.notes
FROM witnesses w
JOIN specs s ON w.spec_id = s.id
JOIN breaks b ON w.break_number = b.number
WHERE w.scope = 'agent'
ORDER BY s.year, w.break_number;

DROP VIEW IF EXISTS spec_axis_summary;
CREATE VIEW spec_axis_summary AS
SELECT
    s.id   AS spec_id,
    s.name AS spec_name,
    s.year AS spec_year,
    MAX(CASE WHEN sa.axis = 'spatial'       THEN sa.declaration END) AS spatial,
    MAX(CASE WHEN sa.axis = 'temporal'      THEN sa.declaration END) AS temporal,
    MAX(CASE WHEN sa.axis = 'parallel'      THEN sa.declaration END) AS parallel,
    MAX(CASE WHEN sa.axis = 'equivalential' THEN sa.declaration END) AS equivalential,
    MAX(CASE WHEN sa.axis = 'eventual'      THEN sa.declaration END) AS eventual
FROM specs s
LEFT JOIN spec_axes sa ON sa.spec_id = s.id
GROUP BY s.id, s.name, s.year
ORDER BY s.year;

-- Lineage transitive closure (recursive CTE in a view)
DROP VIEW IF EXISTS lineage_ancestry;
CREATE VIEW lineage_ancestry AS
WITH RECURSIVE ancestry(descendant, ancestor, depth) AS (
    SELECT descendant_id, ancestor_id, 1
    FROM lineages
    WHERE kind = 'descended-from'
    UNION ALL
    SELECT a.descendant, l.ancestor_id, a.depth + 1
    FROM ancestry a
    JOIN lineages l
      ON l.descendant_id = a.ancestor
     AND l.kind = 'descended-from'
)
SELECT * FROM ancestry;

-- =============================================================================
-- END
--
-- Domain-specific extensions (per-break detail tables, per-domain views,
-- seed data) load on top of this schema. The framework provides the
-- generic shape; domains populate it.
-- =============================================================================
