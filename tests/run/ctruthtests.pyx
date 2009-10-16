__doc__ = u"""
>>> test_int(0)
False
>>> test_int(1)
True

>>> test_short(0)
False
>>> test_short(1)
True

>>> test_Py_ssize_t(0)
False
>>> test_Py_ssize_t(1)
True

>>> test_ptr()
False
>>> test_ptr2()
2

>>> test_attr_int(TestExtInt(0))
False
>>> test_attr_int(TestExtInt(1))
True

>>> test_attr_ptr(TestExtPtr(0))
False
>>> test_attr_ptr(TestExtPtr(1))
True
"""

def test_ptr():
    cdef void* p = NULL
    if p:
        return True
    else:
        return False

def test_ptr2():
    cdef void* p1 = NULL
    cdef void* p2 = NULL
    p1 += 1

    if p1 and p2:
        return 1
    elif p1 or p2:
        return 2
    else:
        return 3

def test_int(int i):
    if i:
        return True
    else:
        return False

def test_short(short i):
    if i:
        return True
    else:
        return False

def test_Py_ssize_t(Py_ssize_t i):
    if i:
        return True
    else:
        return False

cdef class TestExtInt:
    cdef int i
    def __init__(self, i): self.i = i

def test_attr_int(TestExtInt e):
    if e.i:
        return True
    else:
        return False

cdef class TestExtPtr:
    cdef void* p
    def __init__(self, int i): self.p = <void*>i

def test_attr_ptr(TestExtPtr e):
    if e.p:
        return True
    else:
        return False
