
cdef char* cstring = "abcABCqtp"

def slice_charptr_end():
    """
    >>> print str(slice_charptr_end()).replace("b'", "'")
    ('a', 'abc', 'abcABCqtp')
    """
    return cstring[:1], cstring[:3], cstring[:9]

def slice_charptr_decode():
    """
    >>> print str(slice_charptr_decode()).replace("u'", "'")
    ('a', 'abc', 'abcABCqtp')
    """
    return (cstring[:1].decode('UTF-8'),
            cstring[:3].decode('UTF-8'),
            cstring[:9].decode('UTF-8'))

def slice_charptr_decode_errormode():
    """
    >>> print str(slice_charptr_decode_errormode()).replace("u'", "'")
    ('a', 'abc', 'abcABCqtp')
    """
    return (cstring[:1].decode('UTF-8', 'strict'),
            cstring[:3].decode('UTF-8', 'replace'),
            cstring[:9].decode('UTF-8', 'unicode_escape'))
