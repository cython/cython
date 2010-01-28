
cimport cython

cdef class cclass:

    @classmethod
    def test0(cls):
        """
        >>> cclass.test0()
        'type object'
        """
        return cython.typeof(cls)

    @classmethod
    def test0_args(*args):
        """
        >>> cclass.test0_args(1,2,3)
        ('Python object', (1, 2, 3))
        """
        return cython.typeof(args[0]), args[1:]

    @classmethod
    def test1(cls, arg):
        """
        >>> cclass.test1(1)
        ('type object', 1)
        """
        return cython.typeof(cls), arg

    @classmethod
    def test2(cls, arg1, arg2):
        """
        >>> cclass.test2(1,2)
        ('type object', 1, 2)
        """
        return cython.typeof(cls), arg1, arg2

    @classmethod
    def test1_args(cls, *args):
        """
        >>> cclass.test1_args(1,2,3)
        ('type object', (1, 2, 3))
        """
        return cython.typeof(cls), args

    @classmethod
    def test2_args(cls, arg, *args):
        """
        >>> cclass.test2_args(1,2,3)
        ('type object', 1, (2, 3))
        """
        return cython.typeof(cls), arg, args

    @classmethod
    def test0_args_kwargs(*args, **kwargs):
        """
        >>> cclass.test0_args_kwargs(1,2,3)
        ('Python object', (1, 2, 3), {})
        """
        return cython.typeof(args[0]), args[1:], kwargs

    @classmethod
    def test1_args_kwargs(cls, *args, **kwargs):
        """
        >>> cclass.test1_args_kwargs(1,2,3)
        ('type object', (1, 2, 3), {})
        """
        return cython.typeof(cls), args, kwargs

    @classmethod
    def test2_args_kwargs(cls, arg, *args, **kwargs):
        """
        >>> cclass.test2_args_kwargs(1,2,3)
        ('type object', 1, (2, 3), {})
        """
        return cython.typeof(cls), arg, args, kwargs
