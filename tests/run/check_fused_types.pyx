cimport cython
cimport check_fused_types_pxd

ctypedef char *string_t
ctypedef cython.fused_type(int, long, float, string_t) fused_t
ctypedef cython.fused_type(int, long) other_t

cdef func(fused_t a, other_t b):
    cdef int int_a
    cdef string_t string_a
    cdef other_t other_a

    if fused_t is other_t:
        print 'fused_t is other_t'
        other_a = a

    if fused_t is int:
        print 'fused_t is int'
        int_a = a

    if fused_t is string_t:
        print 'fused_t is string_t'
        string_a = a

    if fused_t in check_fused_types_pxd.unresolved_t:
        print 'fused_t in unresolved_t'

    if int in check_fused_types_pxd.unresolved_t:
        print 'int in unresolved_t'

    if string_t in check_fused_types_pxd.unresolved_t:
        print 'string_t in unresolved_t'


def test_int_int():
    """
    >>> test_int_int()
    fused_t is other_t
    fused_t is int
    fused_t in unresolved_t
    int in unresolved_t
    """
    cdef int x = 1
    cdef int y = 2

    func(x, y)

def test_int_long():
    """
    >>> test_int_long()
    fused_t is int
    fused_t in unresolved_t
    int in unresolved_t
    """
    cdef int x = 1
    cdef long y = 2

    func(x, y)

def test_float_int():
    """
    >>> test_float_int()
    fused_t in unresolved_t
    int in unresolved_t
    """
    cdef float x = 1
    cdef int y = 2

    func(x, y)

def test_string_int():
    """
    >>> test_string_int()
    fused_t is string_t
    int in unresolved_t
    """
    cdef string_t x = b"spam"
    cdef int y = 2

    func(x, y)


cdef if_then_else(fused_t a, other_t b):
    cdef other_t other_a
    cdef string_t string_a
    cdef fused_t specific_a

    if fused_t is other_t:
        print 'fused_t is other_t'
        other_a = a
    elif fused_t is string_t:
        print 'fused_t is string_t'
        string_a = a
    else:
        print 'none of the above'
        specific_a = a

def test_if_then_else_long_long():
    """
    >>> test_if_then_else_long_long()
    fused_t is other_t
    """
    cdef long x = 0, y = 0
    if_then_else(x, y)

def test_if_then_else_string_int():
    """
    >>> test_if_then_else_string_int()
    fused_t is string_t
    """
    cdef string_t x = b"spam"
    cdef int y = 0
    if_then_else(x, y)

def test_if_then_else_float_int():
    """
    >>> test_if_then_else_float_int()
    none of the above
    """
    cdef float x = 0.0
    cdef int y = 1
    if_then_else(x, y)

