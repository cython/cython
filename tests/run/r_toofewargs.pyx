__doc__ = """
    >>> s = Spam()
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (0 given)
"""

cdef class Spam:

    def __init__(self, a, b, int c):
        pass
