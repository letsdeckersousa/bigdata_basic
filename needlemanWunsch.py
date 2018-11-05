#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 15:08:05 2017

@author: Leticia Decker de Sousa
@university: UNIBO
@email: leticia.decker.sousa@gmail.com

This implementation can be shared and modified without restrictions. 

Implementation of Needleman Wunsch algorithm:
    - the score matrix as dictionary and
    - a matrix of list (value of match, direction) to find the best alignment - that is the matrix
    has 3 dimension: it's a matrix (list of list) and the each element is also a list with a value of 
    match and the corresponding direction that this value comes from.
    
Tested with the prof example.The trace part isn't tested.

"""
##############
#definitions:#
##############

defaultValueScore = 0
d                 = 2
filePath          ="./subMatrix.txt" # if you had saved the subMatrix.txt in another path, please change this. Here I suppose this file is in the same folder of this program.
seq1 = "ACCA"
seq2 = "ACTGG"

#step 1
def createMatrix(n, m):
    f    = [] #final matrix
    elem = [defaultValueScore, ['B']]
    for i in range(n): #lines
        line = []
        for j in range(m): #collunms
            line.append(elem[:])
        f.append(line[:])
        del(line)
    return f

#step 2
def matrixInicialization (f, d):
    for j in range(1, len(f[0])): #first line inicialization
        f[0][j][0] = f[0][j-1][0]-d
        f[0][j][1] = ['L']
    
    for i in range(1, len(f)): #first collumn inicialization
        f[i][0][0] = f[i-1][0][0]-d 
        f[i][0][1] = ['A']    

    return f

#step 3 - matrix of scores
def substitutionMatrixAsDictionary(filePath):
    subM   = {}
    labels = []
    _file = open(filePath)
    for line in _file:
        line = line.rstrip()
        l = line.split(',')[:]
        if l[1].isalpha():
            labels = l[1:]
        else:
            for j in range(1,len(l)):
                if is_number(l[j]):
                    subM[l[0],labels[j-1]] = l[j]
                    #cambis
                    subM[labels[j-1],l[0]] = l[j]
    return subM

#step 4
#evaluate the 3 possibilities to check which one is bigger
def evaluate_above(i, j, d, f): #with gaps in the sequence 2
    return f[i-1][j][0]-d
    
def evaluate_left(i, j, d, f): #with gaps in the sequence 1
    return f[i][j-1][0]-d
    
def evaluate_match(i, j, score, seq1, seq2): #without gaps        
    return f[i-1][j-1][0] + int(score[seq1[i-1], seq2[j-1]])

#step 5
def maximum(i, j, d, f, score, seq1, seq2):
    valuesEvaluate = {}  
    resultValues   = {}
    directions     = []
    valuesEvaluate['A']  = evaluate_above(i, j, d, f)
    valuesEvaluate['L']  = evaluate_left(i, j, d, f)
    valuesEvaluate['D'] = evaluate_match(i, j, score, seq1, seq2)
    resultValues['maxV']  = max(valuesEvaluate['A'], valuesEvaluate['L'], 
                                valuesEvaluate['D'])
    for i in valuesEvaluate.keys():
        if valuesEvaluate[i] == resultValues['maxV']:
             directions.append(i)
    resultValues['directions'] = directions
    return resultValues

#step 6
def atualizeMatrix(d, f, score, seq1, seq2):
    for i in range(1, len(f)):
        for j in range(1, len(f[0])):        
            possibleAlignments = maximum(i, j, d, f, score, seq1, seq2)
            f[i][j][0] = possibleAlignments['maxV']
            f[i][j][1] = possibleAlignments['directions']
    return f

#step 7
def evaluateBestScoreAlignments(d, f, score, seq1, seq2):
    for i in range(1, len(f)): # lines
        for j in range(1, len(f[0])): #collunms
            f = atualizeMatrix(i, j, d, f, score, seq1, seq2)
    return f

#step 8
def getTheBestAlignmentValue(f):
    return f[-1][-1]

#step 9
def getTheBestAlignments_BruteForceSearch(f, seq1, seq2):
    #alignmentDic  = {}
    #alignmentList = []
    stack         = []
    i = len(f)
    j = len(f[0])
    stack.append([])
    alignment = [seq1[i], seq2[j]]

    while f[i][j][1] != 'B' and len(stack) > 1:
        if len(f[i][j][1]) > 1:
            stack.append([i, j])
        if f[i][j][1][0] == 'D':
           alignment.append([seq1[i], seq2[j]]) 
        elif f[i][j][1][0] == 'A':
            alignment.append([seq1[i], '-'])
        elif f[i][j][1][0] == 'L':   
            alignment.append(['-', seq2[j]])
        #while len(lastPosition(stack)) != 0:
            #tira o primeiro
            #faz caminho alualizando i's e j's 
                #se tem alguem que tem mais de um caminho empilha
        #desempilha stack
        return
   

#prof version
def trace(s1, s2, T):
    align_s1 = ""          
    align_s2 = ""
    i  = len(s1)
    j  = len(s2)
    while i>0 or j>0:
        c, d = T[i][j]
        if c==i-1 and d==j-1: #diagonal
            align_s1 = s1[i-1] + align_s1
            align_s2 = s2[j-1] + align_s2
        elif c==i-1 and d== j: #up
            align_s1 = s1[i-1] + align_s1
            align_s2 ="-"      + align_s2
        else: #left
            align_s1 = "-"    + align_s1
            align_s2 = s2[j-1]+ align_s2
        
        temp = 1
        i = T[i][j][0]
        j = T[temp][j][0]     
    return (align_s1, align_s2)

def trace_version2(s1, s2, T):
    align_s1 = ""          
    align_s2 = ""
    i  = len(s1)
    j  = len(s2)
    while i>0 or j>0:
        if T[i][j] == 'D': #diagonal
            align_s1 = s1[i-1] + align_s1
            align_s2 = s2[j-1] + align_s2
            i=i-1  
            j=j-1
        elif T[i][j] == 'U': #up
            align_s1 = s1[i-1] + align_s1
            align_s2 ="-"      + align_s2
            i=i-1  
        else: #left
            align_s1 = "-"    + align_s1
            align_s2 = s2[j-1]+ align_s2
            j = j-1  
    return (align_s1, align_s2)

#####################
#Auxiliar functions:#
#####################
def lastPosition(s):
    return s[len(s)]        

def getTheBestAlignments(f):
    #alignments = []
    alignment  = []
    for i in range(len(f), 0, -1):
        for j in range(len(f[0]), 0, -1):
            if len(f[i][j][1]) == 1:    
                alignment.append(f[i][j][1])
            #else: #more than one alignment


def printMatrix(f):
    for i in f:
       print i
    return

def printDictionary(d):
    for i in d.keys():
        print i,":", d[i], ";",
    print 
    print
    return

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
    

###############    
#Main Program:#
###############

f    = createMatrix(len(seq1)+1, len(seq2)+1)
#printMatrix(f) 
#print 
f = matrixInicialization(f, d)
#printMatrix(f) 
#print
subM = substitutionMatrixAsDictionary(filePath)
printDictionary(subM) 
atualizeMatrix(d, f, subM, seq1, seq2)
printMatrix(f) 


