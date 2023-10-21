cdef extern from "someheader.h":
    ctypedef const char specialChar
    int process_string(const char* s)
    const u8* look_up_cached_string(const u8* key)
