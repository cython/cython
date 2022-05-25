# mode: error

cimport cython

@cython.autotestdict(False)
def foo():
    pass

_ERRORS = u"""
5:0: The autotestdict compiler directive is not allowed in function scope
"""
