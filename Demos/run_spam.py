from spam import Spam

s = Spam()
print "Created:", s
s.set_amount(42)
print "Amount =", s.get_amount()
s.describe()
s = None
