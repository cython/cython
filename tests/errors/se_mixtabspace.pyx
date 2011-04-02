# mode: error

def f():
 a = b # space space
	c = d # tab
_ERRORS = u"""
5:0: Mixed use of tabs and spaces
"""
