cdef extern from "<numeric>" namespace "std" nogil:
    T inner_product[InputIt1, InputIt2, T](InputIt1 first1, InputIt1 last1, InputIt2 first2, T init)

    void iota[ForwardIt, T](ForwardIt first, ForwardIt last, T value)

    T accumulate[InputIt, T](InputIt first, InputIt last, T init)

    T accumulate[InputIt, T, BinaryOperation](InputIt first, InputIt last, T init, BinaryOperation op)
