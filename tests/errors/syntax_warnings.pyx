# mode: error
# tag: werror

cdef useless_semicolon():
    cdef int i;
    pass;

ctypedef int x;


_ERRORS="""
5:14: useless trailing semicolon
6:8: useless trailing semicolon
8:14: useless trailing semicolon
"""
