__doc__ = u"""
Tests accessing attributes of extension type variables
set to None
"""

cimport cython

cdef class MyClass:
    cdef int a, b
    def __init__(self, a, b):
        self.a = a
        self.b = b

@cython.nonecheck(True)
def getattr_(MyClass var):
    """
    >>> obj = MyClass(2, 3)
    >>> getattr_(obj)
    2
    >>> getattr_(None)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'a'
    >>> setattr_(obj)
    >>> getattr_(obj)
    10
    """
    print var.a

@cython.nonecheck(True)
def setattr_(MyClass var):
    """
    >>> obj = MyClass(2, 3)
    >>> setattr_(obj)
    >>> setattr_(None)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'a'
    """
    var.a = 10

def some():
    return MyClass(4, 5)

@cython.nonecheck(True)
def checking(MyClass var):
    """
    >>> obj = MyClass(2, 3)
    >>> checking(obj)
    2
    2
    >>> checking(None)
    var is None
    """
    state = (var is None)
    if not state:
        print var.a
    if var is not None:
        print var.a
    else:
        print u"var is None"

@cython.nonecheck(True)
def check_and_assign(MyClass var):
    """
    >>> obj = MyClass(2, 3)
    >>> check_and_assign(obj)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'a'
    """
    if var is not None:
        print var.a
        var = None
        print var.a

@cython.nonecheck(True)
def check_buffer_get(object[int] buf):
    """
    >>> check_buffer_get(None)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    return buf[0]

@cython.nonecheck(True)
def check_buffer_set(object[int] buf):
    """
    >>> check_buffer_set(None)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    buf[0] = 1
