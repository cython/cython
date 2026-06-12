# cython: auto_cpdef=True
# mode: run
# tag: directive,auto_cpdef,dunders,cclass,len,repr,str,hash

# Self-only dunders (len/str/repr/hash + unary) have no reflected-operand
# hazard, so they are dispatched through the cpdef vtable slot even on a
# NON-final extension type.  Vtable dispatch still honours Python-subclass
# overrides (skip_dispatch=0), so the semantics match plain Python.

import cython
from cython import cclass, Py_hash_t


@cclass
class Box:
    n: cython.int

    def __init__(self, n: cython.int) -> None:
        self.n = n

    def __len__(self) -> cython.int:
        return self.n

    def __repr__(self) -> str:
        return f"Box({self.n})"

    def __str__(self) -> str:
        return f"<{self.n}>"

    def __hash__(self) -> Py_hash_t:
        return self.n * 7

    def __neg__(self) -> "Box":
        return Box(-self.n)


@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'len']")
def call_len(b: Box) -> cython.Py_ssize_t:
    """
    >>> call_len(Box(42))
    42
    """
    return len(b)


def call_repr(b: Box):
    """
    >>> call_repr(Box(5))
    'Box(5)'
    """
    return repr(b)


def call_str(b: Box):
    """
    >>> call_str(Box(5))
    '<5>'
    """
    return str(b)


def call_hash(b: Box):
    """
    >>> call_hash(Box(3))
    True
    """
    return hash(b) == 3 * 7


def call_neg(b: Box):
    """
    >>> call_neg(Box(4))
    'Box(-4)'
    """
    return repr(-b)


# A pure-Python subclass overriding the dunders must still be reached through
# the non-final vtable dispatch (skip_dispatch=0 runs the override check).
class PyBox(Box):
    def __len__(self):
        return 100

    def __repr__(self):
        return "PyBox!"


def call_len_override():
    """
    >>> call_len_override()
    100
    """
    b: Box = PyBox(1)
    return len(b)


def call_repr_override():
    """
    >>> call_repr_override()
    'PyBox!'
    """
    b: Box = PyBox(1)
    return repr(b)
