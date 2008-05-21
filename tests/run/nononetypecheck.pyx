__doc__ = u"""
>>> g()
"""

cdef class Spam:
    pass

cdef f(Spam s):
    pass

def g():
    f(None)
