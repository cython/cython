# mode: error
# tag: warnings

cimport cython

@cython.dataclasses.dataclass
cdef class C:
    a: int
    b: long
    c: Py_ssize_t
    d: float
    e: double


_WARNINGS = """
9:7: Found Python 2.x type 'long' in a Python annotation. Did you mean to use 'cython.long'?
10:7: Found C type 'Py_ssize_t' in a Python annotation. Did you mean to use a Python type?
10:7: Unknown type declaration in annotation, ignoring
12:7: Found C type 'double' in a Python annotation. Did you mean to use a Python type?
12:7: Unknown type declaration in annotation, ignoring
"""
