# mode: run

cimport cython

# public just so we can specify an objstruct name
cdef public class C[object CObjStruct, type CTypeObj]:
    cdef int attr

    def __cinit__(self, value, *ignore):
        self.attr = value

cdef public class D(C)[object DObjStruct, type DTypeObj]:
    cdef double other_attr

    def __cinit__(self, v1, v2):
        self.other_attr = v2

cdef extern from *:
    cdef struct CObjStruct:
        int attr
    cdef struct DObjStruct:
        double other_attr

def test_objstruct_cast(C c):
    """
    >>> test_objstruct_cast(C(10))
    10
    >>> test_objstruct_cast(C(20))
    20
    >>> test_objstruct_cast(D(-2, 5.5))
    -2
    """
    return cython.cast(cython.pointer(CObjStruct), cython.cast(C, c, objstruct_cast=True)).attr

def test_objstruct_cast_derived(D d):
    """
    >>> test_objstruct_cast_derived(D(-2, 5.5))
    5.5
    """
    return cython.cast(cython.pointer(DObjStruct), cython.cast(D, d, objstruct_cast=True)).other_attr

def test_objstruct_cast_typecheck(o):
    """
    >>> test_objstruct_cast_typecheck(10)
    Traceback (most recent call last):
        ...
    TypeError: Cannot convert int to cast.D
    >>> test_objstruct_cast_typecheck(C(10))
    Traceback (most recent call last):
        ...
    TypeError: Cannot convert cast.C to cast.D
    >>> test_objstruct_cast_typecheck(D(10, -3))
    -3.0
    """
    return cython.cast(cython.pointer(DObjStruct), cython.cast(D, o, objstruct_cast=True, typecheck=True)).other_attr
