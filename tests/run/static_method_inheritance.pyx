# mode: run

cdef class A:
    @staticmethod
    def moo():
        return "moo"

cdef class B(A):
    @staticmethod
    def moo():
        return "boo"

cdef class Foo:
    @staticmethod
    cdef A meth():
        return A()

cdef class Bar(Foo):
    @staticmethod
    cdef B meth():
        return B()

def call_foo():
    """
    >>> call_foo()
    'moo'
    """
    return Foo.meth().moo()

def call_bar():
    """
    >>> call_bar()
    'boo'
    """
    return Bar.meth().moo()

