"""
Check that the @cython.no_gc decorator disables generation of the
tp_clear and tp_traverse slots, that is, disables cycle collection.
"""

cimport cython
from cpython.ref cimport PyObject, Py_TYPE

# Force non-gc'd PyTypeObject when safety is guaranteed by user but not provable

cdef extern from *:
    ctypedef struct PyTypeObject:
        void (*tp_clear)(object)
        void (*tp_traverse)(object)


def is_tp_clear_null(obj):
    return (<PyTypeObject*>Py_TYPE(obj)).tp_clear is NULL

def is_tp_traverse_null(obj):
    return (<PyTypeObject*>Py_TYPE(obj)).tp_traverse is NULL


@cython.no_gc
cdef class DisableGC:
    """
    An extension type that has tp_clear and tp_traverse methods generated 
    to test that it actually clears the references to NULL.

    >>> uut = DisableGC()
    >>> is_tp_clear_null(uut)
    True
    >>> is_tp_traverse_null(uut)
    True
    """

    cdef public object requires_cleanup

    def __cinit__(self):
        self.requires_cleanup = (
                "Tuples to strings don't really need cleanup, cannot take part of cycles",)

