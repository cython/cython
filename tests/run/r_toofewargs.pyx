__doc__ = u"""
    >>> s = Spam()
    Traceback (most recent call last):
    TypeError: __init__() takes exactly 3 positional arguments (0 given)
"""

cdef class Spam:

    def __init__(self, a, b, int c):
        pass
