import cython

def func():
    # Cython types are evaluated as for cdef declarations
    x: cython.int               # cdef int x
    y: cython.double = 0.57721  # cdef double y = 0.57721
    z: cython.float = 0.57721   # cdef float z  = 0.57721

    # Python types shadow Cython types for compatibility reasons
    a: float = 0.54321          # cdef double a = 0.54321
    b: int = 5                  # cdef object b = 5
    c: long = 6                 # cdef object c = 6
    pass

@cython.cclass
class A:
    a: cython.int
    b: cython.int

    def __init__(self, b=0):
        self.a = 3
        self.b = b
