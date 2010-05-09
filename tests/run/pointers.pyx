
cdef char* c_string = b'abcdefg'
cdef void* void_ptr = c_string

cdef int i = 42
cdef int* int_ptr = &i

cdef float x = 42.2
cdef float* float_ptr = &x

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
        print True
    if c_string != void_ptr:
        print False
    if int_ptr != void_ptr:
        print True

def bool_binop():
    """
    >>> bool_binop()
    True
    """
    if c_string == void_ptr and c_string == c_string and int_ptr != void_ptr and void_ptr != float_ptr:
        print True

def bool_binop_truth(int x):
    """
    >>> bool_binop_truth(1)
    True
    True
    >>> bool_binop_truth(0)
    True
    """
    if c_string and void_ptr and int_ptr and (c_string == c_string or int_ptr != void_ptr):
        print True
    if c_string and x or not (void_ptr or int_ptr and float_ptr) or x:
        print True
