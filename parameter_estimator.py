'''
   Copyright (c) 2014, Joonhee Han.
 
   This file is part of MealyHMM.
   MealyHMM is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
'''

from Queue import Queue
import alpha_calculator as ac
import beta_calculator as bc 
import numpy

class ParameterEstimator:
    def __init__(self, hmm, new_hmm, sequences):
        self.hmm = hmm
        self.new_hmm = new_hmm
        self.alphabet = self.hmm.getAlphabet()
        self.numOfStates = self.hmm.getNumOfStates()
        self.state_probs = numpy.zeros( len(sequences) * self.numOfStates ).reshape( len(sequences), self.numOfStates )
        self.tran_probs = numpy.zeros( len(sequences) * self.numOfStates * self.numOfStates ).reshape( len(sequences), self.numOfStates, self.numOfStates ) 
        self.epsil_tran_probs = numpy.zeros( len(sequences) * self.numOfStates * self.numOfStates ).reshape( len(sequences), self.numOfStates, self.numOfStates ) 
        self.obs_probs = numpy.zeros( len(sequences) * self.numOfStates * self.numOfStates * len(self.alphabet) ).reshape( len(sequences), self.numOfStates, self.numOfStates, len(self.alphabet) ) 
        self.sequences = sequences
        self.queue = Queue()

    def estimate(self):
        for idx, seq in enumerate( self.sequences ):
            a = ac.AlphaCalculator(self.hmm, seq)
            b = bc.BetaCalculator(self.hmm, seq)
            alpha = a.getAlpha()
            beta = b.getBeta()

            self.queue.put( self.hmm.getInitialState() )

            while not self.queue.empty():
                state = self.queue.get()

                for nb in self.hmm.getNeighbors(state):
                    for t in range(0, len(seq)+1):
                        if t > 0:
                            self.tran_probs[idx][state][nb] += alpha[state][t-1] * self.hmm.getObsProb(state, nb, seq[t-1]) * self.hmm.getTranProb(state, nb) * beta[nb][t]
                            self.state_probs[idx][state] += alpha[state][t-1] * self.hmm.getObsProb(state, nb, seq[t-1]) * self.hmm.getTranProb(state, nb) * beta[nb][t]
                            self.obs_probs[idx][state][nb][self.alphabet.index(seq[t-1])] += alpha[state][t-1] * self.hmm.getObsProb(state, nb, seq[t-1]) * self.hmm.getTranProb(state, nb) * beta[nb][t]
                    
                        self.epsil_tran_probs[idx][state][nb] += alpha[state][t] * self.hmm.getEpsilonTranProb(state, nb) * beta[nb][t]
                        self.state_probs[idx][state] += alpha[state][t] * self.hmm.getEpsilonTranProb(state, nb) * beta[nb][t]

                    if state != nb:
                        self.queue.put(nb)

        # set
        self.queue.put( self.hmm.getInitialState() )
        while not self.queue.empty():
            state = self.queue.get()

            for nb in self.hmm.getNeighbors(state):
                for idx in range( len(self.sequences) ):
                    self.new_hmm.setTranProb(state, nb, self.new_hmm.getTranProb(state, nb) + (self.tran_probs[idx][state][nb] / self.state_probs[idx][state] / float(len(self.sequences))) )
                    self.new_hmm.setEpsilonTranProb(state, nb, self.new_hmm.getEpsilonTranProb(state, nb) + (self.epsil_tran_probs[idx][state][nb] / self.state_probs[idx][state] / float(len(self.sequences))) )
                

                for a in self.alphabet:
                    for idx in range( len(self.sequences) ):
                        if self.tran_probs[idx][state][nb] == 0.0: 
                            self.new_hmm.setObsProb(state, nb, a, 0.0 )
                        else:
                            self.new_hmm.setObsProb(state, nb, a, self.new_hmm.getObsProb(state, nb, a) + self.obs_probs[idx][state][nb][self.alphabet.index(a)] / self.tran_probs[idx][state][nb] / float(len(self.sequences)) )

                if state != nb:
                    self.queue.put(nb)
