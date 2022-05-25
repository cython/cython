"""
Check that the @cython.no_gc_clear decorator disables generation of the
tp_clear slot so that __dealloc__ will still see the original reference
contents.

Discussed here: https://article.gmane.org/gmane.comp.python.cython.devel/14986
"""

cimport cython
from cpython.ref cimport PyObject, Py_TYPE

# Pull tp_clear for PyTypeObject as I did not find another way to access it
# from Cython code.

cdef extern from *:
    ctypedef struct PyTypeObject:
        void (*tp_clear)(object)

    ctypedef struct __pyx_CyFunctionObject:
        PyObject* func_closure


def is_tp_clear_null(obj):
    return (<PyTypeObject*>Py_TYPE(obj)).tp_clear is NULL


def is_closure_tp_clear_null(func):
    return is_tp_clear_null(
        <object>(<__pyx_CyFunctionObject*>func).func_closure)


@cython.no_gc_clear
cdef class DisableTpClear:
    """
    An extension type that has a tp_clear method generated to test that it
    actually clears the references to NULL.

    >>> uut = DisableTpClear()
    >>> is_tp_clear_null(uut)
    True
    >>> uut.call_tp_clear()
    >>> type(uut.requires_cleanup) == list
    True
    >>> del uut
    """

    cdef public object requires_cleanup

    def __cinit__(self):
        self.requires_cleanup = [
                "Some object that needs cleaning in __dealloc__"]

    def call_tp_clear(self):
        cdef PyTypeObject *pto = Py_TYPE(self)
        if pto.tp_clear != NULL:
            pto.tp_clear(self)


cdef class ReallowTpClear(DisableTpClear):
    """
    >>> import gc
    >>> obj = ReallowTpClear()
    >>> is_tp_clear_null(obj)
    False

    >>> obj.attr = obj  # create hard reference cycle
    >>> del obj; _ignore = gc.collect()

    # Problem: cannot really validate that the cycle was cleaned up without using weakrefs etc...
    """
    cdef public object attr


def test_closure_without_clear(str x):
    """
    >>> c = test_closure_without_clear('abc')
    >>> is_tp_clear_null(c)
    False
    >>> is_closure_tp_clear_null(c)
    True
    >>> c('cba')
    'abcxyzcba'
    """
    def c(str s):
        return x + 'xyz' + s
    return c


def test_closure_with_clear(list x):
    """
    >>> c = test_closure_with_clear(list('abc'))
    >>> is_tp_clear_null(c)
    False
    >>> is_closure_tp_clear_null(c)
    False
    >>> c('cba')
    'abcxyzcba'
    """
    def c(str s):
        return ''.join(x) + 'xyz' + s
    return c
