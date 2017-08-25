# mode: error

def func():
    cdef int i


_ERRORS = """
4:4: The 'cdef' keyword is only allowed in Cython files (pyx/pxi/pxd)
"""
