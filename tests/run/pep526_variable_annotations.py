# cython: language_level=3
# mode: run
# tag: pure3.7, pep526, pep484, warnings

# for the benefit of the pure tests, don't require annotations
# to be evaluated
from __future__ import annotations

import cython

# Don't add FrozenSet to this list - it's necessary for one of the tests
# that it isn't a module global name
from typing import Dict, List, TypeVar, Optional, Generic, Tuple, Union
import sys

try:
    import typing
    from typing import Set as _SET_
    from typing import ClassVar
except ImportError:
    pass  # this should allow Cython to interpret the directives even when the module doesn't exist


pyobj_var = 1  # type: annotation
var: cython.int = 2
fvar: cython.float = 1.2
some_number: cython.int    # variable without initial value
some_list: List[cython.int] = []  # variable with initial value
another_list: list[cython.int] = []
t: Tuple[cython.int, ...] = (1, 2, 3)
t2: tuple[cython.int, ...]
body: Optional[List[str]]
body2: Union[List[str], None]
body3: List[str] | None
descr_only : "descriptions are allowed but ignored"


some_number = 5
body = None
body2 = None


def f():
    """
    >>> f()
    (2, 1.5, [], (1, 2, 3))
    """
    pyobj_var = 1  # type: annotation
    var: cython.int = 2
    fvar: cython.float = 1.5
    some_number: cython.int    # variable without initial value
    some_list: List[cython.int] = []  # variable with initial value
    t: Tuple[cython.int, ...] = (1, 2, 3)
    body: Optional[List[str]]
    body2: Union[None, List[str]]
    body3: None | List[str]
    descr_only: "descriptions are allowed but ignored"

    return var, fvar, some_list, t


class BasicStarship(object):
    """
    >>> bs = BasicStarship(5)
    >>> bs.damage
    5
    >>> bs.captain
    'Picard'
    >>> bs.stats
    {}
    >>> BasicStarship.stats
    {}
    """
    captain: str = 'Picard'               # instance variable with default
    damage: cython.int                    # instance variable without default
    stats: ClassVar[Dict[str, cython.int]] = {}  # class variable
    descr_only: "descriptions are allowed but ignored"

    def __init__(self, damage):
        self.damage = damage


@cython.cclass
class BasicStarshipExt(object):
    """
    >>> bs = BasicStarshipExt(5)
    >>> bs.test()
    (5, 'Picard', {})
    """
    captain: str = 'Picard'               # instance variable with default
    damage: cython.int                    # instance variable without default
    stats: ClassVar[Dict[str, cython.int]] = {}  # class variable
    descr_only: "descriptions are allowed but ignored"

    def __init__(self, damage):
        self.damage = damage

    def test(self):
        return self.damage, self.captain, self.stats


T = TypeVar('T')


class Box(Generic[T]):
    def __init__(self, content):
        self.content: T = content

box = Box(content=5)


class Cls(object):
    pass


c = Cls()
c.x: int = 0  # Annotates c.x with int.
c.y: int      # Annotates c.y with int.

d = {}
d['a']: int = 0  # Annotates d['a'] with int.
d['b']: int      # Annotates d['b'] with int.

(x): int      # Annotates x with int, (x) treated as expression by compiler.
(y): int = 0  # Same situation here.


@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode",
)
def iter_declared_dict(d):
    """
    >>> d = {1.1: 2.5, 3.3: 4.5}
    >>> iter_declared_dict(d)
    7.0

    # specialized "compiled" test in module-level __doc__
    """
    typed_dict : Dict[object, cython.float] = d
    s = 0.0
    for key in typed_dict:
        s += d[key]
    return s


@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode",
)
def iter_declared_dict_arg(d : Dict[object, cython.float]):
    """
    >>> d = {1.1: 2.5, 3.3: 4.5}
    >>> iter_declared_dict_arg(d)
    7.0

    # module level "compiled" test in __doc__ below
    """
    s = 0.0
    for key in d:
        s += d[key]
    return s


