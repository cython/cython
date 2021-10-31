cdef extern from "complexobject.h":

    struct Py_complex:
        double real
        double imag

    ctypedef class __builtin__.complex [object PyComplexObject]:
        cdef Py_complex cval

        @property
        cdef inline double real(self):
            return self.cval.real

        @property
        cdef inline double imag(self):
            return self.cval.imag


def cprint(complex c):
    print(f"{c.real :.4f}{c.imag :+.4f}j")  # uses C calls to the above property methods.
