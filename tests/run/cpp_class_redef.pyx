# tag: cpp

# This gives a warning, but should not give an error.
cdef cppclass Foo:
    int _foo
    int get_foo():
        return this._foo
    void set_foo(int foo):
        this._foo = foo

def test_Foo(n):
    """
    >>> test_Foo(1)
    1
    """
    cdef Foo* foo = NULL
    try:
        foo = new Foo()
        foo.set_foo(n)
        return foo.get_foo()
    finally:
        del foo
