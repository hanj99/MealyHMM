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

class Viterbi:
    def __init__(self, hmm, seq):
        self.hmm = hmm
        self.seq = seq
        self.queue = Queue()
        self.numOfStates = hmm.getNumOfStates()
        self.seqLen = len(seq) + 1
        self.alpha_hat = numpy.zeros( self.numOfStates * self.seqLen ).reshape( self.numOfStates, self.seqLen ) 

    def init_alpha_hat(self):
        self.alpha_hat[0][0] = 1.0
        self.queue.put( self.hmm.getInitialState() )

        while not self.queue.empty():
            state = self.queue.get()

            for successor in self.hmm.getSuccessors(state):
                self.queue.put(successor)
                self.alpha_hat[successor][0] = self.alpha_hat[state][0] * self.hmm.getEpsilonTranProb(state,successor)


    def calc_alpha_hat(self):
        for t in range(1, self.seqLen):
            self.queue.put( self.hmm.getInitialState() )

            while not self.queue.empty():
                state = self.queue.get()
                alpha_hat_list = []

                # self transition (horizontal move)
                alpha_hat_list.append( self.alpha_hat[state][t-1] * self.hmm.getObsProb(state, state, self.seq[t-1]) * self.hmm.getTranProb(state, state) )

                for predecessor in self.hmm.getPredecessors(state):
                    # diagonal move
                    alpha_hat_list.append( self.alpha_hat[predecessor][t-1] * self.hmm.getObsProb(predecessor, state, self.seq[t-1]) * self.hmm.getTranProb(predecessor, state) )

                    # epsilon transition (vertical move)
                    alpha_hat_list.append( self.alpha_hat[predecessor][t] * self.hmm.getEpsilonTranProb(predecessor, state) )

                # take max value only
                self.alpha_hat[state][t] = max(alpha_hat_list)

                # move to the next state
                for successor in self.hmm.getSuccessors(state):
                    self.queue.put(successor)

    def getAlphaHat(self):
        self.init_alpha_hat()
        self.calc_alpha_hat()
        return self.alpha_hat

