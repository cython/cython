
cdef extern from "stdlib.h":
    void free(void *ptr) nogil
    void *malloc(size_t size) nogil
    void *realloc(void *ptr, size_t size) nogil
    size_t strlen(char *s) nogil
    char *strcpy(char *dest, char *src) nogil
