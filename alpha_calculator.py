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
        self.finalState = hmm.getFinalState()
        self.alpha = numpy.zeros( self.numOfStates * (len(self.seq)+1) ).reshape( self.numOfStates, (len(self.seq)+1) ) 

    def init_alpha(self):
        self.alpha[0][0] = 1.0
        self.queue.put( self.hmm.getInitialState() )

        while not self.queue.empty():
            state = self.queue.get()

            for successor in self.hmm.getSuccessors(state):
                if successor != state:
                    self.queue.put(successor)
                    self.alpha[successor][0] += self.alpha[state][0] * self.hmm.getEpsilonTranProb(state,successor)


    def calc_alpha(self):
        for t in range(1, len(self.seq)+1):
            self.queue.put( self.hmm.getInitialState() )

            while not self.queue.empty():
                state = self.queue.get()

                for predecessor in self.hmm.getPredecessors(state):
                    # diagonal or horizontal move
                    self.alpha[state][t] += self.alpha[predecessor][t-1] * self.hmm.getObsProb(predecessor, state, self.seq[t-1]) * self.hmm.getTranProb(predecessor, state)

                    # epsilon transition (vertical move)
                    self.alpha[state][t] += self.alpha[predecessor][t] * self.hmm.getEpsilonTranProb(predecessor, state)

                # move to the next state
                for successor in self.hmm.getSuccessors(state):
                    if state != successor and successor != self.hmm.getFinalState():
                        self.queue.put(successor)

            # final state is calculated lastly because it cannot be computed until its predecessors are calculated.
            for predecessor in self.hmm.getPredecessors( self.finalState ):
                self.alpha[self.finalState][t] += self.alpha[predecessor][t-1] * self.hmm.getObsProb(predecessor, self.finalState, self.seq[t-1]) * self.hmm.getTranProb(predecessor, self.finalState)
                self.alpha[self.finalState][t] += self.alpha[predecessor][t] * self.hmm.getEpsilonTranProb(predecessor, self.finalState)

    def getAlpha(self):
        self.init_alpha()
        self.calc_alpha()
        return self.alpha

