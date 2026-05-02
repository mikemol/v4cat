"""
Symmetry-break cataloguing — Python ISA implementation.

Implements the verbs documented in methodology.md against a SQLite
backing store. The schema is schema.sql.

Each ISA verb is one method. Methods are idempotent on primary keys
(INSERT OR IGNORE). Mutations don't auto-commit; use the catalogue as
a context manager or call commit() explicitly.

Design alignment with methodology.md:

  * Originator, status, and other "global" properties are *derived*
    via views (break_origin, break_status, ...). No verb writes them.
  * Time and lineage are breaks-themselves. Year is an attribute on
    objects; lineage is edges between objects via the lineages table.
  * Substrate is interchangeable: SQLite here, but the verbs would
    map equivalently onto a triple store, document store, or graph DB.
  * Domain-specific extensions (per-break detail tables, per-domain
    views, seed data) load via load_extension() on top of the
    framework schema.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Optional


HERE = Path(__file__).parent
DEFAULT_SCHEMA_PATH = HERE / 'schema.sql'
DEFAULT_FRAMEWORK_SEED_PATH = HERE / 'framework_seed.sql'


class SymmetryCatalogue:
    """The ISA implemented as method calls.

    Open with a path (':memory:' for ephemeral) and either a fresh
    schema or an existing database. Bootstrap loads schema.sql.
    Subsequent re-opens are idempotent (the schema uses CREATE TABLE
    IF NOT EXISTS).

    Self-hosting closure check (Theorem 14.5, theory.md § 14):

      * ``check_self_hosting=True`` (default) loads
        ``framework_seed.sql`` on top of the schema (the
        framework's self-cataloguing data) and runs
        ``bootstrap.check_closure`` after open. A non-empty gap
        raises :class:`SelfHostingViolation` — Corollary 14.5.1's
        to-do list. The seed and check are no-ops when
        ``bootstrap=False`` (no framework schema to attach to).
      * ``check_self_hosting=False`` skips both seed loading and
        the check. Useful for tests that want an entirely empty
        catalogue or for performance-critical paths that don't
        need the audit.

    Per theory.md § 14.8, the default flip from False to True is
    the runtime trigger that licenses the rename from ``kfour``
    to ``v4cat``: the framework now self-hosts at scope on every
    open without an opt-in flag.
    """

    def __init__(
        self,
        db_path: str | Path = ':memory:',
        *,
        bootstrap: bool = True,
        schema_path: Path = DEFAULT_SCHEMA_PATH,
        check_self_hosting: bool = True,
        framework_seed_path: Path = DEFAULT_FRAMEWORK_SEED_PATH,
    ):
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        if bootstrap:
            self._maybe_bootstrap(schema_path)
            if check_self_hosting:
                # Load the framework's self-cataloguing seed
                # (idempotent via INSERT OR IGNORE) and run the
                # closure check. Only meaningful when the schema
                # was actually bootstrapped (otherwise the seed's
                # INSERTs would fail on missing tables).
                self.conn.executescript(framework_seed_path.read_text())
                self.conn.commit()
                from .bootstrap import check_closure
                check_closure(self)
        elif check_self_hosting:
            # bootstrap=False with check_self_hosting=True: still
            # call check_closure, which is a no-op when
            # Q-supported-claims is absent (the expected case for
            # domain-extension catalogues).
            from .bootstrap import check_closure
            check_closure(self)

    def _maybe_bootstrap(self, schema_path: Path) -> None:
        """Load the framework schema. Idempotent."""
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='breaks'"
        )
        if cur.fetchone() is None:
            self.conn.executescript(schema_path.read_text())

    def load_extension(self, sql_path: str | Path) -> None:
        """Load a domain-specific extension (per-break detail tables,
        per-domain views, seed data) on top of the framework schema.

        Re-runnable if the extension SQL is itself idempotent
        (CREATE TABLE IF NOT EXISTS / INSERT OR IGNORE).
        """
        self.conn.executescript(Path(sql_path).read_text())

    def __enter__(self) -> 'SymmetryCatalogue':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()

    def commit(self) -> None:
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # =================================================================
    # ISA — foundational verbs
    # =================================================================

    def introduce_break(
        self,
        number: str,
        name: str,
        *,
        short_desc: Optional[str] = None,
        axes: Optional[Iterable[str]] = None,
    ) -> None:
        """ISA: INTRODUCE break <number>"""
        self.conn.execute(
            "INSERT OR IGNORE INTO breaks (number, name, short_desc) "
            "VALUES (?, ?, ?)",
            (number, name, short_desc),
        )
        if axes:
            for axis in axes:
                self.conn.execute(
                    "INSERT OR IGNORE INTO break_axes "
                    "(break_number, axis, description) "
                    "VALUES (?, ?, NULL)",
                    (number, axis),
                )

    def introduce_object(
        self,
        id: str,
        name: str,
        *,
        year: Optional[int] = None,
        catalogue_order: Optional[int] = None,
        notes: Optional[str] = None,
        lineage: Optional[Iterable[tuple[str, str]]] = None,
        attrs: Optional[dict[str, Any]] = None,
    ) -> None:
        """ISA: INTRODUCE object <id>

        Framework-minimal signature. Only attributes that are
        load-bearing for framework views are first-class columns:

          * ``year`` — tropical-MIN axis for break_origin
          * ``catalogue_order`` — tropical-MIN axis for break_first_seen
          * ``notes`` — free-form annotation
          * ``lineage`` — list of ``(ancestor_id, kind)`` tuples;
            populates the lineages table for inheritance queries

        Domain-specific attributes (vendor, register width, evaluation
        strategy, hardness assumption, etc.) go in ``attrs``: a
        ``dict[str, Any]`` whose entries are stored as
        ``(spec_id, name, value)`` rows in spec_attributes. Values
        are stringified (``str(value)``); cast at query time.

        ``catalogue_order`` defaults to the next available integer:
        when a new object enters the catalogue via the ISA, that's
        its exposition step. Explicit values (loaded from a domain
        extension) are preserved; only new ISA-introduced objects
        auto-assign.
        """
        if catalogue_order is None:
            cur = self.conn.execute("SELECT MAX(catalogue_order) FROM specs")
            max_order = cur.fetchone()[0] or 0
            catalogue_order = max_order + 1
        self.conn.execute(
            "INSERT OR IGNORE INTO specs "
            "(id, name, year, catalogue_order, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            (id, name, year, catalogue_order, notes),
        )
        if lineage:
            for ancestor_id, kind in lineage:
                self.conn.execute(
                    "INSERT OR IGNORE INTO lineages "
                    "(descendant_id, ancestor_id, kind, notes) "
                    "VALUES (?, ?, ?, NULL)",
                    (id, ancestor_id, kind),
                )
        if attrs:
            for attr_name, attr_value in attrs.items():
                self.conn.execute(
                    "INSERT OR IGNORE INTO spec_attributes "
                    "(spec_id, name, value) VALUES (?, ?, ?)",
                    (id, attr_name,
                     None if attr_value is None else str(attr_value)),
                )

    def attributes_for_object(self, object_: str) -> dict[str, str]:
        """Read the spec_attributes (name → value) for one object.

        Values are returned as strings (the on-disk form); callers
        cast as needed.
        """
        cur = self.conn.execute(
            "SELECT name, value FROM spec_attributes "
            "WHERE spec_id = ? ORDER BY name",
            (object_,),
        )
        return {row['name']: row['value'] for row in cur.fetchall()}

    # =================================================================
    # Tropical queries over ordered columns
    #
    # The framework's structural commitment is to *tropical aggregates
    # over ordered columns*, not to any specific column. ``year`` and
    # ``catalogue_order`` are the two canonical ordered axes the
    # framework provides out of the box (each with a documented
    # semantic), but tropical_min/tropical_max work over any column
    # whose values admit a total order.
    #
    # The pre-defined views (break_origin, break_first_seen) are
    # concrete instances. Domain extensions can add ordered columns
    # (via ALTER TABLE specs) and use tropical_min over them, or
    # define their own analogous views.
    # =================================================================

    def _spec_columns(self) -> set[str]:
        """Set of column names currently on the specs table."""
        cur = self.conn.execute("PRAGMA table_info(specs)")
        return {row['name'] for row in cur.fetchall()}

    def tropical_min(
        self,
        *,
        axis_column: str,
        witness_kinds: Iterable[str],
        break_: Optional[str] = None,
        direction: str = 'min',
    ) -> list[dict]:
        """Generic tropical query over an ordered column.

        For each break (or just ``break_`` if specified), find the
        spec(s) where ``axis_column`` is at its extremum among
        witnesses with the given kinds.

        Args:
            axis_column: name of the specs column to aggregate over.
                Must be a real column on specs (not in spec_attributes;
                domain extensions wanting custom tropical axes should
                ALTER TABLE specs first).
            witness_kinds: filter predicate over witness kinds.
            break_: restrict to a single break, or None for all.
            direction: ``'min'`` or ``'max'``.

        The framework's pre-defined views are concrete instances::

            # break_origin equivalent:
            cat.tropical_min(
                axis_column='year',
                witness_kinds=('origin', 'catalogue-introduces'),
            )

            # break_first_seen equivalent:
            cat.tropical_min(
                axis_column='catalogue_order',
                witness_kinds=('catalogue-introduces',),
            )

        Returns rows with ``break_number``, ``break_name``,
        ``spec_id``, ``spec_name``, ``axis_value``.
        """
        if direction not in ('min', 'max'):
            raise ValueError(
                f"direction must be 'min' or 'max', got {direction!r}"
            )
        if axis_column not in self._spec_columns():
            raise ValueError(
                f"axis_column {axis_column!r} not found on specs; "
                f"available: {sorted(self._spec_columns())}"
            )
        # Validate kinds is non-empty
        kinds_tuple = tuple(witness_kinds)
        if not kinds_tuple:
            raise ValueError("witness_kinds must be non-empty")

        agg = 'MIN' if direction == 'min' else 'MAX'
        placeholders = ','.join('?' for _ in kinds_tuple)

        # axis_column is whitelisted via _spec_columns, so substitution
        # is safe (not user-controlled).
        sql = f"""
            SELECT DISTINCT
                b.number AS break_number,
                b.name AS break_name,
                s.id   AS spec_id,
                s.name AS spec_name,
                s.{axis_column} AS axis_value
            FROM breaks b
            JOIN witnesses w ON w.break_number = b.number
            JOIN specs     s ON s.id           = w.spec_id
            WHERE w.kind IN ({placeholders})
              AND s.{axis_column} = (
                  SELECT {agg}(s2.{axis_column})
                  FROM witnesses w2
                  JOIN specs s2 ON w2.spec_id = s2.id
                  WHERE w2.break_number = b.number
                    AND w2.kind IN ({placeholders})
                    AND s2.{axis_column} IS NOT NULL
              )
        """
        params: list[Any] = list(kinds_tuple) + list(kinds_tuple)
        if break_ is not None:
            sql += " AND b.number = ?"
            params.append(break_)
        sql += " ORDER BY b.number, s.id"

        cur = self.conn.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def tropical_max(
        self,
        *,
        axis_column: str,
        witness_kinds: Iterable[str],
        break_: Optional[str] = None,
    ) -> list[dict]:
        """Sugar: ``tropical_min`` with ``direction='max'``.

        Useful for "what's the most recent witness?" queries (the
        dual of "originator")."""
        return self.tropical_min(
            axis_column=axis_column,
            witness_kinds=witness_kinds,
            break_=break_,
            direction='max',
        )

    def introduce_tension(
        self,
        id: str,
        name: str,
        *,
        description: Optional[str] = None,
        status: str = 'open',
        addressing_stage: Optional[str] = None,
        breaks_involved: Optional[Iterable[str]] = None,
    ) -> None:
        """ISA: INTRODUCE tension <id>"""
        self.conn.execute(
            "INSERT OR IGNORE INTO tensions "
            "(id, name, description, status, addressing_stage) "
            "VALUES (?, ?, ?, ?, ?)",
            (id, name, description, status, addressing_stage),
        )
        if breaks_involved:
            for break_ in breaks_involved:
                self.conn.execute(
                    "INSERT OR IGNORE INTO tension_breaks "
                    "(tension_id, break_number, note) "
                    "VALUES (?, ?, NULL)",
                    (id, break_),
                )

    def witness(
        self,
        subject: str,
        break_: str,
        kind: str,
        *,
        notes: Optional[str] = None,
        scope: str = 'spec',
    ) -> None:
        """ISA: WITNESS <subject> <break> <kind>

        ``kind`` should be one of the documented vocabulary in
        methodology.md: origin, catalogue-introduces, confirms,
        refines, first-witness, precedes, cross-vendor, inherits,
        deferred-candidate, sibling-boundary, gates-with-fault.
        """
        self.conn.execute(
            "INSERT OR IGNORE INTO witnesses "
            "(spec_id, break_number, kind, notes, scope) "
            "VALUES (?, ?, ?, ?, ?)",
            (subject, break_, kind, notes, scope),
        )

    def refine(
        self,
        break_: str,
        object_: str,
        name: str,
        *,
        description: Optional[str] = None,
    ) -> None:
        """ISA: REFINE <break> <object> <name>

        Records a named refinement. Multiple refinements per
        (break, object) edge are admitted.
        """
        self.conn.execute(
            "INSERT INTO refinements "
            "(break_number, spec_id, name, description) "
            "VALUES (?, ?, ?, ?)",
            (break_, object_, name, description),
        )

    def query(self, sql: str, *params: Any) -> list[dict]:
        """ISA: QUERY — generic SQL pass-through.

        v1 uses raw SQL. Returns a list of dicts (one per row).
        """
        cur = self.conn.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    # =================================================================
    # ISA — lifecycle verbs
    #
    # In the methodology, these are *witness expressions*: a `defer`
    # is a witness with kind='deferred-candidate'; `boundary` is a
    # witness with kind='sibling-boundary'. Status is derived.
    # =================================================================

    def defer(
        self,
        break_: str,
        *,
        by: str,
        reason: Optional[str] = None,
    ) -> None:
        """ISA: DEFER <break>

        Records a deferred-candidate witness. ``by`` is the spec
        that named the candidate.
        """
        self.witness(by, break_, 'deferred-candidate', notes=reason)

    def promote(
        self,
        break_: str,
        *,
        by: str,
        reason: Optional[str] = None,
    ) -> None:
        """ISA: PROMOTE <break>

        Records a confirms witness. Status changes to 'active' via
        the derived view (because a confirms witness exists from a
        spec other than the original deferred-candidate spec).
        """
        self.witness(by, break_, 'confirms', notes=reason or 'promotion')

    def boundary(
        self,
        break_: str,
        reason: str,
        *,
        by: str,
    ) -> None:
        """ISA: BOUNDARY <break>

        Records a sibling-boundary witness — a deliberate metamodel
        non-extension.
        """
        self.witness(by, break_, 'sibling-boundary', notes=reason)

    # =================================================================
    # Analytic queries — never mutate, always derived
    # =================================================================

    def origin(self, break_: str) -> dict | None:
        """ORIGIN(break) — tropical MIN(year) over origin-class edges."""
        cur = self.conn.execute(
            "SELECT * FROM break_origin WHERE break_number = ?",
            (break_,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def first_seen(self, break_: str) -> dict | None:
        """FIRST_SEEN(break) — tropical MIN(catalogue_order)."""
        cur = self.conn.execute(
            "SELECT * FROM break_first_seen WHERE break_number = ?",
            (break_,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def status(self, break_: str) -> str | None:
        """STATUS(break) — derived from witness pattern."""
        cur = self.conn.execute(
            "SELECT status FROM break_status WHERE break_number = ?",
            (break_,),
        )
        row = cur.fetchone()
        return row['status'] if row else None

    def retroactive_gap(self, break_: str) -> int | None:
        """RETROACTIVE_GAP(break) — first_seen.year - origin.year."""
        cur = self.conn.execute(
            "SELECT retroactive_gap_years FROM breaks_with_origin "
            "WHERE number = ?",
            (break_,),
        )
        row = cur.fetchone()
        return row['retroactive_gap_years'] if row else None

    def lineage(self, object_: str) -> list[dict]:
        """LINEAGE(object) — ancestors via the lineages table.

        Returns rows ordered by depth (1 = direct parent, 2 =
        grandparent, ...).
        """
        cur = self.conn.execute(
            "SELECT la.descendant, la.ancestor, la.depth, "
            "       s.name AS ancestor_name, s.year AS ancestor_year "
            "FROM lineage_ancestry la "
            "JOIN specs s ON s.id = la.ancestor "
            "WHERE la.descendant = ? "
            "ORDER BY la.depth",
            (object_,),
        )
        return [dict(row) for row in cur.fetchall()]

    def inherited_breaks(self, object_: str) -> list[dict]:
        """INHERITED_BREAKS(object) — breaks witnessed by ancestors.

        Returns breaks where any ancestor along the lineage chain
        has an origin or catalogue-introduces witness.
        """
        cur = self.conn.execute(
            """
            SELECT DISTINCT
                w.break_number,
                b.name AS break_name,
                la.ancestor AS via_ancestor,
                la.depth
            FROM lineage_ancestry la
            JOIN witnesses w ON w.spec_id = la.ancestor
            JOIN breaks b    ON b.number  = w.break_number
            WHERE la.descendant = ?
              AND w.kind IN ('origin', 'catalogue-introduces')
            ORDER BY la.depth, w.break_number
            """,
            (object_,),
        )
        return [dict(row) for row in cur.fetchall()]

    # =================================================================
    # Inspection helpers
    # =================================================================

    def all_breaks(self) -> list[dict]:
        cur = self.conn.execute(
            "SELECT * FROM breaks_with_origin ORDER BY number"
        )
        return [dict(row) for row in cur.fetchall()]

    def all_objects(self) -> list[dict]:
        cur = self.conn.execute(
            "SELECT * FROM specs "
            "ORDER BY catalogue_order IS NULL, catalogue_order, year"
        )
        return [dict(row) for row in cur.fetchall()]

    def witnesses_for_object(self, object_: str) -> list[dict]:
        cur = self.conn.execute(
            "SELECT w.*, b.name AS break_name "
            "FROM witnesses w "
            "JOIN breaks b ON b.number = w.break_number "
            "WHERE w.spec_id = ? "
            "ORDER BY w.break_number, w.kind",
            (object_,),
        )
        return [dict(row) for row in cur.fetchall()]

    def witnesses_for_break(self, break_: str) -> list[dict]:
        cur = self.conn.execute(
            "SELECT w.*, s.name AS spec_name, s.year "
            "FROM witnesses w "
            "JOIN specs s ON s.id = w.spec_id "
            "WHERE w.break_number = ? "
            "ORDER BY s.year IS NULL, s.year, w.kind",
            (break_,),
        )
        return [dict(row) for row in cur.fetchall()]

    def refinements_for_break(self, break_: str) -> list[dict]:
        cur = self.conn.execute(
            "SELECT r.*, s.name AS spec_name "
            "FROM refinements r "
            "JOIN specs s ON s.id = r.spec_id "
            "WHERE r.break_number = ? "
            "ORDER BY s.year, r.name",
            (break_,),
        )
        return [dict(row) for row in cur.fetchall()]
