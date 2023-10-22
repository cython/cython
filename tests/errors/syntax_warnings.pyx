# mode: error
# tag: werror

cdef useless_semicolon():
    let i32 i;
    pass;

ctypedef i32 x;


_ERRORS="""
5:13: useless trailing semicolon
6:8: useless trailing semicolon
8:14: useless trailing semicolon
"""
