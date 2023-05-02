cimport cython

ctypedef fused bunch_of_types:
    bytes
    int
    float

ctypedef fused string_t:
    cython.p_char
    bytes
    unicode

cdef cython.integral myfunc(cython.integral i, bunch_of_types s):
    # Only one of these branches will be compiled for each specialization!
    if cython.integral is int:
        print('i is int')
    elif cython.integral is long:
        print('i is long')
    else:
        print('i is short')

    if bunch_of_types in string_t:
        print("s is a string!")
    return i * 2

myfunc(<int> 5, b'm')  # will print "i is an int" and "s is a string"
myfunc(<long> 5, 3)    # will print "i is a long"
myfunc(<short> 5, 3)   # will print "i is a short"
