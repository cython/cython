# cython: linetrace=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1
# mode: run
# tag: trace

import sys
import gc
from contextlib import contextmanager

from cpython.ref cimport PyObject, Py_INCREF, Py_XDECREF

cdef extern from "frameobject.h":
    ctypedef struct PyFrameObject:
        PyObject *f_trace

from cpython.pystate cimport (
    Py_tracefunc,
    PyTrace_CALL, PyTrace_EXCEPTION, PyTrace_LINE, PyTrace_RETURN,
    PyTrace_C_CALL, PyTrace_C_EXCEPTION, PyTrace_C_RETURN)

cdef extern from *:
    void PyEval_SetProfile(Py_tracefunc cfunc, PyObject *obj)
    void PyEval_SetTrace(Py_tracefunc cfunc, PyObject *obj)


map_trace_types = {
    PyTrace_CALL:        'call',
    PyTrace_EXCEPTION:   'exception',
    PyTrace_LINE:        'line',
    PyTrace_RETURN:      'return',
    PyTrace_C_CALL:      'ccall',
    PyTrace_C_EXCEPTION: 'cexc',
    PyTrace_C_RETURN:    'cret',
}.get


cdef int trace_trampoline(PyObject* _traceobj, PyFrameObject* _frame, int what, PyObject* _arg) except -1:
    """
    This is (more or less) what CPython does in sysmodule.c, function trace_trampoline().
    """
    cdef PyObject *tmp

    if what == PyTrace_CALL:
        if _traceobj is NULL:
            return 0
        callback = <object>_traceobj
    elif _frame.f_trace:
        callback = <object>_frame.f_trace
    else:
        return 0

    frame = <object>_frame
    arg = <object>_arg if _arg else None

    try:
        result = callback(frame, what, arg)
    except:
        PyEval_SetTrace(NULL, NULL)
        tmp = _frame.f_trace
        _frame.f_trace = NULL
        Py_XDECREF(tmp)
        raise

    if result is not None:
        # A bug in Py2.6 prevents us from calling the Python-level setter here,
        # or otherwise we would get miscalculated line numbers. Was fixed in Py2.7.
        tmp = _frame.f_trace
        Py_INCREF(result)
        _frame.f_trace = <PyObject*>result
        Py_XDECREF(tmp)

    return 0


def _create_trace_func(trace):
    local_names = {}

    def _trace_func(frame, event, arg):
        trace.append((frame.f_code.co_name, map_trace_types(event, event), frame.f_lineno - frame.f_code.co_firstlineno))

        lnames = frame.f_code.co_varnames
        if frame.f_code.co_name in local_names:
            assert lnames == local_names[frame.f_code.co_name]
        else:
            local_names[frame.f_code.co_name] = lnames

        # Currently, the locals dict is empty for Cython code, but not for Python code.
        if frame.f_code.co_name.startswith('py_'):
            # Change this when we start providing proper access to locals.
            assert frame.f_locals, frame.f_code.co_name
        else:
            assert not frame.f_locals, frame.f_code.co_name

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
            PyEval_SetTrace(NULL, NULL)
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


def global_name(global_name):
    # See GH #1836: accessing "frame.f_locals" deletes locals from globals dict.
    return global_name + 321


cdef int cy_add_nogil(int a, int b) except -1 nogil:
    x = a + b   # 1
    return x    # 2


def cy_try_except(func):
    try:
        return func()
    except KeyError as exc:
        raise AttributeError(exc.args[0])


# CPython 3.11 has an issue when these Python functions are implemented inside of doctests and the trace function fails.
# https://github.com/python/cpython/issues/94381
plain_python_functions = {}
exec("""
def py_add(a,b):
    x = a+b
    return x

def py_add_with_nogil(a,b):
    x=a; y=b                     # 1
    for _ in range(1):           # 2
        z = 0                    # 3
        z += py_add(x, y)        # 4
    return z

def py_return(retval=123): return retval

def py_try_except(func):
    try:
        return func()
    except KeyError as exc:
        raise AttributeError(exc.args[0])
""", plain_python_functions)


@contextmanager
def gc_off():
    was_enabled = gc.isenabled()
    gc.disable()
    try:
        yield
    finally:
        if was_enabled:
            gc.enable()


