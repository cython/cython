# mode: run

"""
>>> BAR == 3
True
>>> HONK == 3+2+1
True
>>> NONPUBLIC         # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'NONPUBLIC' is not defined
>>> NOWPUBLIC == 23 + 42
True
"""

cdef enum SECRET:
    NONPUBLIC = 23 + 42

cdef public enum FOO:
    BAR = 3
    HONK = 3+2+1
    NOWPUBLIC = NONPUBLIC
