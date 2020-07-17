# mode: run
# tag: cpp

# A C++ only test for "duplicate_utilitycode"
from libcpp.utility cimport pair

cdef struct S:
    pair[int, int] pair_member

cdef class ContainsS:
    """
    # FIXME - this doesn't reproduce the bug yet!

    https://github.com/cython/cython/issues/3741
    The auto-pickle function is utility code to be generated which converts member is a dict
     - the main test is that it compiles - the runtime tests aren't very interesting
    >>> inst = ContainsS()
    >>> d = inst.getS()
    >>> d['pair_member'][0]
    0
    >>> d['pair_member'][1]
    1
    """
    cdef S member

    def __init__(self):
        self.member.pair_member.first = 0
        self.member.pair_member.second = 1

    def getS(self):
        return self.member # some conversions

    def getSP(self):
        return self.member.self.pair_member
