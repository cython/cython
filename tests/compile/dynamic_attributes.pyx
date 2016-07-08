# mode: compile

cimport cython

cdef class Spam:
    pass

@cython.dynamic_attributes(True)
cdef class SuperSpam:
    pass

@cython.dynamic_attributes(True)
cdef public class UltraSpam [type UltraSpam_Type, object UltraSpam_Object]:
    pass
