__doc__ = """
    >>> print type(f()).__name__
    Spam
"""

cdef class Spam:
    pass

def f():
    s = Spam()
    return s
