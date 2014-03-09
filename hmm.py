'''
   Copyright (c) 2014, Joonhee Han.
 
   This file is part of MealyHMM.
   MealyHMM is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
'''

import numpy
import random
import networkx

class Hmm:
    def __init__(self):
        self.dag = networkx.DiGraph()
        self.alphabet = None
        self.case3()

    # fundamentals of speaker recognition (p.425)
    def case3(self):
        self.alphabet = ['a','b']
        self.dag.add_node(0, {'sym':'x1'})
        self.dag.add_node(1, {'sym':'x2'})
        self.dag.add_node(2, {'sym':'x3'})
        self.dag.add_edges_from([(0,0),(0,1),(1,1),(1,2)])

        self.dag.edge[0][0]['tran_prob'] = 0.5
        self.dag.edge[0][0]['a'] = 0.8 
        self.dag.edge[0][0]['b'] = 0.2

        self.dag.edge[0][1]['tran_prob'] = 0.3
        self.dag.edge[0][1]['epsil_tran_prob'] = 0.2
        self.dag.edge[0][1]['a'] = 0.7
        self.dag.edge[0][1]['b'] = 0.3

        self.dag.edge[1][1]['tran_prob'] = 0.4
        self.dag.edge[1][1]['a'] = 0.5
        self.dag.edge[1][1]['b'] = 0.5

        self.dag.edge[1][2]['tran_prob'] = 0.5
        self.dag.edge[1][2]['epsil_tran_prob'] = 0.1
        self.dag.edge[1][2]['a'] = 0.3
        self.dag.edge[1][2]['b'] = 0.7

    # fundamentals of speaker recognition (p.438)
    def case2(self):
        self.alphabet = ['a','b']
        self.dag.add_node(0, {'sym':'x1'})
        self.dag.add_node(1, {'sym':'x2'})
        self.dag.add_node(2, {'sym':'x3'})
        self.dag.add_edges_from([(0,0),(0,1),(1,1),(1,2)])

        self.dag.edge[0][0]['tran_prob'] = 1.0/3.0 
        self.dag.edge[0][0]['a'] = 0.5
        self.dag.edge[0][0]['b'] = 0.5

        self.dag.edge[0][1]['tran_prob'] = 1.0/3.0 
        self.dag.edge[0][1]['epsil_tran_prob'] = 1.0/3.0 
        self.dag.edge[0][1]['a'] = 1.0/2.0 
        self.dag.edge[0][1]['b'] = 1.0/2.0 

        self.dag.edge[1][1]['tran_prob'] = 1.0/2.0 
        self.dag.edge[1][1]['a'] = 1.0/2.0 
        self.dag.edge[1][1]['b'] = 1.0/2.0 

        self.dag.edge[1][2]['tran_prob'] = 1.0/2.0 
        self.dag.edge[1][2]['a'] = 1.0/2.0 
        self.dag.edge[1][2]['b'] = 1.0/2.0 

    def case1(self):
        self.alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.dag.add_node(0, {'sym':'initial'})
        self.dag.add_node(1, {'sym':'a'})
        self.dag.add_node(2, {'sym':'c'})
        self.dag.add_node(3, {'sym':'t'})
        self.dag.add_node(4, {'sym':'o'})
        self.dag.add_node(5, {'sym':'r'})
        self.dag.add_node(6, {'sym':'i'})
        self.dag.add_node(7, {'sym':'o'})
        self.dag.add_node(8, {'sym':'n'})
        self.dag.add_node(9, {'sym':'final'})

        # self transition (except final state)
        for state in range(len(self.dag)-1):
            self.dag.add_path([state,state])

        # act
        self.dag.add_path([0,1,2,3,9])

        # actor
        self.dag.add_path([0,1,2,3,4,5,9])
        
        # actress 
        self.dag.add_path([0,1,2,3,6,7,8,9])

        # transitional probabilities (except final state)
        for state in range(len(self.dag)-1):
            neighbors = self.dag.neighbors(state)
            tran_probs = self.getRandomProbabilityList( len(neighbors)*2-1 ) 
             
            idx = 0
            for nb in neighbors:
                if state == nb:
                    self.dag.edge[state][nb]['tran_prob'] = tran_probs[idx]

                    alphabet_probs = self.getRandomProbabilityList( len(self.alphabet) ) 
                    for i, c in enumerate(self.alphabet):
                        self.dag.edge[state][nb][c] = alphabet_probs[i]
                else:
                    self.dag.edge[state][nb]['tran_prob'] = tran_probs[idx]
                    idx += 1
                    self.dag.edge[state][nb]['epsil_tran_prob'] = tran_probs[idx]

                    alphabet_probs = self.getRandomProbabilityList( len(self.alphabet) ) 
                    for i, c in enumerate(self.alphabet):
                        self.dag.edge[state][nb][c] = alphabet_probs[i]

                idx += 1

    def getAlphabet(self):
        return self.alphabet

    def getInitialState(self):
        return 0

    def getFinalState(self):
        return len( self.dag ) - 1

    def getRandomProbabilityList(self, n):
        probs = [random.uniform(0,1) for x in range(n)] 
        norm_probs = [x/sum(probs) for x in probs]
        return norm_probs

    def getInitialState(self):
        return 0 

    def getNumOfStates(self):
        return len( self.dag )

    def getPredecessors(self, state):
        predecessors = self.dag.predecessors(state)
        if state in predecessors:
            predecessors.remove(state)
        return predecessors
        
    def getSuccessors(self, state):
        successors = self.dag.successors(state)
        if state in successors:
            successors.remove(state)
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
