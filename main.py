import hmm
import alpha_calculator as ac
import beta_calculator as bc 
import parameter_estimator as pe 
import viterbi as vi 

h = hmm.Hmm()
seq = ['a','a','b','b']
print h.dag.edges(data=True)

for n in range(1000):
    a = ac.AlphaCalculator(h, seq)
    b = bc.BetaCalculator(h, seq)
    v = vi.Viterbi(h, seq)
    alpha = a.getAlpha()
    beta = b.getBeta()
    alpha_hat = v.getAlphaHat()
    print alpha_hat
    break

    p = pe.ParameterEstimator(h, alpha, beta, seq)
    h = p.estimate()
    print h.dag.edges(data=True)
    print '=================================='
