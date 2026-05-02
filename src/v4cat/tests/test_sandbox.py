"""
Unit tests for v4cat.sandbox — slot validation and path resolution.

Run as a script::

    python -m v4cat.tests.test_sandbox
"""
from __future__ import annotations

import os
import sys
import tempfile
import traceback
from pathlib import Path

from v4cat.sandbox import (
    CatalogueRoot,
    InvalidSlot,
    SlotMissing,
)


# -----------------------------------------------------------------------------
# Fixture helper
# -----------------------------------------------------------------------------

def _fresh_root() -> tuple[Path, CatalogueRoot]:
    """Create a tmpdir-backed root. Caller is responsible for cleanup
    via the directory persisting only for the test's duration."""
    tmp = Path(tempfile.mkdtemp(prefix='v4cat-sandbox-test-'))
    return tmp, CatalogueRoot(tmp)


# -----------------------------------------------------------------------------
# Slug acceptance
# -----------------------------------------------------------------------------

def test_simple_slug_resolves_under_root():
    tmp, root = _fresh_root()
    p = root.path_for('mydomain')
    assert p == tmp / 'mydomain.db'
    assert p.parent == tmp


def test_slug_with_dash_and_underscore():
    _, root = _fresh_root()
    assert root.path_for('a-b_c').name == 'a-b_c.db'


def test_slug_with_digits_and_mixed_case():
    _, root = _fresh_root()
    assert root.path_for('Ab12Cd').name == 'Ab12Cd.db'


def test_slug_max_length_64():
    _, root = _fresh_root()
    long_ok = 'a' * 64
    long_bad = 'a' * 65
    assert root.path_for(long_ok).stem == long_ok
    try:
        root.path_for(long_bad)
    except InvalidSlot:
        return
    raise AssertionError('expected InvalidSlot for 65-char slug')


# -----------------------------------------------------------------------------
# Slug rejection — the load-bearing security cases
# -----------------------------------------------------------------------------

def _expect_invalid(name: str):
    _, root = _fresh_root()
    try:
        root.path_for(name)
    except InvalidSlot:
        return
    raise AssertionError(f'expected InvalidSlot for {name!r}')


def test_rejects_empty_string():
    _expect_invalid('')


def test_rejects_dotdot():
    _expect_invalid('..')


def test_rejects_path_traversal():
    _expect_invalid('../etc/passwd')


def test_rejects_absolute_path():
    _expect_invalid('/etc/passwd')


def test_rejects_forward_slash():
    _expect_invalid('a/b')


def test_rejects_backslash():
    _expect_invalid('a\\b')


def test_rejects_leading_dot():
    _expect_invalid('.hidden')


def test_rejects_leading_dash():
    _expect_invalid('-flag')


def test_rejects_leading_underscore():
    _expect_invalid('_private')


def test_rejects_nul_byte():
    _expect_invalid('a\x00b')


def test_rejects_space():
    _expect_invalid('my domain')


def test_rejects_extension_in_name():
    _expect_invalid('mydomain.db')


def test_rejects_unicode():
    # Slug is ASCII-only by regex; reject e.g. cyrillic look-alikes
    _expect_invalid('mуdomain')  # 'му' looks like 'mu'


# -----------------------------------------------------------------------------
# Symlink escape — the parent-equality belt-and-suspenders check
# -----------------------------------------------------------------------------

def test_symlink_escape_is_caught():
    """If a symlink in the root points outside the root, the
    parent-equality check after resolve() rejects it."""
    if os.name == 'nt':
        return  # symlinks need privilege on Windows; skip
    tmp = Path(tempfile.mkdtemp(prefix='v4cat-sandbox-symlink-'))
    outside = Path(tempfile.mkdtemp(prefix='v4cat-sandbox-outside-'))
    # Place a malicious symlink "evil.db" inside tmp pointing into outside
    (tmp / 'evil.db').symlink_to(outside / 'target.db')
    root = CatalogueRoot(tmp)
    try:
        root.path_for('evil')
    except InvalidSlot:
        return
    raise AssertionError(
        'symlink-escape via valid-looking slug was not caught'
    )


