////////////////////// CythonLockType.proto ////////////////////
//@proto_block: utility_code_proto_before_types

// We support two implementations - a Py3.13+ version using PyMutex and
// an older version using PyThread_type_lock.
// In principle it'd be possible to also use things like c++ std::mutex
// (in the absence of PyMutex). I've decided against this for ABI reasons.

// There is an ABI problem - if the lock type is ever shared between
// modules (e.g. in a cdef class in a pxd file) then it's important that
// the modules agree on the definition.

// Where possible we try not to use the shared ABI to remove a layer of
// indirection, and to ensure we aren't forced into a slower implementation
// by a Limited API module being imported first. 

#ifndef CYTHON_USE_CYTHON_LOCK_ABI
#define CYTHON_USE_CYTHON_LOCK_ABI 0
#endif

static void __Pyx__InitCythonLock(__Pyx_CythonLockType *lock); /* proto */
static void __Pyx__DeallocCythonLock(__Pyx_CythonLockType *lock); /* proto */
static int __Pyx__LockCythonLock(__Pyx_CythonLockType *lock); /* proto */
static int __Pyx__UnlockCythonLock(__Pyx_CythonLockType *lock); /* proto */
static int __Pyx__LockCythonLock_Gil(__Pyx_CythonLockType *lock); /* proto */
static int __Pyx__LockCythonLock_NoGil(__Pyx_CythonLockType *lock); /* proto */

#if CYTHON_USE_CYTHON_LOCK_ABI
typedef union {
    // As of 3.13.0, Py_Mutex is smaller than PyThread_type_lock,
    // so the size is the same whether or not we can see "as_mutex".
    #if PY_VERSION_HEX > 0x030d0000 && !CYTHON_COMPILING_IN_LIMITED_API
    Py_Mutex as_mutex;
    #endif
    PyThread_type_lock as_pythread_lock;
} __Pyx_CythonLockType;

typedef struct {
    void (*init)(__Pyx_CythonLockType*);
    void (*dealloc)(__Pyx_CythonLockType*);
    int (*lock)(__Pyx_CythonLockType*);
    int (*unlock)(__Pyx_CythonLockType*);
    // Optimized versions for when we know the GIL state
    int (*lock_nogil)(__Pyx_CythonLockType*);
    int (*lock_gil)(__Pyx_CythonLockType*)
}  __Pyx_CythonLockAbi;

static __Pyx_CythonLockAbi __Pyx_CythonLockDefaultAbi = {
    &__Pyx__InitCythonLock,
    &__Pyx__DeallocCythonLock,
    &__Pyx__LockCythonLock,
    &__Pyx__UnlockCythonLock,
    &__Pyx__LockCythonLock_NoGil,
    &__Pyx__LockCythonLock_Gil
};

static __Pyx_CythonLockAbi* __Pyx_CythonLockSharedAbi = NULL;

#define __Pyx_InitCythonLock(l) __Pyx_CythonLockSharedAbi->init(&(l))
#define __Pyx_DeallocCythonLock(l) __Pyx_CythonLockSharedAbi->dealloc(&(l))
#define __Pyx_LockCythonLock(l) __Pyx_CythonLockSharedAbi->lock(&(l))
#define __Pyx_UnlockCythonLock __Pyx_CythonLockSharedAbi->unlock(&(l))
#define __Pyx_LockCythonLock_NoGil __Pyx_CythonLockSharedAbi->lock_nogil(&(l))
#define __Pyx_LockCythonLock_Gil __Pyx_CythonLockSharedAbi->lock_gil(&(l))
#else

#endif

#if PY_VERSION_HEX > 0x030d0000 && !CYTHON_COMPILING_IN_LIMITED_API
#define __Pyx_CythonLockType Py_Mutex
#define __Pyx_InitCythonLock(l) (void)(l)
#define __Pyx_DeleteCythonLock(l) (void)(l)
// Py_Mutex takes care of all GIL handling itself
#define __Pyx_LockCythonLock(l) (PyMutex_Lock(&l), 0)
#define __Pyx_UnlockCythonLock(l) (PyMutex_Unlock(&l), 0)

#else

static void __Pyx_RaiseCythonLockError(const char* what); /* proto */

#define __Pyx_CythonLockType PyThread_type_lock
#define __Pyx_InitCythonLock(l) l = PyThread_allocate_lock()
#define __Pyx_DeleteCythonLock(l) = PyThread_free_lock()
static CYTHON_INLINE int __Pyx__LockCythonTryLock(__Pyx_CythonLockType *l_ptr) {
    int result = mtx_trylock(l_ptr);
    if (likely(result == thrd_success)) {
        return 1;
    } else if (unlikely (result == thrd_error)) {
        __Pyx_RaiseCythonLockError("Error when trying to acquire cython.lock");
        return -1;
    }
    return 0;
}

static CYTHON_INLINE int __Pyx__LockCythonLock_NoGil(__Pyx_CythonLockType *l_ptr) {
    int result = mtx_lock(l_ptr);
    if (unlikely (result == thrd_error)) {
        __Pyx_RaiseCythonLockError("Error when acquiring cython.lock");
        return -1;
    }
    return 1;
}

static CYTHON_INLINE int __Pyx__UnlockCythonLock(__Pyx_CythonLockType *l_ptr) {
    PyThread_release_lock(*l_ptr);
    return 0;
}

#define __Pyx_LockCythonLock(l) __Pyx__LockCythonLock(&(l))
static int __Pyx__LockCythonLock(__Pyx_CythonLockType *lock); /* proto*/
#define __Pyx_UnlockCythonLock(l) __Pyx__UnlockCythonLock(&(l));

#endif // PY_VERSION_HEX > 0x030d0000 - i.e. just use Py_Mutex

#define __Pyx_EnterCythonlock(l) (unlikely(__Pyx_LockCythonLock((l)) == -1) ? NULL : &(l))

////////////////////// CythonLockType //////////////////////

#if !(PY_VERSION_HEX > 0x030d0000)
static int __Pyx_LockCythonLock_Gil(__Pyx_CythonLockType *lock) {
    int spin_count = 0;
    while (1) {
        int try_lock_result = __Pyx__LockCythonTryLock(lock);
        if (unlikely(try_lock_result == -1)) {
            return -1;
        } else if (likely(try_lock_result == 1)) {
            // All good - we got the lock
            return 0;
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
            if (unlikely(__Pyx__LockCythonLock_NoGil(lock) == -1)) {
                Py_BLOCK_THREADS;
                return -1;
            }
            __Pyx__UnlockCythonLock(lock);
            Py_END_ALLOW_THREADS
        }
    }
}

static int __Pyx__LockCythonLock(__Pyx_CythonLockType *lock) {
#if CYTHON_COMPILING_IN_LIMITED_API
    // We can't tell if we have the GIL. Therefore make sure we do have it
    // and then restore whatever state was there before.
    PyGILState_STATE state = PyGILState_Ensure();
    int result = __Pyx_LockCythonLock_Gil();
    PyGILState_Release(state);
    return result;
#else
    if (PyGILState_Check()) {
        return __Pyx_LockCythonLock_Gil(lock);
    }
    return __Pyx__LockCythonLock_NoGil(lock);
#endif
}

static void __Pyx_RaiseCythonLockError(const char* what) {
    PyGILState_STATE state = PyGILState_Ensure();
    PyErr_SetString(PyExc_SystemError, what);
    PyGILState_Release(state);
}
#endif // !(PY_VERSION_HEX > 0x030d0000) (where we just use Py_Mutex
