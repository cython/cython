# mode: error
# tag: warnings
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
9:5: total_ordering directive used, but no comparison and equality methods defined
13:5: total_ordering directive used, but no equality method defined
18:5: total_ordering directive used, but no equality method defined
23:5: total_ordering directive used, but no equality method defined
31:5: total_ordering directive used, but no equality method defined
36:5: total_ordering directive used, but no equality method defined
44:5: total_ordering directive used, but no equality method defined
52:5: total_ordering directive used, but no equality method defined
63:5: total_ordering directive used, but no equality method defined
18:5: total_ordering directive used, but no equality method defined
76:5: total_ordering directive used, but no equality method defined
84:5: total_ordering directive used, but no equality method defined
95:5: total_ordering directive used, but no equality method defined
103:5: total_ordering directive used, but no equality method defined
114:5: total_ordering directive used, but no equality method defined
125:5: total_ordering directive used, but no equality method defined
139:5: total_ordering directive used, but no comparison methods defined
171:5: total_ordering directive used, but no comparison methods defined
149:5: total_ordering directive used, but no comparison methods defined
"""
