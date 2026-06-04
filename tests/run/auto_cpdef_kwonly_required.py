# mode: run
# tag: auto_cpdef
# cython: auto_cpdef=True

"""
Required keyword-only args after optional ones (Python 3 syntax: *, a=1, b)
must compile cleanly under auto_cpdef=True.  The method stays as a plain def
(not cpdef-promoted) because the C ABI requires all required args before
optional ones; that is fine — it must not raise an error.
"""

import cython


@cython.cclass
class Widget:
    _width: int
    _height: int
    _name: str

    def __init__(self, *, width: int = 0, height: int = 0, name: str):
        self._width = width
        self._height = height
        self._name = name


@cython.cclass
class Widget2:
    _x: int
    _label: str

    def __init__(self):
        self._x = 0
        self._label = ""

    # Optional positional arg followed by required kw-only arg.
    def method(self, x: int = 0, *, label: str):
        self._x = x
        self._label = label


def test_required_kwonly_after_optional():
    """
    >>> test_required_kwonly_after_optional()
    (0, 0, 'hello')
    (10, 20, 'world')
    """
    w = Widget(name="hello")
    print((w._width, w._height, w._name))
    w2 = Widget(width=10, height=20, name="world")
    print((w2._width, w2._height, w2._name))


def test_positional_optional_then_required_kwonly():
    """
    >>> test_positional_optional_then_required_kwonly()
    (0, 'hi')
    (5, 'there')
    """
    w = Widget2()
    w.method(label="hi")
    print((w._x, w._label))
    w.method(5, label="there")
    print((w._x, w._label))


@cython.cclass
class QueryBase:
    """Base with all-kwonly-optional cpdef — caller may omit leading kw args."""
    def query(self, *, a: int = 0, b: int = 0, c: int = 0) -> int:
        return a + b + c


@cython.cclass
class QuerySub(QueryBase):
    pass


def test_kwonly_optional_gap_call():
    """
    Inherited cpdef called with a gap in kw-only optional args (b missing)
    must fall back to Python dispatch without error.

    >>> test_kwonly_optional_gap_call()
    3
    7
    """
    q = QuerySub()
    # 'b' is omitted (gap between a and c) — must not error at compile time
    print(q.query(a=1, c=2))
    print(q.query(a=3, c=4))
