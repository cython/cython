# 7.19 Input/output <stdio.h>


# deprecated cimports for backwards compatibility:
from libc.string cimport const_char, const_void


cdef extern from "stdio.h" nogil:

    ctypedef struct FILE
    cdef FILE *stdin
    cdef FILE *stdout
    cdef FILE *stderr

    enum: FOPEN_MAX
    enum: FILENAME_MAX
    FILE *fopen   (const char *FILENAME, const char  *OPENTYPE)
    FILE *freopen (const char *FILENAME, const char *OPENTYPE, FILE *STREAM)
    int  fclose   (FILE *STREAM)
    int  remove   (const char *FILENAME)
    int  rename   (const char *OLDNAME, const char *NEWNAME)
    FILE *tmpfile ()

    enum: _IOFBF
    enum: _IOLBF
    enum: _IONBF
    int setvbuf (FILE *STREAM, char *BUF, int MODE, size_t SIZE)
    enum: BUFSIZ
    void setbuf (FILE *STREAM, char *BUF)

    size_t fread  (void *DATA, size_t SIZE, size_t COUNT, FILE *STREAM)
    size_t fwrite (const void *DATA, size_t SIZE, size_t COUNT, FILE *STREAM)
    int    fflush (FILE *STREAM)

    enum: EOF
    int feof   (FILE *STREAM)
    int ferror (FILE *STREAM)

    enum: SEEK_SET
    enum: SEEK_CUR
    enum: SEEK_END
    int      fseek  (FILE *STREAM, long int OFFSET, int WHENCE)
    void     rewind (FILE *STREAM)
    long int ftell  (FILE *STREAM)

    ctypedef long long int fpos_t
    ctypedef const fpos_t const_fpos_t "const fpos_t"
    int fgetpos (FILE *STREAM, fpos_t *POSITION)
    int fsetpos (FILE *STREAM, const fpos_t *POSITION)

    int scanf    (const char *TEMPLATE, ...)
    int sscanf   (const char *S, const char *TEMPLATE, ...)
    int fscanf   (FILE *STREAM, const char *TEMPLATE, ...)

    int printf   (const char *TEMPLATE, ...)
    int sprintf  (char *S, const char *TEMPLATE, ...)
    int snprintf (char *S, size_t SIZE, const char *TEMPLATE, ...)
    int fprintf  (FILE *STREAM, const char *TEMPLATE, ...)

    void perror  (const char *MESSAGE)

    char *gets  (char *S)
    char *fgets (char *S, int COUNT, FILE *STREAM)

    int  puts   (const char *S)
    int  fputs  (const char *S, FILE *STREAM)
