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


cdef class DelItemExt:
    """
    >>> s = DelItemExt()
    >>> s[2] = 4
    Traceback (most recent call last):
    NotImplementedError: Subscript assignment not supported by extdelitem.DelItemExt
    >>> del s[2]
    2

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
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

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
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

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(i)


@cython.collection_type("sequence")
@cython.cclass
class DelItemExtCollectionTypeSequenceInt:
    """
    >>> s = DelItemExtCollectionTypeSequenceInt()
    >>> s[2] = 4
    Traceback (most recent call last):
    NotImplementedError: Subscript assignment not supported by extdelitem.DelItemExtCollectionTypeSequenceInt
    >>> del s[2]
    2

    >>> slot_is_empty(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(i)


@cython.collection_type("sequence")
@cython.cclass
class DelItemExtCollectionTypeSequenceObj:
    """
    >>> s = DelItemExtCollectionTypeSequenceObj()
    >>> s[2] = 4
    Traceback (most recent call last):
    NotImplementedError: Subscript assignment not supported by extdelitem.DelItemExtCollectionTypeSequenceObj
    >>> del s[2]
    2

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __delitem__(self, i):
        print(i)


@cython.collection_type("mapping")
@cython.cclass
class DelItemExtCollectionTypeMppingInt:
    """
    >>> s = DelItemExtCollectionTypeMppingInt()
    >>> s[2] = 4
    Traceback (most recent call last):
    NotImplementedError: Subscript assignment not supported by extdelitem.DelItemExtCollectionTypeMppingInt
    >>> del s[2]
    2

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(i)


@cython.collection_type("mapping")
@cython.cclass
class DelItemExtCollectionTypeMppingObj:
    """
    >>> s = DelItemExtCollectionTypeMppingObj()
    >>> s[2] = 4
    Traceback (most recent call last):
    NotImplementedError: Subscript assignment not supported by extdelitem.DelItemExtCollectionTypeMppingObj
    >>> del s[2]
    2

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __delitem__(self, i):
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

    >>> implements_slot(s, 'mp_ass_subscript')
    True
    >>> implements_slot(s, 'sq_ass_item')
    True
    """
    def __delitem__(self, i: cython.int):
        print(i)


_WARNINGS = """
187:26: Smaller index type 'int' than 'Py_ssize_t' may get truncated in sequence protocol
"""
