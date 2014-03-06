import hmm
import alpha_calculator as ac

h = hmm.Hmm()
a = ac.AlphaCalculator(h, ['a','a','b','b'])

a.init_alpha()
a.calc_alpha()

print a.alpha
