
def stupid_lower_case(char* s):
    cdef Py_ssize_t size, i

    size = len(s)
    for i in range(size):
        if s[i] >= 'A' and s[i] <= 'Z':
            s[i] += 'a' - 'A'
    return s
