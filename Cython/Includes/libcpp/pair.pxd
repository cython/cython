cdef extern from "pair.h":
    cdef cppclass pair[T, U]:
        T first
        U second
        pair()
        pair(T&, U&)

