# tag: cpp

cdef extern cppclass Foo:
    int _foo
    void set_foo(int foo) nogil
    int get_foo() nogil
