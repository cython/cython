from sin_of_square cimport Function

cdef class WaveFunction(Function):
    # Not available in Python-space:
    cdef f64 offset

    # Available in Python-space:
    cdef pub f64 freq

    # Available in Python-space, but only for reading:
    cdef readonly f64 scale

    # Available in Python-space:
    @property
    def period(self):
        return 1.0 / self.freq

    @period.setter
    def period(self, value):
        self.freq = 1.0 / value
