# mode: run
# tag: total_ordering

from __future__ import print_function

"""
    >>> class PyTotalOrdering:
    ...     def __init__(self, value):
    ...         self.value = value
    ...     def __eq__(self, other):
    ...         return self.value == other.value
    ...     def __lt__(self, other):
    ...         return self.value < other.value
    >>> test_all_comp(functools.total_ordering(PyTotalOrdering))
    True
"""

cimport cython
import functools
from functools import total_ordering as total_ordering_by_another_name
import operator

COMPARISONS = [
    # Don't test equals, the directive doesn't add that.
    # ('==', operator.__eq__),
    ('!=', operator.__ne__),
    ('<',  operator.__lt__),
    ('>',  operator.__gt__),
    ('<=', operator.__le__),
    ('>=', operator.__ge__),
]

def test_all_comp(cls):
    """Check every combination of comparison operators."""
    a, b, c = 10, 15, 20
    succeeded = True
    for comp, func in COMPARISONS:
        for left in [cls(a), cls(b), cls(c)]:
            for right in [ValueHolder(a), ValueHolder(b), ValueHolder(c)]:
                expected = func(left.value, right.value)
                try:
                    result = func(left, right)
                    # repeat to rule out deallocation bugs (and assert determinism)
                    for _ in range(10):
                        assert result == func(left, right)
                except TypeError:
                    print("TypeError:", left.value, comp, right.value)
                    succeeded = False
                else:
                    if expected != result:
                        print(
                            left.value, comp, right.value,
                            "expected:", expected, "got:", result
                        )
                        succeeded = False
    return succeeded

class ValueHolder:
    """Has a value, but can't compare."""
    def __init__(self, value):
        self.value = value



cdef class ExtTypeNoTotalOrdering:
    """
    >>> a = ExtTypeNoTotalOrdering(5)
    >>> b = ExtTypeNoTotalOrdering(10)
    >>> a == b
    False
    >>> a != b  # Added in Python 3, but Cython backports
    True
    >>> a < b
    True
    >>> b < a
    False
    >>> a > b
    False
    >>> b > a
    True
    >>> import sys
    >>> try: _ =  a >= b
    ... except TypeError:
    ...     pass
    ... else:
    ...     print("FAILED!")
    >>> try: _ =  a <= b
    ... except TypeError:
    ...     pass
    ... else:
    ...     print("FAILED!")
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

# Every combination of methods which is valid.

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __ge__(self, other):
        return self.value >= other.value

@functools.total_ordering
cdef class ExtTypeTotalOrderingNeLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __le__(self, other):
        return self.value <= other.value

@functools.total_ordering
cdef class ExtTypeTotalOrderingNeLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeGt:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeGt)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeGtGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeGtGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeGtLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeGtLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeGtLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeGtLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeLt:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLt)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeLtGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLtGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeLtLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLtLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeLtLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLtLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeLtGt:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLtGt)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeLtGtGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLtGtGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeLtGtLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLtGtLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingNeLtGtLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingNeLtGtLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@total_ordering_by_another_name
cdef class ExtTypeTotalOrderingEqGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@total_ordering_by_another_name
cdef class ExtTypeTotalOrderingEqGt:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqGt)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqGtGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqGtGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqGtLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqGtLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqGtLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqGtLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

# cython.total_ordering implicitly means cclass too
@cython.total_ordering
class ExtTypeTotalOrderingEqLt:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLt)
    True
    """
    _value: int

    @property
    def value(self):
        return self._value  # it's hard to make value public directly in pure syntax

    def __init__(self, val):
        self._value = val

    def __eq__(self, other):
        return self._value == other.value

    def __lt__(self, other):
        return self._value < other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqLtGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLtGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqLtLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLtLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqLtLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLtLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqLtGt:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLtGt)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqLtGtGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLtGtGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqLtGtLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLtGtLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqLtGtLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqLtGtLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeGt:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeGt)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeGtGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeGtGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeGtLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeGtLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeGtLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeGtLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLt:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLt)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLtGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLtGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLtLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLtLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLtLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLtLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLtGt:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLtGt)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLtGtGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLtGtGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLtGtLe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLtGtLe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

@cython.total_ordering
cdef class ExtTypeTotalOrderingEqNeLtGtLeGe:
    """
    >>> test_all_comp(ExtTypeTotalOrderingEqNeLtGtLeGe)
    True
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value
