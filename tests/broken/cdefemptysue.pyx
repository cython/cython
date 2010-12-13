cdef extern from "cdefemptysue.h":

    cdef struct spam:
        pass

    ctypedef union eggs:
        pass

    cdef enum ham:
        pass

cdef extern spam s
cdef extern eggs e
cdef extern ham h
