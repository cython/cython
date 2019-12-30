from libcpp cimport bool

cdef extern from "<optional>" namespace "std" nogil:
    cdef cppclass optional[T]:
        ctypedef T value_type
        optional()
        optional(optional&) except +
        optional(T&) except +
        bool has_value()
        T& value()
        T& value_or[U](U& default_value)
        void swap(optional& other)
        void reset()
        T& operator*()
        #T* operator->() # Not Supported
        optional& operator=(optional& other)
        optional& operator=[U](U& other)
        bool operator==(optional&, optional&)
        bool operator!=(optional&, optional&)
        bool operator<(optional&, optional&)
        bool operator>(optional&, optional&)
        bool operator<=(optional&, optional&)
        bool operator>=(optional&, optional&)
        bool operator bool()
