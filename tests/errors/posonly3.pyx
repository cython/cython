# mode: error
# tag: posonly

def f(*args, /):
    pass

def f(*args, a, /):
    pass


_ERRORS = u"""
4:13: Expected ')', found '/'
"""
