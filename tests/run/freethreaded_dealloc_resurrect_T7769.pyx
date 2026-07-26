# mode: run
# tag: c11, no-cpp, threads

# cython: freethreading_compatible=True

# Regression test for a free-threading __dealloc__ resurrection race (GH #7769).
#
# Cython's keep-alive guard around a user __dealloc__ must not make the dying
# object acquirable by other threads.  The old Py_SET_REFCNT(o, 1) wrote a "live,
# shared count 1" encoding that a concurrent PyUnstable_TryIncRef() would accept,
# resurrecting an object already in __dealloc__.
#
# Each time an object enters __dealloc__ it publishes "self" and blocks until a
# probe thread answers, so it is provably mid-__dealloc__ (alive, before tp_free)
# when the probe attempts one cross-thread TryIncRef -- which a fixed build must
# refuse.  A separate thread is required (a same-thread TryIncRef takes the owner
# fast path and succeeds even when fixed).  The probe is a threading.Thread so it
# holds a PyThreadState and needs no C11 <threads.h> (absent on macOS).  Outside
# free-threaded CPython 3.14+ the helpers are no-ops and the test is trivial.

from threading import Thread, Event

cdef extern from *:
    """
    #if PY_VERSION_HEX >= 0x030E0000 && defined(Py_GIL_DISABLED)
    #include <stdatomic.h>
    static _Atomic(PyObject *) _ka_slot = NULL;    /* borrowed: object now in __dealloc__ */
    static atomic_long _ka_caught = 0;             /* # of dying objects acquired cross-thread */
    static int  _ka_enabled(void) { return 1; }
    static void _ka_enable(PyObject *o) { PyUnstable_EnableTryIncRef(o); }
    static void _ka_publish(PyObject *o) { atomic_store(&_ka_slot, o); }
    /* One cross-thread upgrade of the mid-__dealloc__ object; success == resurrection. */
    static void _ka_probe(void) {
        PyObject *o = atomic_load(&_ka_slot);
        if (o && PyUnstable_TryIncRef(o)) { atomic_fetch_add(&_ka_caught, 1); Py_DECREF(o); }
    }
    static long _ka_caught_count(void) { return atomic_load(&_ka_caught); }
    #else
    static int  _ka_enabled(void) { return 0; }
    static void _ka_enable(PyObject *o) { (void) o; }
    static void _ka_publish(PyObject *o) { (void) o; }
    static void _ka_probe(void) { }
    static long _ka_caught_count(void) { return 0; }
    #endif
    """
    bint _ka_enabled()
    void _ka_enable(object)
    void _ka_publish(object)
    void _ka_probe()
    long _ka_caught_count()


_request = Event()   # __dealloc__ -> probe: probe now
_answer = Event()    # probe -> __dealloc__: done
_active = False      # False also tells the probe to exit


cdef class Dying:
    def __cinit__(self):
        _ka_enable(self)

    def __dealloc__(self):
        if not _active:
            return
        _ka_publish(self)
        _answer.clear()
        _request.set()
        _answer.wait()   # block in __dealloc__ until the probe has answered


def _probe_main():
    while True:
        _request.wait()
        _request.clear()
        if not _active:
            return
        _ka_probe()
        _answer.set()


def run(int n=1000):
    """
    >>> run()
    0
    """
    global _active
    if not _ka_enabled():
        return 0
    t = Thread(target=_probe_main)
    t.start()
    _active = True
    try:
        for _ in range(n):
            obj = Dying()
            obj = None
    finally:
        _active = False
        _request.set()   # wake the probe so it observes _active and exits
        t.join()
    return _ka_caught_count()
