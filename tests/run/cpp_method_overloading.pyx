# mode: run
# tag: cpp

cdef extern from "cpp_method_overloading_support.h":
    cdef cppclass Base:
        __init__()
        __init__(int a)
        int foo(double)
        int foo(double*)

cdef cppclass Derived(Base):
    pass

cdef cppclass DefinedBase:
    int state

    __init__():
        # If we skip this one, inheritance won't work because of the
        # derived class constructor implicitely calling default constructor
        this.__init__(0)

    __init__(int a):
        this.state = a

    int getter():
        return this.state

    void setter(int a):
        this.state = a

    void setter(int* a):
        if a != NULL:
            this.state = a[0]

cdef cppclass DefinedDerived(DefinedBase):
    __init__(int a):
        DefinedBase.__init__(a)

def testDeclared():
    """
    >>> testDeclared()
    4 3
    """
    #pass
    cdef double a = 4.2
    cdef double *b = &a
    cdef Derived d
    rst_a = d.foo(a)
    rst_b = d.foo(b)
    print rst_a, rst_b

def testDefined():
    """
    >>> testDefined()
    24 42 42
    """

    dd = new DefinedDerived(24)

    dorig = dd.getter()

    cdef int val = 42

    dd.setter(val)

    dstate = dd.getter()
    # dstate should be 42

    da_addr = &dstate

    dd.setter(da_addr)

    # dstate2 should be 42
    dstate2 = dd.getter()

    print dorig, dstate, dstate2
    del dd