def literal_list_ptr():
    """
    >>> literal_list_ptr()
    4
    """
    a : cython.p_int = [1, 2, 3, 4, 5]
    return a[3]


def test_subscripted_types():
    """
    >>> test_subscripted_types()
    dict object
    dict object
    list object
    list object
    list object
    set object
    """
    a1: typing.Dict[cython.int, cython.float] = {}
    a2: dict[cython.int, cython.float] = {}
    b1: List[cython.int] = []
    b2: list[cython.int] = []
    b3: List = []  # doesn't need to be subscripted
    c: _SET_[object] = set()

    print(cython.typeof(a1) + (" object" if not cython.compiled else ""))
    print(cython.typeof(a2) + (" object" if not cython.compiled else ""))
    print(cython.typeof(b1) + (" object" if not cython.compiled else ""))
    print(cython.typeof(b2) + (" object" if not cython.compiled else ""))
    print(cython.typeof(b3) + (" object" if not cython.compiled else ""))
    print(cython.typeof(c) + (" object" if not cython.compiled else ""))

if cython.compiled:
    test_subscripted_types.__doc__ = """
    >>> test_subscripted_types()
    dict[int,float] object
    dict[int,float] object
    list[int] object
    list[int] object
    list object
    set[Python object] object
    """

if sys.version_info >= (3, 11) or cython.compiled:
    # This part of the test is failing in Python 3.9 and 3.10 with the following exception in Shadow.py:
    # isinstance() argument 2 cannot be a parameterized generic

    def test_casting_subscripted_types():
        """
        >>> test_casting_subscripted_types()
        list 1.0
        list 1.0
        dict 2
        dict 2
        int 3
        int 3
        """
        # list
        l: list[cython.float] = [1.0, 2.0]
        x1 = cython.cast(list[cython.int], l)
        y1 = cython.cast(list, l)
        print(cython.typeof(x1), x1[0])
        print(cython.typeof(y1), y1[0])
        # dict
        d: dict[str, cython.int] = {'a': 1, 'b': 2}
        x2 = cython.cast(dict[str, cython.float], d)
        y2 = cython.cast(dict, d)
        print(cython.typeof(x2), x2['b'])
        print(cython.typeof(y2), y2['b'])

        d2: dict[cython.int, str] = {3: '3'}
        for k1 in cython.cast(dict[cython.float, str], d2):
            print(cython.typeof(k1), k1)

        for k2 in cython.cast(dict, d2):
            print(cython.typeof(k2), k2)


if cython.compiled:
    test_casting_subscripted_types.__doc__ = """
    >>> test_casting_subscripted_types()
    list[int] object 1
    list object 1.0
    dict[str object,float] object 2.0
    dict object 2
    float 3.0
    Python object 3
    """


def test_use_typing_attributes_as_non_annotations():
    """
    >>> test_use_typing_attributes_as_non_annotations()
    typing.Tuple typing.Tuple[int]
    Optional True
    Optional True
    Optional True
    Union typing.FrozenSet
    Union typing.Dict
    """
    x1 = typing.Tuple
    x2 = typing.Tuple[int]
    y1 = typing.Optional
    # It's important for the test that FrozenSet isn't available in the module namespace,
    # since one bug would have looked it up there rather than as an attribute of typing
    y2 = typing.Optional[typing.FrozenSet]
    z1 = Optional
    z2 = Optional[Dict]
    q1 = typing.Union
    q2 = typing.Union[typing.FrozenSet]
    w1 = Union
    w2 = Union[Dict]

    def name_of(special_decl):
        try:
            return special_decl.__name__
        except AttributeError:
            return str(special_decl).partition('.')[-1]

    # The result of printing "Optional[type]" is slightly version-dependent
    # so accept different forms.
    allowed_optional_frozenset_strings = [
        "typing.Union[typing.FrozenSet, NoneType]",
        "typing.Optional[typing.FrozenSet]",
        "typing.FrozenSet | None",
    ]
    allowed_optional_dict_strings = [
        "typing.Union[typing.Dict, NoneType]",
        "typing.Optional[typing.Dict]",
        "typing.Dict | None",
    ]
    print(x1, x2)
    print(name_of(y1), y1 is z1 or (y1, z1))
    print(name_of(y1), str(y2) in allowed_optional_frozenset_strings  or  str(y2))
    print(name_of(z1), str(z2) in allowed_optional_dict_strings  or  str(z2))
    print(name_of(q1), str(q2) in ["typing.Union[typing.FrozenSet, NoneType]", "typing.FrozenSet | None"] or str(q2))
    print(name_of(w1), str(w2) in ["typing.Union[typing.Dict, NoneType]", "typing.Dict | None"] or str(w2))

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

