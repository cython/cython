from libc.stdio cimport FILE, fopen


def main():
    cdef FILE* p
    p = fopen("spam.txt", "r")
    if p == NULL:
        raise OSError("Couldn't open the spam file")
    # ...
