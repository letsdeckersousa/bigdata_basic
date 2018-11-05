#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 12:37:46 2018

@author: Leticia Decker de Sousa
@university: UNIBO
@email: leticia.decker.sousa@gmail.com

This implementation can be shared and modified without restrictions. 

the file format of the transmissions is:
.      state1 state2 state3 0
state1 num    num    num    num
state2 num    num    num    num
state3 num    num    num    num 
0      num    num    num    num

The char of separation is blankspace.

the file format of the emission is:
.      char1  char2  char3 
state1 num    num    num    
state2 num    num    num    
state3 num    num    num     

The char of separation is blankspace.

*** Graph as dictionary *** 
The graph is a dictionary with 2 elements: E and A, both also dictionaries. Into E and A, we have:
    - the probs of emissions (charEmission[state, char]) and 
    - the probs of transmissions (transission[fromState1, toState2])
we have also:
    - the number of states of each one (g['A']['A','Size']) and 
    - the state list (g['A']['A','States']).

operations:
    1. createGraph(filenameEmis, filenameTrans)
    2. createMatrixOfTransition(filenameTrans)
    3. createCharEmissionDic(filenameEmis)
    
"""

#1.
def createGraph(fileNameEmis, fileNameTrans):
    hmm = {}
    emission = createCharEmissionDic(fileNameEmis)
    transmission = createMatrixOfTransition(fileNameTrans)
    hmm["E"] = emission
    hmm["A"] = transmission
    return hmm

#2.
def createMatrixOfTransition(filenameTrans):
    trans_file = open(filenameTrans)
    states = trans_file.readline().rstrip().split()[1:] # initial state at position 1
    transitions = {}
    for line in trans_file:
        line = line.rstrip().split() 
        fromState = line[0]
        line = line[1:] # first elem is the char and the rest are the probs
        for i in range(len(line)): 
            transitions[fromState, states[i]] = line[i]
    transitions["A","Size"] = len(states)
    transitions["A","States"] = states
    return transitions

#3.
def createCharEmissionDic(filenameEmis):
    emiss_file = open(filenameEmis)
    states = emiss_file.readline().rstrip().split()[1:] # initial state at position 1
    charEmission = {}
    for line in emiss_file:
        line = line.rstrip().split() 
        char = line[0]
        line = line[1:] # first elem is the char and the rest are the probs
        for i in range(len(line)): 
            charEmission[states[i], char] = line[i]
    charEmission["E","Size"] = len(states)
    charEmission["E","States"] = states
    return charEmission
    
# To test, please, uncomment what you want to test:
    
'''hmm = createGraph("probabilityEmission.txt", "probabilityTransmission.txt")
print "States of emission dic: ", hmm["E"]["E","States"]
print "States of transmission dic: ", hmm["A"]["A","States"]

print
print hmm

em = createCharEmissionDic("probabilityEmission.txt")
t = createMatrixOfTransition("probabilityTransmission.txt")

print t["N", "Y"]
print
print em
print
print t'''
