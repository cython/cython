# mode: run
# tag: cpp, cpp17, no-cpp-locals

# cython: language_level=3

from libcpp.mutex cimport (
    mutex, once_flag, unique_lock, call_once,
    adopt_lock, scoped_lock,
    py_safe_call_once, py_safe_call_object_once, py_safe_once_flag,
    py_safe_construct_unique_lock, py_safe_lock,
)
from libcpp.shared_mutex cimport (
    shared_mutex, shared_lock,
    py_safe_construct_shared_lock,
)

from threading import Thread, Barrier

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


def test_py_safe_construct_unique_lock(n_threads):
    """
    >>> test_py_safe_construct_unique_lock(4)
    4
    """

    cdef mutex m
    cdef count = 0

    barrier = Barrier(n_threads)
    def thread_func():
        nonlocal count

        barrier.wait()
        # lock is released on function exit
        lock = py_safe_construct_unique_lock(m)
        count += 1
    threads = [ Thread(target=thread_func) for _ in range(n_threads) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(count)

def test_py_safe_lock(n_threads):
    """
    >>> test_py_safe_lock(4)
    4
    """

    cdef mutex m1
    cdef mutex m2
    cdef count = 0

    barrier = Barrier(n_threads)
    def thread_func():
        nonlocal count

        barrier.wait()
        # lock is released on function exit
        py_safe_lock(m1, m2)
        try:
            count += 1
        finally:
            m1.unlock()
            m2.unlock()

    threads = [ Thread(target=thread_func) for _ in range(n_threads) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(count)

def test_py_safe_lock_nogil():
    """
    >>> test_py_safe_lock_nogil()
    """
    cdef mutex m
    with nogil:
        py_safe_lock(m)
        m.unlock()

def py_safe_lock_stress_test():
    """
    >>> py_safe_lock_stress_test()
    2000
    """
    cdef mutex m
    cdef int count = 0

    def thread_func():
        nonlocal count
        for i in range(500):
            if i%2:
                with nogil:
                    py_safe_lock(m)
                    count += 1
                    m.unlock()
            else:
                py_safe_lock(m)
                count += 1
                m.unlock()

    threads = [ Thread(target=thread_func) for _ in range(4) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(count)



# Note that it is only safe to acquire the GIL because we aren't actually running the
# tests from multiple threads.
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
    with nogil:
        call_once(flag, call_me_once)
        call_once(flag, call_me_once)  # This shouldn't do anything.

def test_once_flag2():
    """
    # Test disabled - this usage is correct and works but GCCs libstdc++ is broken on every
    # non-x86 platform (and more...) https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66146
    # >>> test_once_flag2()
    """
    cdef once_flag flag
    try:
        with nogil:
            call_once(flag, call_once_unsuccessfully_cpp)
        assert False
    except RuntimeError:
        pass

def test_once_flag3():
    """
    >>> test_once_flag3()
    """
    cdef once_flag flag
    with nogil:
        call_once(flag, call_with_int, 1)

def test_py_safe_once_object():
    """
    >>> test_py_safe_once_object()
    Listen very carefully, I shall say this only once.
    """
    cdef py_safe_once_flag flag

    def py_func():
        print("Listen very carefully, I shall say this only once.")

    n_threads = 4
    barrier = Barrier(n_threads)
    def thread_func():
        barrier.wait()
        py_safe_call_object_once(flag, py_func)
    threads = [ Thread(target=thread_func) for _ in range(n_threads) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def test_py_safe_once_object_fail():
    """
    >>> test_py_safe_once_object_fail()
    Good
    """
    cdef py_safe_once_flag flag
    try:
        py_safe_call_object_once(flag, None)
    except TypeError:
        pass
    else:
        assert False
    py_safe_call_object_once(flag, lambda: print("Good"))

cdef object global_value = 0

cdef void increment_global_value():
    global global_value
    global_value += 1

def test_py_safe_once_cdef():
    """
    >>> test_py_safe_once_cdef()
    1
    """
    global global_value
    global_value = 0

    cdef py_safe_once_flag flag

    n_threads = 4
    barrier = Barrier(n_threads)
    def thread_func():
        barrier.wait()
        py_safe_call_once(flag, increment_global_value)
    threads = [ Thread(target=thread_func) for _ in range(n_threads) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(global_value)

def test_py_safe_once_cdef_nogil():
    """
    >>> test_py_safe_once_cdef_nogil()
    1
    """
    global global_value
    global_value = 0

    cdef py_safe_once_flag flag
    with nogil:
        # function is called with the GIL, but GIL state
        # on exit is the same as on entry.
        py_safe_call_once(flag, increment_global_value)

    print(global_value)


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

def test_py_safe_construct_shared_lock(n_threads):
    """
    >>> test_py_safe_construct_shared_lock(4)
    Good news - we didn't deadlock
    """

    cdef shared_mutex m

    barrier1 = Barrier(n_threads)
    barrier2 = Barrier(n_threads)
    def thread_func():
        barrier1.wait()
        # lock is released on function exit
        lock = py_safe_construct_shared_lock(m)
        barrier2.wait()
    threads = [ Thread(target=thread_func) for _ in range(n_threads) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Good news - we didn't deadlock")
