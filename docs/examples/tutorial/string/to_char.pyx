# define a global name for whatever char type is used in the module
ctypedef unsigned char char_type


cdef char_type[:] _chars(s):
    if isinstance(s, str):
        # encode to the specific encoding used inside of the module
        s = (<str>s).encode('utf8')
    return s