def run_trace(func, *args, bint with_sys=False):
    """
    >>> py_add = plain_python_functions['py_add']
    >>> run_trace(py_add, 1, 2)
    [('py_add', 'call', 0), ('py_add', 'line', 1), ('py_add', 'line', 2), ('py_add', 'return', 2)]
    >>> run_trace(cy_add, 1, 2)
    [('cy_add', 'call', 0), ('cy_add', 'line', 1), ('cy_add', 'line', 2), ('cy_add', 'return', 2)]

    >>> run_trace(py_add, 1, 2, with_sys=True)
    [('py_add', 'call', 0), ('py_add', 'line', 1), ('py_add', 'line', 2), ('py_add', 'return', 2)]
    >>> run_trace(cy_add, 1, 2, with_sys=True)
    [('cy_add', 'call', 0), ('cy_add', 'line', 1), ('cy_add', 'line', 2), ('cy_add', 'return', 2)]

    >>> result = run_trace(cy_add_with_nogil, 1, 2)
    >>> result[:5]
    [('cy_add_with_nogil', 'call', 0), ('cy_add_with_nogil', 'line', 1), ('cy_add_with_nogil', 'line', 2), ('cy_add_with_nogil', 'line', 3), ('cy_add_with_nogil', 'line', 4)]
    >>> result[5:9]
    [('cy_add_nogil', 'call', 0), ('cy_add_nogil', 'line', 1), ('cy_add_nogil', 'line', 2), ('cy_add_nogil', 'return', 2)]
    >>> result[9:]
    [('cy_add_with_nogil', 'line', 2), ('cy_add_with_nogil', 'line', 5), ('cy_add_with_nogil', 'return', 5)]

    >>> result = run_trace(cy_add_with_nogil, 1, 2, with_sys=True)
    >>> result[:5]  # sys
    [('cy_add_with_nogil', 'call', 0), ('cy_add_with_nogil', 'line', 1), ('cy_add_with_nogil', 'line', 2), ('cy_add_with_nogil', 'line', 3), ('cy_add_with_nogil', 'line', 4)]
    >>> result[5:9]  # sys
    [('cy_add_nogil', 'call', 0), ('cy_add_nogil', 'line', 1), ('cy_add_nogil', 'line', 2), ('cy_add_nogil', 'return', 2)]
    >>> result[9:]  # sys
    [('cy_add_with_nogil', 'line', 2), ('cy_add_with_nogil', 'line', 5), ('cy_add_with_nogil', 'return', 5)]

    >>> py_add_with_nogil = plain_python_functions['py_add_with_nogil']
    >>> result = run_trace(py_add_with_nogil, 1, 2)
    >>> result[:5]  # py
    [('py_add_with_nogil', 'call', 0), ('py_add_with_nogil', 'line', 1), ('py_add_with_nogil', 'line', 2), ('py_add_with_nogil', 'line', 3), ('py_add_with_nogil', 'line', 4)]
    >>> result[5:9]  # py
    [('py_add', 'call', 0), ('py_add', 'line', 1), ('py_add', 'line', 2), ('py_add', 'return', 2)]
    >>> result[9:]  # py
    [('py_add_with_nogil', 'line', 2), ('py_add_with_nogil', 'line', 5), ('py_add_with_nogil', 'return', 5)]

    >>> run_trace(global_name, 123)
    [('global_name', 'call', 0), ('global_name', 'line', 2), ('global_name', 'return', 2)]
    >>> run_trace(global_name, 111)
    [('global_name', 'call', 0), ('global_name', 'line', 2), ('global_name', 'return', 2)]
    >>> run_trace(global_name, 111, with_sys=True)
    [('global_name', 'call', 0), ('global_name', 'line', 2), ('global_name', 'return', 2)]
    >>> run_trace(global_name, 111, with_sys=True)
    [('global_name', 'call', 0), ('global_name', 'line', 2), ('global_name', 'return', 2)]
    """
    trace = []
    trace_func = _create_trace_func(trace)
    with gc_off():
        if with_sys:
            sys.settrace(trace_func)
        else:
            PyEval_SetTrace(<Py_tracefunc>trace_trampoline, <PyObject*>trace_func)
        try:
            func(*args)
        finally:
            if with_sys:
                sys.settrace(None)
            else:
                PyEval_SetTrace(NULL, NULL)
    return trace


