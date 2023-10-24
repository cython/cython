# mode: compile
# tag: struct, union, enum, cdefextern

extern from *:
    """
    struct spam { int a; };
    struct flat_spam { int a; };
    typedef struct { int a; } flat_spam_type;

    typedef union { int a; long b; } eggs;
    typedef union { int a; long b; } flat_eggs;

    enum ham { TOAST };
    enum flat_ham { FLAT_TOAST };
    """

    struct Spam:
        pass

    struct FlatSpam: pass

    ctypedef struct flat_spam_type: pass

    ctypedef union eggs:
        pass

    ctypedef union flat_eggs: pass

    enum Ham:
        pass

    enum FlatHam: pass

cdef extern Spam s
cdef extern FlatSpam fs
cdef extern flat_spam_type fst

cdef extern eggs e
cdef extern flat_eggs fe

cdef extern Ham h
cdef extern FlatHam fh
