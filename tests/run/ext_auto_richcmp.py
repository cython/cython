# mode: run

import cython
compiled = cython.compiled

import sys
IS_PY2 = sys.version_info[0] == 2


@cython.cclass
class X(object):
    x = cython.declare(cython.int, visibility="public")

    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return "<%d>" % self.x


@cython.cclass
class ClassEq(X):
    """
    >>> a = ClassEq(1)
    >>> b = ClassEq(2)
    >>> c = ClassEq(1)
    >>> a == a
    True
    >>> a != a
    False

    >>> a == b
    False
    >>> a != b
    True

    >>> a == c
    True
    >>> if IS_PY2 and not compiled: a is c
    ... else: a != c
    False

    >>> b == c
    False
    >>> b != c
    True

    >>> c == a
    True
    >>> if IS_PY2 and not compiled: c is a
    ... else: c != a
    False

    >>> b == a
    False
    >>> b != a
    True

    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a < b
    Traceback (most recent call last):
    TypeError...
    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a > b
    Traceback (most recent call last):
    TypeError...
    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a <= b
    Traceback (most recent call last):
    TypeError...
    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a >= b
    Traceback (most recent call last):
    TypeError...
    """
    def __eq__(self, other):
        if isinstance(self, X):
            if isinstance(other, X):
                return self.x == other.x
        return NotImplemented


@cython.cclass
class ClassEqNe(ClassEq):
    """
    >>> a = ClassEqNe(1)
    >>> b = ClassEqNe(2)
    >>> c = ClassEqNe(1)
    >>> a == a
    True
    >>> a != a
    False

    >>> a == b
    False
    >>> a != b
    True

    >>> a == c
    True
    >>> a != c
    False

    >>> b == c
    False
    >>> b != c
    True

    >>> c == a
    True
    >>> c != a
    False

    >>> b == a
    False
    >>> b != a
    True

    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a < b
    Traceback (most recent call last):
    TypeError...
    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a > b
    Traceback (most recent call last):
    TypeError...
    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a <= b
    Traceback (most recent call last):
    TypeError...
    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a >= b
    Traceback (most recent call last):
    TypeError...
    """
    def __ne__(self, other):
        if isinstance(self, X):
            if isinstance(other, X):
                return self.x != other.x
        return NotImplemented


@cython.cclass
class ClassEqNeGe(ClassEqNe):
    """
    >>> a = ClassEqNeGe(1)
    >>> b = ClassEqNeGe(2)
    >>> c = ClassEqNeGe(1)
    >>> a == a
    True
    >>> a != a
    False
    >>> a >= a
    True
    >>> a <= a
    True

    >>> a == b
    False
    >>> a != b
    True
    >>> a >= b
    False
    >>> b <= a
    False

    >>> a == c
    True
    >>> a != c
    False
    >>> a >= c
    True
    >>> c <= a
    True

    >>> b == c
    False
    >>> b != c
    True
    >>> b >= c
    True
    >>> c <= b
    True

    >>> c == a
    True
    >>> c != a
    False
    >>> c >= a
    True
    >>> a <= c
    True

    >>> b == a
    False
    >>> b != a
    True
    >>> b >= a
    True
    >>> a <= b
    True

    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a < b
    Traceback (most recent call last):
    TypeError...
    >>> if IS_PY2: raise TypeError  # doctest: +ELLIPSIS
    ... else: a > b
    Traceback (most recent call last):
    TypeError...
    """
    def __ge__(self, other):
        if isinstance(self, X):
            if isinstance(other, X):
                return self.x >= other.x
        return NotImplemented


@cython.cclass
class ClassRichcmpOverride(ClassEqNeGe):
    """
    >>> a = ClassRichcmpOverride(1)
    >>> b = ClassRichcmpOverride(1)

    >>> a == a
    True
    >>> a != a
    False

    >>> a != b if compiled else a == b  # Python ignores __richcmp__()
    True
    >>> a == b if compiled else a != b  # Python ignores __richcmp__()
    False

    >>> if IS_PY2 or not compiled: raise TypeError  # doctest: +ELLIPSIS
    ... else: a >= b  # should no longer work when __richcmp__ is overwritten
    Traceback (most recent call last):
    TypeError...
    """
    def __richcmp__(self, other, op):
        return NotImplemented


