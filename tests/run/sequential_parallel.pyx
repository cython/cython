# tag: run

# This file is also included from "parallel.pyx" to run the same tests
# but with OpenMP enabled.

cimport cython.parallel
from cython.parallel import prange, threadid
from cython.view cimport array
from libc.stdlib cimport malloc, calloc, free, abort
from libc.stdio cimport puts

import os
import sys
import sysconfig

try:
    from builtins import next # Py3k
except ImportError:
    def next(it):
        return it.next()

def skip_in_freethreading(f):
    # defined in parallel.pyx
    if "OPENMP_PARALLEL" in globals():
        if sysconfig.get_config_var("Py_GIL_DISABLED"):
            return None
    return f

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

def test_prange_matches_range(int start, int stop, int step):
    """
    >>> test_prange_matches_range(0, 8, 3)
    >>> test_prange_matches_range(0, 9, 3)
    >>> test_prange_matches_range(0, 10, 3)

    >>> test_prange_matches_range(0, 10, -3)

    >>> test_prange_matches_range(0, -10, -3)
    >>> test_prange_matches_range(1, -10, -3)
    >>> test_prange_matches_range(2, -10, -3)
    >>> test_prange_matches_range(3, -10, -3)
    """
    cdef int i = -765432, range_last = -876543, prange_last = -987654
    prange_set = set()
    for i in prange(start, stop, step, nogil=True, num_threads=3):
        prange_last = i
        with gil:
            prange_set.add(i)
    range_set = set(range(start, stop, step))
    assert range_set == prange_set, "missing: %s extra %s" % (sorted(range_set-prange_set), sorted(prange_set - range_set))
    for ii in range(start, stop, step):
        range_last = ii
    if range_set:
        assert prange_last == i
        assert range_last == prange_last


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
            for y in prange(10):
                sum2 += y

    return i, j, x, y, sum1, sum2

# DISABLED, not allowed in OpenMP 3.0 (fails on Windows)
#def test_unsigned_operands():
#    """
#    >>> test_unsigned_operands()
#    10
#    """
#    cdef int i
#    cdef int start = -5
#    cdef unsigned int stop = 5
#    cdef int step = 1
#
#    cdef int steps_taken = 0
#    cdef int *steps_takenp = &steps_taken
#
#    for i in prange(start, stop, step, nogil=True):
#        steps_taken += 1
#        if steps_takenp[0] > 10:
#            abort()
#
#    return steps_taken

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

def test_closure_parallel_with_gil():
    """
    >>> test_closure_parallel_with_gil()
    45
    45
    """
    cdef int sum = 0
    temp1 = 5
    temp2 = -5

    def test_reduction():
        nonlocal sum, temp1, temp2

        cdef int i

        for i in prange(10, nogil=True):
            with gil:
                sum += temp1 + temp2 + i
                # assert abs(sum - sum) == 0

        return sum

    print test_reduction()
    print sum

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

    cdef int i
    for i in prange(10, nogil=True):
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


cdef void nogil_print(char *s) noexcept with gil:
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

    with nogil, cython.parallel.parallel(num_threads=2):
        for i in prange(10, schedule='static'):
            if i == 8:
                break
            else:
                continue

    print i

cdef int parallel_return() noexcept nogil:
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
    I am executed first
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
                    mylist.append("I am executed first")
    except Exception, e:
        print mylist[0]
        print e.args, sum

def test_parallel_exceptions_unnested():
    """
    >>> test_parallel_exceptions_unnested()
    ('I am executed first', 0)
    ('propagate me',) 0
    """
    cdef int i, sum = 0

    mylist = []

    try:
        with nogil, cython.parallel.parallel():
            try:
                for i in prange(10):
                    with gil:
                        raise Exception("propagate me")

                    sum += i
            finally:
                with gil:
                    mylist.append(("I am executed first", sum))
    except Exception, e:
        print mylist[0]
        print e.args, sum

cdef int parallel_exc_cdef() except -3:
    cdef int i, j
    for i in prange(10, nogil=True):
        for j in prange(10, num_threads=6):
            with gil:
                raise Exception("propagate me")

    return 0

cdef int parallel_exc_cdef_unnested() except -3:
    cdef int i
    for i in prange(10, nogil=True):
        with gil:
            raise Exception("propagate me")

    return 0

def test_parallel_exc_cdef():
    """
    >>> test_parallel_exc_cdef()
    Traceback (most recent call last):
        ...
    Exception: propagate me
    """
    parallel_exc_cdef_unnested()
    parallel_exc_cdef()

