from libc.stdlib cimport free


cdef str tounicode(char* s):
    return s.decode('UTF-8', 'strict')


cdef str tounicode_with_length(
        char* s, size_t length):
    return s[:length].decode('UTF-8', 'strict')


cdef str tounicode_with_length_and_free(
        char* s, size_t length):
    try:
        return s[:length].decode('UTF-8', 'strict')
    finally:
        free(s)
