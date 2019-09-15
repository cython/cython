# cython: language_level=3
# mode: run
# tag: pep3135, pure3.0


class C(object):
    """
    >>> obj = C()
    >>> obj.method_1()
    2
    >>> obj.method_2()
    3
    >>> obj.method_3()
    ['__class__', 'self']
    >>> obj.method_4()
    ['self']
    """

    @classmethod
    def class_method(cls):
        return 2

    @staticmethod
    def static_method():
        return 3

    def method_1(self):
        return __class__.class_method()

    def method_2(self):
        return __class__.static_method()

    def method_3(self):
        __class__
        return sorted(list(locals().keys()))

    def method_4(self):
        return sorted(list(locals().keys()))


class D:
    """
    >>> obj = D()
    >>> obj.method(1)
    1
    >>> obj.method(0)
    Traceback (most recent call last):
    ...
    UnboundLocalError: local variable '__class__' referenced before assignment
    """
    def method(self, x):
        if x: __class__ = x
        print(__class__)


class E:
    """
    >>> obj = E()
    >>> obj.method()().__name__
    'E'
    """
    def method(self):
        def inner(): return __class__
        return inner


class F:
    """
    >>> obj = F()
    >>> obj.method()()().__name__
    'F'
    """
    def method(self):
        def inner():
            def inner_inner():
                return __class__
            return inner_inner
        return inner


class G:
    """
    >>> obj = G()
    >>> obj.method().__name__
    'H'
    """
    def method(self):
        class H:
            def inner(self):
                return __class__
        return H().inner()


class I:
    """
    >>> obj = I()
    >>> obj.method()()().__name__
    'J'
    """
    def method(self):
        def inner():
            class J:
                def inner(self):
                    return __class__
            return J().inner
        return inner


class K:
    def method(self): return __class__

__test__ = {
    "k": """
    >>> OldK = K
    >>> K = None
    >>> OldK().method().__name__
    'K'
    """
}

class L:
    """
    >>> OldL().method().__name__
    'L'
    """
    def method(self): return self.__class__

OldL = L
L = None

class M:
    """
    >>> M().method()
    u'overwritten'
    """
    def method(self):
        __class__ = 'overwritten'
        return __class__

class N:
    """
    >>> N().method().__name__
    'N'
    """
    __class__ = 'N'
    def method(self):
        return __class__