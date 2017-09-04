import pytest
import sys
sys.path.append('.')

from turingmachine import Transition, Direction, State
state = State()

def test_creation():
    t = Transition(state, 'a', Direction.RIGHT)
    assert t.new_state == state
    assert t.output_letter == 'a'
    assert t.movement_direction == Direction.RIGHT

def test_malformed_creation():
    with pytest.raises(ValueError):
        t = Transition(None, 'a', Direction.LEFT)
    with pytest.raises(ValueError):
        t2 = Transition(state, None, Direction.RIGHT)
    with pytest.raises(ValueError):
        t3 = Transition(state, 'a', 'c')
