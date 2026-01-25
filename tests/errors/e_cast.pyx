# mode: error

cimport cython

cdef class C:
    pass

c = C()

x = cython.cast(c)
y = cython.cast(C, c, unknown=True)
cdef void *z = cython.cast(int, c, objstruct_cast=True)


_ERRORS = """
10:10: cast() takes exactly two arguments and optional keywords
11:10: Only 'typecheck' and 'objstruct_cast' are valid keywords for cast()
12:21: objstruct_cast can only be applied to extension types

# Extraneous errors
10:10: 'cast' not a valid cython attribute or is being used incorrectly
11:10: 'cast' not a valid cython attribute or is being used incorrectly
"""