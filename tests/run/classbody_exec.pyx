# mode: run

__doc__ = """
    >>> print(D)
    {'answer': (42, 42)}
"""

D = {}

def foo(x):
    return x, x

cdef class Spam:
    answer = 42
    D[u'answer'] = foo(answer)
