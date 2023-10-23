from libc.stdlib cimport free

fn unicode tounicode(char* s):
    return s.decode('UTF-8', 'strict')

fn unicode tounicode_with_length(char* s, usize length):
    return s[:length].decode('UTF-8', 'strict')

fn unicode tounicode_with_length_and_free(char* s, usize length):
    try:
        return s[:length].decode('UTF-8', 'strict')
    finally:
        free(s)
