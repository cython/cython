# mode: run
# tag: py3k_super, gh3246, pure3.0

import cython

class A(object):
    def method(self):
        return 1

    @classmethod
    def class_method(cls):
        return 2

    @staticmethod
    def static_method():
        return 3

    def generator_test(self):
        return [1, 2, 3]

    def super_class(self):
        return __class__

class B(A):
    """
    >>> obj = B()
    >>> obj.method()
    1
    >>> B.class_method()
    2
    >>> B.static_method(obj)
    3
    >>> list(obj.generator_test())
    [1, 2, 3]
    >>> obj.star_method()
    1
    >>> obj.starstar_method()
    1
    >>> obj.starstarstar_method()
    1
    >>> obj.star_class_method()
    2
    >>> obj.starstar_class_method()
    2
    >>> obj.starstarstar_class_method()
    2
    >>> obj.star_static_method(obj)
    3
    >>> obj.starstar_static_method(obj)
    3
    >>> obj.starstarstar_static_method(obj)
    3
    """
    def method(self):
        return super().method()

    @classmethod
    def class_method(cls):
        return super().class_method()

    @staticmethod
    def static_method(instance):
        return super().static_method()

    def generator_test(self):
        for i in super().generator_test():
            yield i

    def star_method(self, *args):
        return super().method()

    def starstar_method(self, **kwargs):
        return super().method()

    def starstarstar_method(cls, *args, **kwargs):
        return super().method()

    @classmethod
    def star_class_method(cls, *args):
        return super().class_method()

    @classmethod
    def starstar_class_method(cls, **kwargs):
        return super().class_method()

    @classmethod
    def starstarstar_class_method(cls, *args, **kwargs):
        return super().class_method()

    @staticmethod
    def star_static_method(instance, *args):
        return super().static_method()

    @staticmethod
    def starstar_static_method(instance, **kwargs):
        return super().static_method()

    @staticmethod
    def starstarstar_static_method(instance, *args, **kwargs):
        return super().static_method()


class C(A):
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
    >>> obj.method_5()  # doctest: +ELLIPSIS
    <class '...py3k_super.C'>
    >>> obj.super_class()  # doctest: +ELLIPSIS
    <class '...py3k_super.A'>
    """

    def method_1(self):
        return __class__.class_method()

    def method_2(self):
        return __class__.static_method()

    def method_3(self):
        __class__
        return sorted(list(locals().keys()))

    def method_4(self):
        return sorted(list(locals().keys()))

    def method_5(self):
        return __class__


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

def test_class_cell_empty():
    """
    >>> test_class_cell_empty()
    Traceback (most recent call last):
    ...
    RuntimeError: super(): empty __class__ cell
    """
    class Base(type):
        def __new__(cls, name, bases, attrs):
            attrs['foo'](None)

    class EmptyClassCell(metaclass=Base):
        def foo(self):
            super()


@cython.cclass
class CClassBase(object):
    def method(self):
        return 'def'

#     cpdef method_cp(self):
#         return 'cpdef'
#     cdef method_c(self):
#         return 'cdef'
#     def call_method_c(self):
#         return self.method_c()

@cython.cclass
class CClassSub(CClassBase):
    """
    >>> CClassSub().method()
    'def'
    """
#     >>> CClassSub().method_cp()
#     'cpdef'
#     >>> CClassSub().call_method_c()
#     'cdef'

    def method(self):
        return super().method()

#     cpdef method_cp(self):
#         return super().method_cp()
#     cdef method_c(self):
#         return super().method_c()


def freeing_class_cell_temp_gh3246():
    # https://github.com/cython/cython/issues/3246
    """
    >>> abc = freeing_class_cell_temp_gh3246()
    >>> abc().a
    1
    """
    class SimpleBase(object):
        def __init__(self):
            self.a = 1

    class ABC(SimpleBase):
        def __init__(self):
            super().__init__()

    return ABC
