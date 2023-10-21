# mode: run
# tag: memoryview

cdef f64[:] foo(i32 i):
    if i == 1:
        raise AttributeError('dummy')
    if i == 2:
        raise RuntimeError('dummy')
    if i == 3:
        raise ValueError('dummy')
    if i == 4:
        raise TypeError('dummy')

cdef f64[:] foo_nogil(i32 i) nogil:
    if i == 1:
        raise AttributeError('dummy')
    if i == 2:
        raise RuntimeError('dummy')
    if i == 3:
        raise ValueError('dummy')
    if i == 4:
        raise TypeError('dummy')

def propagate(i, bint nogil=false):
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

    >>> propagate(0, nogil=true)
    TypeError('Memoryview return value is not initialized')
    >>> propagate(1, nogil=true)
    AttributeError('dummy')
    >>> propagate(2, nogil=true)
    RuntimeError('dummy')
    >>> propagate(3, nogil=true)
    ValueError('dummy')
    >>> propagate(4, nogil=true)
    TypeError('dummy')
    """
    try:
        foo_nogil(i) if nogil else foo(i)
    except Exception as e:
        print '%s(%r)' % (e.__class__.__name__, e.args[0])
    else:
        print 'Exception subclass not raised'
