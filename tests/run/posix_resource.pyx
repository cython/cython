# tag: posix

from posix.unistd cimport *
from posix.resource cimport *


def test_getpriority():
    """
    >>> test_getpriority()
    0
    """
    ret = getpriority(PRIO_PROCESS, getpid())
    # DISABLED - does not work on current test server
    return 0  # ret


def test_getrlimit():
    """
    >>> test_getrlimit()
    0
    True
    """
    cdef rlimit rlim
    rlim.rlim_cur = 0

    ret = getrlimit(RLIMIT_CPU, &rlim)
    print(ret)
    return rlim.rlim_cur != 0


def test_getrusage():
    """
    >>> test_getrusage()
    0
    """
    cdef rusage r
    ret = getrusage(RUSAGE_SELF, &r)
    return ret
