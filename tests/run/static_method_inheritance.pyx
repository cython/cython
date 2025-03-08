# mode: run

cdef class A:
    @staticmethod
    def moo():
        return "mooA"

cdef class B(A):
    @staticmethod
    def moo():
        return "mooB"

cdef class GetBaseA:
    @staticmethod
    cdef A meth():
        return A()

cdef class GetSubB(GetBaseA):
    @staticmethod
    cdef B meth():
        return B()

def call_base():
    """
    >>> call_base()
    'mooA'
    """
    return GetBaseA.meth().moo()

def call_sub():
    """
    >>> call_sub()
    'mooB'
    """
    return GetSubB.meth().moo()

