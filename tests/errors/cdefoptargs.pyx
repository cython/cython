# mode: error

def call5():
    b(1,2,3,4,5)

cdef b(a, b, c=1, d=2):
    pass

_ERRORS = u"""
4:5:Call with wrong number of arguments (expected at most 4, got 5)
"""
