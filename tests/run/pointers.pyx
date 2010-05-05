
cdef char* c_string = b'abcdefg'
cdef void* void_ptr = c_string

def compare():
    """
    >>> compare()
    True
    True
    True
    False
    False
    """
    print c_string == c_string
    print c_string == void_ptr
    print c_string is void_ptr
    print c_string != void_ptr
    print c_string is not void_ptr

def if_tests():
    """
    >>> if_tests()
    True
    """
    if c_string == void_ptr:
        print True
    if c_string != void_ptr:
        print False

def bool_binop():
    """
    >>> bool_binop()
    True
    """
    if c_string == void_ptr and c_string == c_string:
        print True

def bool_binop_truth(int x):
    """
    >>> bool_binop_truth(1)
    True
    True
    >>> bool_binop_truth(0)
    True
    """
    if c_string and void_ptr and c_string == c_string:
        print True
    if c_string and x or not void_ptr or x:
        print True