def test_list_with_int_subscription():
    """
    >>> test_list_with_int_subscription()
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

def test_dict_with_subscription():
    """
    >>> test_list_with_int_subscription()
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

def test_assignment_list_with_subscription():
    """
    >>> test_assignment_list_with_subscription()
    int
    int
    int
    5 5 5
    """
    a: list[cython.int] = [5]
    b: list = a
    c: list[cython.float] = b
    print(cython.typeof(a[0]))
    print(cython.typeof(b[0]))
    print(cython.typeof(c[0]))
    print(a[0], b[0], c[0])

if cython.compiled:
    test_assignment_list_with_subscription.__doc__ = """
    >>> test_assignment_list_with_subscription()
    int
    Python object
    float
    5 5 5.0
    """

def test_assignment_dict_with_subscription():
    """
    >>> test_assignment_dict_with_subscription()
    int
    int
    int
    5 5 5
    """
    a: dict[str, cython.int] = {'a': 5}
    b: dict = a
    c: dict[str, cython.float] = b
    print(cython.typeof(a['a']))
    print(cython.typeof(b['a']))
    print(cython.typeof(c['a']))
    print(a['a'], b['a'], c['a'])

if cython.compiled:
    test_assignment_dict_with_subscription.__doc__ = """
    >>> test_assignment_dict_with_subscription()
    int
    Python object
    float
    5 5 5.0
    """

def test_failed_assignment_list_with_subscription():
    """
    >>> test_failed_assignment_list_with_subscription()
    5 5 5
    """
    a: list[cython.int] = [5]
    b: list = a
    c: list[str] = b
    print(a[0], b[0], c[0])

if cython.compiled:
    test_failed_assignment_list_with_subscription.__doc__ = """
    >>> test_failed_assignment_list_with_subscription()  #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    TypeError: Expected str, got int
    """

@cython.infer_types(True)
def test_iteration_over_list_with_subscription():
    """
    >>> test_iteration_over_list_with_subscription()
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
def test_iteration_over_set_with_subscription():
    """
    >>> test_iteration_over_set_with_subscription()
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
def test_iteration_over_frozenset_with_subscription():
    """
    >>> test_iteration_over_frozenset_with_subscription()
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
def test_iteration_over_set_with_subscription():
    """
    >>> test_iteration_over_set_with_subscription()
    int
    int
    3
    """
    b: cython.int = 1
    a: dict[cython.int, cython.int] = {2: 3}
    for c in a:
        print(cython.typeof(c))
        print(cython.typeof(b + c))
        print(b + c)



try:
    import numpy.typing as npt
    import numpy as np
except ImportError:
    # we can't actually use numpy typing right now, it was just part
    # of a reproducer that caused a compiler crash. We don't need it
    # available to use it in annotations, so don't fail if it's not there
    pass


def list_float_to_numpy(z: List[float]) -> List[npt.NDArray[np.float64]]:
    # since we're not actually requiring numpy, don't make the return type match
    assert cython.typeof(z) == 'list'
    return [z[0]]

if cython.compiled:
    __doc__ = """
    # passing non-dicts to variables declared as dict now fails
    >>> class D(object):
    ...     def __getitem__(self, x): return 2
    ...     def __iter__(self): return iter([1, 2, 3])
    >>> iter_declared_dict(D())  # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError: Expected dict, got D
    >>> iter_declared_dict_arg(D())  # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError: Expected dict, got D
    """

_WARNINGS = """
"""
