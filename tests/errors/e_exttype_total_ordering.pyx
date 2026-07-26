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
9:0: total_ordering directive used, but no comparison and equality methods defined
13:0: total_ordering directive used, but no equality method defined
18:0: total_ordering directive used, but no equality method defined
23:0: total_ordering directive used, but no equality method defined
31:0: total_ordering directive used, but no equality method defined
36:0: total_ordering directive used, but no equality method defined
44:0: total_ordering directive used, but no equality method defined
52:0: total_ordering directive used, but no equality method defined
63:0: total_ordering directive used, but no equality method defined
68:0: total_ordering directive used, but no equality method defined
76:0: total_ordering directive used, but no equality method defined
84:0: total_ordering directive used, but no equality method defined
95:0: total_ordering directive used, but no equality method defined
103:0: total_ordering directive used, but no equality method defined
114:0: total_ordering directive used, but no equality method defined
125:0: total_ordering directive used, but no equality method defined
139:0: total_ordering directive used, but no comparison methods defined
144:0: total_ordering directive used, but no comparison methods defined
149:0: total_ordering directive used, but no comparison methods defined
"""
