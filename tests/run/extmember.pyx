__doc__ = """
    >>> s = Spam()
    >>> s.e = s
    >>> s.e = 1
    Traceback (most recent call last):
    TypeError: Cannot convert int to extmember.Spam
    >>> s.e is s
    True
    >>> s.e = None
"""

cdef class Spam:
	cdef public Spam e
