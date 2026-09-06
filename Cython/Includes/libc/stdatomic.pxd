# https://en.cppreference.com/c/header/stdatomic

from .stddef cimport wchar_t, ptrdiff_t
from .stdint cimport uintptr_t, intptr_t, intmax_t, uintmax_t

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

    ctypedef bint atomic_bool "atomic_bool"
    ctypedef char atomic_char "atomic_char"
    ctypedef signed char atomic_schar "atomic_schar"
    ctypedef unsigned char atomic_uchar "atomic_uchar"
    ctypedef short atomic_short "atomic_short"
    ctypedef unsigned short atomic_ushort "atomic_ushort"
    ctypedef int atomic_int "atomic_int"
    ctypedef unsigned int atomic_uint "atomic_uint"
    ctypedef long atomic_long "atomic_long"
    ctypedef unsigned long atomic_ulong "atomic_ulong"
    ctypedef long long atomic_llong "atomic_llong"
    ctypedef unsigned long long atomic_ullong "atomic_ullong"
    ctypedef char16_t atomic_char16_t "atomic_char16_t"
    ctypedef char32_t atomic_char32_t "atomic_char32_t"
    ctypedef wchar_t atomic_wchar_t "atomic_wchar_t"
    ctypedef char atomic_int_least8_t "atomic_int_least8_t" 
    ctypedef unsigned char atomic_uint_least8_t "atomic_uint_least8_t"
    ctypedef short atomic_int_least16_t "atomic_int_least16_t"
    ctypedef unsigned short atomic_uint_least16_t "atomic_uint_least16_t"
    ctypedef int atomic_int_least32_t "atomic_int_least32_t"
    ctypedef unsigned int atomic_uint_least32_t "atomic_uint_least32_t"
    ctypedef long long atomic_int_least64_t "atomic_int_least64_t"
    ctypedef unsigned long long atomic_uint_least64_t "atomic_uint_least64_t"
    ctypedef char atomic_int_fast8_t "atomic_int_fast8_t" 
    ctypedef unsigned char atomic_uint_fast8_t "atomic_uint_fast8_t"
    ctypedef short atomic_int_fast16_t "atomic_int_fast16_t"
    ctypedef unsigned short atomic_uint_fast16_t "atomic_uint_fast16_t"
    ctypedef int atomic_int_fast32_t "atomic_int_fast32_t" 
    ctypedef unsigned int atomic_uint_fast32_t "atomic_uint_fast32_t" 
    ctypedef long long atomic_int_fast64_t "atomic_int_fast64_t" 
    ctypedef unsigned long long atomic_uint_fast64_t "atomic_uint_fast64_t" 
    ctypedef intptr_t atomic_intptr_t "atomic_intptr_t"
    ctypedef uintptr_t atomic_uintptr_t "atomic_uintptr_t"
    ctypedef size_t atomic_size_t "atomic_size_t" 
    ctypedef ptrdiff_t atomic_ptrdiff_t "atomic_ptrdiff_t"
    ctypedef intmax_t atomic_intmax_t "atomic_intmax_t"
    ctypedef uintmax_t atomic_uintmax_t "atomic_uintmax_t" 
    ctypedef int atomic_flag "atomic_flag"

# XXX: Just a limitation but we need several templates for some 
# of these atomic APIs
ctypedef fused __A:
    atomic_bool
    atomic_char
    atomic_schar
    atomic_uchar
    atomic_short
    atomic_ushort
    atomic_int
    atomic_uint
    atomic_long
    atomic_ulong
    atomic_llong
    atomic_ullong
    atomic_char16_t
    atomic_char32_t
    atomic_wchar_t
    atomic_int_least8_t
    atomic_int_least16_t
    atomic_int_least32_t
    atomic_int_least64_t
    atomic_uint_least8_t
    atomic_uint_least16_t
    atomic_uint_least32_t
    atomic_uint_least64_t
    atomic_int_fast8_t
    atomic_int_fast16_t
    atomic_int_fast32_t
    atomic_int_fast64_t
    atomic_uint_fast8_t
    atomic_uint_fast16_t
    atomic_uint_fast32_t
    atomic_uint_fast64_t
    atomic_intptr_t
    atomic_uintptr_t
    atomic_size_t
    atomic_ptrdiff_t
    atomic_intmax_t
    atomic_uintmax_t

