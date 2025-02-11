# mode: compile

cimport cython

# Complex numbers defined in "cython.locals" weren't having their utility code imported directly
# leading to compile-errors that the type wasn't defined. The test is intentionally minimal since
# anything more thorough ends up creating the utility code
@cython.locals(x=complex)
cdef f(x):
    pass
