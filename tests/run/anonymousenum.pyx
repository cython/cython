__doc__ = u"""
>>> p
42
"""

cdef enum:
    spam = 42
    grail = 17

cdef int i
i = spam

p = i
