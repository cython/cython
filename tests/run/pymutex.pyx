# mode: run
# tag: openmp

cimport cython
cimport cython.parallel

from threading import Thread

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


# Using C is just a quick way to inject a few Python calls
# into the generator tests.  With generators and critical sections
# putting these calls between yields would definitely break.
# We don't expect the same to apply to pymutex but it makes the test
# a little more robust.
g = {}
exec(
    """
class C:
    x = 1
    def f(self):
        self.x += 1
    """, g, g)
C = g['C']
del g

def generator_local():
    """
    Really simple generator - a bit pointless because
    nothing outside it can access the lock, but it should still work.

    >>> g = generator_local()
    >>> next(g)
    1
    >>> C().f()  # inject Python "work"
    >>> next(g)
    2
    >>> try: next(g)
    ... except StopIteration: pass
    ... else: print("Fail")
    """
    cdef cython.pymutex m
    with m:
        yield 1
        yield 2

def generator_global(value_in):
    """
    >>> g = generator_global(1)
    >>> thread_func_result = None
    >>> def thread_func():
    ...    global thread_func_result
    ...    g2 = generator_global(2)
    ...    thread_func_result = [ x for x in g2 ]
    >>> next(g)
    1
    >>> from threading import Thread; t = Thread(target=thread_func); t.start()
    >>> assert thread_func_result is None  # blocked by lock
    >>> try: next(g)
    ... except StopIteration: pass
    ... else: print("Fail")
    >>> t.join(10.)
    >>> thread_func_result
    [2]
    """
    with global_lock:
        yield value_in

def make_captured_mutex_generator():
    """
    >>> gen_func = make_captured_mutex_generator()
    >>> g = gen_func('a')
    >>> thread_func_result = None
    >>> def thread_func():
    ...    global thread_func_result
    ...    thread_func_result = [ x for x in gen_func('b') ]
    >>> next(g)
    'a 0'
    >>> from threading import Thread; t = Thread(target=thread_func); t.start()
    >>> assert thread_func_result is None  # blocked by lock
    >>> C().f()  # dummy Python work
    >>> next(g)
    'a 1'
    >>> assert thread_func_result is None  # blocked by lock
    >>> try: next(g)
    ... except StopIteration: pass
    ... else: print("Fail")
    >>> t.join(10.)
    >>> thread_func_result
    ['b 0', 'b 1']
    """
    cdef cython.pymutex m
    def g(id):
        with m:
            yield f"{id} 0"
            yield f"{id} 1"
    return g

def generator_cclass(HasLockAttribute o, id):
    """
    >>> l = HasLockAttribute()
    >>> g1 = generator_cclass(l, 'a')
    >>> thread_func_result = None
    >>> def thread_func():
    ...    global thread_func_result
    ...    thread_func_result = [ x for x in generator_cclass(l, 'b') ]
    >>> next(g1)
    'a 0'
    >>> from threading import Thread; t = Thread(target=thread_func); t.start()
    >>> assert thread_func_result is None  # blocked by lock
    >>> C().f()  # dummy Python work
    >>> next(g1)
    'a 1'
    >>> assert thread_func_result is None  # blocked by lock
    >>> try: next(g1)
    ... except StopIteration: pass
    ... else: print("Fail")
    >>> t.join(10.)
    >>> thread_func_result
    ['b 0', 'b 1']
    """
    with o.lock:
        yield f"{id} 0"
        yield f"{id} 1"

def pymutex_with_gil():
    """
    >>> pymutex_with_gil()
    4000
    """
    cdef cython.pymutex lock
    cdef int count = 0
    def thread_func():
        nonlocal count
        for i in range(1000):
            with lock:
                count += 1
    threads = [ Thread(target=thread_func) for _ in range(4) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return count

def old_lock_with_gil():
    """
    >>> old_lock_with_gil()
    4000
    """
    cdef cython.pythread_type_lock lock
    cdef int count = 0
    def thread_func():
        nonlocal count
        for i in range(1000):
            with lock:
                count += 1
    threads = [ Thread(target=thread_func) for _ in range(4) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return count

def pymutex_without_gil():
    """
    >>> pymutex_without_gil()
    4000
    """
    cdef cython.pymutex lock
    cdef int count = 0
    def thread_func():
        nonlocal count
        with nogil:
            for i in range(1000):
                with lock:
                    count += 1
    threads = [ Thread(target=thread_func) for _ in range(4) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return count

def old_lock_without_gil():
    """
    >>> old_lock_without_gil()
    4000
    """
    cdef cython.pythread_type_lock lock
    cdef int count = 0
    def thread_func():
        nonlocal count
        with nogil:
            for i in range(1000):
                with lock:
                    count += 1
    threads = [ Thread(target=thread_func) for _ in range(4) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return count

cdef void pymutex_unknown_gil_impl(cython.pymutex* lock, int* count) nogil noexcept:
    with lock[0]:
        count[0] += 1

def pymutex_unknown_gil():
    """
    >>> pymutex_unknown_gil()
    4000
    """
    cdef cython.pymutex lock
    cdef int count = 0
    def thread_func():
        for i in range(1000):
            if i % 2:
                pymutex_unknown_gil_impl(&lock, &count)
            else:
                with nogil:
                    pymutex_unknown_gil_impl(&lock, &count)
    threads = [ Thread(target=thread_func) for _ in range(4) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return count

cdef void old_lock_unknown_gil_impl(cython.pythread_type_lock* lock, int* count) nogil noexcept:
    with lock[0]:
        count[0] += 1

def old_lock_unknown_gil():
    """
    >>> old_lock_unknown_gil()
    4000
    """
    cdef cython.pythread_type_lock lock
    cdef int count = 0
    def thread_func():
        for i in range(1000):
            if i % 2:
                old_lock_unknown_gil_impl(&lock, &count)
            else:
                with nogil:
                    old_lock_unknown_gil_impl(&lock, &count)
    threads = [ Thread(target=thread_func) for _ in range(4) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return count
