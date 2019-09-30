import sys

__doc__ = u"""
>>> class4.plus1(1)
2
>>> class4().plus1(1)
2
>>> class4.bplus1(1)
2
>>> class4().bplus1(1)
2
"""
# for class3, follow Python behaviour tested in method_assignment.py
# (This class hasn't been moved since it isn't pure Python)
if sys.version_info[0] == 2:
    __doc__ += """>>> class3.plus1(1) #doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
TypeError: unbound
"""
else:
    __doc__ += """>>> class3.plus1(1)
2
"""

cimport cython

def f_plus(a):
    return a + 1

# The tests formerly in class1 and class2 have been moved to "method_assignment.py"

cdef class class3:
    plus1 = f_plus

class class4:
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
    class class5(object):
        def __new__(cls): # implicit staticmethod
            return object.__new__(cls)

        @staticmethod
        def plus1(a):
            return a + 1
    return class5


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
