"""
===============================================================================
This file manages the Turing Machine, its states and its transitions
===============================================================================
"""

from enum import Enum, unique

@unique
class Direction(Enum):
    """ Defines the RIGHT and LEFT movement for the tape head """
    LEFT = -1
    RIGHT = +1

    def convert(input):
        if input == 'R' or input == 'r':
            return Direction.RIGHT
        if input == 'L' or input == 'l':
            return Direction.LEFT
        return None

class State():
    """
    Manages each individual state, for example q0, q1, qr and qa are all states
    given in the practical specification
    """
    #This is a dictionary containing the transition class and indexed
    #by the character which causes that transition
    transitions = None

    def __init__(self, transitions=None):
        if transitions == None:
            self.transitions = {}
        else:
            self.transitions = transitions

    def create_transition(self, character, new_state, output, direction):
        """ Creates a new transition to this State """
        assert self.transitions != None
        self.transitions[character] = Transition(new_state, output, direction)

    def add_transition(self, character, transition):
        """ Adds an already created transition to this State """
        assert self.transitions != None
        self.transitions[character] = transition

    def calc(self, character):
        """
        Calculate the new state of the machine after a character.
        Returns the transition object which contains a 3-tuple of:
        The new state, the output letter and the direction to move on
        the tape
        """
        return self.transitions[character]



class Transition():
    """
    Defines a transition, eg q0 a q0 a R.
    This means when in q0 and an a is read we move to q0 and output an a
    then move right on the tape.
    Here we only need to store the new state, the output character and the
    movement direction
    """
    new_state = None
    output_letter = None
    movement_direction = None

    def __init__(self, new_state, output_letter, movement_direction):
        """
        Only allows creation of a potentially valid transition
        eg q0 a R is potentially valid, but
        None, None, Q is not valid
        """
        if new_state == None or type(new_state) is not State:
            raise ValueError("New state must be a State!")
        self.new_state = new_state

        if output_letter == None:
            raise ValueError("Output letter cannot be None")
        self.output_letter = output_letter

        if movement_direction == None or not isinstance(movement_direction, Direction):
            raise ValueError("The direction of movement must be L or R")
        self.movement_direction = movement_direction

class TuringMachine():
    """
    Represents the entire TuringMachine including all states, all
    inputs, all outputs and the tape itself.
    Recall that states themselves hold their transitions so we do not need
    to duplicate all the transitions in the machine itself. All we need
    to store here is the current state, and a way to test if it is accepted,
    rejected or still on going.
    """
    #The tape is a list of characters
    tape = None
    tape_position = 0
    #Accept and reject are just the names of the states.
    #States are unique - they form a set
    accept_state = None
    reject_state = None
    #The current state is a state object
    current_state = None
    EMPTY_SYMBOL = None
    MAX_LOOPS = None
    #The following should only be used internally
    _start_state = None
    _reset_loops = None

    def new_tape(self, tape):
        """ Updates the tape to allow experimentation with the TM """
        self._update_tape(tape)
        #Reset to the first start state
        self._update_current_state(self._start_state)
        assert self._reset_loops >= 0
        self.MAX_LOOPS = self._reset_loops

    def _update_tape(self, tape):
        """ Internal method for updating the tape """
        self.tape_position = 0

        if self.tape != None:
            self.tape.clear()
            assert(len(self.tape) == 0)

        if isinstance(tape, list):
            self.tape = [str(c) for c in tape]
        elif type(tape) is str:
            self.tape = [c for c in tape]
        elif type == None:
            self.tape = []
        else:
            raise ValueError("Tape has to be a list of symbols or a String (or Nothing)")
        self.tape.append(self.EMPTY_SYMBOL) #Add one empty symbol to the end


    def _test_state(state):
        """ Internal method for testing potential States """
        if type(state) is not State:
            raise ValueError("States should be a state!")

    def _update_current_state(self, current_state):
        """ Internal method for updating the current_state """
        TuringMachine._test_state(current_state)
        self.current_state = current_state

    def _update_accept_state(self, accept_state):
        """
        Internal method for updating the accept state
        Generally it is advised that this is not changed at once the
        machine has began
        """
        assert accept_state != None
        TuringMachine._test_state(accept_state)
        self.accept_state = accept_state

    def _update_reject_state(self, reject_state):
        """
        Internal method for updating the reject state
        Generally it is advised that this is not changed at once the
        machine has began
        """
        TuringMachine._test_state(reject_state)
        self.reject_state = reject_state

    def _update_start_state(self, start_state):
        """
        Internal method for updating the start state.
        Can only be update ONCE upon CREATION OF THE TM.
        DO NOT UPDATE DURING RUNTIME OR ELSE BAD THINGS COULD HAPPEN.
        """
        assert self._start_state == None
        TuringMachine._test_state(start_state)
        self._start_state = start_state

    def __init__(self, tape, accept, reject, current_state, empty_symbol="_",
                max_loops=100000):
        """
        Creates us a Turing machine with a specific tape, accept state,
        reject state and current_state in this instance acts as the inital
        state
        """
        self.EMPTY_SYMBOL = empty_symbol
        self._update_tape(tape)
        self._update_accept_state(accept)
        self._update_reject_state(reject)
        self._update_current_state(current_state)
        self._update_start_state(current_state)
        self._update_max_loops(max_loops)

    def _update_max_loops(self, n):
        assert n >= 0
        self.MAX_LOOPS = n
        self._reset_loops = n

    def _move_tape(self, symbol, dir):
        """  Updates the tape """
        assert type(dir) is Direction

        self.tape[self.tape_position] = symbol

        #Special case furthest right entry
        if self.tape_position >= len(self.tape) - 1:
            self.tape.append(self.EMPTY_SYMBOL)

        if dir == Direction.RIGHT:
            self.tape_position = self.tape_position + 1
        else:
            if self.tape_position > 0:
                self.tape_position = self.tape_position - 1

    def _read(self, symbol):
        """ Compute the result after the next symbol """
        #Check our infinite loop detection
        self.MAX_LOOPS = self.MAX_LOOPS - 1
        #Special case None to equal our empty character '_'
        #Get the transition
        t = self.current_state.calc(symbol)
        #Update the tape
        self._move_tape(t.output_letter, t.movement_direction)
        #Update the current state
        self._update_current_state(t.new_state)

    def accept(self):
        """ Returns if the TM is in the accept state """
        return self.accept_state == self.current_state

    def reject(self):
        """ Returns if the TM is in the reject state """
        return self.reject_state == self.current_state or self.MAX_LOOPS < 0

    def begin(self):
        """ Begins computation """
        while not self.accept() and not self.reject():
            self._read(self.tape[self.tape_position])
        return self.accept()
