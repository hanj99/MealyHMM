import numpy

class BetaCalculator
    def __init__(self, hmm, seq):
        self.hmm = hmm
        self.seq = seq
        self.numOfStates = hmm.getNumOfStates()
        self.seqLen = len(seq)
        self.beta = numpy.zeros( self.numOfStates * self.seqLen ).reshape( self.numOfStates, self.seqLen )

    def init_beta(self):
        last_state = self.numOfStates - 1
        self.beta[last_state][self.seqLen]
        
        for s in range(self.numOfStates - 2, -1, -1):
            cs_list = self.hmm.getChildrenState(s)
            
            for cs in cs_list:
                self.beta[s][self.seqLen] += self.beta[cs][self.seqLen] * self.hmm.getEpsilonTranProb(s, cs)

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
