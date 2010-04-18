
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
        if c == 'C':
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
        if c == 'C':
            return 'C'
    else:
        return 'X'

def for_int_in_unicode(unicode s):
    """
    >>> for_int_in_unicode(unicode_abc)
    'X'
    >>> for_int_in_unicode(unicode_ABC)
    'C'
    """
    cdef int c
    for c in s:
        if c == 'C':
            return 'C'
    else:
        return 'X'
