# cython: auto_cpdef=True
# mode: run
# tag: directive,auto_cpdef,dunders,cclass,repr,str,hash
import cython
from cython import cclass, final, Py_hash_t

@final
@cclass
class Point:
    x: cython.int
    y: cython.int

    def __init__(self, x: cython.int, y: cython.int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> Py_hash_t:
        return self.x * 31 + self.y


def test_repr():
    """
    >>> test_repr()
    'Point(1, 2)'
    """
    p = Point(1, 2)
    return repr(p)

def test_str():
    """
    >>> test_str()
    '(1, 2)'
    """
    p = Point(1, 2)
    return str(p)

def test_hash():
    """
    >>> test_hash()
    True
    """
    p = Point(3, 4)
    return hash(p) == 3 * 31 + 4

def test_in_dict():
    """
    >>> test_in_dict()
    True
    """
    p = Point(1, 2)
    d = {p: 'v'}
    return d[p] == 'v'
