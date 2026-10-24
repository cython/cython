# cython: binding=True
# mode: run
# tag: cyfunction, cpp, cpp11

from libcpp.vector cimport vector


cdef enum class DefaultMode:
    DEFAULT = 19
    OTHER = 23


cdef int scoped_enum_default(DefaultMode mode=DefaultMode.DEFAULT) noexcept nogil:
    return <int>mode


def test_nogil_scoped_enum_default():
    """
    >>> test_nogil_scoped_enum_default()
    (19, 23)
    """
    cdef int default_result, explicit_result
    with nogil:
        default_result = scoped_enum_default()
        explicit_result = scoped_enum_default(DefaultMode.OTHER)
    return default_result, explicit_result


cdef class A:
    def f1(self, a, b=1, vector[double] c = vector[double]()):
        pass
    def f2(self, a, b=1,/, vector[double] c = vector[double](1, 2.0)):
        pass
    def f3(self, a, /, b=1, *, c = vector[double](2, 3.0)):
        pass


def check_defaults_on_methods():
    """
    >>> A.f1.__defaults__
    (1, [])
    >>> A.f1.__kwdefaults__
    >>> A.f2.__defaults__
    (1, [2.0])
    >>> A.f2.__kwdefaults__
    >>> A.f3.__defaults__
    (1,)
    >>> A.f3.__kwdefaults__
    {'c': [3.0, 3.0]}
    """
    pass
