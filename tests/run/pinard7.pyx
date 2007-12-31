cdef enum Mode:
    a = 1
    b = 2

cdef class Curseur:
    cdef Mode mode

    def method(self):
        assert False, self.mode
