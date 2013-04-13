# mode: error
# tag: werror

cdef class A:
    cdef a
    """docstring"""

    cdef int b
    """docstring"""

    cdef public c
    """docstring"""

    cdef public dict d
    """docstring"""

    cdef readonly e
    """docstring"""

    cdef readonly list e
    """docstring"""

_ERRORS = """
6:4: Private attributes don't support docstrings.
9:4: Private attributes don't support docstrings.
"""
