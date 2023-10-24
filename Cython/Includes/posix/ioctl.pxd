extern from "<sys/ioctl.h>" nogil:
    enum: FIONBIO

    fn i32 ioctl(i32 fd, i32 fd, ...)
