__doc__ = u"""
>>> class1.plus1(1)
2
>>> class2.plus1(1)
2
>>> class3.plus1(1)
2
>>> class4.plus1(1)
2
"""

def f_plus(a):
    return a + 1

class class1:
    plus1 = f_plus

class class2(object):
    plus1 = f_plus

cdef class class3:
    plus1 = f_plus

class class4:
    @staticmethod
    def plus1(a):
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

