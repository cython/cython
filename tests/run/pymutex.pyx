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


def test_pymutex_locked_basic():
    """
    Test basic locked() functionality for pymutex.
    
    >>> test_pymutex_locked_basic()
    True
    """
    cdef cython.pymutex lock
    
    # Lock should not be locked initially
    if lock.locked():
        return False
    
    # After acquiring, should be locked
    lock.acquire()
    if not lock.locked():
        lock.release()
        return False
    
    # After releasing, should not be locked
    lock.release()
    if lock.locked():
        return False
    
    return True


def test_pymutex_locked_with_statement():
    """
    Test locked() with 'with' statement.
    
    >>> test_pymutex_locked_with_statement()
    True
    """
    cdef cython.pymutex lock
    cdef bint was_locked_inside = False
    cdef bint was_unlocked_before = False
    cdef bint was_unlocked_after = False
    
    was_unlocked_before = not lock.locked()
    
    with lock:
        was_locked_inside = lock.locked()
    
    was_unlocked_after = not lock.locked()
    
    return was_unlocked_before and was_locked_inside and was_unlocked_after


def test_pymutex_locked_nogil():
    """
    Test locked() can be called without GIL.
    
    >>> test_pymutex_locked_nogil()
    True
    """
    cdef cython.pymutex lock
    cdef bint result = False
    
    with nogil:
        if not lock.locked():
            lock.acquire()
            if lock.locked():
                lock.release()
                if not lock.locked():
                    result = True
    
    return result


def test_pymutex_locked_in_parallel():
    """
    Test locked() in parallel context to verify thread-safety.
    
    >>> test_pymutex_locked_in_parallel()
    True
    """
    cdef cython.pymutex lock
    cdef int i
    cdef int failures = 0
    
    for i in cython.parallel.prange(100, nogil=True):
        # Each thread checks if unlocked, acquires, checks if locked, releases
        if not lock.locked():
            lock.acquire()
            if not lock.locked():
                failures = failures + 1
            lock.release()
    
    return failures == 0


def test_locked_on_attribute():
    """
    Test locked() on attribute lock.
    
    >>> test_locked_on_attribute()
    True
    """
    cdef HasLockAttribute obj = HasLockAttribute()
    
    if obj.lock.locked():
        return False
    
    obj.lock.acquire()
    result = obj.lock.locked()
    obj.lock.release()
    
    return result and not obj.lock.locked()


def test_global_lock_locked():
    """
    Test locked() on global lock.
    
    >>> test_global_lock_locked()
    True
    """
    if global_lock.locked():
        return False
    
    with global_lock:
        if not global_lock.locked():
            return False
    
    return not global_lock.locked()
