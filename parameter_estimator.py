'''
   Copyright (c) 2014, Joonhee Han.
 
   This file is part of MealyHMM.
   MealyHMM is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
'''

import copy
from Queue import Queue

class ParameterEstimator:
    def __init__(self, hmm, alpha, beta, seq):
        self.hmm = hmm
        self.new_hmm = copy.copy(hmm)
        self.alpha = alpha
        self.beta = beta
        self.seq = seq
        self.queue = Queue()

    def estimate(self):
        self.estimate_transition_probability()
        self.estimate_observation_probability()
        return self.new_hmm

    def estimate_transition_probability(self):
        self.queue.put( self.hmm.getInitialState() )

        while not self.queue.empty():
            state = self.queue.get()
            neighbors = self.hmm.getNeighbors(state)

            total_tran_prob = 0.0
            for nb in neighbors:
                tran_prob = 0.0
                for n in range(1, len(self.seq)+1):
                    tran_prob += self.alpha[state][n-1] * self.hmm.getObsProb(state, nb, self.seq[n-1]) * self.hmm.getTranProb(state, nb) * self.beta[nb][n]

                epsil_tran_prob = 0.0
                for n in range(0, len(self.seq)+1):
                    epsil_tran_prob += self.alpha[state][n] * self.hmm.getEpsilonTranProb(state, nb) * self.beta[nb][n]

                # need to be normalized
                self.new_hmm.setTranProb(state, nb, tran_prob)
                self.new_hmm.setEpsilonTranProb(state, nb, epsil_tran_prob)
                total_tran_prob += tran_prob
                total_tran_prob += epsil_tran_prob

                # move to the next state
                if state != nb:
                    self.queue.put(nb)

            # normalize
            for nb in neighbors:
                if total_tran_prob > 0:
                    self.new_hmm.setTranProb(state, nb, self.new_hmm.getTranProb(state, nb) / total_tran_prob)
                    self.new_hmm.setEpsilonTranProb(state, nb, self.new_hmm.getEpsilonTranProb(state, nb) / total_tran_prob)


    # this is an implementation of the equation (13.31) of the Fundamentals of speaker recognition
    def estimate_observation_probability(self):
        self.queue.put( self.hmm.getInitialState() )

        while not self.queue.empty():
            state = self.queue.get()
            neighbors = self.hmm.getNeighbors(state)

            for nb in neighbors:
                denominator= 0.0
                for n in range(1, len(self.seq)+1):
                    denominator += self.alpha[state][n-1] * self.hmm.getObsProb(state, nb, self.seq[n-1]) * self.hmm.getTranProb(state, nb) * self.beta[nb][n]

                # this neighbor is not reachable anymore
                if denominator == 0.0:
                    continue

                for a in self.hmm.getAlphabet():
                    numerator= 0.0
                    for n in range(1, len(self.seq)+1):
                        if a == self.seq[n-1]:
                            numerator += self.alpha[state][n-1] * self.hmm.getObsProb(state, nb, self.seq[n-1]) * self.hmm.getTranProb(state, nb) * self.beta[nb][n]
                    
                    self.new_hmm.setObsProb(state, nb, a, numerator/denominator)

                # move to the next state
                if state != nb:
                    self.queue.put(nb)
