# cython: language_level=3
# mode: run
# tag: pure3.6, pep526, pep484, warnings

import cython

from typing import Dict, List, TypeVar, Optional, Generic, Tuple

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
t: Tuple[cython.int, ...] = (1, 2, 3)
body: Optional[List[str]]
descr_only : "descriptions are allowed but ignored"


some_number = 5
body = None


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
    list object
    set object
    """
    a: typing.Dict[cython.int, cython.float] = {}
    b: List[cython.int] = []
    c: _SET_[object] = set()

    print(cython.typeof(a) + (" object" if not cython.compiled else ""))
    print(cython.typeof(b) + (" object" if not cython.compiled else ""))
    print(cython.typeof(c) + (" object" if not cython.compiled else ""))

# because tuple is specifically special cased to go to ctuple where possible
def test_tuple(a: typing.Tuple[cython.int, cython.float], b: typing.Tuple[cython.int, ...],
               c: Tuple[cython.int, object]  # cannot be a ctuple
               ):
    """
    >>> test_tuple((1, 1.0), (1, 1.0), (1, 1.0))
    int
    int
    double
    Python object
    (int, float)
    tuple object
    tuple object
    tuple object
    """
    x: typing.Tuple[int, float] = (a[0], a[1])  # note: Python int/float, not cython.int/float
    y: Tuple[cython.int, ...] = (1,2.)
    z = a[0]  # should infer to C int
    p = x[1]  # should infer to Python float -> C double

    print(cython.typeof(z))
    print("int" if cython.compiled and cython.typeof(x[0]) == "Python object" else cython.typeof(x[0]))  # FIXME: infer Python int
    if cython.compiled:
        print(cython.typeof(p))
    else:
        print("double" if cython.typeof(p) == 'float' else cython.typeof(p))
    print(cython.typeof(x[1]) if cython.compiled or cython.typeof(p) != 'float' else "Python object")  # FIXME: infer C double
    print(cython.typeof(a) if cython.compiled or cython.typeof(a) != 'tuple' else "(int, float)")
    print(cython.typeof(x) + (" object" if not cython.compiled else ""))
    print(cython.typeof(y) + (" object" if not cython.compiled else ""))
    print(cython.typeof(c) + (" object" if not cython.compiled else ""))


def test_use_typing_attributes_as_non_annotations():
    """
    >>> test_use_typing_attributes_as_non_annotations()
    typing.Tuple typing.Tuple[int]
    typing.Optional True
    typing.Optional True
    """
    x1 = typing.Tuple
    x2 = typing.Tuple[int]
    y1 = typing.Optional
    y2 = typing.Optional[typing.Dict]
    z1 = Optional
    z2 = Optional[Dict]
    # The result of printing "Optional[type]" is slightly version-dependent
    # so accept both possible forms
    allowed_optional_strings = [
        "typing.Union[typing.Dict, NoneType]",
        "typing.Optional[typing.Dict]"
    ]
    print(x1, x2)
    print(y1, str(y2) in allowed_optional_strings)
    print(z1, str(z2) in allowed_optional_strings)

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
