import copy
from Queue import Queue

class ObservationEstimator:
    def __init__(self, hmm, alpha, beta, seq):
        self.hmm = hmm
        self.new_hmm = copy.copy(hmm)
        self.alpha = alpha
        self.beta = beta
        self.seq = seq
        self.queue = Queue()

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

                for a in self.hmm.getAlphabet():
                    numerator= 0.0
                    for n in range(1, len(self.seq)+1):
                        if a == self.seq[n-1]:
                            numerator += self.alpha[state][n-1] * self.hmm.getObsProb(state, nb, self.seq[n-1]) * self.hmm.getTranProb(state, nb) * self.beta[nb][n]
                    
                    self.new_hmm.setObsProb(state, nb, a, numerator/denominator)

                if state != nb:
                    self.queue.put(nb)

        return self.new_hmm
