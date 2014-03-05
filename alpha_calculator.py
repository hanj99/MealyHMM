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
        self.queue.put(0)

        while not self.queue.empty():
            state = self.queue.get()

            for successor in self.hmm.getSuccessors(state):
                self.queue.put(successor)
                self.alpha[successor][0] = self.alpha[state][0] * self.hmm.getEpsilonTranProb(state,successor)

    def calc_alpha(self):
        for t in range(1, self.seqLen):
            self.queue.put(0)

            while not self.queue.empty():
                state = self.queue.get()

                for successor in self.hmm.getSuccessors(state):
                    self.queue.put(successor)

                    # from self (horizontal move)
                    print t
                    self.alpha[state][t] += self.alpha[state][t-1] * self.hmm.getObsProb(state, state, self.seq[t-1]) * self.hmm.getTranProb(state, state)
                    # from parent (diagonal move)
                    self.alpha[successor][t] += self.alpha[state][t-1] * self.hmm.getObsProb(state, successor, self.seq[t-1]) * self.hmm.getTranProb(state, successor)

                    # from epsilon (vertical move)
                    self.alpha[successor][t] += self.alpha[state][t] * self.hmm.getEpsilonTranProb(state, successor)

    def getAlpha(self):
        self.init_alpha()
        self.calc_alpha()
        return self.alpha

