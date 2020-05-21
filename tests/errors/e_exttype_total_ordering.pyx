# mode: error
cimport cython

@cython.total_ordering("blah")
cdef class ExtBadParameter:
    pass

# Test all combinations with not enough methods.

@cython.total_ordering
cdef class ExtNoFuncs:
    pass

@cython.total_ordering
cdef class ExtGe:
    def __ge__(self, other):
        return False

@cython.total_ordering
cdef class ExtLe:
    def __le__(self, other):
        return False

@cython.total_ordering
cdef class ExtLeGe:
    def __le__(self, other):
        return False

    def __ge__(self, other):
        return False

@cython.total_ordering
cdef class ExtGt:
    def __gt__(self, other):
        return False

@cython.total_ordering
cdef class ExtGtGe:
    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return False

@cython.total_ordering
cdef class ExtGtLe:
    def __gt__(self, other):
        return False

    def __le__(self, other):
        return False

@cython.total_ordering
cdef class ExtGtLeGe:
    def __gt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __ge__(self, other):
        return False

@cython.total_ordering
cdef class ExtLt:
    def __lt__(self, other):
        return False

@cython.total_ordering
cdef class ExtLtGe:
    def __lt__(self, other):
        return False

    def __ge__(self, other):
        return False

@cython.total_ordering
cdef class ExtLtLe:
    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

@cython.total_ordering
cdef class ExtLtLeGe:
    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __ge__(self, other):
        return False

@cython.total_ordering
cdef class ExtLtGt:
    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return False

@cython.total_ordering
cdef class ExtLtGtGe:
    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return False

@cython.total_ordering
cdef class ExtLtGtLe:
    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __le__(self, other):
        return False

@cython.total_ordering
cdef class ExtLtGtLeGe:
    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __ge__(self, other):
        return False

@cython.total_ordering
cdef class ExtNe:
    def __ne__(self, other):
        return False

@cython.total_ordering
cdef class ExtEq:
    def __eq__(self, other):
        return False

@cython.total_ordering
cdef class ExtEqNe:
    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return False


_ERRORS = """
4:0: The total_ordering directive takes one compile-time boolean argument
10:0: total_ordering requires either ne or eq method, and any of lt/gt/le/ne
14:0: total_ordering requires either ne or eq method
20:0: total_ordering requires either ne or eq method
24:0: total_ordering requires either ne or eq method
32:0: total_ordering requires either ne or eq method
37:0: total_ordering requires either ne or eq method
45:0: total_ordering requires either ne or eq method
53:0: total_ordering requires either ne or eq method
64:0: total_ordering requires either ne or eq method
69:0: total_ordering requires either ne or eq method
78:0: total_ordering requires either ne or eq method
85:0: total_ordering requires either ne or eq method
96:0: total_ordering requires either ne or eq method
104:0: total_ordering requires either ne or eq method
115:0: total_ordering requires either ne or eq method
126:0: total_ordering requires either ne or eq method
140:0: total_ordering requires any of lt/gt/le/ne
145:0: total_ordering requires any of lt/gt/le/ne
150:0: total_ordering requires any of lt/gt/le/ne
"""
