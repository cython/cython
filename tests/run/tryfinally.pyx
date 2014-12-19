# mode: run
# tag: tryfinally

import sys
IS_PY3 = sys.version_info[0] >= 3

cimport cython

try:
    next
except NameError:
    def next(it): return it.next()


def finally_except():
    """
    >>> try:
    ...     raise ValueError
    ... finally:
    ...     raise TypeError
    Traceback (most recent call last):
    TypeError
    >>> finally_except()
    Traceback (most recent call last):
    TypeError
    """
    try:
        raise ValueError
    finally:
        raise TypeError


def finally_pass():
    """
    >>> finally_pass()
    Traceback (most recent call last):
    ValueError
    """
    try:
        raise ValueError()
    finally:
        pass


def except_finally_reraise():
    """
    >>> def py_check():
    ...     try: raise ValueError
    ...     except ValueError:
    ...         for i in range(2):
    ...             try: raise TypeError
    ...             finally:
    ...                 break
    ...         assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
    ...         raise
    ...
    >>> py_check()
    Traceback (most recent call last):
    ValueError
    >>> except_finally_reraise()
    Traceback (most recent call last):
    ValueError
    """
    try:
        raise ValueError
    except ValueError:
        for i in range(2):
            try:
                raise TypeError
            finally:
                break
        assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
        raise


def except_finally_reraise_new():
    """
    >>> def py_check():
    ...     try: raise ValueError
    ...     except ValueError:
    ...         try: raise TypeError
    ...         finally:
    ...             raise
    >>> try: py_check()
    ... except ValueError: assert not IS_PY3
    ... except TypeError: assert IS_PY3
    ... else: assert False
    >>> try: except_finally_reraise_new()
    ... except TypeError: pass  # currently only Py3 semantics implemented
    ... else: assert False
    """
    try:
        raise ValueError
    except ValueError:
        try:
            raise TypeError
        finally:
            raise


def finally_exception_check_return():
    """
    >>> if not IS_PY3:
    ...     sys.exc_clear()
    >>> def py_check():
    ...     try: raise ValueError()
    ...     finally:
    ...         if IS_PY3:
    ...             assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
    ...         else:
    ...             assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    ...         return 1
    >>> py_check()
    1
    >>> finally_exception_check_return()
    1
    """
    try:
        raise ValueError()
    finally:
        if IS_PY3:
            assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
        else:
            assert sys.exc_info() == (None, None, None), str(sys.exc_info())
        return 1


cdef void swallow():
    try:
        raise TypeError()
    except:
        return


def finally_exception_check_swallow():
    """
    >>> if not IS_PY3:
    ...     sys.exc_clear()
    >>> def swallow():
    ...     try: raise TypeError()
    ...     except: return
    >>> def py_check():
    ...     try: raise ValueError()
    ...     finally:
    ...         if IS_PY3:
    ...             assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
    ...         else:
    ...             assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    ...         swallow()
    ...         if IS_PY3:
    ...             assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
    ...         else:
    ...             assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    >>> py_check()
    Traceback (most recent call last):
    ValueError
    >>> if not IS_PY3:
    ...     sys.exc_clear()
    >>> finally_exception_check_swallow()
    Traceback (most recent call last):
    ValueError
    """
    try:
        raise ValueError()
    finally:
        if IS_PY3:
            assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
        else:
            assert sys.exc_info() == (None, None, None), str(sys.exc_info())
        swallow()
        if IS_PY3:
            assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
        else:
            assert sys.exc_info() == (None, None, None), str(sys.exc_info())


def finally_exception_break_check():
    """
    >>> if not IS_PY3:
    ...     sys.exc_clear()
    >>> def py_check():
    ...     i = None
    ...     for i in range(2):
    ...         try: raise ValueError()
    ...         finally:
    ...             if IS_PY3:
    ...                 assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
    ...             else:
    ...                 assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    ...             break
    ...     assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    ...     return i
    >>> py_check()
    0
    >>> finally_exception_break_check()
    0
    """
    i = None
    for i in range(2):
        try:
            raise ValueError()
        finally:
            if IS_PY3:
                assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
            else:
                assert sys.exc_info() == (None, None, None), str(sys.exc_info())
            break
    assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    return i


