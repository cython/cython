# mode: error

# invalid syntax (as handled by the parser)

def syntax():
    *a, *b = 1,2,3,4,5


_ERRORS = u"""
6:4: more than 1 starred expression in assignment
6:8: more than 1 starred expression in assignment
"""
