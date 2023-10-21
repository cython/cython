# mymodule.pxd

# declare a C function as "cpdef" to export it to the module
cdef extern from "math.h":
    cpdef f64 sin(f64 x)
