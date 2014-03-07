import hmm
import alpha_calculator as ac
import beta_calculator as bc 
import transition_estimator as te 

h = hmm.Hmm()
seq = ['a','b','a','a']
a = ac.AlphaCalculator(h, seq)
b = bc.BetaCalculator(h, seq)

a.init_alpha()
a.calc_alpha()
print a.alpha

b.init_beta()
b.calc_beta()
print b.beta

t = te.TransitionEstimator(h, a.alpha, b.beta, seq)
print h.dag.edges(data=True)
new_h = t.estimate_transition_probability()
print new_h.dag.edges(data=True)
