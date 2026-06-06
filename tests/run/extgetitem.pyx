# mode: run
# tag: subscript, warnings
# cython: language_level=3

import cython

import sys

from cpython.object cimport Py_TYPE
from cpython.type cimport PyType_GetSlot, Py_mp_subscript, Py_sq_item

IS_CPYTHON = sys.implementation.name == 'cpython'


def implements_slot(obj, name):
    cdef int slot_id
    if name == 'mp_subscript':
        slot_id = Py_mp_subscript
    elif name == 'sq_item':
        slot_id = Py_sq_item
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


cdef class GetItemExt:
    """
    >>> s = GetItemExt()
    >>> s[1]
    get 1
    >>> implements_slot(s, 'mp_subscript')
    True
    >>> implements_slot(s, 'sq_item')
    True
    """
    def __getitem__(self, x):
        print("get", x)


cdef class GetItemExtSequence:
    """
    >>> s = GetItemExtSequence()
    >>> s[1]
    get 1
    >>> implements_slot(s, 'mp_subscript')
    True
    >>> implements_slot(s, 'sq_item')
    True
    """
    def __getitem__(self, Py_ssize_t x):
        print("get", x)


@cython.cclass
class GetItemExtSequenceAnn:
    """
    >>> s = GetItemExtSequenceAnn()
    >>> s[1]
    get 1
    >>> implements_slot(s, 'mp_subscript')
    True
    >>> implements_slot(s, 'sq_item')
    True
    """
    def __getitem__(self, x: cython.Py_ssize_t):
        print("get", x)


@cython.collection_type("sequence")
@cython.cclass
class GetItemExtCollectionTypeSequenceInt:
    """
    >>> s = GetItemExtCollectionTypeSequenceInt()
    >>> s[1]
    get 1
    >>> slot_is_empty(s, 'mp_subscript')
    True
    >>> implements_slot(s, 'sq_item')
    True
    """
    def __getitem__(self, x: cython.Py_ssize_t):
        print("get", x)


@cython.collection_type("sequence")
@cython.cclass
class GetItemExtCollectionTypeSequenceObj:
    """
    >>> s = GetItemExtCollectionTypeSequenceObj()
    >>> s[1]
    get 1
    >>> implements_slot(s, 'mp_subscript')
    True
    >>> implements_slot(s, 'sq_item')
    True
    """
    def __getitem__(self, x):
        print("get", x)


@cython.collection_type("mapping")
@cython.cclass
class GetItemExtCollectionTypeMappingInt:
    """
    >>> s = GetItemExtCollectionTypeMappingInt()
    >>> s[1]
    get 1
    >>> implements_slot(s, 'mp_subscript')
    True
    >>> implements_slot(s, 'sq_item')
    True
    """
    def __getitem__(self, x: cython.Py_ssize_t):
        print("get", x)


@cython.collection_type("mapping")
@cython.cclass
class GetItemExtCollectionTypeMappingObj:
    """
    >>> s = GetItemExtCollectionTypeMappingObj()
    >>> s[1]
    get 1
    >>> implements_slot(s, 'mp_subscript')
    True
    >>> implements_slot(s, 'sq_item')  # not required but doesn't hurt since 'mp_subscript' takes precedence
    True
    """
    def __getitem__(self, x):
        print("get", x)


@cython.cclass
class GetItemExtSequenceSmallInt:
    """
    >>> s = GetItemExtSequenceSmallInt()
    >>> s[1]
    get 1
    >>> implements_slot(s, 'mp_subscript')
    True
    >>> implements_slot(s, 'sq_item')
    True
    """
    def __getitem__(self, x: cython.int):
        print("get", x)


_WARNINGS = """
155:26: Smaller index type 'int' than 'Py_ssize_t' may get truncated in sequence protocol
"""
