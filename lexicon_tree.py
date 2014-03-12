import networkx as nx

class LexiconTree:
    def __init__(self):
        self.tree = nx.DiGraph()
        self.tree.add_node( 0, {'sym':'init'} )
        self.i_state = 1  # insert state

    def getRoot(self):
        return 0;

    def fit(self, words):
        for w in words:
            t_state = self.getRoot() # traverse state
            self.insert( list(w), t_state )

    def insert(self, word, t_state):
        try: 
            c = word.pop(0)
        except Exception as e:
            return

        for child in self.tree.successors( t_state ):
            if self.tree.node[child]['sym'] == c:
                self.insert(word, child)
                return
    
        # no childrens have this character
        self.tree.add_node( self.i_state, {'sym':c} )
        self.tree.add_edge( t_state, self.i_state )
        t_state = self.i_state
        self.i_state += 1

        # move to the next character
        self.insert( word, t_state )    



lt = LexiconTree()
lt.fit(['actor', 'action'])

print lt.tree.nodes(data=True)
print lt.tree.edges(data=True)
