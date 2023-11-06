# mode: compile
# tag: struct, union, enum, cdefextern

cdef extern from "cheese.h":

    ctypedef int camembert

    struct roquefort:
        int x

    char *swiss

    void cheddar()

    # FIXME: find a real declaration here.
    #class external.runny [object runny_obj]:
    #    cdef int a
    #    def __init__(self):
    #        pass


#cdef runny r = runny()
#r.a = 42
