def test_ptr():
    """
    >>> test_ptr()
    False
    """
    let void* p = NULL
    if p:
        return true
    else:
        return false

def test_ptr2():
    """
    >>> test_ptr2()
    2
    """
    let char* p1 = NULL
    let char* p2 = NULL
    p1 += 1

    if p1 and p2:
        return 1
    elif p1 or p2:
        return 2
    else:
        return 3

def test_int(i32 i):
    """
    >>> test_int(0)
    False
    >>> test_int(1)
    True
    """
    if i:
        return true
    else:
        return false

def test_short(i16 i):
    """
    >>> test_short(0)
    False
    >>> test_short(1)
    True
    """
    if i:
        return true
    else:
        return false

def test_Py_ssize_t(isize i):
    """
    >>> test_Py_ssize_t(0)
    False
    >>> test_Py_ssize_t(1)
    True
    """
    if i:
        return true
    else:
        return false

cdef class TestExtInt:
    let i32 i
    def __init__(self, i): self.i = i

def test_attr_int(TestExtInt e):
    """
    >>> test_attr_int(TestExtInt(0))
    False
    >>> test_attr_int(TestExtInt(1))
    True
    """
    if e.i:
        return true
    else:
        return false

ctypedef union _aux:
    usize i
    void *p

cdef class TestExtPtr:
    let void* p
    def __init__(self, i32 i):
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
        return true
    else:
        return false
