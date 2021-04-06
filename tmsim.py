#!/usr/bin/env python

"""
## ################################################################################ ##
## Name:
##            Turing Machine Simulator
##
## Description:
##            Runs a Turing Machine using multiple infinite tapes and one pointer
##            per tape.
##
## Author:
##            Calvin M.T. (calvinmt.com)
## ################################################################################ ##
"""

import sys
import numpy as np

DEBUGGING = False

OPTION_DEBUG = "-d"

MACHINES_DIRECTORY = "machines/"
TAPES_DIRECTORY = "tapes/"

STEP_CURRENT_STATE = 'Q'
STEP_MOVE = 'm'
STEP_NEXT_STATE = 'N'
STEP_READ = 'r'
STEP_WRITE = 'w'

WILDCARD_ALL = '*'
WILDCARD_ALL_BUT_BLANK = '~'

MOVE_LEFT = "L"
MOVE_RIGHT = "R"


# ########## ########## ########## #
# MACHINE STRUCTURE
#
#     <blank_character>
#     <returned_characters>
#     <initial_state>
#     <final_state>
#     <machine_syntax>
#     <machine_rules>
#
# Example:
#
#     B
#     |X
#     q0
#     halt
#     Q r w m N
#     q0 | B R q1
#     q0 B X - halt
#     q1 | | - halt
#     q1 B B - halt
#
# ########## ########## ########## #


def prepareStepIndices(syntax):
    """
    Order the Turing Machine's execution of a rule depending on the given syntax.

    :param syntax: list of characters
    :return: None
    """
    global stepIndexCurrentState
    global stepIndexMove
    global stepIndexNextState
    global stepIndexRead
    global stepIndexWrite
    stepIndexCurrentState = -1
    stepIndexMove = -1
    stepIndexNextState = -1
    stepIndexRead = -1
    stepIndexWrite = -1
    for i in range(len(syntax)):
        step = syntax[i]
        if step == STEP_CURRENT_STATE:
            stepIndexCurrentState = i
        elif step == STEP_MOVE:
            stepIndexMove = i
        elif step == STEP_NEXT_STATE:
            stepIndexNextState = i
        elif step == STEP_READ:
            stepIndexRead = i
        elif step == STEP_WRITE:
            stepIndexWrite = i
        else:
            sys.exit("ERROR: unknown step in syntax (" + syntax[i] + ")")
    if stepIndexCurrentState <= -1 or stepIndexRead <= -1:
        sys.exit("ERROR: syntax needs a current state (" + STEP_CURRENT_STATE + ") and a read (" + STEP_READ + ")")


def readRules(machineFile):
    """
    Read the instance of a Turing Machine file with the file pointer starting on its rules to create a list of rules.

    :param machineFile: Turing Machine file instance
    :return: list of rules
    """
    rules = []
    STATE_NORMAL = 0
    STATE_PARENTHESIS = 1
    state = STATE_NORMAL
    p = 0
    i = -1
    for line in machineFile:
        if len(line) <= 1:
            continue

        i += 1
        line = line.rstrip('\n')
        rules.append([])
        rules[i].append([""])
        step = 0
        for c in line:
            if c == ' ' and state == STATE_NORMAL:
                rules[i].append([""])
                step += 1
            elif c == ' ' and state == STATE_PARENTHESIS:
                continue
            elif c == '(' and state == STATE_NORMAL:
                state = STATE_PARENTHESIS
            elif c == '(' and state == STATE_PARENTHESIS:
                sys.exit("ERROR: nested parentheses not supported in rules")
            elif c == ')' and state == STATE_NORMAL:
                sys.exit("ERROR: nested parentheses not supported in rules")
            elif c == ')' and state == STATE_PARENTHESIS:
                state = STATE_NORMAL
                p = 0
            elif c == ',' and state == STATE_PARENTHESIS:
                rules[i][step].append("")
                p += 1
            else:
                rules[i][step][p] = rules[i][step][p] + c
    return rules


def readTapes(tapeFile):
    """
    Read the instance of a tape file to create a list of tapes and a list of their pointers.

    :param tapeFile: tape file instance
    :return: list of tapes, list of pointers
    """
    pointers = []
    tapes = []
    for line in tapeFile:
        pointers.append(0)
        tapes.append(list(line.rstrip('\n')))
    tapeFile.close()
    return tapes, pointers


