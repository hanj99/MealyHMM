'''
   Copyright (c) 2014, Joonhee Han.
 
   This file is part of MealyHMM.
   MealyHMM is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
'''

import numpy
import copy
import lexicon_tree as lt

class Hmm:
    def __init__(self, words, test=False):
        self.lexicon_tree = lt.LexiconTree(test)
        self.lexicon_tree.fit(words)
        self.dag = self.lexicon_tree.getDAG()

    def getAlphabet(self):
        return self.lexicon_tree.getAlphabet()

    def getInitialState(self):
        return self.lexicon_tree.getInitialState()

    def getFinalState(self):
        return self.lexicon_tree.getFinalState()

    def getNumOfStates(self):
        return len( self.dag )

    def getPredecessors(self, state):
        predecessors = self.dag.predecessors(state)
        #if state in predecessors:
        #    predecessors.remove(state)
        return predecessors
        
    def getSuccessors(self, state):
        successors = self.dag.successors(state)
        #if state in successors:
        #    successors.remove(state)
        return successors

    def getNeighbors(self, state):
        neighbors = self.dag.successors(state)
        return neighbors 

    def getObsProb(self, s1, s2, o):
        try:
          return self.dag.edge[s1][s2][o]
        except KeyError:
          return 0.0

    def getTranProb(self, s1, s2):
        try:
          return self.dag.edge[s1][s2]['tran_prob']
        except KeyError:
          return 0.0

    def getEpsilonTranProb(self, s1, s2):
        try:
          return self.dag.edge[s1][s2]['epsil_tran_prob']
        except KeyError:
          return 0.0

    def setObsProb(self, s1, s2, o, p):
        try:
          self.dag.edge[s1][s2][o] = p
        except KeyError:
          pass

    def setTranProb(self, s1, s2, p):
        try:
          self.dag.edge[s1][s2]['tran_prob'] = p
        except KeyError:
          pass 

    def setEpsilonTranProb(self, s1, s2, p):
        try:
          self.dag.edge[s1][s2]['epsil_tran_prob'] = p
        except KeyError:
          pass

    def clearProb(self):
        for edge in self.dag.edges(data=True):
            for element in edge[2]: # edge => (0, 2, {'a':0.333, 'tran_prob':0.24, ...})
                edge[2][element] = 0.0

if __name__ == "__main__":
    words = ['act', 'actor', 'action', 'active']
    words = ['act', 'actor']
    hmm = Hmm(words)
    print hmm.dag.nodes(data=True)
    print hmm.dag.edges(data=True)

