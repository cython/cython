# https://en.cppreference.com/c/header/stdatomic

from .stddef cimport wchar_t, ptrdiff_t
from .stdint cimport uintptr_t, intptr_t, intmax_t, uintmax_t

cimport cython

cdef extern from "<stdatomic.h>" nogil:
    ctypedef short char16_t
    ctypedef int char32_t

    ctypedef enum memory_order:
        memory_order_relaxed,
        memory_order_consume,
        memory_order_acquire,
        memory_order_release,
        memory_order_acq_rel,
        memory_order_seq_cst

    int ATOMIC_BOOL_LOCK_FREE
    int ATOMIC_CHAR_LOCK_FREE
    int ATOMIC_CHAR16_T_LOCK_FREE
    int ATOMIC_CHAR32_T_LOCK_FREE
    int ATOMIC_WCHAR_T_LOCK_FREE
    int ATOMIC_SHORT_LOCK_FREE
    int ATOMIC_INT_LOCK_FREE
    int ATOMIC_LONG_LOCK_FREE
    int ATOMIC_LLONG_LOCK_FREE
    int ATOMIC_POINTER_LOCK_FREE

    ctypedef bint atomic_bool
    ctypedef char atomic_char
    ctypedef signed char atomic_schar
    ctypedef unsigned char atomic_uchar
    ctypedef short atomic_short
    ctypedef unsigned short atomic_ushort
    ctypedef int atomic_int
    ctypedef unsigned int atomic_uint
    ctypedef long atomic_long
    ctypedef unsigned long atomic_ulong
    ctypedef long long atomic_llong
    ctypedef unsigned long long atomic_ullong
    ctypedef char16_t atomic_char16_t
    ctypedef char32_t atomic_char32_t
    ctypedef wchar_t atomic_wchar_t
    ctypedef char atomic_int_least8_t 
    ctypedef unsigned char atomic_uint_least8_t
    ctypedef short atomic_int_least16_t
    ctypedef unsigned short atomic_uint_least16_t
    ctypedef int atomic_int_least32_t
    ctypedef unsigned int atomic_uint_least32_t
    ctypedef long long atomic_int_least64_t
    ctypedef unsigned long long atomic_uint_least64_t
    ctypedef char atomic_int_fast8_t 
    ctypedef unsigned char atomic_uint_fast8_t
    ctypedef short atomic_int_fast16_t
    ctypedef unsigned short atomic_uint_fast16_t
    ctypedef int atomic_int_fast32_t 
    ctypedef unsigned int atomic_uint_fast32_t 
    ctypedef long long atomic_int_fast64_t 
    ctypedef unsigned long long atomic_uint_fast64_t 
    ctypedef intptr_t atomic_intptr_t
    ctypedef uintptr_t atomic_uintptr_t
    ctypedef size_t atomic_size_t 
    ctypedef ptrdiff_t atomic_ptrdiff_t
    ctypedef intmax_t atomic_intmax_t
    ctypedef uintmax_t atomic_uintmax_t 
    ctypedef int atomic_flag

# NOTE: atomic_fetch_key and atomic_fetch_key_explicit not implemented yet...
# On windows use /std:c11 and /experimental:c11atomics compiler flags
cdef extern from "<stdatomic.h>" nogil:
    T kill_dependency[cython.implicit_param[T]](T obj)

    void atomic_init[cython.implicit_param[T]](volatile T* obj, T value)

    void atomic_thread_fence(memory_order order)
    void atomic_signal_fence(memory_order order)
    bint atomic_is_lock_free[cython.implicit_param[T]](volatile const T* obj)
    void atomic_store[cython.implicit_param[T], cython.implicit_param[U]](
        volatile T* obj, U desired)
    void atomic_store_explicit[cython.implicit_param[T], cython.implicit_param[U]](
        volatile T* obj, U desired, memory_order order)
    T atomic_load[cython.implicit_param[T]](volatile const T* obj)
    T atomic_load_explicit[cython.implicit_param[T]](volatile const T* obj, memory_order order)
    T atomic_exchange[cython.implicit_param[T], cython.implicit_param[U]](
        volatile T* obj, U desired)
    T atomic_exchange_explicit[cython.implicit_param[T], cython.implicit_param[U]](
        volatile T* obj, U desired, memory_order order)
    bint atomic_compare_exchange_strong[
        cython.implicit_param[T], cython.implicit_param[U], cython.implicit_param[V]](
            volatile T* obj, U* expected, V desired)
    bint atomic_compare_exchange_strong_explicit[
        cython.implicit_param[T], cython.implicit_param[U], cython.implicit_param[V]](
            volatile T* obj, U* expected, V desired, memory_order success, memory_order failure)
    bint atomic_compare_exchange_weak[
        cython.implicit_param[T], cython.implicit_param[U], cython.implicit_param[V]](
            volatile T* obj, U* expected, V desired)
    bint atomic_compare_exchange_weak_explicit[
        cython.implicit_param[T], cython.implicit_param[U], cython.implicit_param[V]](
            volatile T* obj, T* expected, U desired, memory_order success, memory_order failure)

    T atomic_fetch_add[cython.implicit_param[T], cython.implicit_param[U]]( volatile T* obj, U arg )
    T atomic_fetch_add_explicit[cython.implicit_param[T], cython.implicit_param[U]](
        volatile T* obj, U arg, memory_order order )
    T atomic_fetch_sub[cython.implicit_param[T], cython.implicit_param[U]]( volatile T* obj, U arg )
    T atomic_fetch_sub_explicit[cython.implicit_param[T], cython.implicit_param[U]](
        volatile T* obj, U arg, memory_order order )
    T atomic_fetch_or[cython.implicit_param[T], cython.implicit_param[U]]( volatile T* obj, U arg )
    T atomic_fetch_or_explicit[cython.implicit_param[T], cython.implicit_param[U]](
        volatile T* obj, U arg, memory_order order )
    T atomic_fetch_xor[cython.implicit_param[T], cython.implicit_param[U]]( volatile T* obj, U arg )
    T atomic_fetch_xor_explicit[cython.implicit_param[T], cython.implicit_param[U]](
        volatile T* obj, U arg, memory_order order )
    
    T atomic_fetch_and[cython.implicit_param[T], cython.implicit_param[U]]( volatile T* obj, U arg )
    T atomic_fetch_and_explicit[cython.implicit_param[T], cython.implicit_param[U]](
        volatile T* obj, U arg, memory_order order )

    bint atomic_flag_test_and_set(volatile atomic_flag* obj)
    bint atomic_flag_test_and_set_explicit(volatile atomic_flag* obj, memory_order order)
    void atomic_flag_clear(volatile atomic_flag* obj)
    void atomic_flag_clear_explicit(volatile atomic_flag* obj, memory_order order)
