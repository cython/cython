cdef bint is_y_in(const unsigned char[:] string_view):
    cdef int i
    for i in range(string_view.shape[0]):
        if string_view[i] == b'y':
            return True
    return False

print(is_y_in(b'hello world'))   # False
print(is_y_in(b'hello Cython'))  # True
