# mode: error

def f():
	a = b
		c = d
_ERRORS = u"""
5:0: Possible inconsistent indentation
5:0: Expected an identifier or literal
"""
