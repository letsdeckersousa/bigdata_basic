#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 11:20:55 2018

@author: Leticia Decker de Sousa
@university: UNIBO
@email: leticia.decker.sousa@gmail.com

This implementation can be shared and modified without restrictions. 

HMM - algorithms
1. Forward  - tested with prof example
2. Backward - tested with prof example
3. Viterbi  - there is an error on prof slides - so I'm not sure if works well.
4. A Posteriori decoding - not tested

if you test these, let me know if it works well.

"""
import matrix
import graph

# write in file
def writeFile(filename, stringtowrite):
    newFile = open(filename, "w")
    newFile.write(stringtowrite)
    newFile.close() 
    return  "Done"

# entrances
seq = "-ATGCG-"
states = {"0", "Y", "N", "0"} #0 is the states of begin and end. 
# TO DEBUGG the algorithm uncomment the prints
#1. Forward algorith
def forward(seq, filenameEmission, filenameTransmission):
    forwardGraph = graph.createGraph(filenameEmission, filenameTransmission)
    #print forwardGraph
    char = seq[1]
    states = forwardGraph["E"]["E","States"]
    statesCompl = states[:]
    statesCompl.insert(0, "0")
    statesCompl.append("0")
    statesCompl = ["0", "Y", "N", "0"]
    print statesCompl
    
    m = matrix.createMatrix(len(states)+2, len(seq), 0)
    # intialisation part
    matrix.atualiseValueIntoMatrix(m, 0, 0, 1)
    # recurrence part
    # recurrence 1
    for i in range(1,len(m)-1):
        m[i][1] = float(forwardGraph["A"]["0",statesCompl[i]])*float(forwardGraph["E"][statesCompl[i], char])
    # recurrence 2
    for j in range(2, len(m[0])-1): #jump the first 2 collumns
        char = seq[j]
        for i in range(1,len(m)-1): # jump the begin and end states
            for l in range(1,len(m)-1):
                #print "L:",statesCompl[l],", K:",statesCompl[i]
                m[i][j] += float(m[l][j-1])*float(forwardGraph["A"][statesCompl[l],statesCompl[i]])*float(forwardGraph["E"][statesCompl[i],char])
                '''print "partial value: ",float(m[i][j])
                print "lines value:", float(m[l][j-1])
                print "AKL: ",float(forwardGraph["A"][statesCompl[l],statesCompl[i]])
                print "Elc: ", float(forwardGraph["E"][statesCompl[i],char])'''           
    for i in range(1,len(m)-1):
        m[len(m)-1][len(m[0])-1] += float(m[i][len(m[0])-2])*float(forwardGraph["A"][statesCompl[i],"0"])
    matrix.printMatrix(m)
    return m

# 2. Backward algorithm
def backward(seq, filenameEmission, filenameTransmission):
    backwardGraph = graph.createGraph(filenameEmission, filenameTransmission)
    #print backwardGraph
    char = seq[len(seq)-2]
    states = backwardGraph["E"]["E","States"]
    statesCompl = states[:]
    statesCompl.insert(0, "0")
    statesCompl.append("0")
    seq = seq[:-1]
    m = matrix.createMatrix(len(states)+2, len(seq), 0)
    # intialisation part
    # the final state
    for i in range(1,len(m)-1):        
        m[i][len(m[0])-1] = float(backwardGraph["A"][statesCompl[i],"0"])
    #matrix.printMatrix(m)
    # recurrence 
    for j in range(len(m[0])-2, 0, -1): #jump the first 2 collumns
        char = seq[j+1]
        #print "char:", char
        for i in range(1,len(m)-1): # jump the begin and end states
            for l in range(len(m)-2, 0,-1):
                #print "L:",statesCompl[l],", K:",statesCompl[i]
                m[i][j] += float(m[l][j+1])*float(backwardGraph["A"][statesCompl[i],statesCompl[l]])*float(backwardGraph["E"][statesCompl[l],char])
                ''' print "partial value: ",float(m[i][j])
                print "lines value:", float(m[l][j+1])
                print "Alk: ",float(backwardGraph["A"][statesCompl[i],statesCompl[l]])
                print "Elc: ", float(backwardGraph["E"][statesCompl[l],char])'''
    for l in range(1,len(m)-1):
        m[0][0] += float(m[l][1])*float(backwardGraph["A"]["0",statesCompl[l]])*float(backwardGraph["E"][statesCompl[l],seq[1]])
        '''print "psm: ",psm
        print "lines value:", float(m[l][j+1])
        print "Alk: ",float(backwardGraph["A"]["0",statesCompl[l]])
        print "Elc: ", float(backwardGraph["E"][statesCompl[l],seq[1]])
        print "Char: ", seq[1]'''
    #matrix.printMatrix(m)
    return m

#3. Viterbi algorith
def viterbi(seq, filenameEmission, filenameTransmission):
    forwardGraph = graph.createGraph(filenameEmission, filenameTransmission)
    #print forwardGraph
    char = seq[1]
    states = forwardGraph["E"]["E","States"]
    statesCompl = states[:]
    statesCompl.insert(0, "0")
    statesCompl.append("0")
    m     =  matrix.createMatrix(len(states)+2, len(seq), 0)
    trace =  matrix.createMatrix(len(states)+2, len(seq), -1)
    # intialisation part
    matrix.atualiseValueIntoMatrix(m, 0, 0, 1)
    # recurrence part
    # recurrence 1
    trace[1][1]= trace[2][1] = 0
    for i in range(1,len(m)-1):
        m[i][1] = float(forwardGraph["A"]["0",statesCompl[i]])*float(forwardGraph["E"][statesCompl[i], char]) 
    # recurrence 2
    for j in range(2, len(m[0])-1): #jump the first 2 collumns
        char = seq[j]
        for i in range(1,len(m)-1): # jump the begin and end states
            scores = []
            for l in range(1,len(m)-1):
                #print "L:",statesCompl[l],", K:",statesCompl[i]
                scores.append(float(m[l][j-1])*float(forwardGraph["A"][statesCompl[l],statesCompl[i]])*float(forwardGraph["E"][statesCompl[i],char])) 
                '''print "partial value: ",scores[-1]
                print "lines value:", float(m[l][j-1])
                print "AKL: ",float(forwardGraph["A"][statesCompl[l],statesCompl[i]])
                print "Elc: ", float(forwardGraph["E"][statesCompl[i],char])'''
                
            m[i][j] = max(scores)
            #print "Max: ", scores.index(max(scores))+1
            trace[i][j] = scores.index(max(scores))+1
            #print (m[i][j])
            #print "---------------------------------"
            del(scores)
    scores =[]
    for i in range(1,len(m)-1):
        scores.append(float(m[i][len(m[0])-2])*float(forwardGraph["A"][statesCompl[i],"0"]))
    m[len(m)-1][len(m[0])-1] = max(scores)
    trace[len(m)-1][len(m[0])-1] = scores.index(max(scores))+1
    #print "__________________________"
    #matrix.printMatrix(m)
    #matrix.printMatrix(trace)
    return trace

def giveViterbiTrace(trace):
    path =[]
    path.append(trace[-1][-1])
    nextPos = trace[-1][-1]
    for j in range(len(trace[0])-2, 0, -1):
        path.append(trace[nextPos][j])
        nextPos = trace[nextPos][j]
    return path
    
        
def aPosterioriDecoding(seq, fileNameEmis, fileNameTrans):
     statesGraph = graph.createGraph(fileNameEmis, fileNameTrans) # it's a dictionary
     f           = forward(seq, fileNameEmis, fileNameTrans)
     b           = backward(seq, fileNameEmis, fileNameTrans)
     seq         = seq[1:-1]
     psm         = f[len(f)-1][len(f[0])-1] 
     pi          = matrix.createMatrix(len(statesGraph["A"]["A","States"]), len(seq), 0.)
     print "F:"
     matrix.printMatrix(f)
     print "B:"
     matrix.printMatrix(b)
     print "Seq:", seq
     print "Size of Seq: ", len(seq)
     
     for i in range(len(seq)): #pi(i) -> position in the sequence = collunms
         scores = []
         for k in range(1, len(statesGraph["A"]["A","States"])): #num of states that produce chars = lines
             scores.append((f[k][i+1]*b[k][i+1])/psm)
         pi[0][i] = scores.index(max(scores))+1 #states are from 1 to lines-1
         pi[1][i] = scores[0]
         pi[2][i] = scores[1]
         
         del(scores)
     return pi
         
# To test, please, uncomment what you want to test:
filename = "output.txt"
stringtowrite="method: aPosterioriDecoding \n"
#m = forward(seq, "probabilityEmission.txt", "probabilityTransmission.txt")    
#print backward(seq, "probabilityEmission.txt", "probabilityTransmission.txt")
#trace = viterbi(seq, "probabilityEmission.txt", "probabilityTransmission.txt")
#print trace
#print giveViterbiTrace(trace)
apd = aPosterioriDecoding(seq, "probabilityEmission.txt", "probabilityTransmission.txt")
matrix.printMatrix(apd)
stringtowrite += matrix.stringToMatrix(apd)
writeFile(filename, stringtowrite)
            
    
