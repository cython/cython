# mode: error
# ticket: 6393

from cpython.buffer cimport Py_buffer

cdef class Test:
    def __cinit__(self):
        pass

    def __cinit__(self, int a):
        pass

    def __dealloc__(self):
        pass

    def __dealloc__(self):
        pass

    def __getbuffer__(self, Py_buffer* buffer, int flags):
        pass

    def __getbuffer__(self, Py_buffer* buffer, int flags):
        pass

    def __releasebuffer__(self, Py_buffer* buffer):
        pass

    def __releasebuffer__(self, Py_buffer* buffer):
        pass


_ERRORS = """
10:4: '__cinit__' already defined
7:4: Previous declaration is here
16:4: '__dealloc__' already defined
13:4: Previous declaration is here
22:4: '__getbuffer__' already defined
19:4: Previous declaration is here
28:4: '__releasebuffer__' already defined
25:4: Previous declaration is here
"""
