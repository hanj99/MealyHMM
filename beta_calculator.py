import numpy
from Queue import Queue

class BetaCalculator:
    def __init__(self, hmm, seq):
        self.hmm = hmm
        self.seq = seq
        self.queue = Queue()
        self.numOfStates = hmm.getNumOfStates()
        self.seqLen = len(seq) + 1
        self.beta = numpy.zeros( self.numOfStates * self.seqLen ).reshape( self.numOfStates, self.seqLen )

    def init_beta(self):
        final_state = self.hmm.getFinalState()
        self.beta[final_state][self.seqLen-1] = 1.0
        self.queue.put( final_state )

        while not self.queue.empty():
            state = self.queue.get()

            for predecessor in self.hmm.getPredecessors(state):
                self.queue.put(predecessor)
                self.beta[predecessor][self.seqLen-1] = self.beta[state][self.seqLen-1] * self.hmm.getEpsilonTranProb(predecessor, state)

    def calc_beta(self):
        for t in range(self.seqLen - 2, -1, -1):
            self.queue.put( self.hmm.getFinalState() )
                    
            while not self.queue.empty():
                state = self.queue.get()

                for predecessor in self.hmm.getPredecessors(state):
                    self.queue.put(predecessor)

                    # vertical move
                    self.beta[predecessor][t] += self.beta[state][t] * self.hmm.getEpsilonTranProb(predecessor, state)

                    # diagonal move
                    self.beta[predecessor][t] += self.beta[state][t+1] * self.hmm.getObsProb(predecessor, state, self.seq[t]) * self.hmm.getTranProb(predecessor, state)

                    # horizontal move
                    self.beta[predecessor][t] += self.beta[predecessor][t+1] * self.hmm.getObsProb(predecessor, predecessor, self.seq[t]) * self.hmm.getTranProb(predecessor, predecessor)

    def getBeta(self):
        self.init_beta()
        self.calc_beta()
        return self.beta
