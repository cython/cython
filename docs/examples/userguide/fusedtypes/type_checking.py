bunch_of_types = cython.fused_type(bytes, cython.int, cython.float)






string_t = cython.fused_type(cython.p_char, bytes, unicode)



@cython.cfunc
def myfunc(i: cython.integral, s: bunch_of_types) -> cython.integral:
    # Only one of these branches will be compiled for each specialization!
    if cython.integral is int:
        print('i is an int')
    elif cython.integral is long:
        print('i is a long')
    else:
        print('i is a short')

    if bunch_of_types in string_t:
        print("s is a string!")
    return i * 2

myfunc(cython.cast(cython.int, 5), b'm')  # will print "i is an int" and "s is a string"
myfunc(cython.cast(cython.long, 5), 3)    # will print "i is a long"
myfunc(cython.cast(cython.short, 5), 3)   # will print "i is a short"
