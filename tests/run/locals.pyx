# mode: run
# tag: builtins, locals, dir

def get_locals(x, *args, **kwds):
    """
    >>> sorted( get_locals(1,2,3, k=5).items() )
    [('args', (2, 3)), ('kwds', {'k': 5}), ('x', 1), ('y', 'hi'), ('z', 5)]
    """
    cdef int z = 5
    y = "hi"
    return locals()

def get_vars(x, *args, **kwds):
    """
    >>> sorted( get_vars(1,2,3, k=5).items() )
    [('args', (2, 3)), ('kwds', {'k': 5}), ('x', 1), ('y', 'hi'), ('z', 5)]
    """
    cdef int z = 5
    y = "hi"
    return vars()

def get_dir(x, *args, **kwds):
    """
    >>> sorted( get_dir(1,2,3, k=5) )
    ['args', 'kwds', 'x', 'y', 'z']
    """
    cdef int z = 5
    y = "hi"
    return dir()

def in_locals(x, *args, **kwds):
    """
    >>> in_locals('z')
    True
    >>> in_locals('args')
    True
    >>> in_locals('X')
    False
    """
    cdef int z = 5
    y = "hi"
    return x in locals()

def in_dir(x, *args, **kwds):
    """
    >>> in_dir('z')
    True
    >>> in_dir('args')
    True
    >>> in_dir('X')
    False
    """
    cdef int z = 5
    y = "hi"
    return x in dir()

def in_vars(x, *args, **kwds):
    """
    >>> in_vars('z')
    True
    >>> in_vars('args')
    True
    >>> in_vars('X')
    False
    """
    cdef int z = 5
    y = "hi"
    return x in vars()

def sorted(it):
    l = list(it)
    l.sort()
    return l

def locals_ctype():
    """
    >>> locals_ctype()
    False
    """
    cdef int *p = NULL
    return 'p' in locals()

def locals_ctype_inferred():
    """
    >>> locals_ctype_inferred()
    False
    """
    cdef int *p = NULL
    b = p
    return 'b' in locals()


def pass_on_locals(f):
    """
    >>> def print_locals(l, **kwargs):
    ...     print(sorted(l))

    >>> pass_on_locals(print_locals)
    ['f']
    ['f']
    ['f']
    """
    f(locals())
    f(l=locals())
    f(l=locals(), a=1)


def buffers_in_locals(object[char, ndim=1] a):
    """
    >>> sorted(buffers_in_locals(b'abcdefg'))
    ['a', 'b']
    """
    cdef object[unsigned char, ndim=1] b = a

    return locals()
