# mode: run
# tag: closures
# ticket: 1797


def func():
    """
    >>> funcs = func()
    >>> [f(1) for f in funcs]  # doctest: +NORMALIZE_WHITESPACE
    ['eq',
     'str',
     'weakref',
     'new',
     'getitem',
     'setitem',
     'delitem',
     'getslice',
     'setslice',
     'delslice_',
     'getattr',
     'getattribute',
     'setattr',
     'delattr',
     'get',
     'set',
     'delete',
     'dict',
     'dealloc',
     'cinit']
    """
    def __eq__(a):
        return 'eq'

    def __str__(a):
        return 'str'

    def __weakref__(a):
        return 'weakref'

    def __new__(a):
        return 'new'

    def __getitem__(a):
        return 'getitem'

    def __setitem__(a):
        return 'setitem'

    def __delitem__(a):
        return 'delitem'

    def __getslice__(a):
        return 'getslice'

    def __setslice__(a):
        return 'setslice'

    def __delslice__(a):
        return 'delslice_'

    def __getattr__(a):
        return 'getattr'

    def __getattribute__(a):
        return 'getattribute'

    def __setattr__(a):
        return 'setattr'

    def __delattr__(a):
        return 'delattr'

    def __get__(a):
        return 'get'

    def __set__(a):
        return 'set'

    def __delete__(a):
        return 'delete'

    def __dict__(a):
        return 'dict'

    def __dealloc__(a):
        return 'dealloc'

    def __cinit__(a):
        return 'cinit'

    def list_from_gen(g):
        return list(g)

    # move into closure by using inside of generator expression
    return list_from_gen([
            __eq__,
            __str__,
            __weakref__,
            __new__,
            __getitem__,
            __setitem__,
            __delitem__,
            __getslice__,
            __setslice__,
            __delslice__,
            __getattr__,
            __getattribute__,
            __setattr__,
            __delattr__,
            __get__,
            __set__,
            __delete__,
            __dict__,
            __dealloc__,
            __cinit__,
        ][i] for i in range(20))
