cdef extern from "<utility>" namespace "std":
    cdef cppclass pair[T, U]:
        T first
        U second
        pair()
        pair(pair&)
        pair(T&, U&)
        bint operator==(pair&, pair&) nogil
        bint operator!=(pair&, pair&) nogil
        bint operator<(pair&, pair&) nogil
        bint operator>(pair&, pair&) nogil
        bint operator<=(pair&, pair&) nogil
        bint operator>=(pair&, pair&) nogil
