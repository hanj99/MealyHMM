import hmm
import alpha_calculator as ac
import beta_calculator as bc 
import transition_estimator as te 
import observation_estimator as oe 

h = hmm.Hmm()
seq = ['a','b','a','a']
a = ac.AlphaCalculator(h, seq)
b = bc.BetaCalculator(h, seq)

alpha = a.getAlpha()
print alpha

beta = b.getBeta()
print beta

t = te.TransitionEstimator(h, a.alpha, b.beta, seq)
print "========= before transitional parameter reestmation =========="
print h.dag.edges(data=True)
new_h = t.estimate_transition_probability()
print "========= after transitional  parameter reestmation =========="
print new_h.dag.edges(data=True)

o = oe.ObservationEstimator(h, a.alpha, b.beta, seq)
print "========= before observational parameter reestmation =========="
print h.dag.edges(data=True)
new_h = o.estimate_observation_probability()
print "========= after  observational parameter reestmation =========="
print new_h.dag.edges(data=True)
