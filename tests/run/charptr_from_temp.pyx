# mode: run


cdef cfunc1(char* s):
    return s.decode('ASCII')


cdef cfunc3(int x, char* s, object y):
    return cfunc1(s)


def test_one_arg_indexing(s):
    """
    >>> test_one_arg_indexing(b'xyz')
    'y'
    """
    cfunc1(s[:1])
    z = cfunc1(s[2:])
    assert z == 'z', repr(z)
    return cfunc1(s[1:2])


def test_more_args_indexing(s):
    """
    >>> test_more_args_indexing(b'xyz')
    'y'
    """
    cfunc3(1, s[slice(0,1)], 6.5)
    z = cfunc3(2, s[slice(2,None)], 'abc' * 2)
    assert z == 'z', repr(z)
    return cfunc3(3, s[slice(1,2)], 1)


def test_one_arg_slicing(s):
    """
    >>> test_one_arg_slicing(b'xyz')
    'y'
    """
    cfunc1(s[:2])
    z = cfunc1(s[2:])
    assert z == 'z', repr(z)
    return cfunc1(s[1:2])


def test_more_args_slicing(s):
    """
    >>> test_more_args_slicing(b'xyz')
    'y'
    """
    cfunc3(1, s[:2], 'abc')
    z = cfunc3(123, s[2:], 5)
    assert z == 'z', repr(z)
    return cfunc3(2, s[1:2], 1.4)


def test_one_arg_adding(s):
    """
    >>> test_one_arg_adding(b'xyz')
    'abxyzqr'
    """
    return cfunc1(b"a" + b"b" + s + b"q" + b"r")


def test_more_args_adding(s):
    """
    >>> test_more_args_adding(b'xyz')
    'abxyzqr'
    """
    return cfunc3(1, b"a" + b"b" + s + b"q" + b"r", 'xyz%d' % 3)


cdef char* ret_charptr(char* s):
    return s


def test_charptr_and_charptr_func(char* s):
    """
    >>> test_charptr_and_charptr_func(b'abc') == b'abc'
    True
    """
    return s and ret_charptr(s)


def test_charptr_and_ucharptr(char* s):
    """
    >>> test_charptr_and_ucharptr(b'abc') == b'abc'
    True
    """
    return s and <unsigned char*>s
