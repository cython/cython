# cython: language_level=3
# mode: run

import sys
import cython

from typing import Dict, List, Tuple
try:
    import typing
    from typing import Set as _SET_
except ImportError:
    pass  # this should allow Cython to interpret the directives even when the module doesn't exist


@cython.cclass
class A:
    def __str__(self):
        return "A()"


@cython.cclass
class B(A):
    def __str__(self):
        return "B()"


def min_plain_pyversion(major, minor):
    if cython.compiled or sys.version_info >= (major, minor):
        return lambda func: func
    else:
        return lambda func: None


def test_subscripted_types():
    """
    >>> test_subscripted_types()
    dict[int,float] object
    dict[int,float] object
    list[int] object
    list[int] object
    list object
    set[Python object] object
    tuple[int,Python object,float] object
    tuple[int,Python object,float] object
    """
    a1: typing.Dict[cython.int, cython.float] = {}
    a2: dict[cython.int, cython.float] = {}
    b1: List[cython.int] = []
    b2: list[cython.int] = []
    b3: List = []  # doesn't need to be subscripted
    c: _SET_[object] = set()
    t1: Tuple[cython.int, object, cython.float] = (1, 'a', 1.0)
    t2: tuple[cython.int, object, cython.float] = (1, 'a', 1.0)


    print(cython.typeof(a1) + ("[int,float] object" if not cython.compiled else ""))
    print(cython.typeof(a2) + ("[int,float] object" if not cython.compiled else ""))
    print(cython.typeof(b1) + ("[int] object" if not cython.compiled else ""))
    print(cython.typeof(b2) + ("[int] object" if not cython.compiled else ""))
    print(cython.typeof(b3) + (" object" if not cython.compiled else ""))
    print(cython.typeof(c) + ("[Python object] object" if not cython.compiled else ""))
    print(cython.typeof(t1) + ("[int,Python object,float] object" if not cython.compiled else ""))
    print(cython.typeof(t2) + ("[int,Python object,float] object" if not cython.compiled else ""))


@min_plain_pyversion(3, 11)
# This part of the test is failing in Python 3.9 and 3.10 with the following exception in Shadow.py:
# isinstance() argument 2 cannot be a parameterized generic
def test_casting_subscripted_types():
    """
    >>> test_casting_subscripted_types()
    tuple:
    tuple[list object,int,int] object 1 2
    tuple object 1.0 2.0
    list:
    list[int] object 1
    list object 1.0
    dict:
    dict[str object,float] object 2.0
    dict object 2
    float 3.0
    Python object 3
    """
    print('tuple:')
    t: tuple[list, cython.float, cython.float] = ([], 1.0, 2.0)
    x0 = cython.cast(tuple[list, cython.int, cython.int], t)
    y0 = cython.cast(tuple, t)
    print(
        cython.typeof(x0) + ('[list object,int,int] object' if not cython.compiled else ''),
        x0[1] if cython.compiled else int(x0[1]),
        x0[2] if cython.compiled else int(x0[2]),
    )
    print(cython.typeof(y0) + (' object' if not cython.compiled else ''), y0[1], y0[2])
    print('list:')
    l: list[cython.float] = [1.0, 2.0]
    x1 = cython.cast(list[cython.int], l)
    y1 = cython.cast(list, l)
    print(cython.typeof(x1) + ('[int] object' if not cython.compiled else ""), int(x1[0]) if not cython.compiled else x1[0])
    print(cython.typeof(y1) + (' object' if not cython.compiled else ""), y1[0])
    print('dict:')
    d: dict[str, cython.int] = {'a': 1, 'b': 2}
    x2 = cython.cast(dict[str, cython.float], d)
    y2 = cython.cast(dict, d)
    print(
        cython.typeof(x2) + ('[str object,float] object' if not cython.compiled else ""),
        x2['b'] if cython.compiled else float(x2['b'])
    )
    print(cython.typeof(y2) + (' object' if not cython.compiled else ""), y2['b'])

    d2: dict[cython.int, str] = {3: '3'}
    for k1 in cython.cast(dict[cython.float, str], d2):
        print(
            cython.typeof(k1) if cython.compiled else 'float',
            k1 if cython.compiled else float(k1)
        )

    for k2 in cython.cast(dict, d2):
        print(cython.typeof(k2) if cython.compiled else 'Python object', k2)


