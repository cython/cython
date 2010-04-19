
bytes_abc = b'abc'
bytes_ABC = b'ABC'

unicode_abc = u'abc'
unicode_ABC = u'ABC'


def for_in_bytes(bytes s):
    """
    >>> for_in_bytes(bytes_abc)
    'X'
    >>> for_in_bytes(bytes_ABC)
    'C'
    """
    for c in s:
        # Py2/Py3
        if c == b'C' or c == c'C':
            return 'C'
    else:
        return 'X'

def for_char_in_bytes(bytes s):
    """
    >>> for_char_in_bytes(bytes_abc)
    'X'
    >>> for_char_in_bytes(bytes_ABC)
    'C'
    """
    cdef char c
    for c in s:
        if c == b'C':
            return 'C'
    else:
        return 'X'

def for_pyunicode_in_unicode(unicode s):
    """
    >>> for_pyunicode_in_unicode(unicode_abc)
    'X'
    >>> for_pyunicode_in_unicode(unicode_ABC)
    'C'
    """
    cdef Py_UNICODE c
    for c in s:
        if c == u'C':
            return 'C'
    else:
        return 'X'
