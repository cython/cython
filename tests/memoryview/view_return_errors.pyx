# mode: run

cdef double[:] foo(int i):
    if i == 1:
        raise AttributeError('dummy')
    if i == 2:
        raise RuntimeError('dummy')
    if i == 3:
        raise ValueError('dummy')
    if i == 4:
        raise TypeError('dummy')

def propagate(i):
    '''
    >>> propagate(0)
    TypeError('Memoryview return value is not initialized',)
    >>> propagate(1)
    AttributeError('dummy',)
    >>> propagate(2)
    RuntimeError('dummy',)
    >>> propagate(3)
    ValueError('dummy',)
    >>> propagate(4)
    TypeError('dummy',)
    '''
    try:
        foo(i)
    except Exception as e:
        print repr(e)
    else:
        print 'Exception sublass not raised'
