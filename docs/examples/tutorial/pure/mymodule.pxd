# mymodule.pxd

# declare a C function as "cpdef" to export it to the module
cdef extern from "math.h":
    cpdef double sin(double x)
