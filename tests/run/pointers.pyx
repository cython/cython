cimport cython

cdef char* c_string = b'abcdefg'
cdef void* void_ptr = c_string

cdef i32 i = 42
cdef i32* int_ptr = &i

cdef f32 x = 42.2
cdef f32* float_ptr = &x

def compare():
    """
    >>> compare()
    True
    True
    True
    False
    False
    True
    True
    """
    print c_string == c_string
    print c_string == void_ptr
    print c_string is void_ptr
    print c_string != void_ptr
    print c_string is not void_ptr
    print void_ptr != int_ptr
    print void_ptr != float_ptr

def if_tests():
    """
    >>> if_tests()
    True
    True
    """
    if c_string == void_ptr:
        print true
    if c_string != void_ptr:
        print false
    if int_ptr != void_ptr:
        print true

def bool_binop():
    """
    >>> bool_binop()
    True
    """
    if c_string == void_ptr and c_string == c_string and int_ptr != void_ptr and void_ptr != float_ptr:
        print true

def bool_binop_truth(i32 x):
    """
    >>> bool_binop_truth(1)
    True
    True
    >>> bool_binop_truth(0)
    True
    """
    if c_string and void_ptr and int_ptr and (c_string == c_string or int_ptr != void_ptr):
        print true
    if c_string and x or not (void_ptr or int_ptr and float_ptr) or x:
        print true

def binop_voidptr(i32 x, i64 y, char* z):
    """
    >>> binop_voidptr(1, 3, b'abc')
    'void *'
    """
    result = &x and &y and z
    return cython.typeof(result)

def cond_expr_voidptr(i32 x, i64 y, char* z):
    """
    >>> cond_expr_voidptr(0, -1, b'abc')
    ('void *', 0)
    >>> cond_expr_voidptr(-1, 0, b'abc')
    ('void *', -1)
    >>> cond_expr_voidptr(-1, 0, b'')
    ('void *', 0)
    >>> cond_expr_voidptr(0, -1, b'')
    ('void *', -1)
    """
    result = &x if len(z) else &y
    assert sizeof(i64) >= sizeof(i32)
    assert -1 == <i32>(-1L)
    return cython.typeof(result), (<i32*>result)[0]
