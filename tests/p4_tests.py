import pytest
import sys
sys.path.append('.')

from turingmachine import TuringMachine
import runtm

tm = runtm._read_file('examples/logic.txt')

def test_regular_accept():
    tm.new_tape('$1|1=1')
    assert tm.begin()
    tm.new_tape("$1|1=1")
    assert tm.begin()
    tm.new_tape("$1|1=1")
    assert tm.begin()
    tm.new_tape('$1^0=1')
    assert tm.begin()
    tm.new_tape('$0^1=1')
    assert tm.begin()
    tm.new_tape('$1|1=1')
    assert tm.begin()
