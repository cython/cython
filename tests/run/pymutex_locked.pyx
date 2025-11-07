# mode: run
# tag: openmp

cimport cython
cimport cython.parallel

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


cdef class HasLockAttribute:
    cdef cython.pymutex lock
    
    def test_locked(self):
        """
        Test locked() on attribute lock.
        
        >>> obj = HasLockAttribute()
        >>> obj.test_locked()
        True
        """
        if self.lock.locked():
            return False
        
        self.lock.acquire()
        result = self.lock.locked()
        self.lock.release()
        
        return result and not self.lock.locked()


def test_global_lock_locked():
    """
    Test locked() on global lock.
    
    >>> test_global_lock_locked()
    True
    """
    cdef cython.pymutex global_lock
    
    if global_lock.locked():
        return False
    
    with global_lock:
        if not global_lock.locked():
            return False
    
    return not global_lock.locked()