def run_trace_with_exception(func, bint with_sys=False, bint fail=False, call_func=cy_try_except):
    """
    >>> py_return = plain_python_functions["py_return"]
    >>> run_trace_with_exception(py_return)
    OK: 123
    [('cy_try_except', 'call', 0), ('cy_try_except', 'line', 1), ('cy_try_except', 'line', 2), ('py_return', 'call', 0), ('py_return', 'line', 0), ('py_return', 'return', 0), ('cy_try_except', 'return', 2)]
    >>> run_trace_with_exception(py_return, with_sys=True)
    OK: 123
    [('cy_try_except', 'call', 0), ('cy_try_except', 'line', 1), ('cy_try_except', 'line', 2), ('py_return', 'call', 0), ('py_return', 'line', 0), ('py_return', 'return', 0), ('cy_try_except', 'return', 2)]

    >>> run_trace_with_exception(py_return, fail=True)
    ValueError('failing line trace!')
    [('cy_try_except', 'call', 0)]

    #>>> run_trace_with_exception(lambda: 123, with_sys=True, fail=True)
    #ValueError('huhu')
    #[('call', 0), ('line', 1), ('line', 2), ('call', 0), ('line', 0), ('return', 0), ('return', 2)]

    >>> def py_raise_exc(exc=KeyError('huhu')): raise exc
    >>> run_trace_with_exception(py_raise_exc)
    AttributeError('huhu')
    [('cy_try_except', 'call', 0), ('cy_try_except', 'line', 1), ('cy_try_except', 'line', 2), ('py_raise_exc', 'call', 0), ('py_raise_exc', 'line', 0), ('py_raise_exc', 'exception', 0), ('py_raise_exc', 'return', 0), ('cy_try_except', 'line', 3), ('cy_try_except', 'line', 4), ('cy_try_except', 'return', 4)]
    >>> run_trace_with_exception(py_raise_exc, with_sys=True)
    AttributeError('huhu')
    [('cy_try_except', 'call', 0), ('cy_try_except', 'line', 1), ('cy_try_except', 'line', 2), ('py_raise_exc', 'call', 0), ('py_raise_exc', 'line', 0), ('py_raise_exc', 'exception', 0), ('py_raise_exc', 'return', 0), ('cy_try_except', 'line', 3), ('cy_try_except', 'line', 4), ('cy_try_except', 'return', 4)]
    >>> run_trace_with_exception(py_raise_exc, fail=True)
    ValueError('failing line trace!')
    [('cy_try_except', 'call', 0)]

    # Py3.9 issues a spurious additional line event after raising the final exception, so use +ELLIPSIS.
    >>> py_try_except = plain_python_functions['py_try_except']
    >>> run_trace_with_exception(py_raise_exc, call_func=py_try_except)  # doctest: +ELLIPSIS
    AttributeError('huhu')
    [('py_try_except', 'call', 0), ('py_try_except', 'line', 1), ('py_try_except', 'line', 2), ('py_raise_exc', 'call', 0), ('py_raise_exc', 'line', 0), ('py_raise_exc', 'exception', 0), ('py_raise_exc', 'return', 0), ('py_try_except', 'exception', 2), ('py_try_except', 'line', 3), ('py_try_except', 'line', 4), ('py_try_except', 'exception', 4), ...('py_try_except', 'return', 4)]
    >>> run_trace_with_exception(py_raise_exc, with_sys=True, call_func=py_try_except)  # doctest: +ELLIPSIS
    AttributeError('huhu')
    [('py_try_except', 'call', 0), ('py_try_except', 'line', 1), ('py_try_except', 'line', 2), ('py_raise_exc', 'call', 0), ('py_raise_exc', 'line', 0), ('py_raise_exc', 'exception', 0), ('py_raise_exc', 'return', 0), ('py_try_except', 'exception', 2), ('py_try_except', 'line', 3), ('py_try_except', 'line', 4), ('py_try_except', 'exception', 4), ...('py_try_except', 'return', 4)]
    >>> run_trace_with_exception(py_raise_exc, fail=True, call_func=py_try_except)
    ValueError('failing line trace!')
    [('py_try_except', 'call', 0)]

    #>>> run_trace_with_exception(raise_exc, with_sys=True, fail=True)
    #ValueError('huhu')
    #[('call', 0), ('line', 1), ('line', 2), ('call', 0), ('line', 0), ('exception', 0), ('return', 0), ('line', 3), ('line', 4), ('return', 4)]
    """
    trace = [call_func.__name__ if fail else 'NO ERROR']
    trace_func = _create__failing_line_trace_func(trace) if fail else _create_trace_func(trace)
    with gc_off():
        if with_sys:
            sys.settrace(trace_func)
        else:
            PyEval_SetTrace(<Py_tracefunc>trace_trampoline, <PyObject*>trace_func)
        try:
            try:
                retval = call_func(func)
            except ValueError as exc:
                print("%s(%r)" % (type(exc).__name__, str(exc)))
            except AttributeError as exc:
                print("%s(%r)" % (type(exc).__name__, str(exc)))
            else:
                print('OK: %r' % retval)
        finally:
            if with_sys:
                sys.settrace(None)
            else:
                PyEval_SetTrace(NULL, NULL)
    return trace[1:]


