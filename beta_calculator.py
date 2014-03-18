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

class BetaCalculator:
    def __init__(self, hmm, seq):
        self.hmm = hmm
        self.seq = seq
        self.queue = Queue()
        self.numOfStates = hmm.getNumOfStates()
        self.initialState = hmm.getInitialState()
        self.beta = numpy.zeros( self.numOfStates * (len(self.seq)+1) ).reshape( self.numOfStates, (len(self.seq)+1) )

    def init_beta(self):
        final_state = self.hmm.getFinalState()
        self.beta[final_state][len(self.seq)] = 1.0
        self.queue.put( final_state )

        while not self.queue.empty():
            state = self.queue.get()

            for predecessor in self.hmm.getPredecessors(state):
                if predecessor != state:
                    self.queue.put(predecessor)
                    self.beta[predecessor][len(self.seq)] += self.beta[state][len(self.seq)] * self.hmm.getEpsilonTranProb(predecessor, state)

    def calc_beta(self):
        for t in range( len(self.seq)-1, -1, -1):
            self.queue.put( self.hmm.getFinalState() )
                    
            while not self.queue.empty():
                state = self.queue.get()

                for successor in self.hmm.getSuccessors(state):
                    # diagonal or horizontal move
                    self.beta[state][t] += self.beta[successor][t+1] * self.hmm.getObsProb(state, successor, self.seq[t]) * self.hmm.getTranProb(state, successor)

                    # vertical move
                    self.beta[state][t] += self.beta[successor][t] * self.hmm.getEpsilonTranProb(state, successor)

                # move to the next state
                for predecessor in self.hmm.getPredecessors(state):
                    if state != predecessor and predecessor != self.initialState:
                        self.queue.put(predecessor)

            # initial state is calculated lastly because it cannot be computed until its successors are calculated.
            for successor in self.hmm.getSuccessors( self.initialState ):
                self.beta[self.initialState][t] += self.beta[successor][t+1] * self.hmm.getObsProb(self.initialState, successor, self.seq[t]) * self.hmm.getTranProb(self.initialState, successor)
                self.beta[self.initialState][t] += self.beta[successor][t] * self.hmm.getEpsilonTranProb(self.initialState, successor)
            

    def getBeta(self):
        self.init_beta()
        self.calc_beta()
        return self.beta
