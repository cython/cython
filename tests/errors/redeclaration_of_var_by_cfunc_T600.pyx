# ticket: 600
# mode: error

cdef class Bar:
    cdef list _operands

    cdef int _operands(self):
        return -1


_ERRORS = """
7:4: '_operands' redeclared
5:14: Previous declaration is here
"""
