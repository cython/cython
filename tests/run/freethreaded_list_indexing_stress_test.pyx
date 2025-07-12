# mode: run
# tag: cpp, cpp11, no-cpp-locals

# cython: freethreading_compatible=True

# List indexing should be thread-safe (at least as far as not generating
# reference counting errors).
# It's actually surprisingly hard to make a test that reliably breaks and
# so this is pretty tailored to CPython's implementation.
# Essentially you want to catch it in "quick" deallocation (where objects
# are created and destroyed by the same thread).

cimport cython

from libcpp.atomic cimport atomic
from threading import Thread, Barrier

def run(reader, writer, n_threads, n_loops, *args):
    """
    >>> import gc
    >>> import sys
    >>> last_count = Counted.get_count()
    >>> run(read_local_var, write_local_var, 2, 2000, [None])
    >>> _ = gc.collect()
    >>> Counted.get_count() - last_count
    0

    >>> last_count = Counted.get_count()
    >>> run(read_global_var, write_global_var, 4, 100)
    >>> _ = gc.collect()
    >>> Counted.get_count() - last_count
    0

    >>> last_count = Counted.get_count()
    >>> closure_reader, closure_writer = make_closure_funcs()
    >>> run(closure_reader, closure_writer, 4, 100)
    >>> _ = gc.collect()
    >>> Counted.get_count() - last_count
    0
    """
    barrier = Barrier(n_threads+1)
    def call_read():
        barrier.wait()
        reader(n_loops, *args)

    def call_write(arg):
        barrier.wait()
        writer(n_loops, *args)

    l = [None]
    threads = [ Thread(target=call_read) for _ in range(n_threads) ]
    for t in threads:
        t.start()
    call_write(l)
    for t in threads:
        t.join()

cdef atomic[int] count
count.store(0)

cdef class Counted:
    def __cinit__(self):
        count.fetch_add(1)

    def __dealloc__(self):
        count.fetch_sub(1)

    @staticmethod
    def get_count():
        return count.load()

def read_local_var(int n_loops, list l not None):
    for _ in range(n_loops):
        tmp = l[0]

def write_local_var(int n_loops, list l not None):
    for _ in range(n_loops):
        l[0] = Counted()

cdef list global_list = [None]

def read_global_var(int n_loops):
    for _ in range(n_loops):
        tmp = global_list[0]

def write_global_var(int n_loops):
    for _ in range(n_loops):
        global_list[0] = Counted()
    global_list[0] = None


def make_closure_funcs():
    l = [None]
    def reader(int n_loops):
        for n in range(n_loops):
            tmp = l[0]
    def writer(int n_loops):
        for n in range(n_loops):
            l[0] = Counted()
        l[0] = None
    return reader, writer
