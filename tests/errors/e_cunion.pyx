# mode: error

cdef union AllCharptr:
    char *s1
    char *s2
    char *s3


def convert_ok():
    cdef AllCharptr u
    u.s1 = b"abc"
    return u


cdef union IllegalMix:
    char *s1
    char *s2
    int i


def convert_nok():
    cdef IllegalMix u
    u.i = 5
    return u


_ERRORS = """
24:11: Cannot convert 'IllegalMix' to Python object
"""
