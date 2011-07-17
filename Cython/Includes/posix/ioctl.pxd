cdef extern from "sys/ioctl.h" nogil:
    int ioctl(int fd, int request, ...)
