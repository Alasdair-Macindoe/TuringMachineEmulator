import pytest
import sys
sys.path.append('.')

from turingmachine import Transition, Direction, State, TuringMachine

def test_init():
    s1 = State()
    s2 = State()
    tm = TuringMachine("ab", s1, s2, s1)
    assert tm.tape == ['a', 'b', '_']
    assert tm.accept_state == s1
    assert tm.reject_state == s2
    assert tm.current_state == s1

def test_updating():
    s1 = State()
    s2 = State()
    t = Transition(s2, 'b', Direction.RIGHT)
    s1.add_transition('a', t)
    tm = TuringMachine("acd", s1, s2, s1)
    assert tm.tape == ['a', 'c', 'd', '_']
    tm._read('a')
    assert tm.tape[0] == 'b'
    assert tm.current_state == s2

def test_tape_never_negative():
    s1 = State()
    s2 = State()
    t = Transition(s2, 'b', Direction.LEFT)
    s1.add_transition('a', t)
    tm = TuringMachine("acd", s1, s2, s1)
    assert tm.tape == ['a', 'c', 'd', '_']
    tm._read('a')
    assert tm.tape[0] == 'b'
    assert tm.current_state == s2
    assert tm.tape_position == 0

def create_example_from_spec():
    q0 = State()
    q1 = State()
    qa = State()
    qr = State()
    q0.create_transition('a', q0, 'a', Direction.RIGHT)
    q0.create_transition('b', q1, 'b', Direction.RIGHT)
    q0.create_transition('_', qr, '_', Direction.LEFT)
    q1.create_transition('a', qr, 'a', Direction.LEFT)
    q1.create_transition('b', qr, 'a', Direction.LEFT)
    q1.create_transition('_', qa, 'b', Direction.LEFT)
    return q0, q1, qa, qr

def test_example_spec_aab_manually():
    q0, q1, qa, qr = create_example_from_spec()
    tm = TuringMachine('aab', qa, qr, q0)
    assert tm.tape == ['a', 'a', 'b', '_']
    #tm.begin()
    tm._read('a')
    assert tm.tape_position == 1
    assert tm.current_state == q0
    tm._read('a')
    assert tm.tape_position == 2
    assert tm.current_state == q0
    tm._read('b')
    assert tm.tape_position == 3
    assert tm.tape == ['a', 'a', 'b', '_']
    assert tm.current_state == q1
    tm._read('_')
    assert tm.tape_position == 2
    assert tm.tape == ['a', 'a', 'b', 'b', '_']
    assert tm.current_state == qa
    assert tm.accept()

def test_example_spec_aab():
    q0, q1, qa, qr = create_example_from_spec()
    tm = TuringMachine('aab', qa, qr, q0)
    assert tm.begin()

def test_example_spec_aba():
    q0, q1, qa, qr = create_example_from_spec()
    tm = TuringMachine('aba', qa, qr, q0)
    assert tm.begin() == False

def test_updating_tape():
    q0, q1, qa, qr = create_example_from_spec()
    tm = TuringMachine("aab", qa, qr, q0)
    assert tm.begin()
    tm.new_tape("aba")
    assert tm.begin() is False