def test_tuple_with_int_str_subscript():
    """
    >>> test_tuple_with_int_str_subscript()
    str object
    int object
    str object
    int object
    str object
    int object
    FooBar
    3
    """
    a: tuple[str, int] = ("Foo", 1)
    b: Tuple[str, int] = ("Bar", 2)
    print(cython.typeof(a[0]) + (" object" if not cython.compiled else ""))
    print(cython.typeof(a[1]) + (" object" if not cython.compiled else ""))
    print(cython.typeof(b[0]) + (" object" if not cython.compiled else ""))
    print(cython.typeof(b[1]) + (" object" if not cython.compiled else ""))
    print(cython.typeof(a[0] + b[0]) + (" object" if not cython.compiled else ""))
    print(cython.typeof(a[1] + b[1]) + (" object" if not cython.compiled else ""))
    print(a[0] + b[0])
    print(a[1] + b[1])

def test_assignment_tuple_with_subscript():
    """
    >>> test_assignment_tuple_with_subscript()
    int int
    Python object Python object
    float float
    5 5 5.0
    6 6 6.0
    """
    a: tuple[cython.int, cython.int] = (5, 6)
    b: tuple = a
    c: tuple[cython.float, cython.float] = b
    print(cython.typeof(a[0]), cython.typeof(a[1])
    )
    print(
        cython.typeof(b[0]) if cython.compiled else "Python object",
        cython.typeof(b[1]) if cython.compiled else "Python object"
    )
    print(
        cython.typeof(c[0]) if cython.compiled else "float",
        cython.typeof(c[1]) if cython.compiled else "float"
    )
    print(a[0], b[0], c[0] if cython.compiled else float(c[0]))
    print(a[1], b[1], c[1] if cython.compiled else float(c[1]))


def test_list_with_str_subscript():
    """
    >>> test_list_with_str_subscript()
    str object
    str object
    str object
    FooBar
    """
    a: list[str] = ["Foo"]
    b: List[str] = ["Bar"]
    print(cython.typeof(a[0]) + (" object" if not cython.compiled else ""))
    print(cython.typeof(b[0]) + (" object" if not cython.compiled else ""))
    print(cython.typeof(a[0] + b[0]) + (" object" if not cython.compiled else ""))
    print(a[0] + b[0])


def test_list_with_int_subscript():
    """
    >>> test_list_with_int_subscript()
    int
    int
    int
    int
    3
    """
    a: List[cython.int] = [1]
    b: list[cython.int] = [2]
    c = a[0] + b[0]
    print(cython.typeof(a[0]))
    print(cython.typeof(b[0]))
    print(cython.typeof(a[0] + b[0]))
    print(cython.typeof(c))
    print(c)


def test_dict_with_subscript():
    """
    >>> test_dict_with_subscript()
    int
    int
    int
    int
    3
    """
    a: Dict[str, cython.int] = {"a": 1}
    b: Dict[cython.int, cython.int] = {1: 2}
    c = a["a"] + b[1]
    print(cython.typeof(a["a"]))
    print(cython.typeof(b[1]))
    print(cython.typeof(a["a"] + b[1]))
    print(cython.typeof(c))
    print(c)


def test_assignment_list_with_subscript():
    """
    >>> test_assignment_list_with_subscript()
    int
    Python object
    float
    5 5 5.0
    """
    a: list[cython.int] = [5]
    b: list = a
    c: list[cython.float] = b
    print(cython.typeof(a[0]))
    print(cython.typeof(b[0]) if cython.compiled else 'Python object')
    print(cython.typeof(c[0]) if cython.compiled else 'float')
    print(a[0], b[0], c[0] if cython.compiled else float(c[0]))


def test_assignment_dict_with_subscript():
    """
    >>> test_assignment_dict_with_subscript()
    int
    Python object
    float
    5 5 5.0
    """
    a: dict[str, cython.int] = {'a': 5}
    b: dict = a
    c: dict[str, cython.float] = b
    print(cython.typeof(a['a']) if cython.compiled else 'int')
    print(cython.typeof(b['a']) if cython.compiled else 'Python object')
    print(cython.typeof(c['a']) if cython.compiled else 'float')
    print(a['a'], b['a'], c['a'] if cython.compiled else float(c['a']))


@min_plain_pyversion(3, 15)
def test_assignment_frozendict_with_subscript():
    """
    >>> test_assignment_frozendict_with_subscript()
    int
    Python object
    float
    5 5 5.0
    """
    a: frozendict[str, cython.int] = frozendict({'a': 5})
    b: frozendict = a
    c: frozendict[str, cython.float] = b
    print(cython.typeof(a['a']))
    print(cython.typeof(b['a']) if cython.compiled else 'Python object')
    print(cython.typeof(c['a']) if cython.compiled else 'float')
    print(a['a'], b['a'], c['a'] if cython.compiled else float(c['a']))


def test_failed_assignment_tuple_with_subscript():
    """
    >>> test_failed_assignment_tuple_with_subscript()
    5 5 5
    """
    a: tuple[cython.int, cython.int] = (5, 5)
    b: tuple = a
    c: tuple[str, str] = b
    print(a[0], b[0], c[0])

