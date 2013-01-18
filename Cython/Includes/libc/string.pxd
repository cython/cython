# 7.21 String handling <string.h>

cdef extern from *:
    # deprecated backwards compatibility declarations
    ctypedef const char const_char "const char"
    ctypedef const signed char const_schar "const signed char"
    ctypedef const unsigned char const_uchar "const unsigned char"
    ctypedef const void const_void "const void"

cdef extern from "string.h" nogil:

    void *memcpy  (void *TO, const void *FROM, size_t SIZE)
    void *memmove (void *TO, const void *FROM, size_t SIZE)
    void *memset  (void *BLOCK, int C, size_t SIZE)
    int  memcmp   (const void *A1, const void *A2, size_t SIZE)
    void *memchr  (const void *BLOCK, int C, size_t SIZE)

    void *memchr  (const void *BLOCK, int C, size_t SIZE)
    void *memrchr (const void *BLOCK, int C, size_t SIZE)

    size_t strlen   (const char *S)
    char   *strcpy  (char *TO, const char *FROM)
    char   *strncpy (char *TO, const char *FROM, size_t SIZE)
    char   *strdup  (const char *S)
    char   *strndup (const char *S, size_t SIZE)
    char   *strcat  (char *TO, const char *FROM)
    char   *strncat (char *TO, const char *FROM, size_t SIZE)

    int strcmp (const char *S1, const char *S2)
    int strcasecmp (const char *S1, const char *S2)
    int strncmp (const char *S1, const char *S2, size_t SIZE)
    int strncasecmp (const char *S1, const char *S2, size_t N)

    int    strcoll (const char *S1, const char *S2)
    size_t strxfrm (char *TO, const char *FROM, size_t SIZE)

    char *strerror (int ERRNUM)

    char *strchr  (const char *STRING, int C)
    char *strrchr (const char *STRING, int C)

    char *strstr     (const char *HAYSTACK, const char *NEEDLE)
    char *strcasestr (const char *HAYSTACK, const char *NEEDLE)

    size_t strcspn (const char *STRING, const char *STOPSET)
    char * strpbrk (const char *STRING, const char *STOPSET)

    char *strtok (char *NEWSTRING, const char *DELIMITERS)
    char *strsep (char **STRING_PTR, const char *DELIMITER)
