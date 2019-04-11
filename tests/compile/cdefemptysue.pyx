# mode: compile
# tag: struct, union, enum, cdefextern

cdef extern from *:
    """
    struct spam { int a; };
    struct flat_spam { int a; };
    typedef struct { int a; } flat_spam_type;

    typedef union { int a; long b; } eggs;
    typedef union { int a; long b; } flat_eggs;

    enum ham { TOAST };
    enum flat_ham { FLAT_TOAST };
    """

    cdef struct spam:
        pass

    cdef struct flat_spam: pass

    ctypedef struct flat_spam_type: pass

    ctypedef union eggs:
        pass

    ctypedef union flat_eggs: pass

    cdef enum ham:
        pass

    cdef enum flat_ham: pass


cdef extern spam s
cdef extern flat_spam fs
cdef extern flat_spam_type fst

cdef extern eggs e
cdef extern flat_eggs fe

cdef extern ham h
cdef extern flat_ham fh
