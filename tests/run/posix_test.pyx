# tag: posix
from libc.stdio   cimport *
from posix.unistd cimport *
from posix.fcntl  cimport *


cdef int noisy_function() except -1:
    cdef int ret = 0
    ret = printf(b"012%s6789\n", "345")
    assert ret == 11  # printf()
    ret = printf(b"012%d6789\n", 345)
    assert ret == 11  # printf()
    ret = printf(b"0123456789\n")
    assert ret == 11  # printf()
    ret = fflush(stdout)
    assert ret == 0  # fflush()
    ret = fprintf(stdout, b"012%d6789\n", 345)
    assert ret == 11  # fprintf()
    ret = fflush(stdout)
    assert ret == 0  # fflush()
    ret = write(STDOUT_FILENO, b"0123456789\n", 11)
    assert ret == 11  # write()
    return  0


def test_silent_stdout():
    """
    >>> test_silent_stdout()
    """
    cdef int ret
    cdef int stdout_save, dev_null
    stdout_save = dup(STDOUT_FILENO)
    assert stdout_save != -1
    dev_null = open(b"/dev/null", O_WRONLY, 0)
    assert dev_null != -1
    ret = dup2(dev_null, STDOUT_FILENO)
    assert ret == STDOUT_FILENO
    ret = close(dev_null)
    assert ret == 0
    try:
        noisy_function()
    finally:
        ret = dup2(stdout_save, STDOUT_FILENO)
        assert ret == STDOUT_FILENO
        ret = close(stdout_save)
        assert ret == 0


cdef class silent_fd:
    cdef int fd_save, fd

    def __cinit__(self, int fd=-1):
        self.fd_save = -1
        self.fd = STDOUT_FILENO
        if fd != -1:
            self.fd = fd

    def __enter__(self):
        cdef int ret = 0, dev_null = -1
        assert self.fd_save == -1
        dev_null = open(b"/dev/null", O_WRONLY, 0)
        assert dev_null != -1
        try:
            self.fd_save = dup(self.fd)
            assert self.fd_save != -1
            try:
                ret = dup2(dev_null, self.fd)
                assert ret != -1
            except:
                ret = close(self.fd_save)
                self.fd_save = -1
        finally:
            ret = close(dev_null)

    def __exit__(self, t, v, tb):
        cdef int ret = 0
        if self.fd_save != -1:
            ret = dup2(self.fd_save, self.fd)
            assert ret == self.fd
            ret = close(self.fd_save)
            assert ret == 0
            self.fd_save = -1
        return None


def test_silent_stdout_ctxmanager():
    """
    >> test_silent_stdout_ctxmanager()
    """
    with silent_fd():
        noisy_function()
    try:
        with silent_fd():
            noisy_function()
            raise RuntimeError
    except RuntimeError:
        pass
    with silent_fd(STDOUT_FILENO):
        noisy_function()
