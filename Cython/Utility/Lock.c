////////////////////// CythonCompatibleLockType.proto //////////
//@proto_block: utility_code_proto_before_types

// This lock type always uses PyThread_type_lock. The main reason
// to use it is if you are using the Limited API and want to
// share locks between modules.

#define __Pyx_CythonCompatibleLockType PyThread_type_lock
#define __Pyx_InitCythonCompatibleLock(l) l = PyThread_allocate_lock()
#define __Pyx_DeleteCythonCompatibleLock(l) PyThread_free_lock(l)
#define __Pyx_LockCythonCompatibleLock_Nogil(l) (void)PyThread_acquire_lock(l, WAIT_LOCK)
#define __Pyx_UnlockCythonCompatibleLock(l) PyThread_release_lock(l)
static void __Pyx__LockCythonCompatibleLock(__Pyx_CythonCompatibleLockType lock); /* proto */
static void __Pyx__LockCythonCompatibleLock_Gil(__Pyx_CythonCompatibleLockType lock); /* proto */
// CYTHON_INLINE because these may be unused
static CYTHON_INLINE void __Pyx_LockCythonCompatibleLock(__Pyx_CythonCompatibleLockType lock) {
    __Pyx__LockCythonCompatibleLock(lock);
}
static CYTHON_INLINE void __Pyx_LockCythonCompatibleLock_Gil(__Pyx_CythonCompatibleLockType lock) {
    __Pyx__LockCythonCompatibleLock_Gil(lock);
}
#define __Pyx_LockCythonCompatibleLock_WithState(l, nogil_state) \
    nogil_state == 0 ? __Pyx_LockCythonCompatibleLock_Gil(l) : \
    (nogil_state == 1 ? __Pyx_LockCythonCompatibleLock_Nogil(l) : __Pyx_LockCythonCompatibleLock(l)) 

////////////////////// CythonCompatibleLockType ////////////////

static void __Pyx__LockCythonCompatibleLock_Gil(__Pyx_CythonCompatibleLockType lock) {
    int spin_count = 0;
    while (1) {
        if (likely(PyThread_acquire_lock_timed(lock, 0, 0) == PY_LOCK_ACQUIRED)) {
            // All good - we got the lock
            return;
        } else if (spin_count < 100) {
            ++spin_count;
            // Release and re-acquire the GIL, try to get the lock again.
            Py_BEGIN_ALLOW_THREADS
            Py_END_ALLOW_THREADS
        } else {
            // If we've been spinning for a while take a slower path, where
            // we release the GIL, get the lock, release the lock, reacquire the GIL
            // and then hope the lock is still available when we try to reacquire it.
            Py_BEGIN_ALLOW_THREADS
            (void)PyThread_acquire_lock(lock, WAIT_LOCK);
            PyThread_release_lock(lock);
            Py_END_ALLOW_THREADS
        }
    }
}

static void __Pyx__LockCythonCompatibleLock(__Pyx_CythonCompatibleLockType lock) {
#if CYTHON_COMPILING_IN_LIMITED_API
    // We can't tell if we have the GIL. Therefore make sure we do have it
    // and then restore whatever state was there before.
    PyGILState_STATE state = PyGILState_Ensure();
    __Pyx_LockCythonCompatibleLock_Gil(lock);
    PyGILState_Release(state);
#else
    if (PyGILState_Check()) {
        __Pyx_LockCythonCompatibleLock_Gil(lock);
    } else {
        __Pyx_LockCythonCompatibleLock_Nogil(lock);
    }
#endif
}

////////////////////// CythonLockType.proto ////////////////////
//@proto_block: utility_code_proto_before_types
//@requires: CythonCompatibleLockType

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
#define __Pyx_CythonLockType PyMutex
#define __Pyx_CYTHON_LOCK_TYPE_DECL {0}
#define __Pyx_InitCythonLock(l) (void)(l)
#define __Pyx_DeleteCythonLock(l) (void)(l)
// Py_Mutex takes care of all GIL handling itself
#define __Pyx_LockCythonLock(l) PyMutex_Lock(&l)
#define __Pyx_UnlockCythonLock(l) PyMutex_Unlock(&l)
#define __Pyx_LockCythonLock_Gil(l) PyMutex_Lock(&l)
#define  __Pyx_LockCythonLock_Nogil(l) PyMutex_Lock(&l)
#define __Pyx_LockCythonLock_WithState(l, ignore) PyMutex_Lock(&l)

#else

#define __Pyx_CythonLockType __Pyx_CythonCompatibleLockType
#define __Pyx_CYTHON_LOCK_TYPE_DECL NULL
#define __Pyx_InitCythonLock(l) __Pyx_InitCythonCompatibleLock(l)
#define __Pyx_DeleteCythonLock(l) __Pyx_DeleteCythonCompatibleLock(l)
#define __Pyx_LockCythonLock(l) __Pyx_LockCythonCompatibleLock(l)
#define __Pyx_UnlockCythonLock(l) __Pyx_UnlockCythonCompatibleLock(l)
#define __Pyx_LockCythonLock_Gil(l) __Pyx_LockCythonCompatibleLock_Gil(l)
#define __Pyx_LockCythonLock_Nogil(l) __Pyx_LockCythonCompatibleLock_Nogil(l)
#define __Pyx_LockCythonLock_WithState(l, nogil_state) __Pyx_LockCythonCompatibleLock_WithState(l, nogil_state)

#endif

//////////////////////////// CythonLockTypePublicCheck ///////////////////////////////////

#ifndef CYTHON_UNSAFE_IGNORE_LOCK_TYPE_ABI_COMPATIBILITY
#define CYTHON_UNSAFE_IGNORE_LOCK_TYPE_ABI_COMPATIBILITY 0
#endif

/* CYTHON_UNSAFE_IGNORE_LOCK_TYPE_ABI_COMPATIBILITY is left for an advanced user who
 * wants to disable this error.  However, please don't complain to us when your code
 * breaks.  Whatever you do, the Limited API version always uses the "compatible" lock
 * type anyway, so you're only saving yourself a few extra characters typing.
 */
#if CYTHON_COMPILING_IN_LIMITED_API && !CYTHON_UNSAFE_IGNORE_LOCK_TYPE_ABI_COMPATIBILITY
#error cython.lock_type is shared between multiple modules in the Limited API.\
 This is intentionally disabled because it is not possible for regular API and Limited API\
 modules to be compatible with each other.  Use cython.compatible_lock_type for a safe\
 alternative lock type instead.
#endif
