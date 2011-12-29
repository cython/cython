
cdef extern from "template_args.h":

    cdef cppclass Bar [T]:
        Bar()

    cdef cppclass Foo [T]:
        Foo()
        void set_bar(Bar[size_t] & bar)

cpdef func():
    cdef Foo[int] foo
    cdef Bar[size_t] bar
    cdef Bar[size_t] & bref = bar

    foo.set_bar(bref)

