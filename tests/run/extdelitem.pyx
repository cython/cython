# mode: run
# tag: subscript, warnings
# cython: language_level=3

import cython


cdef class DelItemExt:
    """
    >>> s = DelItemExt()
    >>> s[2] = 4
    Traceback (most recent call last):
    NotImplementedError: Subscript assignment not supported by extdelitem.DelItemExt
    >>> del s[2]
    2
    """
    def __delitem__(self, i):
        print(i)


cdef class DelItemExtSequence:
    """
    >>> s = DelItemExtSequence()
    >>> s[2] = 4
    Traceback (most recent call last):
    NotImplementedError: Subscript assignment not supported by extdelitem.DelItemExtSequence
    >>> del s[2]
    2
    """
    def __delitem__(self, Py_ssize_t i):
        print(i)


@cython.cclass
class DelItemExtSequenceAnn:
    """
    >>> s = DelItemExtSequenceAnn()
    >>> s[2] = 4
    Traceback (most recent call last):
    NotImplementedError: Subscript assignment not supported by extdelitem.DelItemExtSequenceAnn
    >>> del s[2]
    2
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(i)


@cython.cclass
class DelItemExtSequenceSmallInt:
    """
    >>> s = DelItemExtSequenceSmallInt()
    >>> s[2] = 4
    Traceback (most recent call last):
    NotImplementedError: Subscript assignment not supported by extdelitem.DelItemExtSequenceSmallInt
    >>> del s[2]
    2
    """
    def __delitem__(self, i: cython.int):
        print(i)


_WARNINGS = """
58:26: Smaller index type 'int' than 'Py_ssize_t' may get truncated in sequence protocol
"""
