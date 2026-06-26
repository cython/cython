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
# To detect this deterministically (rather than relying on timing luck), a
# dedicated probe thread does a single cross-thread PyUnstable_TryIncRef each time
# an object enters __dealloc__: __dealloc__ hands "self" to the probe thread and
# blocks until the probe reports back.  A separate thread is required -- a
# same-thread TryIncRef would take the owner fast path and succeed even with the
# fix, so it could not tell buggy from fixed.  If the probe ever acquires a strong
# reference to an object that is mid-__dealloc__, the guard resurrected it.
#
# PyUnstable_TryIncRef exists only on CPython 3.14+ and the race only exists on
# free-threaded builds, so on every other build the helpers are no-ops and the
# test passes trivially.

cdef extern from *:
    """
    #if PY_VERSION_HEX >= 0x030E0000 && defined(Py_GIL_DISABLED)
    #include <stdatomic.h>
    #include <threads.h>

    typedef int (*_ka_dyingfn)(PyObject *);

    static _Atomic(PyObject *) _ka_slot = NULL;   /* object currently in __dealloc__ */
    static _ka_dyingfn         _ka_dying = NULL;   /* reads the per-object "dying" flag */
    static atomic_int  _ka_request = 0;            /* __dealloc__ -> probe: probe now */
    static atomic_int  _ka_answered = 0;           /* probe -> __dealloc__: done */
    static atomic_int  _ka_quit = 0;               /* shut the probe thread down */
    static atomic_long _ka_caught = 0;             /* # of TryIncRefs that hit a dying object */
    static thrd_t      _ka_thread;

    static int _ka_probe_main(void *unused) {
        (void) unused;
        for (;;) {
            while (!atomic_load(&_ka_request)) {
                if (atomic_load(&_ka_quit))
                    return 0;
                thrd_yield();
            }
            PyObject *o = atomic_load(&_ka_slot);
            /* The object is alive (we are inside its __dealloc__, which is blocked
               in the handshake below), so reading it here is safe.  A correct build
               must refuse this cross-thread upgrade; a buggy one accepts it. */
            if (o && PyUnstable_TryIncRef(o)) {
                if (_ka_dying(o))
                    atomic_fetch_add(&_ka_caught, 1);
                Py_DECREF(o);
            }
            atomic_store(&_ka_request, 0);
            atomic_store(&_ka_answered, 1);
        }
    }

    static void _ka_start(_ka_dyingfn dying) {
        _ka_dying = dying;
        atomic_store(&_ka_quit, 0);
        thrd_create(&_ka_thread, _ka_probe_main, NULL);
    }
    static void _ka_stop(void) {
        atomic_store(&_ka_quit, 1);
        thrd_join(_ka_thread, NULL);
    }
    static void _ka_enable(PyObject *o) { PyUnstable_EnableTryIncRef(o); }

    /* Called from inside __dealloc__: ask the probe thread to TryIncRef "self"
       right now, and block until it has answered. */
    static void _ka_handshake(PyObject *o) {
        atomic_store(&_ka_slot, o);
        atomic_store(&_ka_answered, 0);
        atomic_store(&_ka_request, 1);
        while (!atomic_load(&_ka_answered))
            thrd_yield();
    }
    static long _ka_caught_count(void) { return atomic_load(&_ka_caught); }

    #else
    typedef int (*_ka_dyingfn)(PyObject *);
    static void _ka_start(_ka_dyingfn dying) { (void) dying; }
    static void _ka_stop(void) { }
    static void _ka_enable(PyObject *o) { (void) o; }
    static void _ka_handshake(PyObject *o) { (void) o; }
    static long _ka_caught_count(void) { return 0; }
    #endif
    """
    ctypedef int (*_ka_dyingfn)(object) noexcept
    void _ka_start(_ka_dyingfn)
    void _ka_stop()
    void _ka_enable(object)
    void _ka_handshake(object)
    long _ka_caught_count()


cdef int _is_dying(object o) noexcept:
    return (<Dying>o).dying


cdef class Dying:
    cdef public int dying

    def __cinit__(self):
        _ka_enable(self)

    def __dealloc__(self):
        self.dying = 1
        _ka_handshake(self)


def run(int n=1000):
    """
    >>> run()
    0
    """
    _ka_start(_is_dying)
    try:
        for _ in range(n):
            obj = Dying()
            obj = None
    finally:
        _ka_stop()
    return _ka_caught_count()
