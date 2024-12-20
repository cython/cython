# mode: compile
# tag: warnings

# cython: subinterpreters_compatible=own_gil

cdef extern int some_extern  # OK
cdef int some_int  # bad
cdef object some_object  # really quite bad!

cdef int func() nogil:
    with gil:
        print("Something")
    raise RuntimeError

_WARNINGS = """
7:9: Global cdef variable used with subinterpreter support enabled.
8:12: Global cdef Python variable used with subinterpreter support enabled.
10:0: Acquiring the GIL is currently very unlikely to work correctly with subinterpreters.
11:9: Acquiring the GIL is currently very unlikely to work correctly with subinterpreters.
13:4: Acquiring the GIL is currently very unlikely to work correctly with subinterpreters.
"""
