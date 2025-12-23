# mode: run
# tag: cpp, no-cpp-locals

cdef extern from *:
    """
    class Base {
    public:
        int foo(int a) {
            return a + 1;
        }
    };
    """
    cdef cppclass Base:
        __init__()
        int foo(int)

cdef cppclass Derived(Base):
    # We need to specify noexcept here because Base.foo(int) is by default wrapped as noexcept.
    int foo(int a) noexcept:
        return a * 2;

cdef cppclass DefinedBase:
    int state

    __init__():
        # If we skip this one, inheritance won't work because of the
        # derived class constructor implicitly calling default constructor
        this.__init__(0)

    __init__(int a):
        this.state = a

    int getter():
        return this.state

    int foo(int a):
        return this.state + a

cdef cppclass DefinedDerived(DefinedBase):
    __init__(int a):
        DefinedBase.__init__(2*a)

    int foo(int a):
        return this.state * a

def testDeclared():
    """
    >>> testDeclared()
    5 8
    """
    cdef int a = 4
    cdef Base b
    cdef Derived d
    rst_a = b.foo(a)
    rst_b = d.foo(a)
    print rst_a, rst_b

def testDefined():
    """
    >>> testDefined()
    24 34 48 480
    """

    db = new DefinedBase(24)
    dd = new DefinedDerived(24)

    rst_a = db.getter()
    rst_b = db.foo(10)
    rst_c = dd.getter()
    rst_d = dd.foo(10)

    print rst_a, rst_b, rst_c, rst_d
    del db
    del dd
