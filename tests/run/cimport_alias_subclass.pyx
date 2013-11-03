# mode: compile


cimport cimport_alias_subclass_helper as cash

cdef class Derived(cash.Base):
    cdef bint foo(self):
        print "Hello"

def run():
    """
    >>> run()
    Hello
    """
    d = Derived()
    d.foo()
