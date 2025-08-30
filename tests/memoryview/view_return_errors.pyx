# mode: run
# tag: memoryview


cdef double[:] foo(int i):
    if i == 1:
        raise AttributeError('dummy')
    if i == 2:
        raise RuntimeError('dummy')
    if i == 3:
        raise ValueError('dummy')
    if i == 4:
        raise TypeError('dummy')


cdef double[:] foo_nogil(int i) nogil:
    if i == 1:
        raise AttributeError('dummy')
    if i == 2:
        raise RuntimeError('dummy')
    if i == 3:
        raise ValueError('dummy')
    if i == 4:
        raise TypeError('dummy')


def propagate(i, bint nogil=False):
    """
    >>> propagate(0)
    TypeError('Memoryview return value is not initialized')
    >>> propagate(1)
    AttributeError('dummy')
    >>> propagate(2)
    RuntimeError('dummy')
    >>> propagate(3)
    ValueError('dummy')
    >>> propagate(4)
    TypeError('dummy')

    >>> propagate(0, nogil=True)
    TypeError('Memoryview return value is not initialized')
    >>> propagate(1, nogil=True)
    AttributeError('dummy')
    >>> propagate(2, nogil=True)
    RuntimeError('dummy')
    >>> propagate(3, nogil=True)
    ValueError('dummy')
    >>> propagate(4, nogil=True)
    TypeError('dummy')
    """
    try:
        foo_nogil(i) if nogil else foo(i)
    except Exception as e:
        print '%s(%r)' % (e.__class__.__name__, e.args[0])
    else:
        print 'Exception subclass not raised'
