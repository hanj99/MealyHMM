import numpy
from Queue import Queue

class BetaCalculator
    def __init__(self, hmm, seq):
        self.hmm = hmm
        self.seq = seq
        self.queue = Queue()
        self.numOfStates = hmm.getNumOfStates()
        self.seqLen = len(seq) + 1
        self.beta = numpy.zeros( self.numOfStates * self.seqLen ).reshape( self.numOfStates, self.seqLen )

    def init_beta(self):
        final_state = self.hmm.getFinalState()
        self.beta[final_state][self.seqLen] = 1.0
        self.queue.put( final_state )

        while not self.queue.empty():
            state = self.queue.get()

            for predecessor in self.hmm.getPredecessors(state):
                self.queue.put(predecessor)
                self.beta[predecessor][self.seqLen] = self.beta[state][self.seqLen] * self.hmm.getEpsilonTranProb(predecessor, state)

    # FIXME
    def calc_beta(self):
        for t in range(self.seqLen - 1, 0, -1):
            for s in range(self.numOfStates - 1, -1, -1):
                cs_list = self.hmm.getChildrenState(s)
                    
                # from self
                self.beta[s][t] += self.beta[s][t+1] * self.hmm.getObsProb(self.seq[t+1], s, s) * self.hmm.getTranProb(s, s)

                # from children
                for cs in cs_list:
                    self.beta[s][t] += self.beta[cs][t+1] * self.hmm.getObsProb(self.seq[t+1], s, cs) * self.hmm.getTranProb(s, cs)
                    self.beta[s][t] += self.beta[cs][t] * self.hmm.getEpsilonTranProb(s, cs)



    def getBeta(self):
        self.init_beta()
        self.calc_beta()
        return self.beta
