from libc.stdint cimport uint_fast32_t, uint_fast64_t


cdef extern from "<random>" namespace "std" nogil:
    cdef cppclass mt19937:
        ctypedef uint_fast32_t result_type

        mt19937() except +
        mt19937(result_type seed) except +
        result_type operator()() except +
        result_type min() except +
        result_type max() except +
        void discard(size_t z) except +
        void seed(result_type seed) except +


    cdef cppclass mt19937_64:
        ctypedef uint_fast64_t result_type

        mt19937_64() except +
        mt19937_64(result_type seed) except +
        result_type operator()() except +
        result_type min() except +
        result_type max() except +
        void discard(size_t z) except +
        void seed(result_type seed) except +
