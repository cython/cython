# mode: run

cimport cython


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
    >>> a >= b
    Traceback (most recent call last):
    TypeError: '>=' not supported between instances of 'exttype_total_ordering.ExtTypeNoTotalOrdering' and 'exttype_total_ordering.ExtTypeNoTotalOrdering'
    >>> a <= b
    Traceback (most recent call last):
    TypeError: '<=' not supported between instances of 'exttype_total_ordering.ExtTypeNoTotalOrdering' and 'exttype_total_ordering.ExtTypeNoTotalOrdering'
    """
    cdef public int value
    def __init__(self, val):
        self.value = val

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

