# 7.21 String handling <string.h>

cdef extern from *:
    ctypedef char const_char "const char"
    ctypedef signed char const_schar "const signed char"
    ctypedef unsigned char const_uchar "const unsigned char"
    ctypedef void const_void "const void"

cdef extern from "string.h" nogil:

    void *memcpy  (void *TO, const_void *FROM, size_t SIZE)
    void *memmove (void *TO, const_void *FROM, size_t SIZE)
    void *memset  (void *BLOCK, int C, size_t SIZE)
    int  memcmp   (const_void *A1, const_void *A2, size_t SIZE)
    void *memchr  (const_void *BLOCK, int C, size_t SIZE)

    void *memchr  (const_void *BLOCK, int C, size_t SIZE)
    void *memrchr (const_void *BLOCK, int C, size_t SIZE)

    size_t strlen   (const_char *S)
    char   *strcpy  (char *TO, const_char *FROM)
    char   *strncpy (char *TO, const_char *FROM, size_t SIZE)
    char   *strdup  (const_char *S)
    char   *strndup (const_char *S, size_t SIZE)
    char   *strcat  (char *TO, const_char *FROM)
    char   *strncat (char *TO, const_char *FROM, size_t SIZE)

    int strcmp (const_char *S1, const_char *S2)
    int strcasecmp (const_char *S1, const_char *S2)
    int strncmp (const_char *S1, const_char *S2, size_t SIZE)
    int strncasecmp (const_char *S1, const_char *S2, size_t N)

    int    strcoll (const_char *S1, const_char *S2)
    size_t strxfrm (char *TO, const_char *FROM, size_t SIZE)

    char *strerror (int ERRNUM)

    char *strchr  (const_char *STRING, int C)
    char *strrchr (const_char *STRING, int C)

    char *strstr     (const_char *HAYSTACK, const_char *NEEDLE)
    char *strcasestr (const_char *HAYSTACK, const_char *NEEDLE)

    size_t strcspn (const_char *STRING, const_char *STOPSET)
    char * strpbrk (const_char *STRING, const_char *STOPSET)

    char *strtok (char *NEWSTRING, const_char *DELIMITERS)
    char *strsep (char **STRING_PTR, const_char *DELIMITER)