@cython.cclass
class ClassLe(X):
    """
    >>> a = ClassLe(1)
    >>> b = ClassLe(2)
    >>> c = ClassLe(1)

    >>> a <= b
    True
    >>> b >= a
    True
    >>> b <= a
    False
    >>> a >= b
    False

    >>> a <= c
    True
    >>> c >= a
    True
    >>> c <= a
    True
    >>> a >= c
    True

    >>> b <= c
    False
    >>> c >= b
    False
    >>> c <= b
    True
    >>> b >= c
    True
    """
    def __le__(self, other):
        if isinstance(self, X):
            if isinstance(other, X):
                return self.x <= other.x
        return NotImplemented


@cython.cclass
class ClassLt(X):
    """
    >>> a = ClassLt(1)
    >>> b = ClassLt(2)
    >>> c = ClassLt(1)

    >>> a < b
    True
    >>> b > a
    True
    >>> b < a
    False
    >>> a > b
    False

    >>> a < c
    False
    >>> c > a
    False
    >>> c < a
    False
    >>> a > c
    False

    >>> b < c
    False
    >>> c > b
    False
    >>> c < b
    True
    >>> b > c
    True

    >>> sorted([a, b, c])
    [<1>, <1>, <2>]
    >>> sorted([b, a, c])
    [<1>, <1>, <2>]
    """
    def __lt__(self, other):
        if isinstance(self, X):
            if isinstance(other, X):
                return self.x < other.x
        return NotImplemented


@cython.cclass
class ClassLtGtInherited(X):
    """
    >>> a = ClassLtGtInherited(1)
    >>> b = ClassLtGtInherited(2)
    >>> c = ClassLtGtInherited(1)

    >>> a < b
    True
    >>> b > a
    True
    >>> b < a
    False
    >>> a > b
    False

    >>> a < c
    False
    >>> c > a
    False
    >>> c < a
    False
    >>> a > c
    False

    >>> b < c
    False
    >>> c > b
    False
    >>> c < b
    True
    >>> b > c
    True

    >>> sorted([a, b, c])
    [<1>, <1>, <2>]
    >>> sorted([b, a, c])
    [<1>, <1>, <2>]
    """
    def __gt__(self, other):
        if isinstance(self, X):
            if isinstance(other, X):
                return self.x > other.x
        return NotImplemented


@cython.cclass
class ClassLtGt(X):
    """
    >>> a = ClassLtGt(1)
    >>> b = ClassLtGt(2)
    >>> c = ClassLtGt(1)

    >>> a < b
    True
    >>> b > a
    True
    >>> b < a
    False
    >>> a > b
    False

    >>> a < c
    False
    >>> c > a
    False
    >>> c < a
    False
    >>> a > c
    False

    >>> b < c
    False
    >>> c > b
    False
    >>> c < b
    True
    >>> b > c
    True

    >>> sorted([a, b, c])
    [<1>, <1>, <2>]
    >>> sorted([b, a, c])
    [<1>, <1>, <2>]
    """
    def __lt__(self, other):
        if isinstance(self, X):
            if isinstance(other, X):
                return self.x < other.x
        return NotImplemented

    def __gt__(self, other):
        if isinstance(self, X):
            if isinstance(other, X):
                return self.x > other.x
        return NotImplemented


@cython.cclass
class List(list):
    """
    >>> l = [1, 2, 3, 4]
    >>> notl = List(l)
    >>> notl == l
    False
    >>> notl != l     # implemented by base type
    False
    >>> notl == notl
    True
    >>> notl != notl  # implemented by base type
    False
    """
    def __eq__(self, other):
        return self is other or list(self) != list(other)
