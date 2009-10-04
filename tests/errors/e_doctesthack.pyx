cimport cython

@cython.doctesthack(False)
def foo():
    pass

_ERRORS = u"""
4:0: The doctesthack compiler directive is not allowed in function scope
"""
