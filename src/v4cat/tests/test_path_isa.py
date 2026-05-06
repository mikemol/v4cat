"""
Tests for the cat.events.append / replay / invert ISA verbs.

Closes v4cat#10 (gc-v4cat-path-isa-verbs) and the long-standing
event-log gap (cotype/shadow_event_log_gap.md). Verifies:
  - cat.events is callable on a fresh catalogue
  - introduce_node + edge auto-record into event_log
  - replay produces the ordered sequence
  - replay is idempotent (re-deriving twice yields equal results)
  - invert returns the symbolic inverse for a recorded event
"""
from __future__ import annotations

import pytest

from v4cat.catalogue import SymmetryCatalogue


@pytest.fixture
def cat() -> SymmetryCatalogue:
    with SymmetryCatalogue(':memory:', check_self_hosting=True) as c:
        yield c


def test_events_namespace_callable_on_fresh_catalogue(cat):
    assert hasattr(cat, 'events')
    assert callable(cat.events.append)
    assert callable(cat.events.replay)
    assert callable(cat.events.invert)


def test_introduce_node_auto_records_event(cat):
    initial = cat.events.replay()
    initial_n = len(initial)
    cat.introduce_node('test:a', 'a', 'spec')
    after = cat.events.replay()
    assert len(after) == initial_n + 1
    last = after[-1]
    assert last['generator'] == 'introduce_node'
    assert last['args']['id'] == 'test:a'


def test_edge_auto_records_event(cat):
    cat.introduce_break('TEST-1', 'tb')
    cat.introduce_node('test:agent', 'agent', 'spec')
    pre = cat.events.replay()
    pre_n = len(pre)
    cat.edge('test:agent', 'TEST-1', 'catalogue-introduces')
    post = cat.events.replay()
    assert len(post) == pre_n + 1
    last = post[-1]
    assert last['generator'] == 'edge'
    assert last['args']['src'] == 'test:agent'
    assert last['args']['tgt'] == 'TEST-1'
    assert last['args']['kind'] == 'catalogue-introduces'


def test_replay_produces_ordered_sequence(cat):
    cat.introduce_node('test:n1', 'n1', 'spec')
    cat.introduce_node('test:n2', 'n2', 'spec')
    cat.introduce_node('test:n3', 'n3', 'spec')
    events = cat.events.replay()
    # extract just the introduce_node events for our test nodes
    test_events = [
        e for e in events
        if e['generator'] == 'introduce_node'
        and e['args'].get('id', '').startswith('test:n')
    ]
    assert [e['args']['id'] for e in test_events] == [
        'test:n1', 'test:n2', 'test:n3'
    ]


def test_replay_idempotent(cat):
    cat.introduce_node('test:idem', 'idem', 'spec')
    a = cat.events.replay()
    b = cat.events.replay()
    assert a == b


def test_replay_range(cat):
    cat.introduce_node('test:r1', 'r1', 'spec')
    cat.introduce_node('test:r2', 'r2', 'spec')
    full = cat.events.replay()
    if len(full) >= 2:
        first_id = full[0]['event_id']
        partial = cat.events.replay(start=first_id, end=first_id + 1)
        assert len(partial) == 1
        assert partial[0]['event_id'] == first_id


def test_invert_returns_symbolic_inverse(cat):
    cat.introduce_node('test:inv', 'inv', 'spec')
    events = cat.events.replay()
    # find the introduce_node event for test:inv
    target = next(
        e for e in events
        if e['generator'] == 'introduce_node'
        and e['args'].get('id') == 'test:inv'
    )
    inv = cat.events.invert(target['event_id'])
    assert inv['event_id'] == target['event_id']
    assert inv['generator'] == 'introduce_node'
    assert inv['args']['id'] == 'test:inv'
    assert inv['inverse_intent'] == 'undo'


def test_invert_unknown_event_raises(cat):
    with pytest.raises(ValueError, match='unknown event_id'):
        cat.events.invert(999_999)


def test_path_identity_replay_round_trip(cat):
    """Path identity primitive: two catalogues built from the same
    event sequence end up with the same closed cells."""
    cat.introduce_break('TEST-2', 'tb')
    cat.introduce_node('test:a2', 'a', 'spec')
    cat.edge('test:a2', 'TEST-2', 'catalogue-introduces')

    events_log = cat.events.replay()

    # Replay only the *test-domain* events into a second fresh
    # catalogue (skip framework bootstrap events; those auto-replay).
    test_ids = {'test:a2', 'TEST-2'}
    with SymmetryCatalogue(':memory:', check_self_hosting=True) as cat2:
        for e in events_log:
            if e['generator'] == 'introduce_node':
                a = e['args']
                if a.get('id') in test_ids:
                    cat2.introduce_node(
                        a['id'], a['name'], a['type'],
                        attrs=a.get('attrs'),
                    )
            elif e['generator'] == 'edge':
                a = e['args']
                if a.get('src') in test_ids:
                    cat2.edge(a['src'], a['tgt'], a['kind'],
                              notes=a.get('notes'))

        # The closed EdgeCell from the original should have a counterpart.
        from v4cat import event_cells
        cell_id = event_cells.edge_cell_id(
            'test:a2', 'catalogue-introduces', 'TEST-2'
        )
        row = cat2.conn.execute(
            "SELECT closure_state FROM cells WHERE id = ?", (cell_id,)
        ).fetchone()
        assert row is not None and row[0] == 'closed'
