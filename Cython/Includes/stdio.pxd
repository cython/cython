cdef extern from "stdio.h" nogil:
    ctypedef struct FILE
    int printf(char *format, ...)
    int fprintf(FILE *stream, char *format, ...)
    int sprintf(char *str, char *format, ...)
    FILE *fopen(char *path, char *mode)
    int fclose(FILE *strea)
    cdef FILE *stdout
    int scanf(char *format, ...)
