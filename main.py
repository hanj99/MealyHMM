import hmm
import alpha_calculator as ac
import beta_calculator as bc 
import parameter_estimator as pe 
import viterbi as vi 
import lexicon_tree as lt
import math

def assertTranSum(hmm):
    for node in hmm.dag.nodes(data=True):
        neighbors = hmm.dag.successors( node[0] )

        total = 0.0
            
        for nb in neighbors:
            #self transition
            if node[0] == nb:
                total += hmm.dag.edge[node[0]][nb]['tran_prob']
                
            #transition to the final state
            elif nb == hmm.getFinalState():
                total += hmm.dag.edge[node[0]][nb]['tran_prob']
                total += hmm.dag.edge[node[0]][nb]['epsil_tran_prob'] 
            else:
                total += hmm.dag.edge[node[0]][nb]['tran_prob'] 
                total += hmm.dag.edge[node[0]][nb]['epsil_tran_prob'] 

        if node[0] != hmm.getFinalState():
            pass
            #print total

words = ['abaa', 'babb']

h = hmm.Hmm( words, test=False)
n_h = hmm.Hmm(words, test=False)

print '================ initial hmm =============='
for edge in h.dag.edges(data=True):
    print edge
print '================ ========================'

for n in range(100):
    print '======== training =>', n 

    p = pe.ParameterEstimator(h, n_h, words)
    p.estimate() 
    h.clearProb()

    for edge in n_h.dag.edges(data=True):
        print edge

    # exchange
    h.clearProb()
    tmp_h = n_h
    n_h = h
    h = tmp_h
    
for word in words:
    print 'real word =>', word
    v = vi.Viterbi(h, word)

    for i in v.getOptimalPath():
        print h.dag.node[i]['sym'], i
