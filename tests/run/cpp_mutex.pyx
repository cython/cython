# mode: run
# tag: cpp, cpp17, no-cpp-locals

# cython: language_level=3

from libcpp.mutex cimport (
    mutex, once_flag, unique_lock, call_once,
    adopt_lock, scoped_lock
)
from libcpp.shared_mutex cimport (
    shared_mutex, shared_lock
)

# Note to readers: some of these tests are a bit lazy
# with the GIL because they know the lock is only being
# used from one thread. Be very careful with the GIL and
# C++ locks to avoid deadlocks!

def test_mutex():
    """
    >>> test_mutex()
    """
    cdef mutex m
    cdef unique_lock[mutex] l
    m.try_lock()
    m.unlock()
    m.lock()
    m.unlock()
    l = unique_lock[mutex](m)
    l.unlock()

def test_unique_lock_more():
    """
    >>> test_unique_lock_more()
    """
    cdef mutex m
    cdef unique_lock[mutex] l
    m.lock()
    l = unique_lock[mutex](m, adopt_lock)
    # unlocked automatically when it exits scope


cdef void call_me_once() noexcept with gil:
    print("Listen very carefully, I shall say this only once.")

cdef extern from *:
    """
    #include <stdexcept>
    void call_once_unsuccessfully_cpp() {
        throw std::runtime_error("");
    }

    void call_with_int(int i) {
        if (i != 1) throw std::runtime_error("");
    }
    """
    void call_once_unsuccessfully_cpp() except +
    void call_with_int(int) noexcept

def test_once_flag1():
    """
    >>> test_once_flag1()
    Listen very carefully, I shall say this only once.
    """
    cdef once_flag flag
    call_once(flag, call_me_once)
    call_once(flag, call_me_once)  # This shouldn't do anything.

def test_once_flag2():
    """
    >>> test_once_flag2()
    """
    cdef once_flag flag
    try:
        call_once(flag, call_once_unsuccessfully_cpp)
        assert False
    except RuntimeError:
        pass

def test_once_flag3():
    """
    >>> test_once_flag3()
    """
    cdef once_flag flag
    call_once(flag, call_with_int, 1)


def test_scoped_lock():
    """
    >>> test_scoped_lock()
    """
    cdef mutex m1
    cdef mutex m2
    # use pointers because allocating it on the heap will be hard
    cdef scoped_lock[mutex, mutex]* l = new scoped_lock[mutex, mutex](m1, m2)
    del l

def test_shared_mutex():
    """
    >>> test_shared_mutex()
    """
    cdef shared_mutex m
    cdef shared_lock[shared_mutex] l1
    cdef shared_lock[shared_mutex] l2
    l1 = shared_lock[shared_mutex](m)
    l2 = shared_lock[shared_mutex](m)  # fine - it's shared.
