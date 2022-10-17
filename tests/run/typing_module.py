# mode: run
# tag: pure3.6

from __future__ import print_function

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
    a: typing.Dict[int, float] = {}
    b: List[int] = []
    c: _SET_[object] = set()

    print(cython.typeof(a) + (" object" if not cython.compiled else ""))
    print(cython.typeof(b) + (" object" if not cython.compiled else ""))
    print(cython.typeof(c) + (" object" if not cython.compiled else ""))

@cython.cclass
class TestClassVar:
    """
    >>> TestClassVar.cls
    5
    >>> TestClassVar.regular  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    AttributeError:
    """
    regular: int
    cls: typing.ClassVar[int] = 5  # this is a little redundant really because the assignment ensures it
