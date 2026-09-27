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

def memview_func(int[:] x):
    pass

cpdef enum E:
    A = 1

_WARNINGS = """
1:0: Module 'w_subinterpreters' is declared as 'subinterpreters_compatible' but uses cpdef enums. This is not supported yet since it uses global cdef objects and will likely crash.
1:0: Module 'w_subinterpreters' is declared as 'subinterpreters_compatible' but uses typed memoryviews. This is not supported yet and will likely crash.
7:9: Global cdef variable used with subinterpreter support enabled.
8:12: Global cdef Python variable used with subinterpreter support enabled.
10:0: Acquiring the GIL is currently very unlikely to work correctly with subinterpreters.
11:9: Acquiring the GIL is currently very unlikely to work correctly with subinterpreters.
13:4: Acquiring the GIL is currently very unlikely to work correctly with subinterpreters.
# spurious
26:4: 'cpdef_method' redeclared
36:4: 'cpdef_cname_method' redeclared
"""
