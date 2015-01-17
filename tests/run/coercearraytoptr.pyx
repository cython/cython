cdef char* cstring = "abcdefg"

cdef void spam(char *target):
    cdef char* s = cstring
    while s[0]:
        target[0] = s[0]
        s += 1
        target += 1
    target[0] = c'\0'

cdef struct Grail:
    char silly[42]

def eggs():
    """
    >>> print(str(eggs()).replace("b'", "'"))
    ('abcdefg', 'abcdefg')
    """
    cdef char[42] silly
    cdef Grail grail
    spam(silly)
    spam(grail.silly)
    return silly, grail.silly
