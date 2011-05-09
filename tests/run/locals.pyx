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
