from libcpp cimport bool
from libcpp.utility cimport pair
from libc.stddef import ptrdiff_t


cdef extern from "<algorithm>" namespace "std" nogil:
    # Non-modifying sequence operations
    bool all_of[Iter, Pred](Iter first, Iter last, Pred pred) except +
    bool any_of[Iter, Pred](Iter first, Iter last, Pred pred) except +
    bool none_of[Iter, Pred](Iter first, Iter last, Pred pred) except +

    ptrdiff_t count[Iter, T](Iter first, Iter last, const T& value)
    ptrdiff_t count_if[Iter, Pred](Iter first, Iter last, Pred pred) except +

    pair[Iter1, Iter2] mismatch[Iter1, Iter2](Iter1 first1, Iter1 last1, Iter2 first2)  # other overloads are tricky

    Iter find[Iter, T](Iter first, Iter last, const T& value)
    Iter find_if[Iter, Pred](Iter first, Iter last, Pred pred) except +
    Iter find_if_not[Iter, Pred](Iter first, Iter last, Pred pred) except +

    Iter1 find_end[Iter1, Iter2](Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2)
    Iter1 find_end[Iter1, Iter2, BinaryPred](
        Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2, BinaryPred pred) except +

    Iter1 find_first_of[Iter1, Iter2](Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2)
    Iter1 find_first_of[Iter1, Iter2, BinaryPred](
        Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2, BinaryPred pred) except +

    Iter adjacent_find[Iter](Iter first, Iter last)
    Iter adjacent_find[Iter, BinaryPred](Iter first, Iter last, BinaryPred pred) except +

    Iter1 search[Iter1, Iter2](Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2)
    Iter1 search[Iter1, Iter2, BinaryPred](
        Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2, BinaryPred pred) except +
    Iter search_n[Iter, Size, T](Iter first1, Iter last1, Size count, const T& value)
    Iter search_n[Iter, Size, T, BinaryPred](
        Iter first1, Iter last1, Size count, const T& value, BinaryPred pred) except +

    # Modifying sequence operations
    OutputIt copy[InputIt, OutputIt](InputIt first, InputIt last, OutputIt d_first)
    OutputIt copy_if[InputIt, OutputIt, Pred](InputIt first, InputIt last, OutputIt d_first, Pred pred) except +
    OutputIt copy_n[InputIt, Size, OutputIt](InputIt first, Size count, OutputIt result)
    Iter2 copy_backward[Iter1, Iter2](Iter1 first, Iter1 last, Iter2 d_last)

    OutputIt move[InputIt, OutputIt](InputIt first, InputIt last, OutputIt d_first)
    Iter2 move_backward[Iter1, Iter2](Iter1 first, Iter1 last, Iter2 d_last)

    void fill[Iter, T](Iter first, Iter last, const T& value)
    Iter fill_n[Iter, Size, T](Iter first, Size count, const T& value)

    Iter unique[Iter](Iter first, Iter last)
    Iter unique[Iter, BinaryPredicate](Iter first, Iter last, BinaryPredicate p) except +

    # Partitioning operations

    # Sorting operations
    void sort[Iter](Iter first, Iter last)
    void sort[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void partial_sort[Iter](Iter first, Iter middle, Iter last)
    void partial_sort[Iter, Compare](Iter first, Iter middle, Iter last, Compare comp) except +

    # Binary search operations (on sorted ranges)
    Iter lower_bound[Iter, T](Iter first, Iter last, const T& value)
    Iter lower_bound[Iter, T, Compare](Iter first, Iter last, const T& value, Compare comp) except +

    Iter upper_bound[Iter, T](Iter first, Iter last, const T& value)
    Iter upper_bound[Iter, T, Compare](Iter first, Iter last, const T& value, Compare comp) except +

    bool binary_search[Iter, T](Iter first, Iter last, const T& value)
    bool binary_search[Iter, T, Compare](Iter first, Iter last, const T& value, Compare comp) except +

    # Other operations on sorted ranges

    # Set operations (on sorted ranges)

    # Heap operations
    void make_heap[Iter](Iter first, Iter last)
    void make_heap[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void push_heap[Iter](Iter first, Iter last)
    void push_heap[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void pop_heap[Iter](Iter first, Iter last)
    void pop_heap[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void sort_heap[Iter](Iter first, Iter last)
    void sort_heap[Iter, Compare](Iter first, Iter last, Compare comp) except +

    # Minimum/maximum operations

    # Comparison operations

    # Permutation operations
