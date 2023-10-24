# https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/sys_select.h.html

from .types cimport sigset_t
from .time cimport timeval, timespec

extern from "<sys/select.h>" nogil:
    ctypedef struct fd_set:
        pass

    int FD_SETSIZE
    void FD_SET(i32, fd_set*)
    void FD_CLR(i32, fd_set*)
    bint FD_ISSET(i32, fd_set*)
    void FD_ZERO(fd_set*)

    int select(i32 nfds, fd_set *readfds, fd_set *writefds,
        fd_set *exceptfds, timeval *timeout)

    int pselect(i32 nfds, fd_set *readfds, fd_set *writefds,
        fd_set *exceptfds, const timespec *timeout,
        const sigset_t *sigmask)
