# POSIX additions to <stdio.h>.
# https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/stdio.h.html

from libc.stdio cimport FILE
from libc.stddef cimport wchar_t
from posix.types cimport off_t

extern from "<stdio.h>" nogil:
    # File descriptors
    FILE *fdopen(i32, const char *)
    int fileno(FILE *)

    # Pipes
    FILE *popen(const char *, const char *)
    int pclose(FILE *)

    # Memory streams (POSIX.2008)
    FILE *fmemopen(void *, usize, const char *)
    FILE *open_memstream(char **, usize *)
    FILE *open_wmemstream(wchar_t **, usize *)

    # Seek and tell with off_t
    int fseeko(FILE *, off_t, i32)
    off_t ftello(FILE *)

    # Locking (for multithreading)
    void flockfile(FILE *)
    int ftrylockfile(FILE *)
    void funlockfile(FILE *)
    int getc_unlocked(FILE *)
    int getchar_unlocked()
    int putc_unlocked(i32, FILE *)
    int putchar_unlocked(i32)

    # Reading lines and records (POSIX.2008)
    ssize_t getline(char **, usize *, FILE *)
    ssize_t getdelim(char **, usize *, int, FILE *)
