cdef extern from "<numeric>" namespace "std" nogil:
    T inner_product[InputIt1, InputIt2, T](InputIt1 first1, InputIt1 last1, InputIt2 first2, T init)

    T inner_product[InputIt1, InputIt2, T, BinaryOperation1, BinaryOperation2](InputIt1 first1, InputIt1 last1,
                                                                               InputIt2 first2, T init,
                                                                               BinaryOperation1 op1,
                                                                               BinaryOperation2 op2)

    void iota[ForwardIt, T](ForwardIt first, ForwardIt last, T value)

    T accumulate[InputIt, T](InputIt first, InputIt last, T init)

    T accumulate[InputIt, T, BinaryOperation](InputIt first, InputIt last, T init, BinaryOperation op)

    void adjacent_difference[InputIt, OutputIt](InputIt in_first, InputIt in_last, OutputIt out_first)

    void adjacent_difference[InputIt, OutputIt, BinaryOperation](InputIt in_first, InputIt in_last, OutputIt out_first,
                                                                 BinaryOperation op)

    void partial_sum[InputIt, OutputIt](InputIt in_first, OutputIt in_last, OutputIt out_first)

    void partial_sum[InputIt, OutputIt, BinaryOperation](InputIt in_first, InputIt in_last, OutputIt out_first,
                                                         BinaryOperation op)
