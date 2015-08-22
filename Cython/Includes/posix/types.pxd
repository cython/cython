cdef extern from "sys/types.h":
    # Some types get extra long for large file support (_FILE_OFFSET_BITS).
    # As well as the types below, it affects rlim_t (see resource.pxd)
    # also fsfilcnt_t / fsblkcnt_t for statvfs(), but cython doesn't expose it
    # <https://web.archive.org/web/20000903062829/http://ftp.sas.com/standards/large.file/x_open.20Mar96.html#2.2.2>
    #
    # time_t could also be 64-bit.  OpenBSD changed it already.

    ctypedef long long              blkcnt_t
    ctypedef long                   blksize_t
    ctypedef long                   clockid_t
    ctypedef long                   dev_t
    ctypedef long                   gid_t
    ctypedef long                   id_t
    ctypedef unsigned long long     ino_t
    ctypedef long                   mode_t
    ctypedef long                   nlink_t
    ctypedef long long              off_t
    ctypedef long                   pid_t
    ctypedef long                   sigset_t
    ctypedef long                   suseconds_t
    ctypedef long long              time_t
    ctypedef long                   timer_t
    ctypedef long                   uid_t
