/////////// Atomics.proto /////////////
//@proto_block: utility_code_proto_before_types

#include <pythread.h>

#ifndef CYTHON_ATOMICS
    #define CYTHON_ATOMICS 1
#endif
// using CYTHON_ATOMICS as a cdef extern bint in the Cython memoryview code
// interacts badly with "import *". Therefore, define a helper function-like macro
#define __PYX_CYTHON_ATOMICS_ENABLED() CYTHON_ATOMICS
#define __PYX_GET_CYTHON_COMPILING_IN_CPYTHON_FREETHREADING() CYTHON_COMPILING_IN_CPYTHON_FREETHREADING

#define __pyx_atomic_int_type int
#define __pyx_nonatomic_int_type int

// For standard C/C++ atomics, get the headers first so we have ATOMIC_INT_LOCK_FREE
// defined when we decide to use them.
#if CYTHON_ATOMICS && (defined(__STDC_VERSION__) && \
                        (__STDC_VERSION__ >= 201112L) && \
                        !defined(__STDC_NO_ATOMICS__))
    #include <stdatomic.h>
#elif CYTHON_ATOMICS && (defined(__cplusplus) && ( \
                    (__cplusplus >= 201103L) || \
                    (defined(_MSC_VER) && _MSC_VER >= 1700)))
    #include <atomic>
#endif

#if CYTHON_ATOMICS && (defined(__STDC_VERSION__) && \
                        (__STDC_VERSION__ >= 201112L) && \
                        !defined(__STDC_NO_ATOMICS__) && \
                       ATOMIC_INT_LOCK_FREE == 2)
    // C11 atomics are available and  ATOMIC_INT_LOCK_FREE is definitely on
    #undef __pyx_atomic_int_type
    #define __pyx_atomic_int_type atomic_int
    #define __pyx_atomic_ptr_type atomic_uintptr_t
    #define __pyx_nonatomic_ptr_type uintptr_t
    #define __pyx_atomic_incr_relaxed(value) atomic_fetch_add_explicit(value, 1, memory_order_relaxed)
    #define __pyx_atomic_incr_acq_rel(value) atomic_fetch_add_explicit(value, 1, memory_order_acq_rel)
    #define __pyx_atomic_decr_acq_rel(value) atomic_fetch_sub_explicit(value, 1, memory_order_acq_rel)
    #define __pyx_atomic_sub(value, arg) atomic_fetch_sub(value, arg)
    #define __pyx_atomic_int_cmp_exchange(value, expected, desired) atomic_compare_exchange_strong(value, expected, desired)
    #define __pyx_atomic_load(value) atomic_load(value)
    #define __pyx_atomic_store(value, new_value) atomic_store(value, new_value)
    #define __pyx_atomic_pointer_load_relaxed(value) atomic_load_explicit(value, memory_order_relaxed)
    #define __pyx_atomic_pointer_load_acquire(value) atomic_load_explicit(value, memory_order_acquire)
    #define __pyx_atomic_pointer_exchange(value, new_value) atomic_exchange(value, (__pyx_nonatomic_ptr_type)new_value)
    #if defined(__PYX_DEBUG_ATOMICS) && defined(_MSC_VER)
        #pragma message ("Using standard C atomics")
    #elif defined(__PYX_DEBUG_ATOMICS)
        #warning "Using standard C atomics"
    #endif
