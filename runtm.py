"""
Note:
    Specialised input which is of the format:
    states s
    <list of s states each on a separate line with an optional + or ->
    alphabet n <n letters of alphabet>
    <arbitary amount of states of form:
        current_state input_letter new_state output_letter move_direction
    >
Turing Machines(TM) are deteministic.
An example input is given in the project specification.
"""

import argparse
import re
import sys
from turingmachine import State, Transition, TuringMachine, Direction
ACCEPT_SYMBOL = "+"
REJECT_SYMBOL = "-"
EMPTY_SYMBOL = '_'

def parse():
    """ Parses the input, eg reads in the file's location and opens it """
    parser = argparse.ArgumentParser(description="Reads Turing Machine input")
    parser.add_argument("-i", "--input", type=str, help="The file \
    containing the input (the valid Turing Machine) in the format declared in\
     the specification", required=True)
    parser.add_argument("-o", "--output", type=str, help="The file where the \
     output should be printed to", default=None) #Default is stdout
    input_location_group = parser.add_mutually_exclusive_group()
    input_location_group.add_argument("-w", "--words", type=str, help="The \
    file containing the words to best tested with this TM.", default=None)
    input_location_group.add_argument("-c", "--console", type=str,
    help="Enable console input", default=None)
    #Parse TM
    args = parser.parse_args()
    tm = _read_file(args.input)
    #Cannot have both a location of the words and console input.
    if args.output != None:
        sys.stdout = open(args.output, 'w')
    if args.words != None:
        with open(args.words, 'r') as f:
            for word in f:
                word = word.replace('\n', "") #Remove trailing new line
                tm.new_tape(word)
                print(word + ", " + str(tm.begin()))
    elif args.console != None:
        tm.new_tape(args.console)
        res = tm.begin()
        print(res)
        return res


def _read_file(file):
    with open(file, 'r') as f:
        #The first line should consist of the word 'state' and  then an integer
        number_states = _parse_state_number(f.readline())
        #The next number_states lines are states
        states, inital_state, accept_state, reject_state = _parse_states(number_states, f)
        #That is then followed by the input alphabet
        alphabet = _parse_alphabet(f.readline())
        #Add the transitions to the states
        _parse_transitions(f, alphabet, states)
        #Add these states to the TM
        return TuringMachine("", accept_state, reject_state, inital_state, EMPTY_SYMBOL)

def _parse_transitions(f, alphabet, states):
    #This should loop for the rest of the lines in the file
    regex = re.compile('(\w*) ([^ \n]*) (\w*) ([^ \n]*) ([RL])')
    for line in f:
        res = regex.match(line)
        #If we get None then we have an invalid line
        if res == None:
            raise InvalidInputFormat("Invalid State! {}".format(line))
        #Otherwise it is of the correct format
        state, input_symbol, new_state, output_symbol, direction = res.groups()
        state = states[state] #Change state to a TM state
        direction = Direction.convert(direction) #Convert to enumeration
        new_state = states[new_state]
        #Ensure input_symbol is in alphabet
        state.create_transition(input_symbol, new_state, output_symbol, direction)

def _parse_alphabet(line):
    #alphabet followed by an integer, followed by a space and then
    #a series of word characters (excl. space) followed by an optional space
    #an arbitary amount of times.
    #This allows us to have more complex alphabets eg ab, cd and not a, b, c, d
    regex = re.compile('(alphabet) (\d*) (([^ \n]* ?)*)')
    res = regex.match(line)
    #Res should contain an res.group(2) worth of words
    words, size = res.group(3).split(" "), int(res.group(2))
    if len(words) != size:
        raise InvalidInputFormat("Size of input alphabet does not match characters")
    #Add empty character if necessary
    if EMPTY_SYMBOL not in words:
        words.append(EMPTY_SYMBOL)
    return words

def _parse_states(number_states, f):
    states = {}
    inital_state = None
    accept_state = None
    reject_state = None
    for i in range(number_states):
        line = f.readline()
        state, symbol = _parse_state(states, line)
        if inital_state == None:
            inital_state = state
        if symbol == ACCEPT_SYMBOL:
            if accept_state != None:
                raise InvalidInputFormat("There can only be one accept state!")
            accept_state = state
        if symbol == REJECT_SYMBOL:
            if reject_state != None:
                raise InvalidInputFormat("There can only be one reject state!")
            reject_state = state
    return states, inital_state, accept_state, reject_state

def _parse_state(dict, line):
    #Match a series of valid word characters, followed by an optional space,
    #and then an optional +-.
    #This accepts 'q0 ' but not 'qa+'
    #These are then split into two groups. The name part and the optional
    #additional information
    regex = re.compile('(\w*) ?([+-]?)')
    res = regex.match(line)
    #Add all states to the dictionary of states
    #Do a small check
    name = res.group(1)
    assert dict != None
    if name in dict:
        raise InvalidInputFormat("Two or more states cannot have the same name")
    dict[name] = State()
    #Special test for reject state and accept state
    #Additional characters will be reject by the regex so not need to test
    return dict[name], res.group(2)

def _parse_state_number(line):
    regex = re.compile('states (\d*)', re.IGNORECASE)
    res = regex.match(line)
    if not res:
        raise InvalidInputFormat("First line is not <states> <integer>")
    return int(res.group(1)) #NOTE: Regex counts from 1.

class InvalidInputFormat(Exception):
    pass

if __name__== "__main__":
    parse()
