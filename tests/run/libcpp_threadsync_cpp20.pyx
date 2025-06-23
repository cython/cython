# mode: run
# tag: cpp, cpp20, no-cpp-locals

from libcpp.latch cimport latch
from libcpp.barrier cimport barrier
from libcpp.semaphore cimport binary_semaphore, counting_semaphore
from libcpp.utility cimport move

cimport cython

#from threading import Thread

def test_latch():
    """
    # Really just a compile test
    >>> test_latch()
    """
    # Latch isn't even movable so heap-allocation is the only option for Cython
    cdef latch *l = new latch(4)
    try:
        l.count_down()
        l.count_down(2)
        l.arrive_and_wait()
    finally:
        del l

@cython.cpp_locals(True)  # arrival_token not necessarily default constructible
def test_barrier1():
    """
    >>> test_barrier1()
    """
    cdef barrier *b = new barrier(3)
    try:
        token = b.arrive()
        <void>b.arrive(2)  # Ignore warning about nodiscard
        b.wait(move(token))  # should execute immediately
    finally:
        del b

cdef void print_something() nogil noexcept:
    print("Something")

ctypedef void (*func_type)() nogil noexcept

def test_barrier2():
    """
    >>> test_barrier2()
    Something
    Barrier reset
    Something
    """
    cdef barrier[func_type] *b = new barrier[func_type](2, print_something)
    try:
        b.arrive_and_drop()
        b.arrive_and_wait()  # Should be done so doesn't really wait
        print("Barrier reset")
        b.arrive_and_wait()
    finally:
        del b

def test_counting_semaphore1():
    """
    >>> test_counting_semaphore1()
    """
    cdef counting_semaphore *s = new counting_semaphore(0)
    try:
        assert not s.try_acquire()
        assert s.max() > 0  # probably much greater
        s.release()
        s.release(2)
        s.acquire()
    finally:
        del s

cdef extern from *:
    cdef cppclass two "2":
        pass

def test_counting_semaphore2():
    """
    >>> test_counting_semaphore2()
    """
    cdef counting_semaphore[two] *s = new counting_semaphore[two](0)
    del s

def test_binary_semaphore():
    """
    >>> test_binary_semaphore()
    """
    cdef binary_semaphore *s = new binary_semaphore(1)
    try:
        # Implementations are allowed to spuriously fail, and we're not actually
        # testing the standard library, so don't worry about the outcome, just
        # that it compiles.
        if s.try_acquire():
            s.release()
    finally:
        del s