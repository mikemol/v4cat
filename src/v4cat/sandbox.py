"""
v4cat.sandbox — slot-based persistence under a confined root.

The MCP server is launched with ``--root DIR``; clients refer to
catalogues by *slot name* (a slug), never by path. The slug is
restricted to ``[A-Za-z0-9][A-Za-z0-9_-]{0,63}`` and the resolved
file path is verified to live directly under the root, so a
malicious prompt has no string to redirect — the only filesystem
locations the server ever opens are ``<root>/<slug>.db``.

Validation is layered:

  * The slug regex rules out ``..``, ``/``, ``\\``, leading dots,
    and NUL byte.
  * After joining the slug to the root and calling ``Path.resolve``,
    the candidate's parent must be *exactly* the resolved root.
    This catches symlink-escape attempts even if a valid-looking
    slot filename was placed by an attacker with shell access.

Both checks are cheap; defense in depth.
"""
from __future__ import annotations

import re
from pathlib import Path

_SLUG_RE = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$')


class InvalidSlot(ValueError):
    """Slot name fails the slug rule or escapes the root."""


class SlotExists(ValueError):
    """``create_catalogue`` was called on an existing slot."""


class SlotMissing(ValueError):
    """``open_catalogue`` (or ``path_for(must_exist=True)``) was
    called on a slot that doesn't exist."""


class CatalogueRoot:
    """A pre-validated directory under which slot files live.

    Slot names are slugs matching
    ``[A-Za-z0-9][A-Za-z0-9_-]{0,63}``. The ``.db`` extension is
    appended by the root; clients never pass extensions or paths.
    """

    def __init__(self, root: Path):
        self.root = Path(root).resolve(strict=True)
        if not self.root.is_dir():
            raise NotADirectoryError(self.root)

    def _slot_path(self, name: str) -> Path:
        if not _SLUG_RE.match(name):
            raise InvalidSlot(
                f"invalid slot name {name!r}: must match "
                f"[A-Za-z0-9][A-Za-z0-9_-]{{0,63}}"
            )
        candidate = (self.root / f"{name}.db").resolve()
        if candidate.parent != self.root:
            raise InvalidSlot(
                f"slot {name!r} resolves outside root "
                f"(symlink escape?)"
            )
        return candidate

    def list_slots(self) -> list[str]:
        """List slot names that exist as regular files under root.

        Files whose stem doesn't match the slug rule are filtered
        out — they may have been placed by another tool but are
        not addressable by this sandbox.
        """
        return sorted(
            p.stem for p in self.root.glob('*.db')
            if p.is_file() and _SLUG_RE.match(p.stem)
        )

    def exists(self, name: str) -> bool:
        return self._slot_path(name).is_file()

    def path_for(self, name: str, *, must_exist: bool = False) -> Path:
        """Resolve a slot name to its absolute path.

        Raises :class:`InvalidSlot` if the name fails validation,
        :class:`SlotMissing` if ``must_exist=True`` and the file
        is absent.
        """
        p = self._slot_path(name)
        if must_exist and not p.is_file():
            raise SlotMissing(name)
        return p


__all__ = [
    'CatalogueRoot',
    'InvalidSlot', 'SlotExists', 'SlotMissing',
]
