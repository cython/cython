# mode: error
# tag: cpp

# cpp will convert function arguments to a type if it has suitable constructor
# we do not want that when calling from cython

cdef extern from "no_such_file.cpp" nogil:
    cppclass wrapped_int:
        long long val
        wrapped_int()
        wrapped_int(long long val)
        wrapped_int& operator=(const wrapped_int &other)
        wrapped_int& operator=(const long long other)

    long long constructor_overload(const wrapped_int& x)
    long long constructor_overload(const wrapped_int x)

cdef long long e = constructor_overload(17)
 

_ERRORS = u"""
18:40: Cannot assign type 'long' to 'const wrapped_int'
"""
