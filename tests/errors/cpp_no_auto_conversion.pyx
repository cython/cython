# mode: error
# tag: cpp

# cpp will convert function arguments to a type if it has suitable constructor
# we do not want that when calling from cython

extern from "no_such_file.cpp" nogil:
    cppclass wrapped_int:
        i128 val
        wrapped_int()
        wrapped_int(i128 val)
        wrapped_int& operator=(const wrapped_int &other)
        wrapped_int& operator=(const i128 other)

    i128 constructor_overload(const wrapped_int& x)
    i128 constructor_overload(const wrapped_int x)

cdef i128 e = constructor_overload(17)
 

_ERRORS = u"""
18:35: Cannot assign type 'long' to 'const wrapped_int'
"""
