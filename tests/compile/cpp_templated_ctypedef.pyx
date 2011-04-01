# tag: cpp
# mode: compile

cdef extern from *:
    cdef cppclass Foo[T]:
        pass
    ctypedef Foo[int] IntFoo
