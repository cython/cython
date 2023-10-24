from libcpp cimport bool

extern from "<typeinfo>" namespace "std" nogil:
    cdef cppclass type_info:
        const char* name()
        int before(const type_info&)
        bool operator==(const type_info&)
        bool operator!=(const type_info&)
        # C++11-only
        usize hash_code()
