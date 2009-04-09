cdef extern from "stdio.h":
    ctypedef struct FILE
    int printf(char *format, ...) nogil
    int fprintf(FILE *stream, char *format, ...) nogil
    int sprintf(char *str, char *format, ...) nogil
    FILE *fopen(char *path, char *mode) nogil
    int fclose(FILE *strea) nogil
    cdef FILE *stdout
    int scanf(char *format, ...) nogil
