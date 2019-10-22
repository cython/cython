from libcpp cimport bool
from libcpp.utility cimport pair
from libc.stddef import ptrdiff_t


cdef extern from "<algorithm>" namespace "std" nogil:
    # Non-modifying sequence operations
    bool all_of[Iter, Pred](Iter first, Iter last, Pred pred) except +
    bool any_of[Iter, Pred](Iter first, Iter last, Pred pred) except +
    bool none_of[Iter, Pred](Iter first, Iter last, Pred pred) except +

    void for_each[Iter, UnaryFunction](Iter first, Iter last, UnaryFunction f) except +  # actually returns f

    ptrdiff_t count[Iter, T](Iter first, Iter last, const T& value) except +
    ptrdiff_t count_if[Iter, Pred](Iter first, Iter last, Pred pred) except +

    pair[Iter1, Iter2] mismatch[Iter1, Iter2](
        Iter1 first1, Iter1 last1, Iter2 first2) except +  # other overloads are tricky

    Iter find[Iter, T](Iter first, Iter last, const T& value) except +
    Iter find_if[Iter, Pred](Iter first, Iter last, Pred pred) except +
    Iter find_if_not[Iter, Pred](Iter first, Iter last, Pred pred) except +

    Iter1 find_end[Iter1, Iter2](Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2) except +
    Iter1 find_end[Iter1, Iter2, BinaryPred](
        Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2, BinaryPred pred) except +

    Iter1 find_first_of[Iter1, Iter2](Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2) except +
    Iter1 find_first_of[Iter1, Iter2, BinaryPred](
        Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2, BinaryPred pred) except +

    Iter adjacent_find[Iter](Iter first, Iter last) except +
    Iter adjacent_find[Iter, BinaryPred](Iter first, Iter last, BinaryPred pred) except +

    Iter1 search[Iter1, Iter2](Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2) except +
    Iter1 search[Iter1, Iter2, BinaryPred](
        Iter1 first1, Iter1 last1, Iter2 first2, Iter2 last2, BinaryPred pred) except +
    Iter search_n[Iter, Size, T](Iter first1, Iter last1, Size count, const T& value) except +
    Iter search_n[Iter, Size, T, BinaryPred](
        Iter first1, Iter last1, Size count, const T& value, BinaryPred pred) except +

    # Modifying sequence operations
    OutputIt copy[InputIt, OutputIt](InputIt first, InputIt last, OutputIt d_first) except +
    OutputIt copy_if[InputIt, OutputIt, Pred](InputIt first, InputIt last, OutputIt d_first, Pred pred) except +
    OutputIt copy_n[InputIt, Size, OutputIt](InputIt first, Size count, OutputIt result) except +
    Iter2 copy_backward[Iter1, Iter2](Iter1 first, Iter1 last, Iter2 d_last) except +

    OutputIt move[InputIt, OutputIt](InputIt first, InputIt last, OutputIt d_first) except +
    Iter2 move_backward[Iter1, Iter2](Iter1 first, Iter1 last, Iter2 d_last) except +

    void fill[Iter, T](Iter first, Iter last, const T& value) except +
    Iter fill_n[Iter, Size, T](Iter first, Size count, const T& value) except +

    OutputIt transform[InputIt, OutputIt, UnaryOp](
        InputIt first1, InputIt last1, OutputIt d_first, UnaryOp unary_op) except +
    OutputIt transform[InputIt1, InputIt2, OutputIt, BinaryOp](
        InputIt1 first1, InputIt1 last1, InputIt2 first2, OutputIt d_first, BinaryOp binary_op) except +

    void generate[Iter, Generator](Iter first, Iter last, Generator g) except +
    void generate_n[Iter, Size, Generator](Iter first, Size count, Generator g) except +

    Iter remove[Iter, T](Iter first, Iter last, const T& value) except +
    Iter remove_if[Iter, UnaryPred](Iter first, Iter last, UnaryPred pred) except +
    OutputIt remove_copy[InputIt, OutputIt, T](InputIt first, InputIt last, OutputIt d_first, const T& value) except +
    OutputIt remove_copy_if[InputIt, OutputIt, UnaryPred](
        InputIt first, InputIt last, OutputIt d_first, UnaryPred pred) except +

    void replace[Iter, T](Iter first, Iter last, const T& old_value, const T& new_value) except +
    void replace_if[Iter, UnaryPred, T](Iter first, Iter last, UnaryPred pred, const T& new_value) except +
    OutputIt replace_copy[InputIt, OutputIt, T](
        InputIt first, InputIt last, OutputIt d_first, const T& old_value, const T& new_value) except +
    OutputIt replace_copy_if[InputIt, OutputIt, UnaryPred, T](
        InputIt first, InputIt last, OutputIt d_first, UnaryPred pred, const T& new_value) except +

    void swap[T](T& a, T& b) except +  # array overload also works
    Iter2 swap_ranges[Iter1, Iter2](Iter1 first1, Iter1 last1, Iter2 first2) except +
    void iter_swap[Iter](Iter a, Iter b) except +

    void reverse[Iter](Iter first, Iter last) except +
    OutputIt reverse_copy[InputIt, OutputIt](InputIt first, InputIt last, OutputIt d_first) except +

    Iter rotate[Iter](Iter first, Iter n_first, Iter last) except +
    OutputIt rotate_copy[InputIt, OutputIt](InputIt first, InputIt n_first, InputIt last, OutputIt d_first) except +

    Iter unique[Iter](Iter first, Iter last) except +
    Iter unique[Iter, BinaryPred](Iter first, Iter last, BinaryPred p) except +
    OutputIt unique_copy[InputIt, OutputIt](InputIt first, InputIt last, OutputIt d_first) except +
    OutputIt unique_copy[InputIt, OutputIt, BinaryPred](
        InputIt first, InputIt last, OutputIt d_first, BinaryPred pred) except +

    # Partitioning operations
    bool is_partitioned[Iter, Pred](Iter first, Iter last, Pred p) except +
    Iter partition[Iter, Pred](Iter first, Iter last, Pred p) except +
    pair[OutputIt1, OutputIt2] partition_copy[InputIt, OutputIt1, OutputIt2, Pred](
        InputIt first, InputIt last, OutputIt1 d_first_true, OutputIt2 d_first_false, Pred p) except +
    Iter stable_partition[Iter, Pred](Iter first, Iter last, Pred p) except +
    Iter partition_point[Iter, Pred](Iter first, Iter last, Pred p) except +

    # Sorting operations
    bool is_sorted[Iter](Iter first, Iter last) except +
    bool is_sorted[Iter, Compare](Iter first, Iter last, Compare comp) except +

    Iter is_sorted_until[Iter](Iter first, Iter last) except +
    Iter is_sorted_until[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void sort[Iter](Iter first, Iter last) except +
    void sort[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void partial_sort[Iter](Iter first, Iter middle, Iter last) except +
    void partial_sort[Iter, Compare](Iter first, Iter middle, Iter last, Compare comp) except +

    OutputIt partial_sort_copy[InputIt, OutputIt](
        InputIt first, InputIt last, OutputIt d_first, OutputIt d_last) except +
    OutputIt partial_sort_copy[InputIt, OutputIt, Compare](
        InputIt first, InputIt last, OutputIt d_first, OutputIt d_last, Compare comp) except +

    void stable_sort[Iter](Iter first, Iter last) except +
    void stable_sort[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void nth_element[Iter](Iter first, Iter nth, Iter last) except +
    void nth_element[Iter, Compare](Iter first, Iter nth, Iter last, Compare comp) except +

    # Binary search operations (on sorted ranges)
    Iter lower_bound[Iter, T](Iter first, Iter last, const T& value) except +
    Iter lower_bound[Iter, T, Compare](Iter first, Iter last, const T& value, Compare comp) except +

    Iter upper_bound[Iter, T](Iter first, Iter last, const T& value) except +
    Iter upper_bound[Iter, T, Compare](Iter first, Iter last, const T& value, Compare comp) except +

    bool binary_search[Iter, T](Iter first, Iter last, const T& value) except +
    bool binary_search[Iter, T, Compare](Iter first, Iter last, const T& value, Compare comp) except +

    # Other operations on sorted ranges

    # Set operations (on sorted ranges)

    # Heap operations
    void make_heap[Iter](Iter first, Iter last) except +
    void make_heap[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void push_heap[Iter](Iter first, Iter last) except +
    void push_heap[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void pop_heap[Iter](Iter first, Iter last) except +
    void pop_heap[Iter, Compare](Iter first, Iter last, Compare comp) except +

    void sort_heap[Iter](Iter first, Iter last) except +
    void sort_heap[Iter, Compare](Iter first, Iter last, Compare comp) except +

    # Minimum/maximum operations
    Iter min_element[Iter](Iter first, Iter last) except +

    # Comparison operations

    # Permutation operations
