from cython.cimports.libc.stdlib import free

# @cython.cfunc  # https://github.com/cython/cython/issues/2529
def tounicode(s: cython.p_char) -> cython.unicode:
    return s.decode('UTF-8', 'strict')

# @cython.cfunc  # https://github.com/cython/cython/issues/2529
def tounicode_with_length(
        s: cython.p_char, length: cython.size_t) -> cython.unicode:
    return s[:length].decode('UTF-8', 'strict')

# @cython.cfunc  # https://github.com/cython/cython/issues/2529
def tounicode_with_length_and_free(
        s: cython.p_char, length: cython.size_t) -> cython.unicode:
    try:
        return s[:length].decode('UTF-8', 'strict')
    finally:
        free(s)
