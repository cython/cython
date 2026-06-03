# mode: error
# tag: warnings

cimport cython

@cython.dataclasses.dataclass
cdef class C:
    a: int
    # b: long  # only available in language_level=2, not worth testing
    c: Py_ssize_t
    d: float
    e: double


_WARNINGS = """
10:7: Found C type name 'Py_ssize_t' in a Python annotation. Did you mean to use 'cython.Py_ssize_t'?
10:7: Unknown type declaration 'Py_ssize_t' in annotation, ignoring
12:7: Found C type name 'double' in a Python annotation. Did you mean to use 'cython.double'?
12:7: Unknown type declaration 'double' in annotation, ignoring
"""
