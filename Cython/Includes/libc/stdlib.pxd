# 7.20 General utilities <stdlib.h>

cdef extern from *:
    ctypedef char const_char "const char"
    ctypedef void const_void "const void"

cdef extern from "stdlib.h" nogil:

    # 7.20.1 Numeric conversion functions
    int atoi (const_char *STRING)
    long atol (const_char *STRING)
    long long atoll (const_char *STRING)
    double atof (const_char *STRING)
    long strtol (const_char *STRING, char **TAILPTR, int BASE)
    unsigned long int strtoul (const_char *STRING, char **TAILPTR, int BASE)
    long long int strtoll (const_char *STRING, char **TAILPTR, int BASE)
    unsigned long long int strtoull (const_char *STRING, char **TAILPTR, int BASE)
    float strtof (const_char *STRING, char **TAILPTR)
    double strtod (const_char *STRING, char **TAILPTR)
    long double strtold (const_char *STRING, char **TAILPTR)

    # 7.20.2 Pseudo-random sequence generation functions
    enum: RAND_MAX
    int rand ()
    void srand (unsigned int SEED)

    # 7.20.3 Memory management functions
    void *calloc (size_t COUNT, size_t ELTSIZE)
    void free (void *PTR)
    void *malloc (size_t SIZE)
    void *realloc (void *PTR, size_t NEWSIZE)

    # 7.20.4 Communication with the environment
    enum: EXIT_FAILURE
    enum: EXIT_SUCCESS
    void exit (int STATUS)
    void _Exit (int STATUS)
    int atexit (void (*FUNCTION) ())
    void abort ()
    char *getenv (const_char *NAME)
    int system (const_char *COMMAND)

    #7.20.5 Searching and sorting utilities
    void *bsearch (const_void *KEY, const_void *ARRAY,
                   size_t COUNT, size_t SIZE,
                   int (*COMPARE)(const_void *, const_void *))
    void qsort (void *ARRAY, size_t COUNT, size_t SIZE,
                int (*COMPARE)(const_void *, const_void *))

    # 7.20.6 Integer arithmetic functions
    int abs (int NUMBER)
    long int labs (long int NUMBER)
    long long int llabs (long long int NUMBER)
    ctypedef struct div_t:
        int quot
        int rem
    div_t div (int NUMERATOR, int DENOMINATOR)
    ctypedef struct ldiv_t:
        long int quot
        long int rem
    ldiv_t ldiv (long int NUMERATOR, long int DENOMINATOR)
    ctypedef struct lldiv_t:
        long long int quot
        long long int rem
    lldiv_t lldiv (long long int NUMERATOR, long long int DENOMINATOR)


    # 7.20.7 Multibyte/wide character conversion functions
    # XXX TODO

    # 7.20.8 Multibyte/wide string conversion functions
    # XXX TODO
