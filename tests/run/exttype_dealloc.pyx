# mode: run
# tag: dealloc

import gc
import sys


test_results = []


cdef void add_name(obj):
    name = type(obj).__name__.rsplit('.', 1)[-1]
    test_results.append(name)


def find_name(exttype):
    name = exttype.__name__.rsplit('.', 1)[-1]
    return test_results.count(name)


cdef class ExtTypeSimple:
    """
    >>> obj = ExtTypeSimple()
    >>> find_name(ExtTypeSimple)
    0
    >>> obj = None
    >>> _ = gc.collect()
    >>> find_name(ExtTypeSimple)
    1
    """
    cdef int x
    def __dealloc__(self):
        add_name(self)
        self.x = 0


class PySubTypeSimple(ExtTypeSimple):
    """
    >>> obj = PySubTypeSimple()
    >>> find_name(PySubTypeSimple)
    0
    >>> obj = None
    >>> _ = gc.collect()
    >>> find_name(PySubTypeSimple)
    1
    """


class PySubTypeDel(ExtTypeSimple):
    """
    >>> obj = PySubTypeDel()
    >>> find_name(PySubTypeDel)
    0
    >>> obj = None
    >>> _ = gc.collect()
    >>> find_name(PySubTypeDel)
    2
    """
    def __del__(self):
        add_name(self)


cdef class ExtSubTypeObjAttr(ExtTypeSimple):
    """
    >>> obj = ExtSubTypeObjAttr()
    >>> find_name(ExtSubTypeObjAttr)
    0
    >>> obj = None
    >>> _ = gc.collect()

    # both this type and the base class add the same name
    >>> find_name(ExtSubTypeObjAttr)
    2
    """
    cdef object attr
    def __dealloc__(self):
        add_name(self)
        self.x = 1


cdef class ExtTypeRaise:
    """
    >>> obj = ExtTypeRaise()
    >>> find_name(ExtTypeRaise)
    0
    >>> obj = None
    >>> _ = gc.collect()
    >>> find_name(ExtTypeRaise)
    1
    """
    def __dealloc__(self):
        add_name(self)
        raise RuntimeError("HUHU !")


class PySubTypeRaise(ExtTypeRaise):
    """
    >>> obj = PySubTypeRaise()
    >>> obj.ref = obj
    >>> find_name(PySubTypeRaise)
    0
    >>> obj = None
    >>> _ = gc.collect()
    >>> find_name(PySubTypeRaise)
    1
    """


cdef class ExtTypeRefCycle:
    """
    >>> obj = ExtTypeRefCycle()
    >>> obj.ref = obj
    >>> find_name(ExtTypeRefCycle)
    0
    >>> obj = None
    >>> _ = gc.collect()
    >>> find_name(ExtTypeRefCycle)
    1
    """
    cdef public object ref
    cdef int x
    def __dealloc__(self):
        add_name(self)
        self.x = 1


class PySubTypeRefCycleDel(ExtTypeRefCycle):
    """
    >>> obj = PySubTypeRefCycleDel()
    >>> obj.ref = obj
    >>> find_name(PySubTypeRefCycleDel)
    0
    >>> obj = None
    >>> _ = gc.collect()

    >>> find_name(PySubTypeRefCycleDel)
    2
    """
    def __del__(self):
        add_name(self)


cdef class ExtTypeRefCycleRaise:
    """
    >>> obj = ExtTypeRefCycleRaise()
    >>> obj.ref = obj
    >>> find_name(ExtTypeRefCycleRaise)
    0
    >>> obj = None
    >>> _ = gc.collect()
    >>> find_name(ExtTypeRefCycleRaise)
    1
    """
    cdef public object ref
    def __dealloc__(self):
        add_name(self)
        raise RuntimeError("Cleaning up !")


class PySubTypeRefCycleRaise(ExtTypeRefCycleRaise):
    """
    >>> obj = PySubTypeRefCycleRaise()
    >>> obj.ref = obj
    >>> find_name(PySubTypeRefCycleRaise)
    0
    >>> obj = None
    >>> _ = gc.collect()
    >>> find_name(PySubTypeRefCycleRaise)
    1
    """
