# mode: run

cdef int dummy_number = 1234

cdef class CustomType(type):
    cdef int struct_number
    def __cinit__(self):
        self.struct_number = 5678

cdef class ClassOne:
    cdef CustomType __metaclass__

cdef class MonkeypatchableType(type):
    cdef dict __dict__

cdef class MonkeypatchableClass:
    """
    >>> MonkeypatchableClass.foo = 'bar'
    >>> MonkeypatchableClass.foo
    'bar'
    """
    cdef MonkeypatchableType __metaclass__

cdef class WithProperties(type):
    cdef dict __dict__
    @property
    def dummy_number(self):
        return dummy_number
    @dummy_number.setter
    def dummy_number(self, int val):
        global dummy_number
        dummy_number = val

cdef class ClassTwo:
    cdef WithProperties __metaclass__

cdef class ClassThree(ClassTwo):
    """
    >>> ClassThree.dummy_number
    1234
    >>> ClassThree.dummy_number = 5678
    >>> ClassThree.dummy_number
    5678
    >>> ClassTwo.dummy_number
    5678
    """

class PyBaseClass(metaclass=CustomType):
    pass

class PyDerivedClass(ClassTwo):
    pass

def test_struct_number(CustomType cls):
    """
    >>> test_struct_number(ClassOne)
    5678
    >>> test_struct_number(PyBaseClass)
    5678
    """
    return cls.struct_number
