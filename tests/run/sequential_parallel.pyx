# tag: run

cimport cython.parallel
from cython.parallel import prange, threadid
from libc.stdlib cimport malloc, calloc, free, abort
from libc.stdio cimport puts

import sys

try:
    from builtins import next # Py3k
except ImportError:
    def next(it):
        return it.next()

#@cython.test_assert_path_exists(
#    "//ParallelWithBlockNode//ParallelRangeNode[@schedule = 'dynamic']",
#    "//GILStatNode[@state = 'nogil]//ParallelRangeNode")
def test_prange():
    """
    >>> test_prange()
    (9, 9, 45, 45)
    """
    cdef Py_ssize_t i, j, sum1 = 0, sum2 = 0

    with nogil, cython.parallel.parallel():
        for i in prange(10, schedule='dynamic'):
            sum1 += i

    for j in prange(10, nogil=True):
        sum2 += j

    return i, j, sum1, sum2

def test_descending_prange():
    """
    >>> test_descending_prange()
    5
    """
    cdef int i, start = 5, stop = -5, step = -2
    cdef int sum = 0

    for i in prange(start, stop, step, nogil=True):
        sum += i

    return sum

def test_propagation():
    """
    >>> test_propagation()
    (9, 9, 9, 9, 450, 450)
    """
    cdef int i = 0, j = 0, x = 0, y = 0
    cdef int sum1 = 0, sum2 = 0

    for i in prange(10, nogil=True):
        for j in prange(10):
            sum1 += i

    with nogil, cython.parallel.parallel():
        for x in prange(10):
            with cython.parallel.parallel():
                for y in prange(10):
                    sum2 += y

    return i, j, x, y, sum1, sum2

def test_unsigned_operands():
    """
    >>> test_unsigned_operands()
    10
    """
    cdef int i
    cdef int start = -5
    cdef unsigned int stop = 5
    cdef int step = 1

    cdef int steps_taken = 0

    for i in prange(start, stop, step, nogil=True):
        steps_taken += 1
        if steps_taken > 10:
            abort()

    return steps_taken

def test_reassign_start_stop_step():
    """
    >>> test_reassign_start_stop_step()
    20
    """
    cdef int start = 0, stop = 10, step = 2
    cdef int i
    cdef int sum = 0

    for i in prange(start, stop, step, nogil=True):
        start = -2
        stop = 2
        step = 0

        sum += i

    return sum

def test_closure_parallel_privates():
    """
    >>> test_closure_parallel_privates()
    9 9
    45 45
    0 0 9 9
    """
    cdef int x

    def test_target():
        nonlocal x
        for x in prange(10, nogil=True):
            pass
        return x

    print test_target(), x

    def test_reduction():
        nonlocal x
        cdef int i

        x = 0
        for i in prange(10, nogil=True):
            x += i

        return x

    print test_reduction(), x

    def test_generator():
        nonlocal x
        cdef int i

        x = 0
        yield x
        x = 2

        for i in prange(10, nogil=True):
            x = i

        yield x

    g = test_generator()
    print next(g), x, next(g), x

def test_pure_mode():
    """
    >>> test_pure_mode()
    0
    1
    2
    3
    4
    4
    3
    2
    1
    0
    0
    """
    import Cython.Shadow
    pure_parallel = sys.modules['cython.parallel']

    for i in pure_parallel.prange(5):
        print i

    for i in pure_parallel.prange(4, -1, -1, schedule='dynamic', nogil=True):
        print i

    with pure_parallel.parallel():
        print pure_parallel.threadid()

cdef extern from "types.h":
    ctypedef short actually_long_t
    ctypedef long actually_short_t

ctypedef int myint_t