cpdef int parallel_exc_cpdef() except -3:
    cdef int i, j
    for i in prange(10, nogil=True):
        for j in prange(10, num_threads=6):
            with gil:
                raise Exception("propagate me")

    return 0

cpdef int parallel_exc_cpdef_unnested() except -3:
    cdef int i, j
    for i in prange(10, nogil=True):
        with gil:
            raise Exception("propagate me")

    return 0


def test_parallel_exc_cpdef():
    """
    >>> test_parallel_exc_cpdef()
    Traceback (most recent call last):
        ...
    Exception: propagate me
    """
    parallel_exc_cpdef_unnested()
    parallel_exc_cpdef()

cdef int parallel_exc_nogil_swallow() except -1:
    cdef int i, j
    for i in prange(10, nogil=True):
        try:
            for j in prange(10):
                with gil:
                    raise Exception("propagate me")
        finally:
            return i

    return 0

cdef int parallel_exc_nogil_swallow_unnested() except -1:
    cdef int i
    with nogil:
        try:
            for i in prange(10):
                with gil:
                    raise Exception("propagate me")
        finally:
            return i

    return 0

def test_parallel_exc_nogil_swallow():
    """
    >>> test_parallel_exc_nogil_swallow()
    execute me
    execute me
    """
    parallel_exc_nogil_swallow_unnested()
    print 'execute me'
    parallel_exc_nogil_swallow()
    print 'execute me'

def parallel_exc_replace():
    """
    >>> parallel_exc_replace()
    Traceback (most recent call last):
        ...
    Exception: propagate me instead
    """
    cdef int i, j
    for i in prange(10, nogil=True):
        with gil:
            try:
                for j in prange(10, nogil=True):
                    with gil:
                        raise Exception("propagate me")
            except Exception, e:
                raise Exception("propagate me instead")

    return 0


def parallel_exceptions2():
    """
    >>> parallel_exceptions2()
    Traceback (most recent call last):
       ...
    Exception: propagate me
    """
    cdef int i, j, k

    for i in prange(10, nogil=True):
        for j in prange(10):
            for k in prange(10):
                if i + j + k > 20:
                    with gil:
                        raise Exception("propagate me")
                        break
                    continue
                    return

@skip_in_freethreading  # Reassignment of 'obj'
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

def test_parallel_with_gil_continue_unnested():
    """
    >>> test_parallel_with_gil_continue_unnested()
    20
    """
    cdef int i, sum = 0

    for i in prange(10, nogil=True):
        with gil:
            if i % 2:
                continue

        sum += i

    print sum


cdef int inner_parallel_section() noexcept nogil:
    cdef int j, sum = 0
    for j in prange(10):
        sum += j
    return sum

def outer_parallel_section():
    """
    >>> outer_parallel_section()
    450
    """
    cdef int i, sum = 0
    for i in prange(10, nogil=True):
        sum += inner_parallel_section()
    return sum

cdef int nogil_cdef_except_clause() except -1 nogil:
    return 1

cdef void nogil_cdef_except_star() except * nogil:
    pass

def test_nogil_cdef_except_clause():
    """
    >>> test_nogil_cdef_except_clause()
    """
    cdef int i
    for i in prange(10, nogil=True):
        nogil_cdef_except_clause()
        nogil_cdef_except_star()

def test_num_threads_compile():
    cdef int i
    for i in prange(10, nogil=True, num_threads=2):
        pass

    with nogil, cython.parallel.parallel(num_threads=2):
        pass

    with nogil, cython.parallel.parallel(num_threads=2):
        for i in prange(10):
            pass

cdef int chunksize() noexcept nogil:
    return 3

def test_chunksize():
    """
    >>> test_chunksize()
    45
    45
    45
    """
    cdef int i, sum

    sum = 0
    for i in prange(10, nogil=True, num_threads=2, schedule='static', chunksize=chunksize()):
        sum += i
    print sum

    sum = 0
    for i in prange(10, nogil=True, num_threads=6, schedule='dynamic', chunksize=chunksize()):
        sum += i
    print sum

    sum = 0
    with nogil, cython.parallel.parallel():
        for i in prange(10, schedule='guided', chunksize=chunksize()):
            sum += i
    print sum


cdef class PrintOnDealloc(object):
    def __dealloc__(self):
        print "deallocating..."

def error():
    raise Exception("propagate me")

def test_clean_temps():
    """
    >>> test_clean_temps()
    deallocating...
    propagate me
    """
    cdef Py_ssize_t i

    try:
        for i in prange(100, nogil=True, num_threads=1):
            with gil:
                # freethreading - if we actually assigned to x this would currently be dodgy
                # but the test doesn't get that far.
                x = PrintOnDealloc() + error()
    except Exception, e:
        print e.args[0]