if cython.compiled:
    test_failed_assignment_tuple_with_subscript.__doc__ = """
    >>> test_failed_assignment_tuple_with_subscript()  #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    TypeError: Expected str, got int
    """


def test_failed_assignment_list_with_subscript():
    """
    >>> test_failed_assignment_list_with_subscript()
    5 5 5
    """
    a: list[cython.int] = [5]
    b: list = a
    c: list[str] = b
    print(a[0], b[0], c[0])

if cython.compiled:
    test_failed_assignment_list_with_subscript.__doc__ = """
    >>> test_failed_assignment_list_with_subscript()  #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    TypeError: Expected str, got int
    """

@cython.infer_types(True)
def test_iteration_over_tuple_with_subscript():
    """
    >>> test_iteration_over_tuple_with_subscript()
    2 int
    bar str
    A() A
    B() B
    """
    a: tuple[cython.int, str] = (2, 'bar')
    for c in a:
        print(c, cython.typeof(c))
    # Iterating must use spanning type, not subscripted type, so that it works even when the tuple is heterogeneous.
    b: tuple[A, B] = (A(), B())
    for s in b:
        print(s, cython.typeof(s))

if cython.compiled:
    test_iteration_over_tuple_with_subscript.__doc__ = """
    >>> test_iteration_over_tuple_with_subscript()
    2 Python object
    bar Python object
    A() A
    B() A
    """


@cython.infer_types(True)
def test_iteration_over_list_with_subscript():
    """
    >>> test_iteration_over_list_with_subscript()
    int
    int
    3
    """
    b: cython.int = 1
    a: list[cython.int] = [2]
    for c in a:
        print(cython.typeof(c))
        print(cython.typeof(b + c))
        print(b + c)


@cython.infer_types(True)
def test_iteration_over_set_with_subscript():
    """
    >>> test_iteration_over_set_with_subscript()
    int
    int
    3
    """
    b: cython.int = 1
    a: set[cython.int] = {2}
    for c in a:
        print(cython.typeof(c))
        print(cython.typeof(b + c))
        print(b + c)


@cython.infer_types(True)
def test_iteration_over_frozenset_with_subscript():
    """
    >>> test_iteration_over_frozenset_with_subscript()
    int
    int
    3
    """
    b: cython.int = 1
    a: frozenset[cython.int] = frozenset({2})
    for c in a:
        print(cython.typeof(c))
        print(cython.typeof(b + c))
        print(b + c)


@cython.infer_types(True)
def test_iteration_over_dict_with_subscript():
    """
    >>> test_iteration_over_dict_with_subscript()
    int
    int
    3
    """
    b: cython.int = 1
    a: dict[cython.int, cython.str] = {2: 'a'}
    for c in a:
        print(cython.typeof(c))
        print(cython.typeof(b + c))
        print(b + c)


@min_plain_pyversion(3, 15)
@cython.infer_types(True)
def test_iteration_over_frozendict_with_subscript():
    """
    >>> test_iteration_over_frozendict_with_subscript()
    int
    int
    3
    """
    b: cython.int = 1
    a: frozendict[cython.int, cython.str] = frozendict({2: 'a'})
    for c in a:
        print(cython.typeof(c))
        print(cython.typeof(b + c))
        print(b + c)


def test_inference_of_list_constructor():
    """
    >>> test_inference_of_list_constructor()
    list[str object] object
    list[int] object
    list[str object] object
    list[int] object
    list[int] object
    """
    t: tuple[str, str, str] = ('a', 'b', 'c')
    l: list[cython.int] = [1, 2, 3]
    d: dict[str, cython.int] = {'a': 1, 'b': 2}
    s: set[cython.int] = {1, 2, 3}
    f: frozenset[cython.int] = frozenset({1, 2, 3})

    lt = list(t)
    ll = list(l)
    ld = list(d)
    ls = list(s)
    lf = list(f)

    print(cython.typeof(lt) + ("[str object] object" if not cython.compiled else ""))
    print(cython.typeof(ll) + ("[int] object" if not cython.compiled else ""))
    print(cython.typeof(ld) + ("[str object] object" if not cython.compiled else ""))
    print(cython.typeof(ls) + ("[int] object" if not cython.compiled else ""))
    print(cython.typeof(lf) + ("[int] object" if not cython.compiled else ""))


