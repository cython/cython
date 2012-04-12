__doc__ = u"""
>>> BAR == 3
True
>>> HONK == 3+2+1
True
>>> X == 4*5 + 1
True
>>> NONPUBLIC         # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'NONPUBLIC' is not defined
>>> NOWPUBLIC == 23 + 42
True
"""

DEF X = 4*5

cdef enum SECRET:
    NONPUBLIC = 23 + 42

cdef public enum FOO:
    BAR = 3
    HONK = 3+2+1
    NOWPUBLIC = NONPUBLIC
    X = X + 1          # FIXME: should this really work?
