# mode: run
# tag: tryfinally

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