def fail_on_call_trace(func, *args):
    """
    >>> py_add = plain_python_functions["py_add"]
    >>> fail_on_call_trace(py_add, 1, 2)
    Traceback (most recent call last):
    ValueError: failing call trace!

    >>> fail_on_call_trace(cy_add, 1, 2)
    Traceback (most recent call last):
    ValueError: failing call trace!
    """
    trace = []
    trace_func = _create_failing_call_trace_func(trace)
    with gc_off():
        PyEval_SetTrace(<Py_tracefunc>trace_trampoline, <PyObject*>trace_func)
        try:
            func(*args)
        finally:
            PyEval_SetTrace(NULL, NULL)
    assert not trace


def fail_on_line_trace(fail_func, add_func, nogil_add_func):
    """
    >>> result = fail_on_line_trace(None, cy_add, cy_add_with_nogil)
    >>> len(result)
    17
    >>> result[:5]
    ['NO ERROR', ('cy_add', 'call', 0), ('cy_add', 'line', 1), ('cy_add', 'line', 2), ('cy_add', 'return', 2)]
    >>> result[5:10]
    [('cy_add_with_nogil', 'call', 0), ('cy_add_with_nogil', 'line', 1), ('cy_add_with_nogil', 'line', 2), ('cy_add_with_nogil', 'line', 3), ('cy_add_with_nogil', 'line', 4)]
    >>> result[10:14]
    [('cy_add_nogil', 'call', 0), ('cy_add_nogil', 'line', 1), ('cy_add_nogil', 'line', 2), ('cy_add_nogil', 'return', 2)]
    >>> result[14:]
    [('cy_add_with_nogil', 'line', 2), ('cy_add_with_nogil', 'line', 5), ('cy_add_with_nogil', 'return', 5)]

    >>> py_add = plain_python_functions["py_add"]
    >>> py_add_with_nogil = plain_python_functions['py_add_with_nogil']
    >>> result = fail_on_line_trace(None, py_add, py_add_with_nogil)
    >>> len(result)
    17
    >>> result[:5]  # py
    ['NO ERROR', ('py_add', 'call', 0), ('py_add', 'line', 1), ('py_add', 'line', 2), ('py_add', 'return', 2)]
    >>> result[5:10]  # py
    [('py_add_with_nogil', 'call', 0), ('py_add_with_nogil', 'line', 1), ('py_add_with_nogil', 'line', 2), ('py_add_with_nogil', 'line', 3), ('py_add_with_nogil', 'line', 4)]
    >>> result[10:14]  # py
    [('py_add', 'call', 0), ('py_add', 'line', 1), ('py_add', 'line', 2), ('py_add', 'return', 2)]
    >>> result[14:]  # py
    [('py_add_with_nogil', 'line', 2), ('py_add_with_nogil', 'line', 5), ('py_add_with_nogil', 'return', 5)]

    >>> result = fail_on_line_trace('cy_add_with_nogil', cy_add, cy_add_with_nogil)
    failing line trace!
    >>> result
    ['cy_add_with_nogil', ('cy_add', 'call', 0), ('cy_add', 'line', 1), ('cy_add', 'line', 2), ('cy_add', 'return', 2), ('cy_add_with_nogil', 'call', 0)]

    >>> result = fail_on_line_trace('py_add_with_nogil', py_add, py_add_with_nogil)  # py
    failing line trace!
    >>> result  # py
    ['py_add_with_nogil', ('py_add', 'call', 0), ('py_add', 'line', 1), ('py_add', 'line', 2), ('py_add', 'return', 2), ('py_add_with_nogil', 'call', 0)]

    >>> result = fail_on_line_trace('cy_add_nogil', cy_add, cy_add_with_nogil)
    failing line trace!
    >>> result[:5]
    ['cy_add_nogil', ('cy_add', 'call', 0), ('cy_add', 'line', 1), ('cy_add', 'line', 2), ('cy_add', 'return', 2)]
    >>> result[5:]
    [('cy_add_with_nogil', 'call', 0), ('cy_add_with_nogil', 'line', 1), ('cy_add_with_nogil', 'line', 2), ('cy_add_with_nogil', 'line', 3), ('cy_add_with_nogil', 'line', 4), ('cy_add_nogil', 'call', 0)]

    >>> result = fail_on_line_trace('py_add', py_add, py_add_with_nogil)  # py
    failing line trace!
    >>> result[:5]  # py
    ['py_add', ('py_add', 'call', 0), ('py_add', 'line', 1), ('py_add', 'line', 2), ('py_add', 'return', 2)]
    >>> result[5:]  # py
    [('py_add_with_nogil', 'call', 0), ('py_add_with_nogil', 'line', 1), ('py_add_with_nogil', 'line', 2), ('py_add_with_nogil', 'line', 3), ('py_add_with_nogil', 'line', 4), ('py_add', 'call', 0)]
    """
    cdef int x = 1
    trace = ['NO ERROR']
    exception = None
    trace_func = _create__failing_line_trace_func(trace)
    with gc_off():
        PyEval_SetTrace(<Py_tracefunc>trace_trampoline, <PyObject*>trace_func)
        try:
            x += 1
            add_func(1, 2)
            x += 1
            if fail_func:
                trace[0] = fail_func  # trigger error on first line
            x += 1
            nogil_add_func(3, 4)
            x += 1
        except Exception as exc:
            exception = str(exc)
        finally:
            PyEval_SetTrace(NULL, NULL)
    if exception:
        print(exception)
    else:
        assert x == 5
    return trace


