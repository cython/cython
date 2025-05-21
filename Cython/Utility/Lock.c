////////////////////// PyThreadTypeLock.proto //////////
//@proto_block: utility_code_proto_before_types

// This lock type always uses PyThread_type_lock. The main reason
// to use it is if you are using the Limited API and want to
// share locks between modules.

#define __Pyx_Locks_PyThreadTypeLock PyThread_type_lock
#define __Pyx_Locks_PyThreadTypeLock_DECL NULL
#define __Pyx_Locks_PyThreadTypeLock_Init(l) l = PyThread_allocate_lock()
#define __Pyx_Locks_PyThreadTypeLock_Delete(l) PyThread_free_lock(l)
#define __Pyx_Locks_PyThreadTypeLock_LockNogil(l) (void)PyThread_acquire_lock(l, WAIT_LOCK)
#define __Pyx_Locks_PyThreadTypeLock_Unlock(l) PyThread_release_lock(l)
static void __Pyx__Locks_PyThreadTypeLock_Lock(__Pyx_Locks_PyThreadTypeLock lock); /* proto */
static void __Pyx__Locks_PyThreadTypeLock_LockGil(__Pyx_Locks_PyThreadTypeLock lock); /* proto */
// CYTHON_INLINE because these may be unused
static CYTHON_INLINE void __Pyx_Locks_PyThreadTypeLock_Lock(__Pyx_Locks_PyThreadTypeLock lock) {
    __Pyx__Locks_PyThreadTypeLock_Lock(lock);
}
static CYTHON_INLINE void __Pyx_Locks_PyThreadTypeLock_LockGil(__Pyx_Locks_PyThreadTypeLock lock) {
    __Pyx__Locks_PyThreadTypeLock_LockGil(lock);
}

////////////////////// PyThreadTypeLock ////////////////

static void __Pyx__Locks_PyThreadTypeLock_LockGil_slow_spin(__Pyx_Locks_PyThreadTypeLock lock) {
    while (1) {
        // If we've been spinning for a while take a slower path, where
        // we release the GIL, get the lock, release the lock, reacquire the GIL
        // and then hope the lock is still available when we try to reacquire it.
        Py_BEGIN_ALLOW_THREADS
        (void)PyThread_acquire_lock(lock, WAIT_LOCK);
        PyThread_release_lock(lock);
        Py_END_ALLOW_THREADS
        if (likely(PyThread_acquire_lock_timed(lock, 0, 0) == PY_LOCK_ACQUIRED)) {
            // All good - we got the lock
            return;
        }
    }
}

static void __Pyx__Locks_PyThreadTypeLock_LockGil_quick_spin(__Pyx_Locks_PyThreadTypeLock lock) {
    for (int spin_count=0; spin_count<100; ++spin_count) {
        // Release and re-acquire the GIL, try to get the lock again.
        Py_BEGIN_ALLOW_THREADS
        Py_END_ALLOW_THREADS
        if (likely(PyThread_acquire_lock_timed(lock, 0, 0) == PY_LOCK_ACQUIRED)) {
            // All good - we got the lock
            return;
        }
    }
    __Pyx__Locks_PyThreadTypeLock_LockGil_slow_spin(lock);
}

static CYTHON_INLINE void __Pyx__Locks_PyThreadTypeLock_LockGil(__Pyx_Locks_PyThreadTypeLock lock) {
    if (likely(PyThread_acquire_lock_timed(lock, 0, 0) == PY_LOCK_ACQUIRED)) {
        // All good - we got the lock
        return;
    }
    __Pyx__Locks_PyThreadTypeLock_LockGil_quick_spin(lock);
}

static void __Pyx__Locks_PyThreadTypeLock_Lock(__Pyx_Locks_PyThreadTypeLock lock) {
#if CYTHON_COMPILING_IN_LIMITED_API
    // We can't tell if we have the GIL. Therefore make sure we do have it
    // and then restore whatever state was there before.
    PyGILState_STATE state = PyGILState_Ensure();
    __Pyx_Locks_PyThreadTypeLock_LockNogil(lock);
    PyGILState_Release(state);
#else
    if (PyGILState_Check()) {
        __Pyx_Locks_PyThreadTypeLock_LockGil(lock);
    } else {
        __Pyx_Locks_PyThreadTypeLock_LockNogil(lock);
    }
#endif
}

