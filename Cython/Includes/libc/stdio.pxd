# 7.19 Input/output <stdio.h>

cdef extern from *:
    ctypedef char const_char "const char"
    ctypedef void const_void "const void"

cdef extern from "stdio.h" nogil:

    ctypedef struct FILE
    cdef FILE *stdin
    cdef FILE *stdout
    cdef FILE *stderr

    enum: FOPEN_MAX
    enum: FILENAME_MAX
    FILE *fopen   (const_char *FILENAME, const_char  *OPENTYPE)
    FILE *freopen (const_char *FILENAME, const_char *OPENTYPE, FILE *STREAM)
    int  fclose   (FILE *STREAM)
    int  remove   (const_char *FILENAME)
    int  rename   (const_char *OLDNAME, const_char *NEWNAME)
    FILE *tmpfile ()

    enum: _IOFBF
    enum: _IOLBF
    enum: _IONBF
    int setvbuf (FILE *STREAM, char *BUF, int MODE, size_t SIZE)
    enum: BUFSIZ
    void setbuf (FILE *STREAM, char *BUF)

    size_t fread  (void *DATA, size_t SIZE, size_t COUNT, FILE *STREAM)
    size_t fwrite (const_void *DATA, size_t SIZE, size_t COUNT, FILE *STREAM)
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
    ctypedef fpos_t const_fpos_t "const fpos_t"
    int fgetpos (FILE *STREAM, fpos_t *POSITION)
    int fsetpos (FILE *STREAM, const_fpos_t *POSITION)

    int scanf    (const_char *TEMPLATE, ...)
    int sscanf   (const_char *S, const_char *TEMPLATE, ...)
    int fscanf   (FILE *STREAM, const_char *TEMPLATE, ...)

    int printf   (const_char *TEMPLATE, ...)
    int sprintf  (char *S, const_char *TEMPLATE, ...)
    int snprintf (char *S, size_t SIZE, const_char *TEMPLATE, ...)
    int fprintf  (FILE *STREAM, const_char *TEMPLATE, ...)

    void perror  (const_char *MESSAGE)

    char *gets  (char *S)
    char *fgets (char *S, int COUNT, FILE *STREAM)

    int  puts   (const_char *S)
    int  fputs  (const_char *S, FILE *STREAM)