#elif CYTHON_ATOMICS && (defined(__cplusplus) && ( \
                    (__cplusplus >= 201103L) || \
                    /*_MSC_VER 1700 is Visual Studio 2012 */ \
                    (defined(_MSC_VER) && _MSC_VER >= 1700)) && \
                    ATOMIC_INT_LOCK_FREE == 2)
    // C++11 atomics are available and ATOMIC_INT_LOCK_FREE is definitely on
    #undef __pyx_atomic_int_type
    #define __pyx_atomic_int_type std::atomic_int
    #define __pyx_atomic_ptr_type std::atomic_uintptr_t
    #define __pyx_nonatomic_ptr_type uintptr_t
    #define __pyx_atomic_incr_relaxed(value) std::atomic_fetch_add_explicit(value, 1, std::memory_order_relaxed)
    #define __pyx_atomic_incr_acq_rel(value) std::atomic_fetch_add_explicit(value, 1, std::memory_order_acq_rel)
    #define __pyx_atomic_decr_acq_rel(value) std::atomic_fetch_sub_explicit(value, 1, std::memory_order_acq_rel)
    #define __pyx_atomic_sub(value, arg) std::atomic_fetch_sub(value, arg)
    #define __pyx_atomic_int_cmp_exchange(value, expected, desired) std::atomic_compare_exchange_strong(value, expected, desired)
    #define __pyx_atomic_load(value) std::atomic_load(value)
    #define __pyx_atomic_store(value, new_value) std::atomic_store(value, new_value)
    #define __pyx_atomic_pointer_load_relaxed(value) std::atomic_load_explicit(value, std::memory_order_relaxed)
    #define __pyx_atomic_pointer_load_acquire(value) std::atomic_load_explicit(value, std::memory_order_acquire)
    #define __pyx_atomic_pointer_exchange(value, new_value) std::atomic_exchange(value, (__pyx_nonatomic_ptr_type)new_value)

    #if defined(__PYX_DEBUG_ATOMICS) && defined(_MSC_VER)
        #pragma message ("Using standard C++ atomics")
    #elif defined(__PYX_DEBUG_ATOMICS)
        #warning "Using standard C++ atomics"
    #endif
#elif CYTHON_ATOMICS && (__GNUC__ >= 5 || (__GNUC__ == 4 && \
                    (__GNUC_MINOR__ > 1 ||  \
                    (__GNUC_MINOR__ == 1 && __GNUC_PATCHLEVEL__ >= 2))))
    /* gcc >= 4.1.2 */
    #define __pyx_atomic_ptr_type void*
    #define __pyx_atomic_incr_relaxed(value) __sync_fetch_and_add(value, 1)
    #define __pyx_atomic_incr_acq_rel(value) __sync_fetch_and_add(value, 1)
    #define __pyx_atomic_decr_acq_rel(value) __sync_fetch_and_sub(value, 1)
    #define __pyx_atomic_sub(value, arg) __sync_fetch_and_sub(value, arg)
    static CYTHON_INLINE int __pyx_atomic_int_cmp_exchange(__pyx_atomic_int_type* value, __pyx_nonatomic_int_type* expected, __pyx_nonatomic_int_type desired) {
        __pyx_nonatomic_int_type old = __sync_val_compare_and_swap(value, *expected, desired);
        int result = old == *expected;
        *expected = old;
        return result;
    }
    // the legacy gcc sync builtins don't seem to have plain "load" or "store".
    #define __pyx_atomic_load(value) __sync_fetch_and_add(value, 0)
    #define __pyx_atomic_store(value, new_value) __sync_lock_test_and_set(value, new_value)
    #define __pyx_atomic_pointer_load_relaxed(value) __sync_fetch_and_add(value, 0)
    #define __pyx_atomic_pointer_load_acquire(value) __sync_fetch_and_add(value, 0)
    #define __pyx_atomic_pointer_exchange(value, new_value) __sync_lock_test_and_set(value, (__pyx_atomic_ptr_type)new_value)

    #ifdef __PYX_DEBUG_ATOMICS
        #warning "Using GNU atomics"
    #endif
