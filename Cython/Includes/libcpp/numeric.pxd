cdef extern from "<numeric>" namespace "std" nogil:
    T inner_product[InputIt1, InputIt2, T](InputIt1 first1, InputIt1 last1, InputIt2 first2, T init)
