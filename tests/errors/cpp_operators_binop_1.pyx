# mode: error
# tag: cpp

cimport cython

cdef extern from *:
    cdef cppclass NoAddSub:
        pass

    cdef cppclass HasOps:
        pass

    int operator+(const HasOps&, int)
    int operator-(int, const HasOps&)

# Don't add to this testcase! it's to test the case that there is *one*
# non-member operator found that it should be discarded

cdef void misuse_classes():
    # similar to https://github.com/cython/cython/issues/4539
    # Unlike the case for increment/decrement operators it wasn't actually failing
    # but is still worth testing
    # Cython should not match the operators for a different type
    cdef NoAddSub no
    print(no + 1)
    print(1 + no)
    print(no - 1)
    print(1 - no)

_ERRORS = """
23:10: Cannot assign type 'NoAddSub' to 'const HasOps'
24:10: Cannot assign type 'long' to 'const HasOps'
24:14: Cannot assign type 'NoAddSub' to 'int'
25:10: Cannot assign type 'NoAddSub' to 'int'
"""
