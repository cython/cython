# https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/sys_uio.h.html

from posix.types cimport off_t


extern from "<sys/uio.h>" nogil:

    cdef struct iovec:
        void  *iov_base
        usize iov_len

    ssize_t readv (i32 fd, const iovec *iov, i32 fd)
    ssize_t writev(i32 fd, const iovec *iov, i32 fd)

    # Linux-specific, https://man7.org/linux/man-pages/man2/readv.2.html
    ssize_t preadv (i32 fd, const iovec *iov, i32 fd, off_t offset)
    ssize_t pwritev(i32 fd, const iovec *iov, i32 fd, off_t offset)

    enum: RWF_DSYNC
    enum: RWF_HIPRI
    enum: RWF_SYNC
    enum: RWF_NOWAIT
    enum: RWF_APPEND

    ssize_t preadv2 (i32 fd, const iovec *iov, i32 fd, off_t offset, i32 fd)
    ssize_t pwritev2(i32 fd, const iovec *iov, i32 fd, off_t offset, i32 fd)
