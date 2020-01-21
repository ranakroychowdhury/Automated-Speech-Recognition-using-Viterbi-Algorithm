# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 00:24:46 2019

@author: Ranak Roy Chowdhury
"""
import numpy as np
import math
from matplotlib import pyplot
from matplotlib.pyplot import figure


def readFiles():
    with open("observations.txt", "r") as file:
        data = [int(x) for x in file.read().split()]
        
    with open("initialStateDistribution.txt", "r") as file:
        prior = [float(line) for line in file]
        
    with open("transitionMatrix.txt", "r") as file:
        transition = [[float(x) for x in line.split()] for line in file]
    
    with open("emissionMatrix.txt", "r") as file:
        emission = [[float(x) for x in line.split()] for line in file]

    return data, prior, transition, emission


def backtrack(tracker, temp_prob, length):
    tag_sequence = []
    m = max(temp_prob)
    idx = temp_prob.index(m)
    tag_sequence.append(idx)
    
    for i in range(length, 0, -1):
        idx = tracker[i-1][idx]
        tag_sequence.append(idx)
        
    tag_sequence = tag_sequence[ : : -1]
    return tag_sequence
    

def mapping(tag_sequence):
    char_sequence = []
    for i in range(len(tag_sequence)):
        if tag_sequence[i] < 26:
            char_sequence.append(chr(97 + tag_sequence[i]))
        else:
            char_sequence.append(' ')
    
    s = ''
    s = s.join(char_sequence)
    return s

    
def HMM(data, prior, transition, emission):
    prob = []
    if data[0]:
        init = [(math.log(prior[i]) + math.log(emission[i][1])) for i in range(len(prior))]
    else:
        init = [(math.log(prior[i]) + math.log(emission[i][0])) for i in range(len(prior))]
    prob.append(init)
    
    tracker = []
    for i in range(1, len(data)):
        temp_prob = []
        temp_tracker = []
        for j in range(len(prior)):
            l = [prob[i - 1][k] + math.log(transition[j][k]) for k in range(len(prior))]
            m = max(l)
            if data[i]:
                temp_prob.append(m + math.log(emission[j][1]))
            else:
                temp_prob.append(m + math.log(emission[j][0]))
            idx = l.index(m)
            temp_tracker.append(idx)
        prob.append(temp_prob)
        tracker.append(temp_tracker)
    
    tag_sequence = backtrack(tracker, temp_prob, len(data)-1)
    string = mapping(tag_sequence)
    return tag_sequence, string


def writeResult(string):
    text_file = open("result.txt", "wt")
    text_file.write(string)
    text_file.close()
    

def plotGraph(length, tags):
    fig = pyplot.gcf()
    fig.set_size_inches(20, 15)
    x = list(range(length))
    pyplot.plot(x, tags)
    pyplot.show()    
    
    
if __name__ == "__main__":
    print("Reading Files")
    data, prior, transition, emission = readFiles()
    print("Building HMM")
    tag_sequence, string = HMM(data, prior, transition, emission)
    writeResult(string)
    plotGraph(len(data), tag_sequence)