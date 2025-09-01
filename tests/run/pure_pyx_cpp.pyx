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
    double (*)(int) except *
    double (*)(int, ...) except *
    """
    cdef double (*f1)(int)
    f2: cython.pointer[cython.function_type([cython.int], cython.double)]
    f3: cython.pointer[cython.function_type([cython.int], cython.double, nogil=True)]
    f4: cython.pointer[cython.function_type([cython.int], cython.double, nogil=False)]
    f5: cython.pointer[cython.function_type([cython.int], cython.double, has_varargs=True)]
    print(cython.typeof(f1))
    print(cython.typeof(f2))
    print(cython.typeof(f3))
    print(cython.typeof(f4))
    print(cython.typeof(f5))

def test_fn_pointer_type_exceptions():
    """
    >>> test_fn_pointer_type_exceptions()
    double (*)(int) noexcept
    double (*)(int) noexcept
    double (*)(int) except +
    double (*)(int) except -1
    double (*)(int) except? -1
    """
    f1: cython.pointer[cython.function_type([cython.int], cython.double, noexcept=True)]
    f2: cython.pointer[cython.function_type([cython.int], cython.double, check_exception=False)]
    f3: cython.pointer[cython.function_type([cython.int], cython.double, except_plus=True)]
    f4: cython.pointer[cython.function_type([cython.int], cython.double, exceptval=-1)]
    f5: cython.pointer[cython.function_type([cython.int], cython.double, exceptval=-1, check_exception=True)]
    print(cython.typeof(f1))
    print(cython.typeof(f2))
    print(cython.typeof(f3))
    print(cython.typeof(f4))
    print(cython.typeof(f5))
