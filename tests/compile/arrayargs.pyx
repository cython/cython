cdef extern from *:

    cdef void foo(int[])

    ctypedef int MyInt
    cdef void foo(MyInt[])

    struct MyStruct:
        pass
    cdef void bar(MyStruct[])

    ctypedef MyStruct* MyStructP
    cdef void baz(MyStructP[])
