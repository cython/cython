cimport cython

#[cython.locals(egg=double)]
fn foo(egg)

#[cython.locals(egg=cython.double)]
fn foo_defval(egg=*)

#[cython.locals(egg=cython.bint, v=cython.int)]
cpdef cpfoo(egg=*)
