# mode: run

import cython

try:
    import typing
    from typing import List
    from typing import Set as _SET_
except ImportError:
    pass  # this should allow Cython to interpret the directives even when the module doesn't exist

def test_subscripted_types():
    """
    >>> test_subscripted_types()
    dict object
    list object
    set object
    """
    cdef typing.Dict[int, float] a = {}
    cdef List[int] b = []
    cdef _SET_[object] c = set()

    print(cython.typeof(a))
    print(cython.typeof(b))
    print(cython.typeof(c))

cdef class TestClassVar:
    """
    >>> TestClassVar.cls
    5
    >>> TestClassVar.regular  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    AttributeError:
    """
    cdef int regular
    cdef typing.ClassVar[int] cls
    cls = 5