def finally_exception_break_check_with_swallowed_raise():
    """
    >>> if not IS_PY3:
    ...     sys.exc_clear()
    >>> def swallow():
    ...     try: raise TypeError()
    ...     except: return
    >>> def py_check():
    ...     i = None
    ...     for i in range(2):
    ...         try: raise ValueError()
    ...         finally:
    ...             if IS_PY3:
    ...                 assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
    ...             else:
    ...                 assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    ...             swallow()
    ...             if IS_PY3:
    ...                 assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
    ...             else:
    ...                 assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    ...             break
    ...     assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    ...     return i
    >>> py_check()
    0
    >>> finally_exception_break_check_with_swallowed_raise()
    0
    """
    i = None
    for i in range(2):
        try:
            raise ValueError()
        finally:
            if IS_PY3:
                assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
            else:
                assert sys.exc_info() == (None, None, None), str(sys.exc_info())
            swallow()
            if IS_PY3:
                assert sys.exc_info()[0] == ValueError, str(sys.exc_info())
            else:
                assert sys.exc_info() == (None, None, None), str(sys.exc_info())
            break
    assert sys.exc_info() == (None, None, None), str(sys.exc_info())
    return i


def try_return_cy():
    """
    >>> def try_return_py():
    ...    try:
    ...        return 1
    ...    finally:
    ...        return 2
    >>> try_return_py()
    2
    >>> try_return_cy()
    2
    """
    try:
        return 1
    finally:
        return 2

cdef int try_return_c():
    try:
        return 1
    finally:
        return 2

def call_try_return_c():
    """
    >>> call_try_return_c()
    2
    """
    return try_return_c()

cdef int try_return_with_exception():
    try:
        raise TypeError
    finally:
        return 1

def call_try_return_with_exception():
    """
    >>> call_try_return_with_exception()
    1
    """
    return try_return_with_exception()

def try_return_temp(a):
    b = a+2
    try:
        c = a+b
        return c
    finally:
        print b-a

def try_continue(a):
    """
    >>> i=1
    >>> for i in range(3):
    ...     try:
    ...         continue
    ...     finally:
    ...         i+=1
    >>> i
    3
    >>> try_continue(3)
    3
    """
    i=1
    for i in range(a):
        try:
            continue
        finally:
            i+=1
    return i


def try_return_none_1():
    """
    >>> try_return_none_1()
    """
    try:
        return
    finally:
        return

cdef extern from *:
    ctypedef struct PyObject
    void Py_INCREF(object)

cdef PyObject* _none():
    ret = None
    Py_INCREF(ret)
    return <PyObject*> ret

def try_return_none_2():
    """
    >>> try_return_none_2()
    """
    try:
        return <object> _none()
    finally:
        return <object> _none()

def try_break():
    """
    >>> try_break()
    """
    for a in "abcd":
        try:
            if a == 'c':
                break
        except:
            break


def empty_try():
    """
    >>> empty_try()
    1
    """
    try:
        pass
    finally:
        return 1


def empty_try_in_except_raise(raise_in_finally):
    """
    >>> empty_try_in_except_raise(False)
    Traceback (most recent call last):
    ValueError: HUHU
    >>> empty_try_in_except_raise(True)
    Traceback (most recent call last):
    TypeError: OLA
    """
    try:
        raise ValueError("HUHU")
    except ValueError:
        try:
            pass
        finally:
            if raise_in_finally:
                raise TypeError('OLA')
        raise


def try_all_cases(x):
    """
    >>> try_all_cases(None)
    2
    >>> try_all_cases('break')
    4
    >>> try_all_cases('raise')
    Traceback (most recent call last):
    ValueError
    >>> try_all_cases('return')
    3
    >>> try_all_cases('tryraise')
    Traceback (most recent call last):
    TypeError
    >>> try_all_cases('trybreak')
    4
    """
    for i in range(3):
        try:
            if i == 0:
                pass
            elif i == 1:
                continue
            elif x == 'trybreak':
                break
            elif x == 'tryraise':
                raise TypeError()
            else:
                return 2
        finally:
            if x == 'raise':
                raise ValueError()
            elif x == 'break':
                break
            elif x == 'return':
                return 3
    return 4


def finally_yield(x):
    """
    >>> g = finally_yield(None)
    >>> next(g)  # 1
    1
    >>> next(g)  # 2
    1
    >>> next(g)  # 3
    Traceback (most recent call last):
    StopIteration

    >>> g = finally_yield('raise')
    >>> next(g)  # raise 1
    1
    >>> next(g)  # raise 2
    1
    >>> next(g)  # raise 3
    Traceback (most recent call last):
    TypeError

    >>> g = finally_yield('break')
    >>> next(g)   # break 1
    1
    >>> next(g)   # break 2
    1
    >>> next(g)   # break 3
    Traceback (most recent call last):
    StopIteration
    """
    for i in range(3):
        try:
            if i == 0:
                continue
            elif x == 'raise':
                raise TypeError()
            elif x == 'break':
                break
            else:
                return
        finally:
            yield 1
