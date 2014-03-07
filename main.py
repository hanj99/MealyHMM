import hmm
import alpha_calculator as ac
import beta_calculator as bc 

h = hmm.Hmm()
#a = ac.AlphaCalculator(h, ['a','a','b','b'])
#b = bc.BetaCalculator(h, ['a','a','b','b'])

a = ac.AlphaCalculator(h, ['a','b','a','a'])
b = bc.BetaCalculator(h, ['a','b','a','a'])

a.init_alpha()
a.calc_alpha()
print a.alpha

b.init_beta()
b.calc_beta()
print b.beta
