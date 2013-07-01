# cython: linetrace=True
# mode: run
# tag: trace

from cpython.ref cimport PyObject

from cpython.pystate cimport (
    Py_tracefunc, PyFrameObject,
    PyTrace_CALL, PyTrace_EXCEPTION, PyTrace_LINE, PyTrace_RETURN,
    PyTrace_C_CALL, PyTrace_C_EXCEPTION, PyTrace_C_RETURN)

cdef extern from *:
    void PyEval_SetProfile(Py_tracefunc cfunc, object obj)
    void PyEval_SetTrace(Py_tracefunc cfunc, object obj)


map_trace_types = {
    PyTrace_CALL:        'call',
    PyTrace_EXCEPTION:   'exc',
    PyTrace_LINE:        'line',
    PyTrace_RETURN:      'return',
    PyTrace_C_CALL:      'ccall',
    PyTrace_C_EXCEPTION: 'cexc',
    PyTrace_C_RETURN:    'cret',
}.get


cdef int _trace_func(PyObject* _traceobj, PyFrameObject* _frame, int what, PyObject* arg) except -1:
    frame, traceobj = <object>_frame, <object>_traceobj
    traceobj.append((map_trace_types(what), frame.f_lineno - frame.f_code.co_firstlineno))
    return 0


def cy_add(a,b):
    x = a + b
    return x


def cy_add_nogil(a,b):
    cdef int z, x=a, y=b
    with nogil:    # no traces in this block !
        z = 0
        z += x + y
    return z


def run_trace(func, *args):
    """
    >>> def py_add(a,b):
    ...     x = a+b
    ...     return x
    >>> run_trace(py_add, 1, 2)
    [('call', 0), ('line', 1), ('line', 2), ('return', 2)]
    >>> run_trace(cy_add, 1, 2)
    [('call', 0), ('line', 1), ('line', 2), ('return', 2)]
    >>> run_trace(cy_add_nogil, 1, 2)
    [('call', 0), ('line', 1), ('line', 2), ('line', 5), ('return', 5)]
    """
    trace = []
    PyEval_SetTrace(<Py_tracefunc>_trace_func, trace)
    try:
        func(*args)
    finally:
        PyEval_SetTrace(NULL, None)
    return trace
