cdef extern from "graminit.c":
    pass

def p_module(source):
    print "Using formal grammar to parse", source
