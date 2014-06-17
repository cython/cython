# tag: posix
from posix.unistd    cimport *
from posix.resource cimport *

def test_getpriority():
    """
    >>> test_getpriority()
    """
    ret = getpriority(PRIO_PROCESS, getpid())
    assert ret == 0

def test_getrlimit():
    """
    >>> test_getrlimit()
    """
    cdef rlimit rlim
    ret = getrlimit(RLIMIT_CPU, &rlim)
    assert ret == 0
    assert rlim.rlim_cur != 0

def test_getrusage():
    """
    >>> test_getrusage()
    """
    cdef rusage r
    ret = getrusage(RUSAGE_SELF, &r)
    assert ret == 0
