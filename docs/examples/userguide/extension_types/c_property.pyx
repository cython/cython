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
    print(f"{c.real}+{c.imag}j")  # uses C calls to the above property methods.
