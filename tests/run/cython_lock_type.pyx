# mode: run
# tag: openmp

cimport cython
cimport cython.parallel

cdef cython.pymutex global_lock

cdef void hide_the_reduction(int *x) noexcept nogil:
    x[0] = x[0] + 1

def global_lock_with_prange():
    """
    >>> global_lock_with_prange()
    5000
    """
    cdef int count = 0
    cdef int i
    for i in cython.parallel.prange(5000, nogil=True):
        with global_lock:
            hide_the_reduction(&count)
    return count

def local_lock_with_prange():
    """
    >>> local_lock_with_prange()
    5000
    """
    cdef int count = 0
    cdef int i
    cdef cython.pymutex lock
    for i in cython.parallel.prange(5000, nogil=True):
        with lock:
            hide_the_reduction(&count)
    return count

cdef class HasLockAttribute:
    cdef cython.pymutex lock

def lock_on_attribute(HasLockAttribute has_lock):
    """
    >>> lock_on_attribute(HasLockAttribute())
    5000
    """
    cdef int count = 0
    cdef int i
    for i in cython.parallel.prange(5000, nogil=True):
        with has_lock.lock:
            hide_the_reduction(&count)
    return count

def lock_in_closure():
    """
    >>> lock_in_closure()
    5000
    """
    cdef int count = 0
    cdef int i
    # pythread_type_lock and pymutex should behave basically the same. So test them both
    cdef cython.pythread_type_lock lock

    def inner():
        with lock:
            hide_the_reduction(&count)

    for i in cython.parallel.prange(5000, nogil=True):
        with gil:
            inner()

    return count 

def manual_acquire_release():
    """
    >>> manual_acquire_release()
    5000
    """
    cdef int count = 0
    cdef int i
    cdef cython.pymutex lock

    for i in cython.parallel.prange(5000, nogil=True):
        # Test it both with and without the GIL
        if i % 2 == 0:
            with gil:
                lock.acquire()
                hide_the_reduction(&count)
                lock.release()
        else:
            lock.acquire()
            hide_the_reduction(&count)
            lock.release()
    return count

# Although forbidden to pass a copy of the lock, pointers are fine
cdef void acquire_and_hide(cython.pymutex* l, int* i) nogil noexcept:
    with l[0]:
        hide_the_reduction(i)

def pass_as_pointer():
    """
    >>> pass_as_pointer()
    5000
    """
    cdef int count = 0
    cdef int i
    cdef cython.pymutex lock
    for i in cython.parallel.prange(5000, nogil=True):
        acquire_and_hide(&lock, &count)
    return count
