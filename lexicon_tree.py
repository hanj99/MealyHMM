'''
   Copyright (c) 2014, Joonhee Han.
 
   This file is part of MealyHMM.
   MealyHMM is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
'''

import random
import networkx as nx
import copy

class LexiconTree:
    def __init__(self, test=False):
        self.test = test

        if test:
            self.alphabet = ['a','b']
            self.initial_state = 0
            self.final_state = None 
            self.tree = nx.DiGraph()
            self.initProbabilitiesForTest()
        else:
            self.alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            self.initial_state = 0
            self.final_state = None 

            self.tree = nx.DiGraph()
            self.last_states = []  # last state per word
            self.i_state = 1  # insert state

    def getInitialState(self):
        return self.initial_state

    def getFinalState(self):
        return self.final_state

    def getAlphabet(self):
        return self.alphabet

    def setFinalState(self, state):
        self.final_state = state

    def fit(self, words):
        if self.test == False:
            self.tree.add_node( self.initial_state, {'sym':'init'} ) 
            self.tree.add_edge( self.initial_state, self.initial_state )

            for word in words:
                c_state = self.getInitialState() # current state
                self.insert( list(word), c_state )

            self.setFinalEdges()

            self.setProbabilities()

    def insert(self, word, c_state):
        try: 
            c = word.pop(0)
        except Exception as e:
            self.last_states.append( c_state )
            return

        for child in self.tree.successors( c_state ):
            # self
            if c_state == child:
                continue

            if self.tree.node[child]['sym'] == c:
                self.insert(word, child)
                return
    
        # no childrens have this character
        self.tree.add_node( self.i_state, {'sym':c} )
        self.tree.add_edge( c_state, self.i_state )
        self.tree.add_edge( self.i_state, self.i_state )
        c_state = self.i_state
        self.i_state += 1

        # move to the next character
        self.insert( word, c_state )    

    def setFinalEdges(self):
        self.tree.add_node( self.i_state, {'sym':'final'} ) 

        for state in self.last_states:
            self.tree.add_edge( state, self.i_state ) # edge to the final state

        self.setFinalState( self.i_state )

    def setProbabilities(self):
        for node in self.tree.nodes(data=True):
            neighbors = self.tree.successors( node[0] )
            t, e, s, ec, rc = self.getRandomProbabilities( len(neighbors) )
            
            for nb in neighbors:
                if nb == self.getInitialState():
                    self.tree.edge[node[0]][nb]['tran_prob'] = 0.1
                    self.tree.edge[node[0]][nb]['epsil_tran_prob'] = 0.0

                    for char in self.alphabet:
                        self.tree.edge[node[0]][nb][char] = 1.0 / len(self.alphabet)

                elif nb == self.getFinalState():
                    self.tree.edge[node[0]][nb]['tran_prob'] = 0.0
                    self.tree.edge[node[0]][nb]['epsil_tran_prob'] = 0.9

                elif node[0] == nb:
                    self.tree.edge[node[0]][nb]['tran_prob'] = s
                    self.tree.edge[node[0]][nb]['epsil_tran_prob'] = 0.0

                    for char in self.alphabet:
                        rand = random.uniform(0, 0)
                        if char == self.tree.node[nb]['sym']:
                            self.tree.edge[node[0]][nb][char] = (ec+rand)
                        else:
                            self.tree.edge[node[0]][nb][char] = (rc-rand)
                else:
                    self.tree.edge[node[0]][nb]['tran_prob'] = t 
                    self.tree.edge[node[0]][nb]['epsil_tran_prob'] = e

                    for char in self.alphabet:
                        rand = random.uniform(0, 0)
                        if char == self.tree.node[nb]['sym']:
                            self.tree.edge[node[0]][nb][char] = (ec+rand)
                        else:
                            self.tree.edge[node[0]][nb][char] = (rc-rand)

        # make sure 
        for node in self.tree.nodes(data=True):
            neighbors = self.tree.successors( node[0] )

            total = 0.0
            
            for nb in neighbors:
                #self transition
                if node[0] == nb:
                    total += self.tree.edge[node[0]][nb]['tran_prob']
                
                #transition to the final state
                elif nb == self.getFinalState():
                    total += self.tree.edge[node[0]][nb]['tran_prob']
                    total += self.tree.edge[node[0]][nb]['epsil_tran_prob'] 
                else:
                    total += self.tree.edge[node[0]][nb]['tran_prob'] 
                    total += self.tree.edge[node[0]][nb]['epsil_tran_prob'] 

            #print total
            
                
    def initProbabilitiesForTest(self):
        self.tree.add_node(0, {'sym':'init'})
        self.tree.add_node(1, {'sym':'x1'})
        self.tree.add_node(2, {'sym':'x2'})
        self.tree.add_node(3, {'sym':'x3'})
        self.tree.add_node(4, {'sym':'final'})
        self.tree.add_edges_from([(0,1),(1,1),(1,2),(2,2),(2,3),(3,4)])

        self.tree.edge[0][1]['epsil_tran_prob'] = 1.0
        self.tree.edge[0][1]['tran_prob'] = 0.0

        self.tree.edge[1][1]['epsil_tran_prob'] = 0.0
        self.tree.edge[1][1]['tran_prob'] = 1.0/3.0
        self.tree.edge[1][1]['a'] = 0.5
        self.tree.edge[1][1]['b'] = 0.5

        self.tree.edge[1][2]['tran_prob'] = 1.0/3.0
        self.tree.edge[1][2]['epsil_tran_prob'] = 1.0/3.0
        self.tree.edge[1][2]['a'] = 0.5
        self.tree.edge[1][2]['b'] = 0.5

        self.tree.edge[2][2]['epsil_tran_prob'] = 0.0
        self.tree.edge[2][2]['tran_prob'] = 0.5
        self.tree.edge[2][2]['a'] = 0.5
        self.tree.edge[2][2]['b'] = 0.5

        self.tree.edge[2][3]['tran_prob'] = 0.5
        self.tree.edge[2][3]['epsil_tran_prob'] = 0.0
        self.tree.edge[2][3]['a'] = 0.5
        self.tree.edge[2][3]['b'] = 0.5

        self.tree.edge[3][4]['tran_prob'] = 0.0
        self.tree.edge[3][4]['epsil_tran_prob'] = 1.0

        self.setFinalState(4)

    def getDAG(self):
        return self.tree

    def getRandomProbabilities(self, n):
        #final state
        if n == 0:
            tran = 0.0
            epsil = 1.0
            sel = 0.0
        else:
            if n > 1:
                tran = 0.7 / (n-1) 
                epsil = 0.2 / (n-1) 
                sel = 0.1
            else:
                tran = 0.7 
                epsil = 0.2 
                sel = 0.1

        expected_char = 0.9
        random_char = 0.1 / (len(self.alphabet)-1)
        return tran, epsil, sel, expected_char, random_char

if __name__ == '__main__':
    lt = LexiconTree()

    for edge in lt.tree.edges(data=True):
        print edge

