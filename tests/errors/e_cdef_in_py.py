# mode: error

def func():
    cdef i32 i


_ERRORS = """
4:4: The 'cdef' keyword is only allowed in Cython files (pyx/pxi/pxd)
"""
