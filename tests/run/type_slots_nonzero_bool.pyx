__doc__ = """

>>> not not BoolA(0)
False
>>> not not BoolA(1)
True

>>> not not BoolB(0)
False
>>> not not BoolB(1)
True

>>> not not BoolX(0)
False
>>> not not BoolX(1)
True

>>> not not BoolY(0)
False
>>> not not BoolY(1)
True

"""

cdef class BoolA:
    cdef bint value
    def __cinit__(self, bint value):
        self.value = value
    def __nonzero__(self):
        return self.value

cdef class BoolB:
    cdef bint value
    def __cinit__(self, bint value):
        self.value = value
    def __bool__(self):
        return self.value

cdef class BoolX(BoolA):
    pass

cdef class BoolY(BoolB):
    pass
