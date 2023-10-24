# 7.21 String handling <string.h>

extern from *:
    # deprecated backwards compatibility declarations
    ctypedef const char const_char "const char"
    ctypedef const signed char const_schar "const signed char"
    ctypedef const unsigned char const_uchar "const unsigned char"
    ctypedef const void const_void "const void"

extern from "<string.h>" nogil:
    fn void *memcpy  (void *pto, const void *pfrom, usize size)
    fn void *memmove (void *pto, const void *pfrom, usize size)
    fn void *memset  (void *block, i32 c, usize size)
    fn i32  memcmp   (const void *a1, const void *a2, usize size)
    fn void *memchr  (const void *block, i32 c, usize size)

    fn void *memchr  (const void *block, i32 c, usize size)
    fn void *memrchr (const void *block, i32 c, usize size)

    fn usize strlen   (const char *s)
    fn char   *strcpy  (char *pto, const char *pfrom)
    fn char   *strncpy (char *pto, const char *pfrom, usize size)
    fn char   *strdup  (const char *s)
    fn char   *strndup (const char *s, usize size)
    fn char   *strcat  (char *pto, const char *pfrom)
    fn char   *strncat (char *pto, const char *pfrom, usize size)

    fn i32 strcmp (const char *s1, const char *s2)
    fn i32 strcasecmp (const char *s1, const char *s2)
    fn i32 strncmp (const char *s1, const char *s2, usize size)
    fn i32 strncasecmp (const char *s1, const char *s2, usize n)

    fn i32    strcoll (const char *s1, const char *s2)
    fn usize strxfrm (char *pto, const char *pfrom, usize size)

    fn char *strerror (i32 errnum)

    fn char *strchr  (const char *string, i32 c)
    fn char *strrchr (const char *string, i32 c)

    fn char *strstr     (const char *haystack, const char *needle)
    fn char *strcasestr (const char *haystack, const char *needle)

    fn usize strcspn (const char *string, const char *stopset)
    fn usize strspn  (const char *string, const char *set)
    fn char * strpbrk (const char *string, const char *stopset)

    fn char *strtok (char *newstring, const char *delimiters)
    fn char *strsep (char **string_ptr, const char *delimiter)
