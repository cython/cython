from libcpp cimport bool
from .typeinfo cimport type_info

# This class is C++11-only
extern from "<typeindex>" namespace "std" nogil:
    cdef cppclass type_index:
        type_index(const type_info &)
        const char* name()
        usize hash_code()
        bool operator==(const type_index &)
        bool operator!=(const type_index &)
        bool operator<(const type_index &)
        bool operator<=(const type_index &)
        bool operator>(const type_index &)
        bool operator>=(const type_index &)
