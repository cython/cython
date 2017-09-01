# cython: linetrace=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1
# mode: run
# tag: trace

from cpython.ref cimport PyObject, Py_INCREF, Py_XINCREF, Py_XDECREF

cdef extern from "frameobject.h":
    ctypedef struct PyFrameObject:
        PyObject *f_trace

from cpython.pystate cimport (
    Py_tracefunc,
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


cdef int trace_trampoline(PyObject* _traceobj, PyFrameObject* _frame, int what, PyObject* _arg) except -1:
    frame = <object>_frame
    traceobj = <object>_traceobj if _traceobj else None
    arg = <object>_arg if _arg else None

    if what == PyTrace_CALL:
        callback = traceobj
    else:
        callback = <object>_frame.f_trace

    if callback is None:
        return 0

    result = callback(frame, what, arg)

    # A bug in Py2.6 prevents us from calling the Python-level setter here,
    # or otherwise we would get miscalculated line numbers. Was fixed in Py2.7.
    cdef PyObject *tmp = _frame.f_trace
    Py_INCREF(result)
    _frame.f_trace = <PyObject*>result
    Py_XDECREF(tmp)

    if result is None:
        PyEval_SetTrace(NULL, None)
    return 0


def _create_trace_func(trace):
    def _trace_func(frame, event, arg):
        trace.append((map_trace_types(event), frame.f_lineno -
                                      frame.f_code.co_firstlineno))

        return _trace_func
    return _trace_func


def _create_failing_call_trace_func(trace):
    func = _create_trace_func(trace)
    def _trace_func(frame, event, arg):
        if event == PyTrace_CALL:
            raise ValueError("failing call trace!")

        func(frame, event, arg)
        return _trace_func

    return _trace_func


def _create__failing_line_trace_func(trace):
    func = _create_trace_func(trace)
    def _trace_func(frame, event, arg):
        if event == PyTrace_LINE and trace:
            if trace and trace[0] == frame.f_code.co_name:
                # first line in the right function => fail!
                raise ValueError("failing line trace!")

        func(frame, event, arg)
        return _trace_func
    return _trace_func

def _create_disable_tracing(trace):
    func = _create_trace_func(trace)
    def _trace_func(frame, event, arg):
        if frame.f_lineno - frame.f_code.co_firstlineno == 2:
            return None

        func(frame, event, arg)
        return _trace_func

    return _trace_func

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
    PyEval_SetTrace(<Py_tracefunc>trace_trampoline, _create_trace_func(trace))
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
    PyEval_SetTrace(<Py_tracefunc>trace_trampoline, _create_failing_call_trace_func(trace))
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
    PyEval_SetTrace(<Py_tracefunc>trace_trampoline, _create__failing_line_trace_func(trace))
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


def disable_trace(func, *args):
    """
    >>> def py_add(a,b):
    ...     x = a+b
    ...     return x
    >>> disable_trace(py_add, 1, 2)
    [('call', 0), ('line', 1)]
    >>> disable_trace(cy_add, 1, 2)
    [('call', 0), ('line', 1)]
    >>> disable_trace(cy_add_with_nogil, 1, 2)
    [('call', 0), ('line', 1)]
    """
    trace = []
    PyEval_SetTrace(<Py_tracefunc>trace_trampoline, _create_disable_tracing(trace))
    try:
        func(*args)
    finally:
        PyEval_SetTrace(NULL, None)
    return trace
