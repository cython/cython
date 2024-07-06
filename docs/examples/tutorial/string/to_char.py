# define a global name for whatever char type is used in the module
char_type = cython.typedef(cython.uchar)

@cython.cfunc
def _chars(s) -> char_type[:]:
    if isinstance(s, str):
        # encode to the specific encoding used inside of the module
        s = cython.cast(str, s).encode('utf8')
    return s
