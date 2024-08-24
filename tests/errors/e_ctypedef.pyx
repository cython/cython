# mode: error

ctypedef int slong
ctypedef double float

cdef extern from *:
    ctypedef int ulong

_ERRORS = """
3:0: ctypedef tries to overwrite existing type 'slong'
4:0: ctypedef tries to overwrite existing type 'float'
7:4: ctypedef tries to overwrite existing type 'ulong'; consider using the "cname" feature to use a different typename in C and Cython, e.g. `ctypedef ... ulong_ "ulong"`
"""