def test_pointer_temps(double x):
    """
    >>> test_pointer_temps(1.0)
    4.0
    """
    cdef Py_ssize_t i
    cdef double* f
    cdef double[:] arr = array(format="d", shape=(10,), itemsize=sizeof(double))
    arr[0] = 4.0
    arr[1] = 3.0

    for i in prange(10, nogil=True, num_threads=1):
        f = &arr[0]

    return f[0]


@skip_in_freethreading  #  "+=" on a Python object isn't atomic
def test_prange_in_with(int x, ctx):
    """
    >>> from contextlib import contextmanager
    >>> @contextmanager
    ... def ctx(l): yield l
    >>> test_prange_in_with(4, ctx([0]))
    6
    """
    cdef int i
    with ctx as l:
        for i in prange(x, nogil=True):
            with gil:
                l[0] += i
        return l[0]


cdef extern from *:
    """
    #ifdef _OPENMP
    #define _get_addr(_x, _idx) &_x
    #else
    #define _get_addr(_x, _idx) (&_x+_idx)
    #endif
    #define address_of_temp(store, temp, idx) store = _get_addr(temp, idx)
    #define address_of_temp2(store, ignore, temp, idx) store = _get_addr(temp, idx)

    double get_value() {
        return 1.0;
    }
    """
    void address_of_temp(...) nogil
    void address_of_temp2(...) nogil
    double get_value() except -1.0 nogil  # will generate a temp for exception checking

def test_inner_private():
    """
    Determines if a temp variable is private by taking its address in multiple threads
    and seeing if they're the same (thread private variables should have different
    addresses
    >>> test_inner_private()
    ok
    """
    cdef double* not_parallel[2]
    cdef double* inner_vals[2]
    cdef double* outer_vals[2]
    cdef Py_ssize_t n, m

    for n in range(2):
        address_of_temp(not_parallel[n], get_value(), 0)
    assert not_parallel[0] == not_parallel[1], "Addresses should be the same since they come from the same temp"

    for n in prange(2, num_threads=2, schedule='static', chunksize=1, nogil=True):
        address_of_temp(outer_vals[n], get_value(), n)
        for m in prange(1):
            # second temp just ensures different numbering
            address_of_temp2(inner_vals[n], get_value(), get_value(), n)

    inner_are_the_same = inner_vals[0] == inner_vals[1]
    outer_are_the_same = outer_vals[0] == outer_vals[1]

    assert outer_are_the_same == False, "Temporary variables in outer loop should be private"
    assert inner_are_the_same == False,  "Temporary variables in inner loop should be private"

    print('ok')

cdef void prange_exception_checked_function(int* ptr, int id) except * nogil:
    # requires the GIL after each call
    ptr[0] = id;

cdef void prange_call_exception_checked_function_impl(int* arr, int N) nogil:
    # Inside a nogil function, prange can't be sure the GIL has been released.
    # Therefore Cython must release the GIL itself.
    # Otherwise, we can experience cause lock-ups if anything inside it acquires the GIL
    # (since if any other thread has finished, it will be holding the GIL).
    #
    # An equivalent test with prange is in "sequential_parallel.pyx"
    cdef int i
    for i in prange(N, num_threads=4, schedule='static', chunksize=1):
        prange_exception_checked_function(arr+i, i)

def test_prange_call_exception_checked_function():
    """
    >>> test_prange_call_exception_checked_function()
    """

    cdef int N = 10000
    cdef int* buf = <int*>malloc(sizeof(int)*N)
    if buf == NULL:
        raise MemoryError
    try:
        # Don't release the GIL
        prange_call_exception_checked_function_impl(buf, N)

        for i in range(N):
            assert buf[i] == i
    finally:
        free(buf)

def test_prange_type_inference_1(short end):
    """
    >>> test_prange_type_inference_1(1)
    """
    for i in prange(end, nogil=True):
        pass
    assert cython.typeof(i) == "short", cython.typeof(i)

def test_prange_type_inference_2(long start, short end):
    """
    >>> test_prange_type_inference_2(-100, 5)
    """
    for i in prange(start, end, nogil=True):
        pass
    assert cython.typeof(i) == "long", cython.typeof(i)

def test_prange_type_inference_3(short start, short end, short step):
    """
    >>> test_prange_type_inference_3(-100, 5, 2)
    """
    for i in prange(start, end, step, nogil=True):
        pass
    # Addition in "step" makes it expand the type to "int"
    assert cython.typeof(i) == "int", cython.typeof(i)
