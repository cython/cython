# mode: run
# tag: cpp

import cython


@cython.cfunc
def takes_reference(x: cython.reference[int], y: cython.rvalue_reference[int]) -> object:
    return None

@cython.cfunc
def takes_const_reference(x: cython.reference[cython.const[int]], y: cython.rvalue_reference[cython.const[int]]) -> object:
    return None



def test_references():
    """
    >>> test_references()
    object (int &, int &&)
    object (const int &, const int &&)
    """
    print(cython.typeof(takes_reference))
    print(cython.typeof(takes_const_reference))


cdef int raise_py_error() except *:
    raise TypeError("custom")


def test_fn_pointer_type():
    """
    >>> test_fn_pointer_type()
    double (*)(int) except *
    double (*)(int) except *
    double (*)(int) except * nogil
    double (*)(int) except * nogil
    double (*)(int) except *
    double (*)(int) except *
    double (*)(int, ...) except *
    double (*)(int, ...) except *
    """
    cdef double (*f1a)(int)
    f1b: cython.pointer[cython.function_type([cython.int], cython.double)]
    cdef double (*f2a)(int) nogil
    f2b: cython.pointer[cython.function_type([cython.int], cython.double, nogil=True)]
    cdef double (*f3a)(int)
    f3b: cython.pointer[cython.function_type([cython.int], cython.double, nogil=False)]
    cdef double (*f4a)(int, ...)
    f4b: cython.pointer[cython.function_type([cython.int], cython.double, has_varargs=True)]
    print(cython.typeof(f1a))
    print(cython.typeof(f1b))
    print(cython.typeof(f2a))
    print(cython.typeof(f2b))
    print(cython.typeof(f3a))
    print(cython.typeof(f3b))
    print(cython.typeof(f4a))
    print(cython.typeof(f4b))

def test_fn_pointer_type_exceptions():
    """
    >>> test_fn_pointer_type_exceptions()
    double (*)(int) noexcept
    double (*)(int) noexcept
    double (*)(int) noexcept
    double (*)(int) except +
    double (*)(int) except +
    double (*)(int) except -1.0
    double (*)(int) except -1
    double (*)(int) except? -1.0
    double (*)(int) except? -1
    """
    cdef double (*f1a)(int) noexcept
    f1b: cython.pointer[cython.function_type([cython.int], cython.double, noexcept=True)]
    f1c: cython.pointer[cython.function_type([cython.int], cython.double, check_exception=False)]
    cdef double (*f2a)(int) except +
    f2b: cython.pointer[cython.function_type([cython.int], cython.double, except_cpp=True)]
    cdef double (*f3a)(int) except -1
    f3b: cython.pointer[cython.function_type([cython.int], cython.double, exceptval=-1)]
    cdef double (*f4a)(int) except? -1
    f4b: cython.pointer[cython.function_type([cython.int], cython.double, exceptval=-1, check_exception=True)]
    print(cython.typeof(f1a))
    print(cython.typeof(f1b))
    print(cython.typeof(f1c))
    print(cython.typeof(f2a))
    print(cython.typeof(f2b))
    print(cython.typeof(f3a))
    print(cython.typeof(f3b))
    print(cython.typeof(f4a))
    print(cython.typeof(f4b))
