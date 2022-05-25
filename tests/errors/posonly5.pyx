# mode: error
# tag: posonly

def test_multiple_seps(a,/,b,/):
    pass

_ERRORS = u"""
4:29: Expected ')', found '/'
"""


