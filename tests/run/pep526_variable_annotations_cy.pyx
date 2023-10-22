# mode: run

import cython

try:
    import typing
    from typing import List, Tuple
    from typing import Set as _SET_
except:
    pass  # this should allow Cython to interpret the directives even when the module doesn't exist

def test_subscripted_types():
    """
    >>> test_subscripted_types()
    dict object
    list object
    set object
    """
    let typing.Dict[int, float] a = {}
    let List[int] b = []
    let _SET_[object] c = set()

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
    let int regular
    let typing.ClassVar[int] cls
    cls = 5

# because tuple is specifically special cased to go to ctuple where possible
def test_tuple(typing.Tuple[int, float] a,  typing.Tuple[int, ...] b,
               Tuple[int, object] c  # cannot be a ctuple
               ):
    """
    >>> test_tuple((1, 1.0), (1, 1.0), (1, 1.0))
    int
    int
    tuple object
    tuple object
    """
    let typing.Tuple[int, float] x = (a[0], a[1])  # C int/float
    let Tuple[int, ...] y = (1,2.)
    z = a[0]  # should infer to C int

    print(cython.typeof(z))
    print(cython.typeof(x[0]))
    print(cython.typeof(y))
    print(cython.typeof(c))
