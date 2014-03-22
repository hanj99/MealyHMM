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
                if total_obs_probs < 0.9:
                    exit(1)
               

        if nb != hmm.getFinalState():
            print 'tran_probs =', node[0], nb, total_tran_probs
            if total_tran_probs < 0.9:
                exit(1)


real_words = ['abababbb', 'bababaaa']
training_words = ['abababbb', 'bababaaa', 'abababab', 'babababa', 'abababaa', 'bababbab', 'abaaabbb', 'babbbaaa', 'abbaabbb']

h = hmm.Hmm( real_words, test=False)
n_h = hmm.Hmm( real_words, test=False)
n_h.clearProb() 

print '================ initial hmm =============='
for edge in h.dag.edges(data=True):
    print edge
print '================ ========================'

for n in range(50):
    print '======== training =>', n 

    p = pe.ParameterEstimator(h, n_h, training_words)
    p.estimate() 

    for edge in n_h.dag.edges(data=True):
        print edge
    #assertSum(n_h)

    # exchange
    h.clearProb()
    tmp_h = n_h
    n_h = h
    h = tmp_h

for edge in h.dag.edges(data=True):
    print edge
    
for word in training_words:
    print 'obfuscated word =>', word
    v = vi.Viterbi(h, word)

    for i in v.getOptimalPath():
        print h.dag.node[i]['sym'], i
