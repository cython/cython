
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

def slice_charptr_decode_unbound():
    """
    >>> print str(slice_charptr_decode_unbound()).replace("u'", "'")
    ('a', 'abc', 'abcABCqtp')
    """
    return (bytes.decode(cstring[:1], 'UTF-8'),
            bytes.decode(cstring[:3], 'UTF-8', 'replace'),
            bytes.decode(cstring[:9], 'UTF-8'))

def slice_charptr_decode_errormode():
    """
    >>> print str(slice_charptr_decode_errormode()).replace("u'", "'")
    ('a', 'abc', 'abcABCqtp')
    """
    return (cstring[:1].decode('UTF-8', 'strict'),
            cstring[:3].decode('UTF-8', 'replace'),
            cstring[:9].decode('UTF-8', 'unicode_escape'))

def slice_charptr_for_loop():
    """
    >>> slice_charptr_for_loop()
    ['a', 'b', 'c']
    ['b', 'c', 'A', 'B']
    ['B', 'C', 'q', 't', 'p']
    """
    print str([ c for c in cstring[:3] ]).replace(" b'", "'").replace("[b'", "'")
    print str([ c for c in cstring[1:5] ]).replace(" b'", "'").replace("[b'", "'")
    print str([ c for c in cstring[4:9] ]).replace(" b'", "'")
