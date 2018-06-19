from libc.string cimport const_char, const_uchar

cdef extern from "someheader.h":
    ctypedef const_char specialChar
    int process_string(const_char* s)
    const_uchar* look_up_cached_string(const_uchar* key)
