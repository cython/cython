__doc__ = u"""
    >>> print D
    {'answer': (42, 42)}
"""

D = {}

def foo(x):
    return x, x

cdef class Spam:
    answer = 42
    D['answer'] = foo(answer)
