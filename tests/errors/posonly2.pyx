# mode: error
# tag: posonly

def f(a, b/2, c):
    pass

_ERRORS = u"""
4:11: Syntax error in Python function argument list
"""
