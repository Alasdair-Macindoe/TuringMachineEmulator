import pytest
import sys
sys.path.append('.')

from turingmachine import TuringMachine
import runtm

tm = runtm._read_file('examples/parity.txt')

def test_single_1():
    tm.new_tape('1')
    assert tm.begin()

def test_single_0():
    tm.new_tape('0')
    assert tm.begin()

def test_correct_even_pairty():
    tm.new_tape('10010')
    assert tm.begin()

def test_correct_odd_parity():
    tm.new_tape('11001001')
    assert tm.begin()

def test_incorrect_even_parity():
    tm.new_tape('11100')
    assert not tm.begin()

def test_incorrect_odd_parity():
    tm.new_tape('110010')
    assert not tm.begin()

def test_detect_final_bit():
    tm.new_tape('10011') #Should be 1000 - proves it can tell apart the final 1
    assert not tm.begin()
