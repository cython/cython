# mode: error
# tag: warnings

cimport cython

@cython.dataclasses.dataclass
cdef class C:
    a: i32
    b: i64
    c: isize
    d: f32
    e: f64


_WARNINGS = """
8:7: Found C type 'i32' in a Python annotation. Did you mean to use 'cython.i32'?
8:7: Unknown type declaration 'i32' in annotation, ignoring
9:7: Found C type 'i64' in a Python annotation. Did you mean to use 'cython.i64'?
9:7: Unknown type declaration 'i64' in annotation, ignoring
10:7: Found C type 'isize' in a Python annotation. Did you mean to use 'cython.isize'?
10:7: Unknown type declaration 'isize' in annotation, ignoring
11:7: Found C type 'f32' in a Python annotation. Did you mean to use 'cython.f32'?
11:7: Unknown type declaration 'f32' in annotation, ignoring
12:7: Found C type 'f64' in a Python annotation. Did you mean to use 'cython.f64'?
12:7: Unknown type declaration 'f64' in annotation, ignoring
"""
