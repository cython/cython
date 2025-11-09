# declare C-level exception values

cdef int func_a() except -1:
    return 0

cdef int func_b() except -1:
    return 0
 
cdef int func_c() except *:
    return 0
    
cdef int func_d() except -1:
    return 0
    
cdef int func_e():
    return 0   
