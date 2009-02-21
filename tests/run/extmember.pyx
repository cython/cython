__doc__ = u"""
    >>> s = Spam()
    >>> s.e = s
    >>> s.e = 1
    Traceback (most recent call last):
    TypeError: Cannot convert int to extmember.Spam
    >>> s.e is s
    True
    >>> s.e = None

    >>> s = Bot()
    >>> s.e = s
    >>> s.e = 1
    Traceback (most recent call last):
    TypeError: Cannot convert int to extmember.Bot
    >>> s.e is s
    True
    >>> s.e = None
"""

# declared in the pxd
cdef class Spam:
    pass

# not declared in the pxd
cdef class Bot:
    cdef public Bot e
