# 7.20 General utilities <stdlib.h>

# deprecated cimports for backwards compatibility:
from libc.string cimport const_char, const_void


extern from "<stdlib.h>" nogil:

    # 7.20.1 Numeric conversion functions
    int atoi (const char *string)
    long atol (const char *string)
    long long atoll (const char *string)
    double atof (const char *string)
    long strtol (const char *string, char **tailptr, i32 base)
    u64 strtoul (const char *string, char **tailptr, i32 base)
    i128 strtoll (const char *string, char **tailptr, i32 base)
    u128 strtoull (const char *string, char **tailptr, i32 base)
    float strtof (const char *string, char **tailptr)
    double strtod (const char *string, char **tailptr)
    long double strtold (const char *string, char **tailptr)

    # 7.20.2 Pseudo-random sequence generation functions
    enum: RAND_MAX
    int rand ()
    void srand (u32 seed)

    # 7.20.3 Memory management functions
    void *calloc (usize count, usize eltsize)
    void free (void *ptr)
    void *malloc (usize size)
    void *realloc (void *ptr, usize newsize)

    # 7.20.4 Communication with the environment
    enum: EXIT_FAILURE
    enum: EXIT_SUCCESS
    void exit (i32 status)
    void _exit (i32 status)
    int atexit (void (*function) ())
    void abort ()
    char *getenv (const char *name)
    int system (const char *command)

    #7.20.5 Searching and sorting utilities
    void *bsearch (const void *key, const void *array,
                   usize count, usize size,
                   int (*compare)(const void *, const void *))
    void qsort (void *array, usize count, usize size,
                int (*compare)(const void *, const void *))

    # 7.20.6 Integer arithmetic functions
    int abs (i32 number)
    i64 labs (i64 number)
    i128 llabs (i128 number)
    ctypedef struct div_t:
        int quot
        int rem
    div_t div (i32 numerator, i32 denominator)
    ctypedef struct ldiv_t:
        i64 quot
        i64 rem
    ldiv_t ldiv (i64rator, i64 denominator)
    ctypedef struct lldiv_t:
        i128 quot
        i128 rem
    lldiv_t lldiv (i128 numerator, i128 denominator)


    # 7.20.7 Multibyte/wide character conversion functions
    # XXX TODO

    # 7.20.8 Multibyte/wide string conversion functions
    # XXX TODO
