# mode: run
# tag: subscript, warnings
# cython: language_level=3

import cython


cdef class SetItemExt:
    """
    >>> s = SetItemExt()
    >>> s[2] = 4
    2 4
    >>> del s[2]
    Traceback (most recent call last):
    NotImplementedError: Subscript deletion not supported by extsetitem.SetItemExt
    """
    def __setitem__(self, i, x):
        print(i, x)


cdef class SetItemExtSequence:
    """
    >>> s = SetItemExtSequence()
    >>> s[2] = 4
    2 4
    >>> del s[2]
    Traceback (most recent call last):
    NotImplementedError: Subscript deletion not supported by extsetitem.SetItemExtSequence
    """
    def __setitem__(self, Py_ssize_t i, x):
        print(i, x)


@cython.cclass
class SetItemExtSequenceAnn:
    """
    >>> s = SetItemExtSequenceAnn()
    >>> s[2] = 4
    2 4
    >>> del s[2]
    Traceback (most recent call last):
    NotImplementedError: Subscript deletion not supported by extsetitem.SetItemExtSequenceAnn
    """
    def __setitem__(self, i: cython.Py_ssize_t, x):
        print(i, x)


@cython.cclass
class SetItemExtSequenceSmallInt:
    """
    >>> s = SetItemExtSequenceSmallInt()
    >>> s[2] = 4
    2 4
    >>> del s[2]
    Traceback (most recent call last):
    NotImplementedError: Subscript deletion not supported by extsetitem.SetItemExtSequenceSmallInt
    """
    def __setitem__(self, i: cython.int, x):
        print(i, x)


_WARNINGS = """
58:26: Smaller index type 'int' than 'Py_ssize_t' may get truncated in sequence protocol
"""
