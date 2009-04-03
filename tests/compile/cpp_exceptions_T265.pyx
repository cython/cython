cdef void raise_py_error():
    pass

cdef extern from "foo.h":
    cdef int generic_error() except +
    cdef int specified_error() except +MemoryError
    cdef int dynamic_error() except +raise_py_error

def test_it():
    generic_error()
    specified_error()
    dynamic_error()
