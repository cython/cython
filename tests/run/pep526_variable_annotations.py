# cython: language_level=3
# mode: run
# tag: pure3.6, pep526, pep484, warnings

import cython

from typing import Dict, List, TypeVar, Optional, Generic, Tuple
try:
    from typing import ClassVar
except ImportError:
    ClassVar = Optional  # fake it in Py3.5


var = 1  # type: annotation
var: int = 2
fvar: float = 1.2
some_number: cython.int    # variable without initial value
some_list: List[int] = []  # variable with initial value
t: Tuple[int, ...] = (1, 2, 3)
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
    var: int = 2
    fvar: float = 1.5
    some_number: cython.int    # variable without initial value
    some_list: List[int] = []  # variable with initial value
    t: Tuple[int, ...] = (1, 2, 3)
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
    """
    captain: str = 'Picard'               # instance variable with default
    damage: cython.int                    # instance variable without default
    stats: ClassVar[Dict[str, int]] = {}  # class variable
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
    stats: ClassVar[Dict[str, int]] = {}  # class variable
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

    >>> class D(object):
    ...     def __getitem__(self, x): return 2
    ...     def __iter__(self): return iter([1, 2, 3])
    >>> iter_declared_dict(D())
    6.0
    """
    typed_dict : Dict[float, float] = d
    s = 0.0
    for key in typed_dict:
        s += d[key]
    return s


@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode",
)
def iter_declared_dict_arg(d : Dict[float, float]):
    """
    >>> d = {1.1: 2.5, 3.3: 4.5}
    >>> iter_declared_dict_arg(d)
    7.0

    >>> class D(object):
    ...     def __getitem__(self, x): return 2
    ...     def __iter__(self): return iter([1, 2, 3])
    >>> iter_declared_dict_arg(D())
    6.0
    """
    s = 0.0
    for key in d:
        s += d[key]
    return s


_WARNINGS = """
37:19: Unknown type declaration in annotation, ignoring
38:12: Unknown type declaration in annotation, ignoring
39:18: Unknown type declaration in annotation, ignoring
73:19: Unknown type declaration in annotation, ignoring
# FIXME: these are sort-of evaluated now, so the warning is misleading
126:21: Unknown type declaration in annotation, ignoring
137:35: Unknown type declaration in annotation, ignoring
"""
