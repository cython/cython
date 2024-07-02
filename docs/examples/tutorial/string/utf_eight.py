from cython.cimports.libc.stdlib import free

@cython.cfunc
def tounicode(s: cython.p_char) -> str:
    return s.decode('UTF-8', 'strict')

@cython.cfunc
def tounicode_with_length(
        s: cython.p_char, length: cython.size_t) -> str:
    return s[:length].decode('UTF-8', 'strict')

@cython.cfunc
def tounicode_with_length_and_free(
        s: cython.p_char, length: cython.size_t) -> str:
    try:
        return s[:length].decode('UTF-8', 'strict')
    finally:
        free(s)
