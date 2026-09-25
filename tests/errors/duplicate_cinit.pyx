# mode: error
# ticket: 6393

cdef class Test:
    def __cinit__(self):
        pass

    def __cinit__(self, int a):
        pass


_ERRORS = """
8:4: '__cinit__' already defined
5:4: Previous declaration is here
"""