# -----------------------------------------------------------------------------
# Listing + existence
# -----------------------------------------------------------------------------

def test_list_slots_empty_root():
    _, root = _fresh_root()
    assert root.list_slots() == []


def test_list_slots_after_create():
    tmp, root = _fresh_root()
    (tmp / 'alpha.db').write_text('')
    (tmp / 'beta.db').write_text('')
    assert root.list_slots() == ['alpha', 'beta']


def test_list_slots_filters_non_db_files():
    tmp, root = _fresh_root()
    (tmp / 'alpha.db').write_text('')
    (tmp / 'README.txt').write_text('')
    (tmp / 'subdir').mkdir()
    assert root.list_slots() == ['alpha']


def test_list_slots_filters_invalid_stem():
    tmp, root = _fresh_root()
    (tmp / 'good.db').write_text('')
    (tmp / '.hidden.db').write_text('')  # leading dot — invalid stem
    assert root.list_slots() == ['good']


def test_exists_returns_false_for_absent():
    _, root = _fresh_root()
    assert root.exists('nonesuch') is False


def test_exists_returns_true_for_present():
    tmp, root = _fresh_root()
    (tmp / 'present.db').write_text('')
    assert root.exists('present') is True


def test_path_for_must_exist_raises_when_absent():
    _, root = _fresh_root()
    try:
        root.path_for('missing', must_exist=True)
    except SlotMissing:
        return
    raise AssertionError('expected SlotMissing')


def test_path_for_must_exist_returns_path_when_present():
    tmp, root = _fresh_root()
    (tmp / 'here.db').write_text('')
    assert root.path_for('here', must_exist=True) == tmp / 'here.db'


# -----------------------------------------------------------------------------
# Construction
# -----------------------------------------------------------------------------

def test_construct_requires_existing_directory():
    nonexistent = Path('/tmp/v4cat-this-should-not-exist-xyzzy')
    if nonexistent.exists():
        return  # skip; can't reliably test
    try:
        CatalogueRoot(nonexistent)
    except FileNotFoundError:
        return
    raise AssertionError('expected FileNotFoundError')


def test_construct_rejects_file_path():
    tmp = Path(tempfile.mkdtemp(prefix='v4cat-sandbox-'))
    f = tmp / 'a-file'
    f.write_text('')
    try:
        CatalogueRoot(f)
    except NotADirectoryError:
        return
    raise AssertionError('expected NotADirectoryError')


# -----------------------------------------------------------------------------
# Test harness
# -----------------------------------------------------------------------------

ALL_TESTS = [
    test_simple_slug_resolves_under_root,
    test_slug_with_dash_and_underscore,
    test_slug_with_digits_and_mixed_case,
    test_slug_max_length_64,
    test_rejects_empty_string,
    test_rejects_dotdot,
    test_rejects_path_traversal,
    test_rejects_absolute_path,
    test_rejects_forward_slash,
    test_rejects_backslash,
    test_rejects_leading_dot,
    test_rejects_leading_dash,
    test_rejects_leading_underscore,
    test_rejects_nul_byte,
    test_rejects_space,
    test_rejects_extension_in_name,
    test_rejects_unicode,
    test_symlink_escape_is_caught,
    test_list_slots_empty_root,
    test_list_slots_after_create,
    test_list_slots_filters_non_db_files,
    test_list_slots_filters_invalid_stem,
    test_exists_returns_false_for_absent,
    test_exists_returns_true_for_present,
    test_path_for_must_exist_raises_when_absent,
    test_path_for_must_exist_returns_path_when_present,
    test_construct_requires_existing_directory,
    test_construct_rejects_file_path,
]


def main() -> int:
    passed, failed = 0, 0
    for test in ALL_TESTS:
        try:
            test()
            print(f'  ✓ {test.__name__}')
            passed += 1
        except Exception as e:
            print(f'  ✗ {test.__name__}: {e}')
            traceback.print_exc()
            failed += 1
    print(f'\n{passed} passed, {failed} failed')
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
