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
        return super(B, self).method()

    @classmethod
    def class_method(cls):
        return super(B, cls).class_method()

    @staticmethod
    def static_method(instance):
        return super(B, instance).static_method()

    def generator_test(self):
        for i in super(B, self).generator_test():
            yield i


cdef class CClassBase(object):
    def method(self):
        return 'def'
    cpdef method_cp(self):
        return 'cpdef'

#     cdef method_c(self):
#         return 'cdef'
#     def call_method_c(self):
#         return self.method_c()

cdef class CClassSub(CClassBase):
    """
    >>> CClassSub().method()
    'def'
    >>> CClassSub().method_cp()
    'cpdef'
    """
#     >>> CClassSub().call_method_c()
#     'cdef'

    def method(self):
        return super(CClassSub, self).method()
    cpdef method_cp(self):
        return super(CClassSub, self).method_cp()

#     cdef method_c(self):
#         return super(CClassSub, self).method_c()

cdef class Base(object):
    """
    >>> Base().method()
    'Base'
    >>> Base.method(Base())
    'Base'
    """
    cpdef method(self):
        return "Base"

cdef class Sub(Base):
    """
    >>> Sub().method()
    'Sub'
    >>> Sub.method(Sub())
    'Sub'
    >>> Base.method(Sub())
    'Base'
    """
    cpdef method(self):
        return "Sub"
