# ticket: 462

cimport cython

cdef class cclass:
    def test_self(self):
        """
        >>> cclass().test_self()
        'cclass'
        """
        return cython.typeof(self)

    def test_self_1(self, arg):
        """
        >>> cclass().test_self_1(1)
        ('cclass', 1)
        """
        return cython.typeof(self), arg

    def test_self_args(self, *args):
        """
        >>> cclass().test_self_args(1,2,3)
        ('cclass', (1, 2, 3))
        """
        return cython.typeof(self), args

    def test_args(*args):
        """
        >>> cclass().test_args(1,2,3)
        ('Python object', (1, 2, 3))
        """
        return cython.typeof(args[0]), args[1:]

    def test_args_kwargs(*args, **kwargs):
        """
        >>> cclass().test_args_kwargs(1,2,3, a=4)
        ('Python object', (1, 2, 3), {'a': 4})
        """
        return cython.typeof(args[0]), args[1:], kwargs
