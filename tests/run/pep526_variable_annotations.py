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

try:
    import typing
    from typing import Set as _SET_
    from typing import ClassVar
except ImportError:
    pass  # this should allow Cython to interpret the directives even when the module doesn't exist


var = 1  # type: annotation
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
    var = 1  # type: annotation
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


# FIXME: this fails in Py3.7 now
#class Box(Generic[T]):
#    def __init__(self, content):
#        self.content: T = content
#
#box = Box(content=5)


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
    typed_dict : Dict[cython.float, cython.float] = d
    s = 0.0
    for key in typed_dict:
        s += d[key]
    return s


@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode",
)
def iter_declared_dict_arg(d : Dict[cython.float, cython.float]):
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
