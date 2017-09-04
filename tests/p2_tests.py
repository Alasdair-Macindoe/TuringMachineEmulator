import pytest
import sys
sys.path.append('.')

from turingmachine import TuringMachine
import runtm

tm = runtm._read_file('examples/bword.txt')

def test_examples_from_spec():
    tm.new_tape('0#0#0')
    assert tm.begin()
    tm.new_tape('01#1#11')
    assert tm.begin()

def test_carry():
    tm.new_tape('1#1#01')
    assert tm.begin()
