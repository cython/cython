# mode: error
# tag: total_ordering, warnings

cimport cython


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


_WARNINGS = """
10:0: total_ordering directive used, but no comparison and equality methods defined
14:0: total_ordering directive used, but no equality method defined
19:0: total_ordering directive used, but no equality method defined
24:0: total_ordering directive used, but no equality method defined
32:0: total_ordering directive used, but no equality method defined
37:0: total_ordering directive used, but no equality method defined
45:0: total_ordering directive used, but no equality method defined
53:0: total_ordering directive used, but no equality method defined
64:0: total_ordering directive used, but no equality method defined
69:0: total_ordering directive used, but no equality method defined
77:0: total_ordering directive used, but no equality method defined
85:0: total_ordering directive used, but no equality method defined
96:0: total_ordering directive used, but no equality method defined
104:0: total_ordering directive used, but no equality method defined
115:0: total_ordering directive used, but no equality method defined
126:0: total_ordering directive used, but no equality method defined
140:0: total_ordering directive used, but no comparison methods defined
145:0: total_ordering directive used, but no comparison methods defined
150:0: total_ordering directive used, but no comparison methods defined
"""
