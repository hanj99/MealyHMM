import copy
from Queue import Queue

class TransitionEstimator:
    def __init__(self, hmm, alpha, beta, seq):
        self.hmm = hmm
        self.new_hmm = copy.copy(hmm)
        self.alpha = alpha
        self.beta = beta
        self.seq = seq
        self.queue = Queue()

    def estimate_transition_probability(self):
        self.queue.put( self.hmm.getInitialState() )

        while not self.queue.empty():
            state = self.queue.get()
            neighbors = self.hmm.getNeighbors(state)

            total_neighbors_prob = 0.0
            for nb in neighbors:

                # transition
                prob = 0.0
                for n in range(1, len(self.seq)+1):
                    prob += self.alpha[state][n-1] * self.hmm.getObsProb(state, nb, self.seq[n-1]) * self.hmm.getTranProb(state, nb) * self.beta[nb][n]

                # not yet normalized
                self.new_hmm.setTranProb(state, nb, prob)
                total_neighbors_prob += prob

                # epsilon transition is not allowed on the self transition
                if state != nb:
                    self.queue.put(nb)

                    # epsilon transition
                    prob = 0.0
                    for n in range(0, len(self.seq)):
                        prob += self.alpha[state][n] * self.hmm.getEpsilonTranProb(state, nb) * self.beta[nb][n]

                    # not yet normalized
                    self.new_hmm.setEpsilonTranProb(state, nb, prob)
                    total_neighbors_prob += prob

            # normalize
            for nb in neighbors:
                self.new_hmm.setTranProb(state, nb, self.new_hmm.getTranProb(state, nb) / total_neighbors_prob)
                self.new_hmm.setEpsilonTranProb(state, nb, self.new_hmm.getEpsilonTranProb(state, nb) / total_neighbors_prob)

        return self.new_hmm
