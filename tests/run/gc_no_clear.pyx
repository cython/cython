"""
Check that the @cython.no_gc_clear decorator disables generation of the
tp_clear slot so that __dealloc__ will still see the original reference
contents.

Discussed here: http://article.gmane.org/gmane.comp.python.cython.devel/14986
"""

cimport cython
from cpython.ref cimport PyObject, Py_TYPE

# Pull tp_clear for PyTypeObject as I did not find another way to access it
# from Cython code.

cdef extern from "Python.h":
    ctypedef struct PyTypeObject:
        void (*tp_clear)(object)


@cython.no_gc_clear
cdef class DisableTpClear:
    """
    An extension type that has a tp_clear method generated to test that it
    actually clears the references to NULL.

    >>> uut = DisableTpClear()
    >>> uut.call_tp_clear()
    >>> type(uut.requires_cleanup)
    <type 'list'>
    >>> del uut
    """

    cdef public object requires_cleanup

    def __cinit__(self):
        self.requires_cleanup = [
                "Some object that needs cleaning in __dealloc__"]

    cpdef public call_tp_clear(self):
        cdef PyTypeObject *pto = Py_TYPE(self)
        if pto.tp_clear != NULL:
            pto.tp_clear(self)
