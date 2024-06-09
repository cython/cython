# mode: compile
# tag: warnings, c, no-cpp

cdef extern from *:
    cdef cppclass X:
        pass

_WARNINGS="""
5:9: Using 'cppclass' while Cython is not in C++ mode.
"""
