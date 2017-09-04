import pytest
import sys
sys.path.append('.')

from turingmachine import Transition, Direction, State


def test_create_transition():
    q0 = State()
    q1 = State()
    #In q0 upon reading a move to q1, output b, and move the tape 1 right
    q0.create_transition('a', q1, 'b', Direction.RIGHT)
    assert q0.transitions['a'].new_state == q1
    assert q0.transitions['a'].output_letter == 'b'
    assert q0.transitions['a'].movement_direction == Direction.RIGHT

def test_create_multiple_transitions():
    q0 = State()
    q1 = State()
    q2 = State()
    q0.create_transition('a', q1, 'b', Direction.RIGHT)
    q1.create_transition('c', q2, 'd', Direction.LEFT)
    with pytest.raises(KeyError):
        q0.transitions['b'] is None
    assert q0.transitions['a'].new_state.transitions['c'].new_state == q2
    assert q1.transitions['c'].new_state == q2

    assert q0.transitions['a'].new_state.transitions['c'].output_letter == 'd'
    assert q1.transitions['c'].output_letter == 'd'

    assert q0.transitions['a'].new_state.transitions['c'].movement_direction == Direction.LEFT
    assert q1.transitions['c'].movement_direction == Direction.LEFT

def test_add_transition():
    q0 = State()
    q1 = State()
    t = Transition(q1, 'b', Direction.RIGHT)
    q0.add_transition('a', t)
    assert q0.transitions['a'] == t

def test_create_with_transitions():
    q0 = State()
    t1 = Transition(q0, 'c', Direction.LEFT)
    t2 = Transition(q0, 'd', Direction.RIGHT)
    q1 = State({'a': t1, 'b' : t2})
    assert q1.transitions['a'] == t1
    assert q1.transitions['b'] == t2

def test_calc():
    q0 = State()
    t1 = Transition(q0, 'a', Direction.RIGHT)
    q1 = State()
    q1.add_transition('b', t1)
    res = q1.calc('b')
    assert res == t1
