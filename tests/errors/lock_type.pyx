# mode: error

cimport cython

cdef takes_a_lock(cython.lock_type l):
    pass

cdef cython.lock_type uncopyable():
    cdef cython.lock_type l
    cdef object o
    takes_a_lock(l)
    l2 = l
    o = l
    return l

def no_yield():
    cdef cython.lock_type l
    with l:
        yield  # banned due to very high possibility of deadlock


cdef void misuse_the_gil() noexcept nogil:
    cdef cython.lock_type l
    with l:
        with gil:
            pass

_ERRORS = """
11:17: cython.lock_type cannot be copied
12:9: cython.lock_type cannot be copied
13:8: Cannot convert 'cython.lock_type' to Python object
14:11: cython.lock_type cannot be copied
18:9: Cannot use a 'with' statement with a 'cython.lock_type' in a generator. If you really want to do this (and you are confident that there are no deadlocks) then use try-finally.
"""
