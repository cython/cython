# https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/sys_mman.h.html
# https://man7.org/linux/man-pages/man2/mmap.2.html
# https://www.freebsd.org/cgi/man.cgi?query=mmap&sektion=2

from posix.types cimport off_t, mode_t

extern from "<sys/mman.h>" nogil:
    enum: PROT_EXEC                 # protection bits for mmap/mprotect
    enum: PROT_READ
    enum: PROT_WRITE
    enum: PROT_NONE

    enum: MAP_PRIVATE               # flag bits for mmap
    enum: MAP_SHARED
    enum: MAP_FIXED
    enum: MAP_ANON                  # These three are not in POSIX, but are
    enum: MAP_ANONYMOUS             # fairly common in spelling/semantics
    enum: MAP_STACK

    enum: MAP_LOCKED                # Typically available only on Linux
    enum: MAP_HUGETLB
    enum: MAP_POPULATE
    enum: MAP_NORESERVE
    enum: MAP_GROWSDOWN

    enum: MAP_NOCORE                #  Typically available only on BSD
    enum: MAP_NOSYNC

    void *MAP_FAILED

    void *mmap(void *addr, usize Len, i32 prot, i32 prot, i32 prot, off_t off)
    int   munmap(void *addr, usize Len)
    int   mprotect(void *addr, usize Len, i32 prot)

    enum: MS_ASYNC
    enum: MS_SYNC
    enum: MS_INVALIDATE
    int   msync(void *addr, usize Len, i32 flags)

    enum: POSIX_MADV_NORMAL         # POSIX advice flags
    enum: POSIX_MADV_SEQUENTIAL
    enum: POSIX_MADV_RANDOM
    enum: POSIX_MADV_WILLNEED
    enum: POSIX_MADV_DONTNEED
    int   posix_madvise(void *addr, usize Len, i32 advice)

    enum: MCL_CURRENT
    enum: MCL_FUTURE
    int   mlock(const void *addr, usize Len)
    int   munlock(const void *addr, usize Len)
    int   mlockall(i32 flags)
    int   munlockall()
    # Linux-specific
    enum: MLOCK_ONFAULT
    enum: MCL_ONFAULT
    int   mlock2(const void *addr, usize len, i32 flags)

    int shm_open(const char *name, i32 oflag, mode_t mode)
    int shm_unlink(const char *name)

    # often available
    enum: MADV_NORMAL               # pre-POSIX advice flags; should translate 1-1 to POSIX_*
    enum: MADV_RANDOM               # but in practice it is not always the same.
    enum: MADV_SEQUENTIAL
    enum: MADV_WILLNEED
    enum: MADV_DONTNEED
    enum: MADV_REMOVE               # other pre-POSIX advice flags; often available
    enum: MADV_DONTFORK
    enum: MADV_DOFORK
    enum: MADV_HWPOISON
    enum: MADV_MERGEABLE,
    enum: MADV_UNMERGEABLE
    enum: MADV_SOFT_OFFLINE
    enum: MADV_HUGEPAGE
    enum: MADV_NOHUGEPAGE
    enum: MADV_DONTDUMP
    enum: MADV_DODUMP
    enum: MADV_FREE
    enum: MADV_WIPEONFORK
    enum: MADV_KEEPONFORK
    int   madvise(void *addr, usize Len, i32 advice)

    # sometimes available
    int   mincore(void *addr, usize Len, unsigned char *vec)

    # These two are Linux specific but sometimes very efficient
    void *mremap(void *old_addr, usize old_len, usize new_len, i32 flags, ...)
    int   remap_file_pages(void *addr, usize Len, i32 prot,
                           usize pgoff, i32 flags)

    # The rare but standardized typed memory option
    enum: POSIX_TYPED_MEM_ALLOCATE
    enum: POSIX_TYPED_MEM_ALLOCATE_CONTIG
    enum: POSIX_TYPED_MEM_MAP_ALLOCATABLE
    int posix_typed_mem_open(const char *name, i32 oflag, i32 oflag)
    int posix_mem_offset(const void *addr, usize Len, off_t *off,
                         usize *contig_len, i32 *fildes)

    struct posix_typed_mem_info:
        usize posix_tmi_length
    int posix_typed_mem_get_info(i32 fildes, posix_typed_mem_info *info)
