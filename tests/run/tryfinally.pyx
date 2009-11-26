__doc__ = u"""
>>> try:
...     raise ValueError
... finally:
...     raise TypeError
Traceback (most recent call last):
TypeError
>>> finally_except()
Traceback (most recent call last):
TypeError

>>> call_try_return_with_exception()
1

>>> def try_return_py():
...    try:
...        return 1
...    finally:
...        return 2
>>> try_return_py()
2
>>> try_return_cy()
2
>>> call_try_return_c()
2

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
>>> try_return_none_1()
>>> try_return_none_2()
>>> try_break()
"""

def finally_except():
    try:
        raise ValueError
    finally:
        raise TypeError

def try_return_cy():
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
    return try_return_c()

cdef int try_return_with_exception():
    try:
        raise TypeError
    finally:
        return 1

def call_try_return_with_exception():
    return try_return_with_exception()

def try_return_temp(a):
    b = a+2
    try:
        c = a+b
        return c
    finally:
        print b-a

def try_continue(a):
    i=1
    for i in range(a):
        try:
            continue
        finally:
            i+=1
    return i


def try_return_none_1():
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
    try:
        return <object> _none()
    finally:
        return <object> _none()

def try_break():
    for a in "abcd":
        try:
            if a == 'c':
                break
        except:
            break
