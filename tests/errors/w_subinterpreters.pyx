# mode: compile
# tag: warnings

# cython: subinterpreters_compatible=own_gil

cdef extern int some_extern  # OK
cdef int some_int  # OK
cdef object some_object  # OK
cdef public int some_public_int  # bad
cdef public object some_public_object  # really quite bad

cdef int func() nogil:
    with gil:
        print("Something")
    raise RuntimeError

_WARNINGS = """
9:16: Global cdef public variable used with subinterpreter support enabled.
10:19: Global cdef public Python variable used with subinterpreter support enabled.
12:0: Acquiring the GIL is currently very unlikely to work correctly with subinterpreters.
13:9: Acquiring the GIL is currently very unlikely to work correctly with subinterpreters.
15:4: Acquiring the GIL is currently very unlikely to work correctly with subinterpreters.
"""
