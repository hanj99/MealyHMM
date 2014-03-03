import numpy

class AlphaCalculator

    def __init__(self, hmm, seq):
        self.hmm = hmm
        self.seq = seq
        self.numOfStates = hmm.getNumOfStates()
        self.seqLen = len(seq)
        self.alpha = numpy.zeros( self.numOfStates * self.seqLen ).reshape( self.numOfStates, self.seqLen ) 

    def init_alpha(self):
        self.alpha[0][0] = 1.0
        
        for s in range(1, self.numOfStates):
            ps = self.hmm.getParentState(s)
            self.alpha[s][0] = self.alpha[ps][0] * self.hmm.getEpsilonTranProb(ps,s)


    def calc_alpha(self):
        for t in range(1, self.seqLen+1):
            for s in range(1, self.numOfStates):
                ps = self.hmm.getParentState(s)

                assert( ps < s )

                # from parent
                self.alpha[s][t] += self.alpha[ps][t-1] * self.hmm.getObsProb(self.seq[t], ps, s) * self.hmm.getTranProb(ps, s)

                # from self 
                self.alpha[s][t] += self.alpha[s][t-1] * self.hmm.getObsProb(self.seq[t], s, s) * self.hmm.getTranProb(s, s)
               
                # from epsilon
                self.alpha[s][t] += self.alpha[ps][t] * self.hmm.getEpsilonTranProb(ps, s)

    def getAlpha(self):
        self.init_alpha()
        self.calc_alpha()
        return self.alpha