def test_nan_init():
    """
    >>> test_nan_init()
    """
    cdef int mybool = 0
    cdef int err = 0
    cdef int *errp = &err

    cdef signed char a1 = 10
    cdef unsigned char a2 = 10
    cdef short b1 = 10
    cdef unsigned short b2 = 10
    cdef int c1 = 10
    cdef unsigned int c2 = 10
    cdef long d1 = 10
    cdef unsigned long d2 = 10
    cdef long long e1 = 10
    cdef unsigned long long e2 = 10
    
    cdef actually_long_t miss1 = 10
    cdef actually_short_t miss2 = 10
    cdef myint_t typedef1 = 10

    cdef float f = 10.0
    cdef double g = 10.0
    cdef long double h = 10.0

    cdef void *p = <void *> 10

    with nogil, cython.parallel.parallel():
        # First, trick the error checking to make it believe these variables
        # are initialized after this if

        if mybool: # mybool is always false!
            a1 = a2 = b1 = b2 = c1 = c2 = d1 = d2 = e1 = e2 = 0
            f = g = h = 0.0
            p = NULL
            miss1 = miss2 = typedef1 = 0

        if (a1 == 10 or a2 == 10 or
            b1 == 10 or b2 == 10 or
            c1 == 10 or c2 == 10 or
            d1 == 10 or d2 == 10 or
            e1 == 10 or e2 == 10 or
            f == 10.0 or g == 10.0 or h == 10.0 or
            p == <void *> 10 or miss1 == 10 or miss2 == 10
            or typedef1 == 10):
            errp[0] = 1

    if err:
        raise Exception("One of the values was not initialized to a maximum "
                        "or NaN value")

    c1 = 20
    with nogil, cython.parallel.parallel():
        c1 = 16

    assert c1 == 20, c1

cdef void nogil_print(char *s) with gil:
    print s.decode('ascii')

def test_else_clause():
    """
    >>> test_else_clause()
    else clause executed
    """
    cdef int i

    for i in prange(5, nogil=True):
        pass
    else:
        nogil_print('else clause executed')

def test_prange_break():
    """
    >>> test_prange_break()
    """
    cdef int i

    for i in prange(10, nogil=True):
        if i == 8:
            break
    else:
        nogil_print('else clause executed')

def test_prange_continue():
    """
    >>> test_prange_continue()
    else clause executed
    0 0
    1 0
    2 2
    3 0
    4 4
    5 0
    6 6
    7 0
    8 8
    9 0
    """
    cdef int i
    cdef int *p = <int *> calloc(10, sizeof(int))

    if p == NULL:
        raise MemoryError

    for i in prange(10, nogil=True):
        if i % 2 != 0:
            continue

        p[i] = i
    else:
        nogil_print('else clause executed')

    for i in range(10):
       print i, p[i]

    free(p)

def test_nested_break_continue():
    """
    >>> test_nested_break_continue()
    6 7 6 7
    8
    """
    cdef int i, j, result1 = 0, result2 = 0

    for i in prange(10, nogil=True, num_threads=2, schedule='static'):
        for j in prange(10, num_threads=2, schedule='static'):
            if i == 6 and j == 7:
                result1 = i
                result2 = j
                break
        else:
            continue

        break

    print i, j, result1, result2

    with nogil, cython.parallel.parallel():
        for i in prange(10, num_threads=2, schedule='static'):
            with cython.parallel.parallel():
                if i == 8:
                    break
                else:
                    continue

    print i

cdef int parallel_return() nogil:
    cdef int i

    for i in prange(10):
        if i == 8:
            return i
    else:
        return 1

    return 2

def test_return():
    """
    >>> test_return()
    8
    """
    print parallel_return()

def test_parallel_exceptions():
    """
    >>> test_parallel_exceptions()
    ('I am executed first', 0)
    ('propagate me',) 0
    """
    cdef int i, j, sum = 0

    mylist = []

    try:
        for i in prange(10, nogil=True):
            try:
                for j in prange(10):
                    with gil:
                        raise Exception("propagate me")

                    sum += i * j
                sum += i
            finally:
                with gil:
                    mylist.append(("I am executed first", sum))
    except Exception, e:
        print mylist[0]
        print e.args, sum

def test_parallel_with_gil_return():
    """
    >>> test_parallel_with_gil_return()
    True
    45
    """
    cdef int i, sum = 0

    for i in prange(10, nogil=True):
        with gil:
            obj = i
            sum += obj

    print obj in range(10)

    with nogil, cython.parallel.parallel():
        with gil:
            return sum

def test_parallel_with_gil_continue():
    """
    >>> test_parallel_with_gil_continue()
    20
    """
    cdef int i, sum = 0

    for i in prange(10, nogil=True):
        with cython.parallel.parallel():
            with gil:
                if i % 2:
                    continue

        sum += i

    print sum
