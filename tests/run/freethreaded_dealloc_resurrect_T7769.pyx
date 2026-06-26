# mode: run
# tag: c11, no-cpp, threads

# cython: freethreading_compatible=True

# Regression test for a free-threading __dealloc__ resurrection race.
#
# The reference-count guard that Cython emits around a user __dealloc__ must not
# make the dying object acquirable by other threads.  On a free-threaded build,
# using Py_SET_REFCNT(o, 1) on the (unowned, merged) dying object writes the
# "live, shared count 1" encoding into ob_ref_shared, which a concurrent
# PyUnstable_TryIncRef() would accept -- resurrecting an object whose __dealloc__
# has already started.  The fix keeps the object alive owner-locally, leaving the
# shared refcount at the refuse sentinel so cross-thread TryIncRef keeps failing.
#
# This test publishes each instance to a borrowed slot and, from another thread,
# repeatedly upgrades that borrowed pointer with the documented
# PyUnstable_EnableTryIncRef/PyUnstable_TryIncRef protocol.  If a TryIncRef ever
# succeeds on an object that is already in __dealloc__, the run is buggy (and an
# unfixed free-threaded build also aborts with
# "Py_SET_REFCNT: Assertion `refcnt >= 0' failed").  The PyUnstable_TryIncRef API
# exists only on CPython 3.14+, and the race only exists on free-threaded builds,
# so the consumer is a no-op elsewhere and the test then trivially passes.

cdef extern from *:
    """
    #if PY_VERSION_HEX >= 0x030E0000 && defined(Py_GIL_DISABLED)
    #include <stdatomic.h>
    static _Atomic(PyObject*) _ka_slot = NULL;
    static atomic_long _ka_caught = 0;
    static void _ka_publish(PyObject *o) { atomic_store(&_ka_slot, o); }
    static void _ka_enable(PyObject *o) { PyUnstable_EnableTryIncRef(o); }
    static void _ka_consume(int (*dying)(PyObject *)) {
        PyObject *o = atomic_load(&_ka_slot);
        if (o && PyUnstable_TryIncRef(o)) {       /* borrowed -> strong upgrade */
            if (dying(o)) atomic_fetch_add(&_ka_caught, 1);
            Py_DECREF(o);
        }
    }
    static long _ka_caught_count(void) { return atomic_load(&_ka_caught); }
    #else
    static void _ka_publish(PyObject *o) { (void)o; }
    static void _ka_enable(PyObject *o) { (void)o; }
    static void _ka_consume(int (*dying)(PyObject *)) { (void)dying; }
    static long _ka_caught_count(void) { return 0; }
    #endif
    """
    void _ka_publish(object)
    void _ka_enable(object)
    void _ka_consume(int (*)(object) noexcept)
    long _ka_caught_count()


from threading import Thread


cdef int _is_dying(object o) noexcept:
    return (<Dying>o).dying


cdef class Dying:
    cdef public int dying

    def __cinit__(self):
        _ka_enable(self)
        _ka_publish(self)

    def __dealloc__(self):
        # Mark the object as mid-deallocation, then widen the window a little so
        # the consumer thread has a chance to race the guard.
        self.dying = 1
        cdef int i
        for i in range(200):
            pass


def _consume_loop(long iterations):
    cdef long i
    for i in range(iterations):
        _ka_consume(_is_dying)


def run(long producer_loops=100000, long consumer_iterations=2000000):
    """
    >>> run()
    0
    """
    t = Thread(target=_consume_loop, args=(consumer_iterations,))
    t.start()
    try:
        for _ in range(producer_loops):
            obj = Dying()
            obj = None
    finally:
        t.join()
    return _ka_caught_count()
