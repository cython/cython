# mode: run
# tag: typeinference, generators

cimport cython

def test_type_inference():
    """
    >>> list(test_type_inference())
    [(2.0, 'double'), (2.0, 'double'), (2.0, 'double')]
    """
    x = 1.0
    for i in range(3):
        yield x * 2.0, cython.typeof(x)

def test_unicode_loop():
    """
    >>> chars = list(test_unicode_loop())
    1 Py_UCS4
    2 Py_UCS4
    2 Py_UCS4
    2 Py_UCS4
    2 Py_UCS4
    >>> len(chars)
    4
    >>> ''.join(chars) == 'abcd'
    True
    """
    ustr = u'abcd'
    print 1, cython.typeof(ustr[0])
    for c in ustr:
        print 2, cython.typeof(c)
        yield c

def test_with_nonlocal():
    """
    >>> chars = list(test_with_nonlocal())
    1 Py_UCS4
    2 Py_UCS4
    2 Py_UCS4
    >>> len(chars)
    2
    >>> ''.join(chars) == 'ab'
    True
    """
    ustr = u'ab'
    print 1, cython.typeof(ustr[0])
    def gen():
        nonlocal ustr
        for c in ustr:
            print 2, cython.typeof(c)
            yield c
    return gen()