////////////////////// PyMutex.proto ////////////////////
//@proto_block: utility_code_proto_before_types
//@requires: PyThreadTypeLock

// We support two implementations - a Py3.13+ version using PyMutex and
// an older version using PyThread_type_lock.
// In principle it'd be possible to also use things like c++ std::mutex
// (in the absence of PyMutex). I've decided against this for ABI reasons.

// With the Limited API There is an ABI problem - if a lock is ever
// shared between two modules then they must agree on the definition,
// and so Limited API sharing with regular API will disagree.

// Therefore I explicitly ban Limited API modules from using
// CythonLockType in a public way. However, they can use
// CythonCompatibleLockType which will always be PyThread_type_lock.

#if PY_VERSION_HEX > 0x030d0000 && !CYTHON_COMPILING_IN_LIMITED_API
#define __Pyx_Locks_PyMutex PyMutex
#define __Pyx_Locks_PyMutex_DECL {0}
#define __Pyx_Locks_PyMutex_Init(l) (void)(l)
#define __Pyx_Locks_PyMutex_Delete(l) (void)(l)
// Py_Mutex takes care of all GIL handling itself
#define __Pyx_Locks_PyMutex_Lock(l) PyMutex_Lock(&l)
#define __Pyx_Locks_PyMutex_Unlock(l) PyMutex_Unlock(&l)
#define __Pyx_Locks_PyMutex_LockGil(l) PyMutex_Lock(&l)
#define  __Pyx_Locks_PyMutex_LockNogil(l) PyMutex_Lock(&l)

#else

#define __Pyx_Locks_PyMutex __Pyx_Locks_PyThreadTypeLock
#define __Pyx_Locks_PyMutex_DECL __Pyx_Locks_PyThreadTypeLock_DECL
#define __Pyx_Locks_PyMutex_Init(l) __Pyx_Locks_PyThreadTypeLock_Init(l)
#define __Pyx_Locks_PyMutex_Delete(l) __Pyx_Locks_PyThreadTypeLock_Delete(l)
#define __Pyx_Locks_PyMutex_Lock(l) __Pyx_Locks_PyThreadTypeLock_Lock(l)
#define __Pyx_Locks_PyMutex_Unlock(l) __Pyx_Locks_PyThreadTypeLock_Unlock(l)
#define __Pyx_Locks_PyMutex_LockGil(l) __Pyx_Locks_PyThreadTypeLock_LockGil(l)
#define __Pyx_Locks_PyMutex_LockNogil(l) __Pyx_Locks_PyThreadTypeLock_LockNogil(l)

#endif

//////////////////////////// CythonPyMutexPublicCheck ///////////////////////////////////

#ifndef CYTHON_UNSAFE_IGNORE_PYMUTEX_ABI_COMPATIBILITY
#define CYTHON_UNSAFE_IGNORE_PYMUTEX_ABI_COMPATIBILITY 0
#endif

/* CYTHON_UNSAFE_IGNORE_PYMUTEX_ABI_COMPATIBILITY is left for an advanced user who
 * wants to disable this error.  However, please don't complain to us when your code
 * breaks.  Whatever you do, the Limited API version always uses the "compatible" lock
 * type anyway, so you're only saving yourself a few extra characters typing.
 */
#if CYTHON_COMPILING_IN_LIMITED_API && !CYTHON_UNSAFE_IGNORE_PYMUTEX_ABI_COMPATIBILITY
#error cython.pymutex is shared between multiple modules in the Limited API.\
 This is intentionally disabled because it is not possible for regular API and Limited API\
 modules to be compatible with each other.  Use cython.pythread_type_lock for a safe\
 alternative lock type instead.
#endif
