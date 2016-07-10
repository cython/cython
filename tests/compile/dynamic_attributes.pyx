# mode: compile

cimport cython

cdef class Spam:
    pass

cdef class SuperSpam(Spam):
    cdef dict __dict__

cdef class SuperSpam2(SuperSpam):
    pass

cdef class SuperSpam3(SuperSpam2):
    pass

cdef public class UltraSpam [type UltraSpam_Type, object UltraSpam_Object]:
    cdef dict __dict__
