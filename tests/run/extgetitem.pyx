# mode: run
# tag: subscript, warnings
# cython: language_level=3

import cython


cdef class GetItemExt:
    """
    >>> s = GetItemExt()
    >>> s[1]
    get 1
    """
    def __getitem__(self, x):
        print("get", x)


cdef class GetItemExtSequence:
    """
    >>> s = GetItemExtSequence()
    >>> s[1]
    get 1
    """
    def __getitem__(self, Py_ssize_t x):
        print("get", x)


@cython.cclass
class GetItemExtSequenceAnn:
    """
    >>> s = GetItemExtSequenceAnn()
    >>> s[1]
    get 1
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
    """
    def __getitem__(self, x):
        print("get", x)


@cython.cclass
class GetItemExtSequenceSmallInt:
    """
    >>> s = GetItemExtSequenceSmallInt()
    >>> s[1]
    get 1
    """
    def __getitem__(self, x: cython.int):
        print("get", x)


_WARNINGS = """
94:26: Smaller index type 'int' than 'Py_ssize_t' may get truncated in sequence protocol
"""
