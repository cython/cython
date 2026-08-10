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
    cdef C c = C(i=0)


_ERRORS = u"""
22:16: Non-trivial keyword arguments and starred arguments not allowed in cdef functions.
"""
