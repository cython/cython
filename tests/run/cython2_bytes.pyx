# -*- coding: utf-8 -*-
# cython: language_level=2

b = b'abcüöä \x12'

cdef char* cs = 'abcüöä \x12'

def compare_cs():
    """
    >>> b == compare_cs()
    True
    """
    return cs
