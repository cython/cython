#def func():
    # Cython types are evaluated as for cdef declarations
 #   cdef int x
 #   cdef double y = 0.57721
 #   cdef float z = 0.57721

    # Python types shadow Cython types for compatibility reasons
 #   cdef double a = 0.54321
 #   cdef object b = 5
 #   cdef object c = 6
 #   pass

# Traditional Cython syntax for extension type (cdef class)
#cdef class A:
 #   cdef int a
 #   cdef int b

 #   def __init__(self, b=0):
 #       self.a = 3
 #       self.b = b
