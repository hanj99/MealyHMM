import numpy
import random
import networkx

class Hmm:
    def __init__(self):
        self.dag = networkx.DiGraph()
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
            tran_probs = self.getProbabilityList( len(neighbors)*2-1 ) 
             
            idx = 0
            for nb in neighbors:
                if state == nb:
                    self.dag.edge[state][nb]['tran_prob'] = tran_probs[idx]

                    alphabet_probs = self.getProbabilityList( len(self.alphabet) ) 
                    for i, c in enumerate(self.alphabet):
                        self.dag.edge[state][nb][c] = alphabet_probs[i]
                else:
                    self.dag.edge[state][nb]['tran_prob'] = tran_probs[idx]
                    idx += 1
                    self.dag.edge[state][nb]['epsil_tran_prob'] = tran_probs[idx]

                    alphabet_probs = self.getProbabilityList( len(self.alphabet) ) 
                    for i, c in enumerate(self.alphabet):
                        self.dag.edge[state][nb][c] = alphabet_probs[i]

                idx += 1

    def getProbabilityList(self, n):
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

    def getObsProb(self, s1, s2, o):
        return self.dag.edge[s1][s2][o]

    def getTranProb(self, s1, s2):
        return self.dag.edge[s1][s2]['tran_prob']

    def getEpsilonTranProb(self, s1, s2):
        return self.dag.edge[s1][s2]['epsil_tran_prob']
