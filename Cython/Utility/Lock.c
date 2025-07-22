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

#if CYTHON_COMPILING_IN_PYPY || PYPY_VERSION_NUM < 0x07031400
#define PY_LOCK_ACQUIRED 1
#endif

static void __Pyx__Locks_PyThreadTypeLock_LockGil_spin(__Pyx_Locks_PyThreadTypeLock lock) {
    while (1) {
        int res;
        Py_BEGIN_ALLOW_THREADS
#if !CYTHON_COMPILING_IN_PYPY || PYPY_VERSION_NUM >= 0x07031400
        // Don't block indefinitely. This ensures we don't deadlock (forever) on
        //
        // with nogil:
        //   with lock:
        //     with gil:
        //       ...
        //
        // Arguably that's user error, but it seems better to try to help them out.
        res = PyThread_acquire_lock_timed(lock, CYTHON_LOCK_AND_GIL_DEADLOCK_AVOIDANCE_TIME, 0);
#else
        res = PyThread_acquire_lock(lock, WAIT_LOCK);
#endif
        // Wait on the GIL while holding the lock. But importantly we never do the inverse
        // and wait on the lock while holding the GIL.
        Py_END_ALLOW_THREADS
        if (likely(res == PY_LOCK_ACQUIRED)) {
            // All good - we got the lock
            return;
        }
    }
}

static CYTHON_INLINE void __Pyx__Locks_PyThreadTypeLock_LockGil(__Pyx_Locks_PyThreadTypeLock lock) {
    #if !CYTHON_COMPILING_IN_PYPY || PYPY_VERSION_NUM >= 0x07031400
    // This is possibly dubious - it makes things faster in the uncontended case, but
    // in the heavily-contended case it makes it more likely that one thread will dominate.
    if (likely(PyThread_acquire_lock_timed(lock, 0, 0) == PY_LOCK_ACQUIRED)) {
        // All good - we got the lock
        return;
    }
    #endif
    __Pyx__Locks_PyThreadTypeLock_LockGil_spin(lock);
}

static void __Pyx__Locks_PyThreadTypeLock_Lock(__Pyx_Locks_PyThreadTypeLock lock) {
    int has_gil = 0;
#if CYTHON_COMPILING_IN_LIMITED_API
    if (__PYX_LIMITED_VERSION_HEX >= 0x030d0000 || __Pyx_get_runtime_version() >= 0x030d0000) {
        // Swap the existing thread state to see if we had the GIL.
        // Requires re-acquiring the thread state if we had it, but no-op if we didn't.
        PyThreadState *tstate = PyThreadState_Swap(NULL);
        has_gil = tstate != NULL;
        if (has_gil)
            PyThreadState_Swap(tstate);
    } else {
        // We can't tell if we have the GIL. Therefore make sure we do have it
        // and then restore whatever state was there before.
        PyGILState_STATE state = PyGILState_Ensure();
        __Pyx_Locks_PyThreadTypeLock_LockNogil(lock);
        PyGILState_Release(state);
        return;
    }
#elif CYTHON_COMPILING_IN_PYPY || PY_VERSION_HEX < 0x030B0000
    has_gil = PyGILState_Check();
#elif PY_VERSION_HEX < 0x030d0000
    has_gil = _PyThreadState_UncheckedGet() != NULL;
#else
    has_gil = PyThreadState_GetUnchecked() != NULL;
#endif
    if (has_gil) {
        __Pyx_Locks_PyThreadTypeLock_LockGil(lock);
    } else {
        __Pyx_Locks_PyThreadTypeLock_LockNogil(lock);
    }
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