def disable_trace(func, *args, bint with_sys=False):
    """
    >>> py_add = plain_python_functions["py_add"]
    >>> disable_trace(py_add, 1, 2)
    [('py_add', 'call', 0), ('py_add', 'line', 1)]
    >>> disable_trace(py_add, 1, 2, with_sys=True)
    [('py_add', 'call', 0), ('py_add', 'line', 1)]

    >>> disable_trace(cy_add, 1, 2)
    [('cy_add', 'call', 0), ('cy_add', 'line', 1)]
    >>> disable_trace(cy_add, 1, 2, with_sys=True)
    [('cy_add', 'call', 0), ('cy_add', 'line', 1)]

    >>> disable_trace(cy_add_with_nogil, 1, 2)
    [('cy_add_with_nogil', 'call', 0), ('cy_add_with_nogil', 'line', 1)]
    >>> disable_trace(cy_add_with_nogil, 1, 2, with_sys=True)
    [('cy_add_with_nogil', 'call', 0), ('cy_add_with_nogil', 'line', 1)]
    """
    trace = []
    trace_func = _create_disable_tracing(trace)
    with gc_off():
        if with_sys:
            sys.settrace(trace_func)
        else:
            PyEval_SetTrace(<Py_tracefunc>trace_trampoline, <PyObject*>trace_func)
        try:
            func(*args)
        finally:
            if with_sys:
                sys.settrace(None)
            else:
                PyEval_SetTrace(NULL, NULL)
    return trace