#elif CYTHON_ATOMICS && defined(_MSC_VER)
    /* msvc */
    #include <intrin.h>
    #undef __pyx_atomic_int_type
    #define __pyx_atomic_int_type long
    #define __pyx_atomic_ptr_type void*
    #undef __pyx_nonatomic_int_type
    #define __pyx_nonatomic_int_type long
    #pragma intrinsic (_InterlockedExchangeAdd, _InterlockedExchange, _InterlockedCompareExchange, _InterlockedCompareExchangePointer, _InterlockedExchangePointer)
    #define __pyx_atomic_incr_relaxed(value) _InterlockedExchangeAdd(value, 1)
    #define __pyx_atomic_incr_acq_rel(value) _InterlockedExchangeAdd(value, 1)
    #define __pyx_atomic_decr_acq_rel(value) _InterlockedExchangeAdd(value, -1)
    #define __pyx_atomic_sub(value, arg) _InterlockedExchangeAdd(value, -arg)
    static CYTHON_INLINE int __pyx_atomic_int_cmp_exchange(__pyx_atomic_int_type* value, __pyx_nonatomic_int_type* expected, __pyx_nonatomic_int_type desired) {
        __pyx_nonatomic_int_type old = _InterlockedCompareExchange(value, desired, *expected);
        int result = old == *expected;
        *expected = old;
        return result;
    }
    #define __pyx_atomic_load(value) _InterlockedExchangeAdd(value, 0)
    #define __pyx_atomic_store(value, new_value) _InterlockedExchange(value, new_value)
    // Microsoft says that simple reads are guaranteed to be atomic.
    // https://learn.microsoft.com/en-gb/windows/win32/sync/interlocked-variable-access?redirectedfrom=MSDN
    // The volatile cast is what CPython does.
    #define __pyx_atomic_pointer_load_relaxed(value) *(void * volatile *)value
    // compare/exchange is probably overkill nonsense, but plain "load" intrinsics are hard to get.
    #define __pyx_atomic_pointer_load_acquire(value) _InterlockedCompareExchangePointer(value, 0, 0)
    #define __pyx_atomic_pointer_exchange(value, new_value) _InterlockedExchangePointer(value, (__pyx_atomic_ptr_type)new_value)

    #ifdef __PYX_DEBUG_ATOMICS
        #pragma message ("Using MSVC atomics")
    #endif
#else
    #undef CYTHON_ATOMICS
    #define CYTHON_ATOMICS 0

    #ifdef __PYX_DEBUG_ATOMICS
        #warning "Not using atomics"
    #endif
#endif

#if CYTHON_ATOMICS
    #define __pyx_add_acquisition_count(memview) \
             __pyx_atomic_incr_relaxed(__pyx_get_slice_count_pointer(memview))
    #define __pyx_sub_acquisition_count(memview) \
            __pyx_atomic_decr_acq_rel(__pyx_get_slice_count_pointer(memview))
#else
    #define __pyx_add_acquisition_count(memview) \
            __pyx_add_acquisition_count_locked(__pyx_get_slice_count_pointer(memview), memview->lock)
    #define __pyx_sub_acquisition_count(memview) \
            __pyx_sub_acquisition_count_locked(__pyx_get_slice_count_pointer(memview), memview->lock)
#endif


/////////////////////// CriticalSections.proto /////////////////////
//@proto_block: utility_code_proto_before_types

#if !CYTHON_COMPILING_IN_CPYTHON_FREETHREADING
#define __Pyx_PyCriticalSection void*
#define __Pyx_PyCriticalSection2 void*
#define __Pyx_PyCriticalSection_Begin1(cs, arg) (void)cs
#define __Pyx_PyCriticalSection_Begin2(cs, arg1, arg2) (void)cs
#define __Pyx_PyCriticalSection_End1(cs)
#define __Pyx_PyCriticalSection_End2(cs)
#else
#define __Pyx_PyCriticalSection PyCriticalSection
#define __Pyx_PyCriticalSection2 PyCriticalSection2
#define __Pyx_PyCriticalSection_Begin1 PyCriticalSection_Begin
#define __Pyx_PyCriticalSection_Begin2 PyCriticalSection2_Begin
#define __Pyx_PyCriticalSection_End1 PyCriticalSection_End
#define __Pyx_PyCriticalSection_End2 PyCriticalSection2_End
#endif

#if PY_VERSION_HEX < 0x030d0000 || CYTHON_COMPILING_IN_LIMITED_API
#define __Pyx_BEGIN_CRITICAL_SECTION(o) {
#define __Pyx_END_CRITICAL_SECTION() }
#else
#define __Pyx_BEGIN_CRITICAL_SECTION Py_BEGIN_CRITICAL_SECTION
#define __Pyx_END_CRITICAL_SECTION Py_END_CRITICAL_SECTION
#endif


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


////////////////////////// SharedInFreeThreading.proto //////////////////

#if CYTHON_COMPILING_IN_CPYTHON_FREETHREADING
#define __Pyx_shared_in_cpython_freethreading(x) shared(x)
#else
#define __Pyx_shared_in_cpython_freethreading(x)
#endif
