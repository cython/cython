# mode: run
# tag: subscript, warnings
# cython: language_level=3

import cython

import sys

from cpython.object cimport Py_TYPE
from cpython.type cimport PyType_GetSlot, Py_mp_ass_subscript, Py_sq_ass_item

IS_CPYTHON = sys.implementation.name == 'cpython'


def implements_slot(obj, name):
    cdef int slot_id
    if name == 'mp_ass_subscript':
        slot_id = Py_mp_ass_subscript
    elif name == 'sq_ass_item':
        slot_id = Py_sq_ass_item
    else:
        raise ValueError

    if not IS_CPYTHON or sys.version_info < (3,10):
        # Don't assume that other implementations fill all slots.
        return True

    return PyType_GetSlot(<type>Py_TYPE(obj), slot_id) is not NULL


def slot_is_empty(obj, name):
    if not IS_CPYTHON or sys.version_info < (3,10):
        return True
    return not implements_slot(obj, name)


cdef class SetItemExt:
    """
    >>> s = SetItemExt()
    >>> s[2] = 4
    2 4
    >>> del s[2]
    Traceback (most recent call last):
    NotImplementedError: Subscript deletion not supported by extsetitem.SetItemExt

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
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

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
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

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __setitem__(self, i: cython.Py_ssize_t, x):
        print(i, x)


@cython.collection_type("sequence")
@cython.cclass
class SetItemExtCollectionTypeSequenceInt:
    """
    >>> s = SetItemExtCollectionTypeSequenceInt()
    >>> s[2] = 4
    2 4
    >>> del s[2]
    Traceback (most recent call last):
    NotImplementedError: Subscript deletion not supported by extsetitem.SetItemExtCollectionTypeSequenceInt

    >>> slot_is_empty(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __setitem__(self, i: cython.Py_ssize_t, x):
        print(i, x)


@cython.collection_type("sequence")
@cython.cclass
class SetItemExtCollectionTypeSequenceObj:
    """
    >>> s = SetItemExtCollectionTypeSequenceObj()
    >>> s[2] = 4
    2 4
    >>> del s[2]
    Traceback (most recent call last):
    NotImplementedError: Subscript deletion not supported by extsetitem.SetItemExtCollectionTypeSequenceObj

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __setitem__(self, i, x):
        print(i, x)


@cython.collection_type("mapping")
@cython.cclass
class SetItemExtCollectionTypeMappingInt:
    """
    >>> s = SetItemExtCollectionTypeMappingInt()
    >>> s[2] = 4
    2 4
    >>> del s[2]
    Traceback (most recent call last):
    NotImplementedError: Subscript deletion not supported by extsetitem.SetItemExtCollectionTypeMappingInt

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __setitem__(self, i: cython.Py_ssize_t, x):
        print(i, x)


@cython.collection_type("mapping")
@cython.cclass
class SetItemExtCollectionTypeMappingObj:
    """
    >>> s = SetItemExtCollectionTypeMappingObj()
    >>> s[2] = 4
    2 4
    >>> del s[2]
    Traceback (most recent call last):
    NotImplementedError: Subscript deletion not supported by extsetitem.SetItemExtCollectionTypeMappingObj

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')  # not required but doesn't hurt since 'mp_ass_subscript' takes precedence
    True
    """
    def __setitem__(self, i, x):
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

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __setitem__(self, i: cython.int, x):
        print(i, x)


_WARNINGS = """
187:26: Smaller index type 'int' than 'Py_ssize_t' may get truncated in sequence protocol
"""
