import hmm
import parameter_estimator as pe 
import viterbi as vi 

def assertSum(hmm):
    for node in hmm.dag.nodes(data=True):
        neighbors = hmm.dag.successors( node[0] )
        total_tran_probs  = 0.0
            
        for nb in neighbors:
            total_tran_probs += hmm.dag.edge[node[0]][nb]['tran_prob']
            total_tran_probs += hmm.dag.edge[node[0]][nb]['epsil_tran_prob'] 

            total_obs_probs  = 0.0
            for a in hmm.getAlphabet():
              if hmm.dag.edge[node[0]][nb]['epsil_tran_prob'] != 1.0:
                total_obs_probs += hmm.dag.edge[node[0]][nb][a]

            if nb != hmm.getFinalState():
              print 'obs_probs =', node[0], nb, total_obs_probs

        print 'tran_probs =', node[0], nb, total_tran_probs

words = ['act', 'actor', 'action', 'active', 'actress']

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

    #assertSum(n_h)

    for edge in n_h.dag.edges(data=True):
        print edge

    # exchange
    h.clearProb()
    tmp_h = n_h
    n_h = h
    h = tmp_h
    
for word in words:
    print 'obfuscated word =>', word
    v = vi.Viterbi(h, word)

    for i in v.getOptimalPath():
        print h.dag.node[i]['sym'], i
