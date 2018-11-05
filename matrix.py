#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 11:41:40 2018

@author: Leticia Decker de Sousa
@university: UNIBO
@email: leticia.decker.sousa@gmail.com

This implementation can be shared and modified without restrictions. 

*** Matrix ***
Operations:
    1. createMatrix (n - # of Lines, m - # of Collunms, defaultValue)
    2. atualiseValueIntoMatrix (m - the Matrix, i - index of line, j - index of collunm, newValue)
    3. getValueFromMatrix(m - the Matrix, i - index of line, j - index of collunm):
    4. printMatrix(m - the Matrix)
    5. stringToMatrix(m- the Matrix)    
"""
# 1.
def createMatrix(n, m, defaultValue):
    f    = [] #final matrix
    elem = defaultValue
    for i in range(n): #lines
        line = []
        for j in range(m): #collunms
            line.append(elem)
        f.append(line[:])
        del(line)
    return f

#2.
def atualiseValueIntoMatrix(m, i, j, newValue):
    m[i][j] = newValue
    return m

#3.
def getValueFromMatrix(m, i, j):
    return m[i][j]

#4.
def printMatrix(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            print m[i][j],
        print
    print
    return


#5.
def stringToMatrix(m):
    stringMatrix=""
    for i in range(len(m)):
        for j in range(len(m[0])):
            stringMatrix += str(m[i][j])
        stringMatrix += "\n"
    stringMatrix += "\n"
    return stringMatrix

