import hmm
import alpha_calculator as ac
import beta_calculator as bc 
import parameter_estimator as pe 

h = hmm.Hmm()
seq = ['a','b','a','a']
print h.dag.edges(data=True)

for n in range(1000):
    a = ac.AlphaCalculator(h, seq)
    b = bc.BetaCalculator(h, seq)
    alpha = a.getAlpha()
    beta = b.getBeta()

    p = pe.ParameterEstimator(h, alpha, beta, seq)
    h = p.estimate()
    print h.dag.edges(data=True)
    print '=================================='