def prepareMachine(machinePath, tapePath):
    """
    Read Turing Machine file and tape file to set and initialise blank character, returning characters, initial state,
    final state, rules, pointers and tapes.

    :param machinePath: Turing Machine file
    :param tapePath: tape file
    :return: None
    """
    global blankCharacter
    global returnedCharacters
    global initialState
    global finalState
    global rules
    global pointers
    global tapes
    machineFile = open(machinePath, 'r')
    blankCharacter = machineFile.readline().rstrip('\n')
    returnedCharacters = machineFile.readline().rstrip('\n')
    initialState = machineFile.readline().rstrip('\n')
    finalState = machineFile.readline().rstrip('\n')
    syntax = np.loadtxt(machineFile, dtype='str', max_rows=1, delimiter=' ')
    rules = readRules(machineFile)
    machineFile.close()

    DEBUG("Blank character:\t" + blankCharacter)
    DEBUG("Returned characters:\t" + returnedCharacters)
    DEBUG("Initial state:\t\t" + initialState)
    DEBUG("Final state:\t\t" + finalState)
    DEBUG("Syntax:\t\t\t" + str(syntax))

    prepareStepIndices(syntax)

    tapeFile = open(tapePath, 'r')
    tapes, pointers = readTapes(tapeFile)
    tapeFile.close()


def findStateIndices(state):
    """
    Search through the list of rules for the ones for which their beginning state matches state.

    :param state: beginning state
    :return: list of rule indices
    """
    result = []
    for i in range(len(rules)):
        if rules[i][stepIndexCurrentState][0] == state:
            result.append(i)
    if len(result) == 0:
        sys.exit("ERROR: no state found (" + state + ")")
    return result


def findStateUniqueIndex(state):
    """
    Search through the list of rules for the one for which its beginning state matches current state and its reading
    characters match currently pointed characters from each tape.

    :param state: beginning state
    :return: rule index
    """
    result = -1
    stateIndices = findStateIndices(state)
    for i in stateIndices:
        count = 0
        for j in range(len(tapes)):
            readCharacter = tapes[j][pointers[j]]
            if rules[i][stepIndexRead][j] == readCharacter or \
                    rules[i][stepIndexRead][j] == WILDCARD_ALL or \
                    (rules[i][stepIndexRead][j] == WILDCARD_ALL_BUT_BLANK and readCharacter != blankCharacter):
                count += 1
        if count == len(tapes):
            if result > -1:
                sys.exit("ERROR: non-unique rule (" + state + ", " + str(rules[i][stepIndexRead]) + ")")
            result = i
    if result <= -1:
        characters = []
        for i in range(len(tapes)):
            characters.append(tapes[i][pointers[i]])
        sys.exit("ERROR: no rule found (" + state + ", " + str(characters) + ")")
    return result


def runRule(currentState):
    """
    Run a single rule for which its beginning state matches current state and its read characters match currently
    pointed characters from each tape.

    :param currentState: beginning state
    :return: next state
    """
    global pointers
    nextState = currentState
    currentStateIndex = findStateUniqueIndex(currentState)
    for i, tape in enumerate(tapes):
        if stepIndexWrite > -1:
            if rules[currentStateIndex][stepIndexWrite][i] != WILDCARD_ALL and \
                    rules[currentStateIndex][stepIndexWrite][i] != WILDCARD_ALL_BUT_BLANK:
                tape[pointers[i]] = rules[currentStateIndex][stepIndexWrite][i]
        if stepIndexMove > -1:
            stepMove = rules[currentStateIndex][stepIndexMove][i]
            if stepMove == MOVE_LEFT:
                pointers[i] -= 1
                if pointers[i] == -1:
                    tape.insert(0, blankCharacter)
                    pointers[i] = 0
            if stepMove == MOVE_RIGHT:
                pointers[i] += 1
                if pointers[i] == len(tape):
                    tape.append(blankCharacter)
        if stepIndexNextState > -1:
            nextState = rules[currentStateIndex][stepIndexNextState][0]
    return nextState


def computeResult():
    """
    Count the number of returning characters for each tape.

    :return: None
    """
    if len(returnedCharacters) > 0:
        for i in range(len(tapes)):
            print("Tape", i)
            for r in returnedCharacters:
                counter = 0
                for c in tapes[i]:
                    if c == r:
                        counter += 1
                print("\t", r, ":", counter)


def runMachine():
    """
    Run the prepared Turing Machine.

    :return: None
    """
    currentState = initialState
    while currentState != finalState:
        DEBUG(STEP_CURRENT_STATE + ": " + currentState + ";\tpointer: " + str(pointers))
        print(tapes)
        currentState = runRule(currentState)
    DEBUG(STEP_CURRENT_STATE + ": " + currentState + ";\tpointer: " + str(pointers))
    print(tapes)
    print("Terminated")


def DEBUG(string):
    if DEBUGGING:
        print(string)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ", sys.argv[0], "[-d] machine_filename tape_filename")
        sys.exit()
    else:
        nbOptions = 0
        if len(sys.argv) >= 4:
            if sys.argv[1] == OPTION_DEBUG:
                DEBUGGING = True
                nbOptions += 1
        machinePath = MACHINES_DIRECTORY + sys.argv[1 + nbOptions]
        tapePath = TAPES_DIRECTORY + sys.argv[2 + nbOptions]
        prepareMachine(machinePath, tapePath)
        runMachine()
        computeResult()
