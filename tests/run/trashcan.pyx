# mode: run

cimport cython

import sys

# The tests here are to do with a deterministic order of destructors which
# isn't reliable for PyPy. Therefore, on PyPy we treat the test as
# "compiles and doesn't crash"
IS_PYPY = hasattr(sys, 'pypy_version_info')

# Count number of times an object was deallocated twice. This should remain 0.
cdef int double_deallocations = 0
def assert_no_double_deallocations():
    if IS_PYPY:
        return
    global double_deallocations
    err = double_deallocations
    double_deallocations = 0
    assert not err


# Compute x = f(f(f(...(None)...))) nested n times and throw away the result.
# The real test happens when exiting this function: then a big recursive
# deallocation of x happens. We are testing two things in the tests below:
# that Python does not crash and that no double deallocation happens.
# See also https://github.com/python/cpython/pull/11841
def recursion_test(f, int n=2**20):
    x = None
    cdef int i
    for i in range(n):
        x = f(x)


@cython.trashcan(True)
cdef class Recurse:
    """
    >>> recursion_test(Recurse)
    >>> assert_no_double_deallocations()
    """
    cdef public attr
    cdef int deallocated

    def __cinit__(self, x):
        self.attr = x

    def __dealloc__(self):
        # Check that we're not being deallocated twice
        global double_deallocations
        double_deallocations += self.deallocated
        self.deallocated = 1


cdef class RecurseSub(Recurse):
    """
    >>> recursion_test(RecurseSub)
    >>> assert_no_double_deallocations()
    """
    cdef int subdeallocated

    def __dealloc__(self):
        # Check that we're not being deallocated twice
        global double_deallocations
        double_deallocations += self.subdeallocated
        self.subdeallocated = 1


@cython.freelist(4)
@cython.trashcan(True)
cdef class RecurseFreelist:
    """
    >>> recursion_test(RecurseFreelist)
    >>> recursion_test(RecurseFreelist, 1000)
    >>> assert_no_double_deallocations()
    """
    cdef public attr
    cdef int deallocated

    def __cinit__(self, x):
        self.attr = x

    def __dealloc__(self):
        # Check that we're not being deallocated twice
        global double_deallocations
        double_deallocations += self.deallocated
        self.deallocated = 1


# Subclass of list => uses trashcan by default
# As long as https://github.com/python/cpython/pull/11841 is not fixed,
# this does lead to double deallocations, so we skip that check.
cdef class RecurseList(list):
    """
    >>> RecurseList(42)
    [42]
    >>> recursion_test(RecurseList)
    """
    def __init__(self, x):
        super().__init__((x,))


# Some tests where the trashcan is NOT used. When the trashcan is not used
# in a big recursive deallocation, the __dealloc__s of the base classes are
# only run after the __dealloc__s of the subclasses.
# We use this to detect trashcan usage.
cdef int base_deallocated = 0
cdef int trashcan_used = 0
def assert_no_trashcan_used():
    if IS_PYPY:
        return
    global base_deallocated, trashcan_used
    err = trashcan_used
    trashcan_used = base_deallocated = 0
    assert not err


cdef class Base:
    def __dealloc__(self):
        global base_deallocated
        base_deallocated = 1


# Trashcan disabled by default
cdef class Sub1(Base):
    """
    >>> recursion_test(Sub1, 100)
    >>> assert_no_trashcan_used()
    """
    cdef public attr

    def __cinit__(self, x):
        self.attr = x

    def __dealloc__(self):
        global base_deallocated, trashcan_used
        trashcan_used += base_deallocated


@cython.trashcan(True)
cdef class Middle(Base):
    cdef public foo


# Trashcan disabled explicitly
@cython.trashcan(False)
cdef class Sub2(Middle):
    """
    >>> recursion_test(Sub2, 1000)
    >>> assert_no_trashcan_used()
    """
    cdef public attr

    def __cinit__(self, x):
        self.attr = x

    def __dealloc__(self):
        global base_deallocated, trashcan_used
        trashcan_used += base_deallocated
