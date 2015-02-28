# cython: linetrace=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1
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


cdef int _failing_call_trace_func(PyObject* _traceobj, PyFrameObject* _frame, int what, PyObject* arg) except -1:
    if what == PyTrace_CALL:
        raise ValueError("failing call trace!")
    return _trace_func(_traceobj, _frame, what, arg)


cdef int _failing_line_trace_func(PyObject* _traceobj, PyFrameObject* _frame, int what, PyObject* arg) except -1:
    if what == PyTrace_LINE and _traceobj:
        frame, traceobj = <object>_frame, <object>_traceobj
        if traceobj and traceobj[0] == frame.f_code.co_name:
            # first line in the right function => fail!
            raise ValueError("failing line trace!")
    return _trace_func(_traceobj, _frame, what, arg)


def cy_add(a,b):
    x = a + b     # 1
    return x      # 2


def cy_add_with_nogil(a,b):
    cdef int z, x=a, y=b         # 1
    with nogil:                  # 2
        z = 0                    # 3
        z += cy_add_nogil(x, y)  # 4
    return z                     # 5


cdef int cy_add_nogil(int a, int b) nogil except -1:
    x = a + b   # 1
    return x    # 2


def run_trace(func, *args):
    """
    >>> def py_add(a,b):
    ...     x = a+b
    ...     return x
    >>> run_trace(py_add, 1, 2)
    [('call', 0), ('line', 1), ('line', 2), ('return', 2)]
    >>> run_trace(cy_add, 1, 2)
    [('call', 0), ('line', 1), ('line', 2), ('return', 2)]
    >>> result = run_trace(cy_add_with_nogil, 1, 2)
    >>> result[:5]
    [('call', 0), ('line', 1), ('line', 2), ('line', 3), ('line', 4)]
    >>> result[5:9]
    [('call', 0), ('line', 1), ('line', 2), ('return', 2)]
    >>> result[9:]
    [('line', 2), ('line', 5), ('return', 5)]
    """
    trace = []
    PyEval_SetTrace(<Py_tracefunc>_trace_func, trace)
    try:
        func(*args)
    finally:
        PyEval_SetTrace(NULL, None)
    return trace


def fail_on_call_trace(func, *args):
    """
    >>> def py_add(a,b):
    ...     x = a+b
    ...     return x
    >>> fail_on_call_trace(py_add, 1, 2)
    Traceback (most recent call last):
    ValueError: failing call trace!
    """
    trace = []
    PyEval_SetTrace(<Py_tracefunc>_failing_call_trace_func, trace)
    try:
        func(*args)
    finally:
        PyEval_SetTrace(NULL, None)
    assert not trace


def fail_on_line_trace(fail_func):
    """
    >>> result = fail_on_line_trace(None)
    >>> len(result)
    17
    >>> result[:5]
    ['NO ERROR', ('call', 0), ('line', 1), ('line', 2), ('return', 2)]
    >>> result[5:10]
    [('call', 0), ('line', 1), ('line', 2), ('line', 3), ('line', 4)]
    >>> result[10:14]
    [('call', 0), ('line', 1), ('line', 2), ('return', 2)]
    >>> result[14:]
    [('line', 2), ('line', 5), ('return', 5)]

    >>> result = fail_on_line_trace('cy_add_with_nogil')
    failing line trace!
    >>> result
    ['cy_add_with_nogil', ('call', 0), ('line', 1), ('line', 2), ('return', 2), ('call', 0), ('return', 1)]

    >>> result = fail_on_line_trace('cy_add_nogil')
    failing line trace!
    >>> result[:5]
    ['cy_add_nogil', ('call', 0), ('line', 1), ('line', 2), ('return', 2)]
    >>> result[5:]
    [('call', 0), ('line', 1), ('line', 2), ('line', 3), ('line', 4), ('call', 0), ('return', 1), ('return', 4)]
    """
    cdef int x = 1
    trace = ['NO ERROR']
    exception = None
    PyEval_SetTrace(<Py_tracefunc>_failing_line_trace_func, trace)
    try:
        x += 1
        cy_add(1, 2)
        x += 1
        if fail_func:
            trace[0] = fail_func  # trigger error on first line
        x += 1
        cy_add_with_nogil(3, 4)
        x += 1
    except Exception as exc:
        exception = str(exc)
    finally:
        PyEval_SetTrace(NULL, None)
    if exception:
        print(exception)
    else:
        assert x == 5
    return trace
