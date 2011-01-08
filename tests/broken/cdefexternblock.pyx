cdef extern from "cheese.h":

    ctypedef int camembert

    struct roquefort:
        int x

    char *swiss

    void cheddar()

    class external.runny [object runny_obj]:
        cdef int a
        def __init__(self):
            pass

cdef runny r
r = x
r.a = 42
