# cython: language_level=3
# mode: run
# tag: pep3135, pure3.0

import cython

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
    >>> list(obj.generator())
    ['C']

    >>> C.l() == C
    True
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

    def generator(self):
        yield __class__.__name__

    l = lambda: __class__


@cython.cclass
class CC(object):
    """
    >>> obj = CC()
    >>> obj.method_1()
    2
    >>> obj.method_2()
    3
    >>> obj.method_3()
    ['__class__', 'self']
    >>> obj.method_4()
    ['self']
    >>> list(obj.generator())
    ['CC']

    >>> CC.l() == CC
    True
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

    def generator(self):
        yield __class__.__name__

    l = lambda: __class__


class D:
    """
    >>> obj = D()
    >>> obj.method(1)
    1
    >>> obj.method(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    UnboundLocalError: ... '__class__' ...
    """
    def method(self, x):
        if x: __class__ = x
        print(__class__)


@cython.cclass
class CD:
    """
    >>> obj = CD()
    >>> obj.method(1)
    1
    >>> obj.method(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    UnboundLocalError: ... '__class__' ...
    """
    def method(self, x):
        if x: __class__ = x
        print(__class__)


class E:
    """
    >>> obj = E()
    >>> obj.method()().__name__
    'E'
    >>> obj.method2()()().__name__
    'E'
    """
    def method(self):
        def inner(): return __class__
        return inner

    def method2(self):
        def inner():
            def inner_inner():
                return __class__
            return inner_inner
        return inner


@cython.cclass
class CE:
    """
    >>> obj = CE()
    >>> obj.method()().__name__
    'CE'
    >>> obj.method2()()().__name__
    'CE'
    """
    def method(self):
        def inner(): return __class__
        return inner

    def method2(self):
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


@cython.cclass
class CK:
    def method(self): return __class__


__test__ = {
    "k": """
    >>> OldK = K
    >>> K = None
    >>> OldK().method().__name__
    'K'
    """,
    "ck": """
    >>> OldCK = CK
    >>> CK = None
    >>> OldCK().method().__name__
    'CK'
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
    'overwritten'
    """
    def method(self):
        __class__ = 'overwritten'
        return __class__

@cython.cclass
class CM:
    """
    >>> CM().method()
    'overwritten'
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

if cython.compiled:
    @cython.cclass
    class CDefFuncTest:
        """
        >>> obj = CDefFuncTest()
        >>> obj.call_cfunc1().__name__
        'CDefFuncTest'

        #>>> obj.call_cfunc2()().__name__ - GH 4092
        #'CDefFuncTest'
        >>> obj.call_cfunc3()
        ['__class__', 'self']
        """
        @cython.cfunc
        def cfunc1(self):
            return __class__
        def call_cfunc1(self):
            return self.cfunc1()
        #@cython.cfunc - disabled, GH 4092. This works outside pure Python mode
        #def cfunc2(self):
        #    def inner():
        #        return __class__
        #    return inner
        def call_cfunc2(self):
            return self.cfunc2()
        @cython.cfunc
        def cfunc3(self):
            __class__
            return sorted(list(locals().keys()))
        def call_cfunc3(self):
            return self.cfunc3()
