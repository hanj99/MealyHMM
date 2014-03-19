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
        self.epsilon_path = numpy.zeros( self.numOfStates * (len(seq)+1), dtype=bool).reshape( self.numOfStates, len(seq)+1 ) 

    def init_alpha_hat(self):
        self.alpha_hat[0][0] = 1.0
        self.queue.put( self.hmm.getInitialState() )

        while not self.queue.empty():
            state = self.queue.get()

            for successor in self.hmm.getSuccessors(state):
                if successor != state:
                    self.queue.put(successor)
                    self.alpha_hat[successor][0] = self.alpha_hat[state][0] * self.hmm.getEpsilonTranProb(state,successor)


    def calc_alpha_hat(self):
        for t in range(1, self.seqLen):
            self.queue.put( self.hmm.getInitialState() )

            while not self.queue.empty():
                state = self.queue.get()
                tran_alpha_hat_list = []
                epsil_tran_alpha_hat_list = []
                tran_path_list = []
                epsil_tran_path_list = []

                for predecessor in self.hmm.getPredecessors(state):
                    # diagonal or horizontal move
                    tran_alpha_hat_list.append( self.alpha_hat[predecessor][t-1] * self.hmm.getObsProb(predecessor, state, self.seq[t-1]) * self.hmm.getTranProb(predecessor, state) )
                    tran_path_list.append(predecessor)

                    # epsilon transition (vertical move)
                    epsil_tran_alpha_hat_list.append( self.alpha_hat[predecessor][t] * self.hmm.getEpsilonTranProb(predecessor, state) )
                    epsil_tran_path_list.append(predecessor)

                if len( tran_alpha_hat_list ) > 0:
                    tran_alpha_max = max(tran_alpha_hat_list)
                else:
                    tran_alpha_max = 0.0

                if len( epsil_tran_alpha_hat_list ) > 0:
                    epsil_tran_alpha_max = max(epsil_tran_alpha_hat_list)
                else:
                    epsil_tran_alpha_max = 0.0

                if tran_alpha_max == 0.0 and epsil_tran_alpha_max == 0.0:
                    self.alpha_hat[state][t] = 0.0 
                    self.optimal_path[state][t] = 0
                    self.epsilon_path[state][t] = False

                elif tran_alpha_max >= epsil_tran_alpha_max:
                    self.alpha_hat[state][t] = tran_alpha_max
                    self.optimal_path[state][t] = tran_path_list[ tran_alpha_hat_list.index( tran_alpha_max ) ]
                    self.epsilon_path[state][t] = False
                else:
                    self.alpha_hat[state][t] = epsil_tran_alpha_max
                    self.optimal_path[state][t] = epsil_tran_path_list[ epsil_tran_alpha_hat_list.index( epsil_tran_alpha_max ) ]
                    self.epsilon_path[state][t] = True 

                # move to the next state
                for successor in self.hmm.getSuccessors(state):
                    if successor != state:
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
        epsilon_path = []
        state = self.getMaxFinalState()
        path.insert(0, state)

        t = len(self.seq)
        while True:
            state = self.optimal_path[state][t]
    
            # epsilon transition
            if self.epsilon_path[state][t] == True:
                epsilon_path.insert(0, True)
                path.insert(0, state)
            else:
                epsilon_path.insert(0, False)
                path.insert(0, state)
                t -= 1

            if t == 0:
                while( state != self.hmm.getInitialState() ):
                    predecessors = self.hmm.getPredecessors(state)
                    if state in predecessors:
                        predecessors.remove(state)

                    path.insert(0, predecessors[0])
                    epsilon_path.insert(0, True)
                    state = predecessors[0]

                break

        print epsilon_path
        return path
