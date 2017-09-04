import pytest
import sys
sys.path.append('.')

from turingmachine import TuringMachine
import runtm

tm = runtm._read_file('examples/palin.txt')


def test_examples_from_spec():
    tm.new_tape('aba')
    assert tm.begin()
    tm.new_tape('cabbbbac')
    assert tm.begin()
    tm.new_tape('aaaa')
    assert tm.begin()
    tm.new_tape('aab')
    assert not tm.begin()
    tm.new_tape('ac')
    assert not tm.begin()
    tm.new_tape('cabbba')
    assert not tm.begin()

def test_empty_word():
    tm.new_tape('')
    assert tm.begin()

def test_odd_length():
    tm.new_tape('aabaa')
    assert tm.begin()

def test_single_char():
    tm.new_tape('a')
    assert tm.begin()

def test_invalid_alphabet():
    with pytest.raises(KeyError):
        tm.new_tape('d')
        assert tm.begin()
