'''
   Copyright (c) 2014, Joonhee Han.
 
   This file is part of MealyHMM.
   MealyHMM is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
'''

import numpy
from Queue import Queue

class AlphaCalculator:
    def __init__(self, hmm, seq):
        self.hmm = hmm
        self.seq = seq
        self.queue = Queue()
        self.numOfStates = hmm.getNumOfStates()
        self.seqLen = len(seq) + 1
        self.alpha = numpy.zeros( self.numOfStates * self.seqLen ).reshape( self.numOfStates, self.seqLen ) 

    def init_alpha(self):
        self.alpha[0][0] = 1.0
        self.queue.put( self.hmm.getInitialState() )

        while not self.queue.empty():
            state = self.queue.get()

            for successor in self.hmm.getSuccessors(state):
                self.queue.put(successor)
                self.alpha[successor][0] = self.alpha[state][0] * self.hmm.getEpsilonTranProb(state,successor)

    def calc_alpha(self):
        for t in range(1, self.seqLen):
            self.queue.put( self.hmm.getInitialState() )

            while not self.queue.empty():
                state = self.queue.get()

                # self transition (horizontal move)
                self.alpha[state][t] += self.alpha[state][t-1] * self.hmm.getObsProb(state, state, self.seq[t-1]) * self.hmm.getTranProb(state, state)

                for predecessor in self.hmm.getPredecessors(state):
                    # diagonal move
                    self.alpha[state][t] += self.alpha[predecessor][t-1] * self.hmm.getObsProb(predecessor, state, self.seq[t-1]) * self.hmm.getTranProb(predecessor, state)

                    # epsilon transition (vertical move)
                    self.alpha[state][t] += self.alpha[predecessor][t] * self.hmm.getEpsilonTranProb(predecessor, state)

                # move to the next state
                for successor in self.hmm.getSuccessors(state):
                    self.queue.put(successor)

    def getAlpha(self):
        self.init_alpha()
        self.calc_alpha()
        return self.alpha