ctypedef fused __B:
    atomic_bool
    atomic_char
    atomic_schar
    atomic_uchar
    atomic_short
    atomic_ushort
    atomic_int
    atomic_uint
    atomic_long
    atomic_ulong
    atomic_llong
    atomic_ullong
    atomic_char16_t
    atomic_char32_t
    atomic_wchar_t
    atomic_int_least8_t
    atomic_int_least16_t
    atomic_int_least32_t
    atomic_int_least64_t
    atomic_uint_least8_t
    atomic_uint_least16_t
    atomic_uint_least32_t
    atomic_uint_least64_t
    atomic_int_fast8_t
    atomic_int_fast16_t
    atomic_int_fast32_t
    atomic_int_fast64_t
    atomic_uint_fast8_t
    atomic_uint_fast16_t
    atomic_uint_fast32_t
    atomic_uint_fast64_t
    atomic_intptr_t
    atomic_uintptr_t
    atomic_size_t
    atomic_ptrdiff_t
    atomic_intmax_t
    atomic_uintmax_t

ctypedef fused __C:
    atomic_bool
    atomic_char
    atomic_schar
    atomic_uchar
    atomic_short
    atomic_ushort
    atomic_int
    atomic_uint
    atomic_long
    atomic_ulong
    atomic_llong
    atomic_ullong
    atomic_char16_t
    atomic_char32_t
    atomic_wchar_t
    atomic_int_least8_t
    atomic_int_least16_t
    atomic_int_least32_t
    atomic_int_least64_t
    atomic_uint_least8_t
    atomic_uint_least16_t
    atomic_uint_least32_t
    atomic_uint_least64_t
    atomic_int_fast8_t
    atomic_int_fast16_t
    atomic_int_fast32_t
    atomic_int_fast64_t
    atomic_uint_fast8_t
    atomic_uint_fast16_t
    atomic_uint_fast32_t
    atomic_uint_fast64_t
    atomic_intptr_t
    atomic_uintptr_t
    atomic_size_t
    atomic_ptrdiff_t
    atomic_intmax_t
    atomic_uintmax_t


# NOTE: atomic_fetch_key and atomic_fetch_key_explicit not implemented yet...
# On windows use /std:c11 and /experimental:c11atomics compiler flags
cdef extern from "<stdatomic.h>" nogil:
    __A kill_dependency(__A obj)

    void atomic_init(volatile __A* obj, __C value)

    void atomic_thread_fence(memory_order order)
    void atomic_signal_fence(memory_order order)
    bint atomic_is_lock_free(volatile const __A* obj)
    void atomic_store(volatile __A* obj, __C desired)
    void atomic_store_explicit(volatile __A* obj, __C desired, memory_order order)
    __A atomic_load(volatile const __A* obj)
    __A atomic_load_explicit(volatile const __A* obj, memory_order order)
    __A atomic_exchange(volatile __A* obj, __C desired)
    __A atomic_exchange_explicit(volatile __A* obj, __C desired, memory_order order)
    bint atomic_compare_exchange_strong(volatile __A* obj, __B expected, __C desired)
    bint atomic_compare_exchange_strong_explicit(volatile __A* obj, __B expected,
    __C desired, memory_order success, memory_order failure)
    bint atomic_compare_exchange_weak(volatile __A* obj, __B expected, __C desired)
    bint atomic_compare_exchange_weak_explicit(volatile __A* obj, __B expected, __C desired, memory_order success, memory_order failure)
    bint atomic_flag_test_and_set(volatile atomic_flag* obj)
    bint atomic_flag_test_and_set_explicit(volatile atomic_flag* obj, memory_order order)
    void atomic_flag_clear(volatile atomic_flag* obj)
    void atomic_flag_clear_explicit(volatile atomic_flag* obj, memory_order order)

