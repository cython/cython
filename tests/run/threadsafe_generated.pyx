# mode: run

cimport cython

import threading
import pickle

cdef class C:
    cdef public object o
    cdef readonly int i

def test_properties(n_writers, n_readers):
    """
    >>> test_properties(2, 2)
    """

    # Mostly just a "do the references get messed up?" stress test
    c = C()
    o1 = object()
    o2 = object()
    cdef object c_obj = c
    cdef object two = eval("2")  # obfuscate from Cython a bit
    
    barrier = threading.Barrier(n_writers+n_readers)
    done = threading.Event()

    def writer():
        barrier.wait()
        while not done.is_set():
            c_obj.o = o1
            # Test documented interaction of locking with threadsafe properties
            with cython.critical_section(c):
                c.i += 1
                c.i *= <int>two
                if c.i > 1000:
                    c.i = 0
            c_obj.o = o2
    
    def reader():
        barrier.wait()
        for _ in range(5000):
            p = pickle.dumps(c_obj)
            o = c_obj.o
            assert c_obj.i % 2 == 0

    readers = [ threading.Thread(target=reader) for _ in range(n_readers) ]
    writers = [ threading.Thread(target=writer) for _ in range(n_writers) ]

    for thread in readers+writers:
        thread.start()
    for thread in readers:
        thread.join()
    done.set()
    for thread in writers:
        thread.join()

@cython.dataclasses.dataclass(order=True)
cdef class DC:
    x: object
    y: object

def test_dataclasses():
    """
    >>> test_dataclasses()
    """
    cdef object dc1 = DC(x=1.0, y=1.0)
    cdef object dc2 = DC(x=2.0, y=2.0)

    barrier = threading.Barrier(2)
    done = threading.Event()

    def writer():
        barrier.wait()
        while not done.is_set():
            # only one writer thread so no race between reader and writer
            dc1.__init__(x=dc1.x+0.1, y=dc1.y+0.1)
            dc2.__init__(x=dc2.x+0.1, y=dc2.y+0.1)

    def reader():
        barrier.wait()
        for _ in range(5000):
            assert dc1 < dc2

    t1 = threading.Thread(target=reader)
    t2 = threading.Thread(target=writer)
    t1.start()
    t2.start()
    t1.join()
    done.set()
    t2.join()
