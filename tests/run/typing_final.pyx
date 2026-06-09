# mode: run
# tag: typing, final

# typing.final must get the same compile semantics as cython.final:
# final types (no subclassing) and final cdef/cpdef methods.

from typing import final


@final
cdef class FinalClass:
    """
    >>> f = FinalClass()
    >>> test_final_class(f)
    Type tested

    >>> try:
    ...     class SubType(FinalClass): pass
    ... except TypeError:
    ...     print('PASSED!')
    PASSED!
    """


@final
cdef class FinalWithMethod:
    """
    >>> FinalWithMethod().value()
    42
    """
    @final
    cpdef int value(self):
        return 42


# aliased import still resolves to the `final` directive
from typing import final as _final


@_final
cdef class FinalAliased:
    """
    >>> f = FinalAliased()
    >>> try:
    ...     class SubType(FinalAliased): pass
    ... except TypeError:
    ...     print('PASSED!')
    PASSED!
    """


# typing.final on a plain Python class is advisory (pure-Python no-op): it must NOT
# raise "final not allowed in class scope" (unlike @cython.final) and must not make
# the class un-subclassable.
@final
class PlainFinal:
    """
    >>> class Sub(PlainFinal): pass
    >>> Sub is not None
    True
    """


# typing.final on a method of a NON-final cdef class is also advisory: it must compile
# without the "Only final types can have final Python (def/cpdef) methods" error that
# strict @cython.final raises, and the method stays overridable.
cdef class NonFinalBase:
    """
    >>> NonFinalBase().mtd()
    1
    >>> class PySub(NonFinalBase): pass   # still subclassable (not a final type)
    """
    @final
    cpdef int mtd(self):
        return 1


def test_final_class(FinalClass c):
    print(u"Type tested")
