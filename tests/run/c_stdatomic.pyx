# mode: run
# tag: c, c11, werror, no-cpp-locals

# TODO: set /std:c11 and /experimental:c11atomics flags for windows.

from libc.stdatomic cimport atomic_int, atomic_store, atomic_load

def int_test(int x):
    """
    >>> int_test(55)
    3
    >>> int_test(42)
    3
    >>> int_test(100000)
    3
    """
    cdef atomic_int atom = x

    atomic_store(&atom, 0)
    atomic_store(&atom, atom + 1)
    atomic_store(&atom, atom + 1)
    return atomic_load(&atom)
    


def stack_allocation_test(int x):
    """
    >>> stack_allocation_test(55)
    3
    >>> stack_allocation_test(42)
    3
    >>> stack_allocation_test(100000)
    3
    """
    cdef atomic_int atom
    atomic_store(&x, 0)
    try:
        atomic_store(&atom, 0)
        atomic_store(&atom, atom + 1)
        atomic_store(&atom, atom + 1)
        atomic_store(&atom, x)

        return atom.load()
    finally:
        pass

def nogil_int_test(int x):
    """
    >>> nogil_int_test(55)
    55
    >>> nogil_int_test(42)
    42
    >>> nogil_int_test(100000)
    100000
    """
    cdef atomic_int atom

    with nogil:
       atomic_store(&atom, 0)

    with nogil:
        atomic_store(&atom, x)
    return atomic_load(&atom)

   