def test_inference_of_set_constructor():
    """
    >>> test_inference_of_set_constructor()
    set[str object] object
    set[int] object
    set[str object] object
    set[int] object
    set[int] object
    """
    t: tuple[str, str, str] = ('a', 'b', 'c')
    l: list[cython.int] = [1, 2, 3]
    d: dict[str, cython.int] = {'a': 1, 'b': 2}
    s: set[cython.int] = {1, 2, 3}
    f: frozenset[cython.int] = frozenset({1, 2, 3})

    st = set(t)
    sl = set(l)
    sd = set(d)
    ss = set(s)
    sf = set(f)

    print(cython.typeof(st) + ("[str object] object" if not cython.compiled else ""))
    print(cython.typeof(sl) + ("[int] object" if not cython.compiled else ""))
    print(cython.typeof(sd) + ("[str object] object" if not cython.compiled else ""))
    print(cython.typeof(ss) + ("[int] object" if not cython.compiled else ""))
    print(cython.typeof(sf) + ("[int] object" if not cython.compiled else ""))


def test_inference_of_frozenset_constructor():
    """
    >>> test_inference_of_frozenset_constructor()
    frozenset[str object] object
    frozenset[int] object
    frozenset[str object] object
    frozenset[int] object
    frozenset[int] object
    """
    t: tuple[str, str, str] = ('a', 'b', 'c')
    l: list[cython.int] = [1, 2, 3]
    d: dict[str, cython.int] = {'a': 1, 'b': 2}
    s: set[cython.int] = {1, 2, 3}
    f: frozenset[cython.int] = frozenset({1, 2, 3})

    ft = frozenset(t)
    fl = frozenset(l)
    fd = frozenset(d)
    fs = frozenset(s)
    ff = frozenset(f)

    print(cython.typeof(ft) + ("[str object] object" if not cython.compiled else ""))
    print(cython.typeof(fl) + ("[int] object" if not cython.compiled else ""))
    print(cython.typeof(fd) + ("[str object] object" if not cython.compiled else ""))
    print(cython.typeof(fs) + ("[int] object" if not cython.compiled else ""))
    print(cython.typeof(ff) + ("[int] object" if not cython.compiled else ""))


def test_inference_of_dict_constructor():
    """
    >>> test_inference_of_dict_constructor()
    dict[str object,int] object
    dict[str object,int object] object
    dict[str object,str object] object
    dict object
    dict object
    """
    d: dict[str, cython.int] = {'a': 1, 'b': 2}
    lt: list[tuple[str, int]] = [('a', 1), ('b', 2)]
    lls: list[list[str]] = [['a', 'b'], ['c', 'd']]
    ll: list[list] = [['a', 'b'], ['c', 'd']]
    l: list = [['a', 'b'], ['c', 'd']]

    dd = dict(d)
    dlt = dict(lt)
    dlls = dict(lls)
    dll = dict(ll)
    dl = dict(l)

    print(cython.typeof(dd) + ("[str object,int] object" if not cython.compiled else ""))
    print(cython.typeof(dlt) + ("[str object,int object] object" if not cython.compiled else ""))
    print(cython.typeof(dlls) + ("[str object,str object] object" if not cython.compiled else ""))
    print(cython.typeof(dll) + (" object" if not cython.compiled else ""))
    print(cython.typeof(dl) + (" object" if not cython.compiled else ""))


@min_plain_pyversion(3, 15)
def test_inference_of_frozendict_constructor():
    """
    >>> test_inference_of_frozendict_constructor()
    frozendict[str object,int] object
    frozendict[str object,int] object
    frozendict[str object,int object] object
    frozendict[str object,str object] object
    frozendict object
    frozendict object
    """
    d: dict[str, cython.int] = {'a': 1, 'b': 2}
    fd: frozendict[str, cython.int] = frozendict({'a': 1, 'b': 2})
    lt: list[tuple[str, int]] = [('a', 1), ('b', 2)]
    lls: list[list[str]] = [['a', 'b'], ['c', 'd']]
    ll: list[list] = [['a', 'b'], ['c', 'd']]
    l: list = [['a', 'b'], ['c', 'd']]


    dd = frozendict(d)
    fdd = frozendict(fd)
    fdlt = frozendict(lt)
    fdlls = frozendict(lls)
    fdll = frozendict(ll)
    fdl = frozendict(l)

    print(cython.typeof(dd) + ("[str object,int] object" if not cython.compiled else ""))
    print(cython.typeof(fdd) + ("[str object,int] object" if not cython.compiled else ""))
    print(cython.typeof(fdlt) + ("[str object,int object] object" if not cython.compiled else ""))
    print(cython.typeof(fdlls) + ("[str object,str object] object" if not cython.compiled else ""))
    print(cython.typeof(fdll) + (" object" if not cython.compiled else ""))
    print(cython.typeof(fdl) + (" object" if not cython.compiled else ""))


def test_inference_of_tuple_common_subscripted_type():
    """
    >>> test_inference_of_tuple_common_subscripted_type()
    list[A] object
    """
    t: tuple[A, B] = (A(), B())
    l = list(t)
    print(cython.typeof(l) + ("[A] object" if not cython.compiled else ""))

