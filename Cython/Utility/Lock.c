////////////////////// CythonLockType.proto ////////////////////
//@proto_block: utility_code_proto_before_types

// TODO - this imposes an ABI so we need to do something clever on public functions/classes

#if PY_VERSION_HEX > 0x030d0000 && !CYTHON_COMPILING_IN_LIMITED_API
#define __Pyx_CythonLockType Py_Mutex
#define __Pyx_InitCythonLock(l) (void)(l)
#define __Pyx_DeleteCythonLock(l) (void)(l)
// Py_Mutex takes care of all GIL handling itself
#define __Pyx_LockCythonLock(l) (PyMutex_Lock(l), 0)
#define __Pyx_UnlockCythonLock(l) (PyMutex_Unlock(l), 0)

#else

static void __Pyx_RaiseCythonLockError(const char* what); /* proto */

#if defined(__cplusplus) && __cplusplus >= 201103L
#include <mutex>
#include <new>
#include <system_error>
union __Pyx_CythonLockType { std::mutex m; };
#define __Pyx_InitCythonLock(l) new (&(l).m) std::mutex()
#define __Pyx_DeleteCythonLock(l) (l).m.~mutex()

static CYTHON_INLINE int __Pyx__LockCythonTryLock(__Pyx_CythonLockType *l_ptr) {
    try {
        return l_ptr->m.try_lock();
    } catch (const std::system_error& e) {
        __Pyx_RaiseCythonLockError(e.what());
        return -1;
    }
}

static CYTHON_INLINE int __Pyx__LockCythonLock_NoGil(__Pyx_CythonLockType *l_ptr) {
    try {
        l_ptr->m.lock();
        return 1;
    } catch (const std::system_error& e) {
        __Pyx_RaiseCythonLockError(e.what());
        return -1;
    }
}

static CYTHON_INLINE int __Pyx__UnlockCythonLock(__Pyx_CythonLockType *l_ptr) {
    try {
        l_ptr->m.unlock();
        return 0;
    } catch (const std::system_error& e) {
        __Pyx_RaiseCythonLockError(e.what());
        return -1;
    }
}

#elif __STDC_VERSION__ >= 201112L && !defined(__STDC_NO_THREADS__)
#include  <threads.h>
#define __Pyx_CythonLockType mtx_t
#define __Pyx_InitCythonLock(l) mtx_init(&(l), mtx_plain)
#define __Pyx_DeleteCythonLock(l) mtx_destroy(&(l))

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
    int result = mtx_unlock(l_ptr);
    if (unlikely (result == thrd_error)) {
        __Pyx_RaiseCythonLockError("Error when acquiring cython.lock");
        return -1;
    }
    return 0;
}

// TODO other implementations like pthreads, MSVC.

#else

#define __Pyx_CythonLockType PyThread_type_lock
#define __Pyx_InitCythonLock(l) l = PyThread_allocate_lock()
#define __Pyx_DeleteCythonLock(l) = PyThread_free_lock()

#endif

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
