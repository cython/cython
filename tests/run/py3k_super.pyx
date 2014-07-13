# mode: run
# tag: py3k_super

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


def test_class_cell_empty():
    """
    >>> test_class_cell_empty()
    Traceback (most recent call last):
    ...
    SystemError: super(): empty __class__ cell
    """
    class Base(type):
        def __new__(cls, name, bases, attrs):
            attrs['foo'](None)

    class EmptyClassCell(metaclass=Base):
        def foo(self):
            super()


cdef class CClassBase(object):
    def method(self):
        return 'def'

#     cpdef method_cp(self):
#         return 'cpdef'
#     cdef method_c(self):
#         return 'cdef'
#     def call_method_c(self):
#         return self.method_c()

cdef class CClassSub(CClassBase):
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
