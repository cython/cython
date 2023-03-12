from libcpp cimport bool

cdef extern from "<any>" namespace "std" nogil:
    cdef cppclass any:
        any()
        any(any&)
        void reset()
        bool has_value()
        T& emplace[T](...)
        void swap(any&)
        any& operator=(any&)
        any& operator=[U](U&)

    cdef T any_cast[T](any&) except +


