# mode: run
# tag: c, c11, werror, no-cpp

from libc.stdatomic cimport (atomic_int, atomic_store, atomic_load,
    atomic_fetch_add, atomic_fetch_add_explicit,
    atomic_compare_exchange_strong, atomic_compare_exchange_strong_explicit,
    memory_order_acq_rel, memory_order_seq_cst)

def int_test(int x):
    """
    >>> int_test(55)
    56
    >>> int_test(42)
    43
    >>> int_test(100000)
    100001
    """
    cdef atomic_int atom = x
    atomic_fetch_add(&atom, 1)
    # Note that this returns the previous value
    return atomic_fetch_add_explicit(&atom, 1, memory_order_acq_rel)


def nogil_int_test():
    """
    >>> nogil_int_test()
    55
    """
    cdef atomic_int atom
    cdef int expected1 = 1

    with nogil:
        atomic_store(&atom, 0)
        assert not atomic_compare_exchange_strong(
            &atom, &expected1, 200)
        assert expected1 == 0
        assert atomic_compare_exchange_strong_explicit(
            &atom, &expected1, 55, memory_order_seq_cst, memory_order_seq_cst)
    return atomic_load(&atom)
