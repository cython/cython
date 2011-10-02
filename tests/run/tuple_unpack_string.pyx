# mode: run
# tag: string, unicode, sequence unpacking, starexpr

def unpack_single_str():
    """
    >>> print(unpack_single_str())
    a
    """
    a, = 'a'
    return a

def unpack_str():
    """
    >>> a,b = unpack_str()
    >>> print(a)
    a
    >>> print(b)
    b
    """
    a,b = 'ab'
    return a,b

def star_unpack_str():
    """
    >>> a,b,c = star_unpack_str()
    >>> print(a)
    a
    >>> type(b) is list
    True
    >>> print(''.join(b))
    bbb
    >>> print(c)
    c
    """
    a,*b,c = 'abbbc'
    return a,b,c

def unpack_single_unicode():
    """
    >>> print(unpack_single_unicode())
    a
    """
    a, = u'a'
    return a

def unpack_unicode():
    """
    >>> a,b = unpack_unicode()
    >>> print(a)
    a
    >>> print(b)
    b
    """
    a,b = u'ab'
    return a,b

def star_unpack_unicode():
    """
    >>> a,b,c = star_unpack_unicode()
    >>> print(a)
    a
    >>> type(b) is list
    True
    >>> print(''.join(b))
    bbb
    >>> print(c)
    c
    """
    a,*b,c = u'abbbc'
    return a,b,c

# the following is not supported due to Py2/Py3 bytes differences

## def unpack_single_bytes():
##     """
##     >>> print(unpack_single_bytes().decode('ASCII'))
##     a
##     """
##     a, = b'a'
##     return a

## def unpack_bytes():
##     """
##     >>> a,b = unpack_bytes()
##     >>> print(a.decode('ASCII'))
##     a
##     >>> print(b.decode('ASCII'))
##     b
##     """
##     a,b = b'ab'
##     return a,b

## def star_unpack_bytes():
##     """
##     >>> a,b,c = star_unpack_bytes()
##     >>> print(a.decode('ASCII'))
##     a
##     >>> type(b) is list
##     True
##     >>> print(''.join([ch.decode('ASCII') for ch in b]))
##     bbb
##     >>> print(c.decode('ASCII'))
##     c
##     """
##     a,*b,c = b'abbbc'
##     return a,b,c
