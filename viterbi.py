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
        self.alpha_hat = numpy.zeros( self.numOfStates * (len(seq)+1) ).reshape( self.numOfStates, len(seq)+1 ) 
        self.optimal_path = numpy.zeros( self.numOfStates * (len(seq)+1), dtype=int ).reshape( self.numOfStates, len(seq)+1 ) 

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
                optimal_path_list = []

                # self transition (horizontal move)
                alpha_hat_list.append( self.alpha_hat[state][t-1] * self.hmm.getObsProb(state, state, self.seq[t-1]) * self.hmm.getTranProb(state, state) )
                optimal_path_list.append(state)

                for predecessor in self.hmm.getPredecessors(state):
                    # diagonal move
                    alpha_hat_list.append( self.alpha_hat[predecessor][t-1] * self.hmm.getObsProb(predecessor, state, self.seq[t-1]) * self.hmm.getTranProb(predecessor, state) )
                    optimal_path_list.append(predecessor)

                    # epsilon transition (vertical move)
                    alpha_hat_list.append( self.alpha_hat[predecessor][t] * self.hmm.getEpsilonTranProb(predecessor, state) )
                    optimal_path_list.append(predecessor)

                # take max value only
                self.alpha_hat[state][t] = max(alpha_hat_list)
                self.optimal_path[state][t] = optimal_path_list[ alpha_hat_list.index( max(alpha_hat_list) ) ]

                # move to the next state
                for successor in self.hmm.getSuccessors(state):
                    self.queue.put(successor)


    def getAlphaHat(self):
        self.init_alpha_hat()
        self.calc_alpha_hat()
        return self.alpha_hat

    def getMaxFinalState(self):
        alpha_hat = self.getAlphaHat();
        last_column = []

        for s in range(self.numOfStates):
            last_column.append( alpha_hat[s, len(self.seq)] )
        return last_column.index( max(last_column) )
        
    def getOptimalPath(self):
        path = []
        state = self.getMaxFinalState()
        path.insert(0, state)
        
        for t in range( len(self.seq), 0, -1 ):
            state = int(self.optimal_path[state][t])
            path.insert(0, state)

        return path
