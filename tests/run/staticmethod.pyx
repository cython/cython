cimport cython


class class1:
    u"""
    >>> class1.plus1(1)
    2
    >>> class1().plus1(1)
    2
    >>> class1.bplus1(1)
    2
    >>> class1().bplus1(1)
    2
    """
    @staticmethod
    def plus1(a):
        return a + 1

    @staticmethod
    @cython.binding(True)
    def bplus1(a):
        return a + 1


def nested_class():
    """
    >>> cls = nested_class()
    >>> cls.plus1(1)
    2
    >>> obj = cls()
    >>> obj.plus1(1)
    2
    """
    class class2(object):
        def __new__(cls): # implicit staticmethod
            return object.__new__(cls)

        @staticmethod
        def plus1(a):
            return a + 1
    return class2


cdef class BaseClass(object):
    """
    Test cdef static methods with super() and Python subclasses

    >>> obj = BaseClass()
    >>> obj.mystaticmethod(obj, 1)
    1
    >>> BaseClass.mystaticmethod(obj, 1)
    1
    >>> obj.mystaticmethod2(1, 2, 3)
    1 2 3
    >>> BaseClass.mystaticmethod2(1, 2, 3)
    1 2 3
    """

    @staticmethod
    def mystaticmethod(self, arg1):
        print arg1

    @staticmethod
    @cython.binding(True)
    def mystaticmethod2(a, b, c):
        print a, b, c


cdef class SubClass(BaseClass):
    """
    >>> obj = SubClass()
    >>> obj.mystaticmethod(obj, 1)
    1
    2
    >>> SubClass.mystaticmethod(obj, 1)
    1
    2
    """

    @staticmethod
    def mystaticmethod(self, arg1):
        print arg1
        super().mystaticmethod(self, arg1 + 1)


class SubSubClass(SubClass):
    """
    >>> obj = SubSubClass()
    >>> obj.mystaticmethod(obj, 1)
    1
    2
    3
    >>> SubSubClass.mystaticmethod(obj, 1)
    1
    2
    3
    """

    @staticmethod
    def mystaticmethod(self, arg1):
        print arg1
        super().mystaticmethod(self, arg1 + 1)


cdef class ArgsKwargs(object):
    @staticmethod
    def with_first_arg(arg1, *args, **kwargs):
        """
        >>> ArgsKwargs().with_first_arg(1, 2, 3, a=4, b=5)
        (1, 'pos', 2, 3, ('a', 4), ('b', 5))
        """
        return (arg1, 'pos') + args + tuple(sorted(kwargs.items()))

    @staticmethod
    def only_args_kwargs(*args, **kwargs):
        """
        >>> ArgsKwargs().only_args_kwargs()
        ()
        >>> ArgsKwargs().only_args_kwargs(1, 2, a=3)
        (1, 2, ('a', 3))
        """
        return args + tuple(sorted(kwargs.items()))

    @staticmethod
    def no_args():
        """
        >>> ArgsKwargs().no_args()
        OK!
        """
        print("OK!")


class StaticmethodSubclass(staticmethod):
    """
    >>> s = StaticmethodSubclass(None)
    >>> s.is_subtype()
    True
    """
    def is_subtype(self):
        return isinstance(self, staticmethod)
