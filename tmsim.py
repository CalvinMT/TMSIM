#!/usr/bin/env python

## ################################################################################ ##
## Name:
##			Turing Machine Simulator
##
## Description:
##			Runs a Turing Machine using one infinite tape and one pointer.
##
## Author:
##			Calvin M.T. (calvinmt.com)
## ################################################################################ ##

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

MOVE_LEFT = "L"
MOVE_RIGHT = "R"

# ########## ########## ########## #
# MACHINE STRUCTURE
#
# 	<blank_character>
# 	<returned_characters>
# 	<initial_state>
# 	<final_state>
# 	<machine_syntax>
# 	<machine_rules>
#
# Example:
#
# 	B
# 	|X
# 	q0
# 	halt
# 	Q r w m N
# 	q0 | B R q1
# 	q0 B X - halt
# 	q1 | | - halt
# 	q1 B B - halt
#
# ########## ########## ########## #

def initialiseStepIndices():
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

def prepareStepIndices(syntax):
	global stepIndexCurrentState
	global stepIndexMove
	global stepIndexNextState
	global stepIndexRead
	global stepIndexWrite
	initialiseStepIndices()
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
	if stepIndexCurrentState <= -1  or  stepIndexRead <= -1:
		sys.exit("ERROR: syntax needs a current state (" + STEP_CURRENT_STATE + ") and a read (" + STEP_READ + ")")

def prepareMachine(machinePath, tapePath):
	global returnedCharacters
	global initialState
	global finalState
	global rules
	global tapePointer
	global tape
	machineFile = open(machinePath, 'r')
	blankCharacter = machineFile.readline().rstrip('\n')
	returnedCharacters = machineFile.readline().rstrip('\n')
	initialState = machineFile.readline().rstrip('\n')
	finalState = machineFile.readline().rstrip('\n')
	syntax = np.loadtxt(machineFile, dtype='str', max_rows=1, delimiter=' ')
	rules = np.loadtxt(machineFile, dtype='str', delimiter=' ')
	machineFile.close()
	
	DEBUG("Blank character:\t" + blankCharacter)
	DEBUG("Returned characters:\t" + returnedCharacters)
	DEBUG("Initial state:\t\t" + initialState)
	DEBUG("Final state:\t\t" + finalState)
	DEBUG("Syntax:\t\t\t" + str(syntax))
	
	prepareStepIndices(syntax)
	
	tapeFile = open(tapePath, 'r')
	tapePointer = 0
	tape = list(np.loadtxt(tapeFile, dtype='str').item())
	tapeFile.close()

def findStateIndices(state):
	result = []
	for i in range(len(rules)):
		if rules[i][0] == state:
			result.append(i)
	if len(result) == 0:
		sys.exit("ERROR: no state found (" + state + ")")
	return result

def findStateUniqueIndex(state, readCharacter):
	result = -1
	stateIndices = findStateIndices(state)
	for i in stateIndices:
		if rules[i][1] == readCharacter:
			if result > -1:
				sys.exit("ERROR: non-unique rule (" + state + ", " + readCharacter + ")")
			result = i
	if result <= -1:
		sys.exit("ERROR: no rule found (" + state + ", " + readCharacter + ")")
	return result

def runRule(currentState):
	global tapePointer
	nextState = currentState
	readCharacter = tape[tapePointer]
	currentStateIndex = findStateUniqueIndex(currentState, readCharacter)
	if stepIndexWrite > -1:
		tape[tapePointer] = rules[currentStateIndex][stepIndexWrite]
	if stepIndexMove > -1:
		stepMove = rules[currentStateIndex][stepIndexMove]
		if stepMove == MOVE_LEFT:
			tapePointer -= 1
			if tapePointer == -1:
				tape.insert(0, blankCharacter)
				tapePointer = 0
		if stepMove == MOVE_RIGHT:
			tapePointer += 1
			if tapePointer == len(tape):
				tape.append(blankCharacter)
	if stepIndexNextState > -1:
		nextState = rules[currentStateIndex][stepIndexNextState]
	return nextState

def computeResult():
	for r in returnedCharacters:
		counter = 0
		for c in tape:
			if c == r:
				counter += 1
		print r, ":", counter

def runMachine():
	currentState = initialState
	while currentState != finalState:
		DEBUG(STEP_CURRENT_STATE + ": " + currentState + ";\tpointer: " + str(tapePointer))
		print tape
		currentState = runRule(currentState)
	DEBUG(STEP_CURRENT_STATE + ": " + currentState + ";\tpointer: " + str(tapePointer))
	print tape
	print "Terminated"

def DEBUG(string):
	if DEBUGGING:
		print string

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "Usage: ", sys.argv[0], "[-d] machine_filename tape_filename"
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
