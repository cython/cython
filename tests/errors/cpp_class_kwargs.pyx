# mode: error
# tag: cpp
# ticket: 7206

cdef extern from *:
    """
    class C {
        public:
            int i;
            C() : i(0) {}
            C(int j) : i(j) {}
    };
    """

    cdef cppclass C:
        int i
        C()
        C(int j)


def f():
    cdef C wrong_keyword_name = C(i=0)
    cdef C ok = C(j=0)


_ERRORS = u"""
22:33: Non-trivial keyword arguments and starred arguments not allowed in cdef functions.
23:17: Non-trivial keyword arguments and starred arguments not allowed in cdef functions.
"""
