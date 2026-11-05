# mode: error
# tag: werror

cdef useless_semicolon():
    cdef int i;
    pass;
    a = 1;

ctypedef int x;


_ERRORS="""
5:14: useless trailing semicolon
6:8: useless trailing semicolon
7:9: useless trailing semicolon
9:14: useless trailing semicolon
"""
