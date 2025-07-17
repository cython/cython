def test_ptr():
    """
    >>> test_ptr()
    False
    """
    cdef void* p = NULL
    if p:
        return True
    else:
        return False

def test_ptr2():
    """
    >>> test_ptr2()
    2
    """
    cdef char* p1 = NULL
    cdef char* p2 = NULL
    p1 += 1

    if p1 and p2:
        return 1
    elif p1 or p2:
        return 2
    else:
        return 3

def test_int(int i):
    """
    >>> test_int(0)
    False
    >>> test_int(1)
    True
    """
    if i:
        return True
    else:
        return False

def test_short(short i):
    """
    >>> test_short(0)
    False
    >>> test_short(1)
    True
    """
    if i:
        return True
    else:
        return False

def test_Py_ssize_t(Py_ssize_t i):
    """
    >>> test_Py_ssize_t(0)
    False
    >>> test_Py_ssize_t(1)
    True
    """
    if i:
        return True
    else:
        return False

cdef class TestExtInt:
    cdef int i
    def __init__(self, i): self.i = i

def test_attr_int(TestExtInt e):
    """
    >>> test_attr_int(TestExtInt(0))
    False
    >>> test_attr_int(TestExtInt(1))
    True
    """
    if e.i:
        return True
    else:
        return False

ctypedef union _aux:
    size_t i
    void *p

cdef class TestExtPtr:
    cdef void* p
    def __init__(self, int i):
        cdef _aux aux
        aux.i = i
        self.p = aux.p

def test_attr_ptr(TestExtPtr e):
    """
    >>> test_attr_ptr(TestExtPtr(0))
    False
    >>> test_attr_ptr(TestExtPtr(1))
    True
    """
    if e.p:
        return True
    else:
        return False
