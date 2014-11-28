# mode: run
# ticket: 466
# extension to T409

cimport cython

def simple_parallel_typed():
    """
    >>> simple_parallel_typed()
    (1, 2, [1, 2], [1, 2])
    """
    cdef int a,c
    a, c = d = e = [1,2]
    return a, c, d, e

def simple_parallel_int_mix():
    """
    >>> simple_parallel_int_mix()
    (1, 2, 1, 2, 1, 2, [1, 2], [1, 2])
    """
    cdef int ai,bi
    cdef long al,bl
    cdef object ao, bo
    ai, bi = al, bl = ao, bo = c = d = [1,2]
    return ao, bo, ai, bi, al, bl, c, d

def simple_parallel_int_mix_recursive():
    """
    >>> simple_parallel_int_mix_recursive()
    (1, 2, 3, 1, [2, 3], 1, 2, 3, 1, 2, 3, [1, [2, 3]], [1, [2, 3]])
    """
    cdef int ai, bi, ci
    cdef long al, bl, cl
    cdef object ao, bo, co
    cdef object xo, yo
    ai, [bi, ci] = al, [bl, cl] = xo, yo = ao, [bo, co] = c = d = [1, [2, 3]]
    return ao, bo, co, xo, yo, ai, bi, ci, al, bl, cl, c, d

cdef int called = 0

cdef char* get_string():
    global called
    called += 1
    return "abcdefg"

def non_simple_rhs():
    """
    >>> non_simple_rhs()
    1
    """
    cdef char *a, *b
    cdef int orig_called = called
    a = b = <char*>get_string()
    assert a is b
    return called - orig_called

from libc.stdlib cimport malloc, free

def non_simple_rhs_malloc():
    """
    >>> non_simple_rhs_malloc()
    """
    cdef char *a, *b, **c

    c = &b
    c[0] = a = <char*>malloc(2)
    a[0] = c'X'
    b[1] = c'\0'

    # copy from different pointers to make sure they all point to the
    # same memory
    cdef char[2] x
    x[0] = b[0]
    x[1] = a[1]

    # clean up
    free(a)
    if b is not a: # shouldn't happen
        free(b)

    # check copied values
    assert x[0] == c'X'
    assert x[1] == c'\0'

@cython.test_assert_path_exists(
    '//CascadedAssignmentNode',
    '//CascadedAssignmentNode//CoerceToTempNode',
    '//CascadedAssignmentNode//CoerceToTempNode[@type.is_ptr]')
def assign_carray():
    """
    assign_carray()
    (1, 2, 3)
    """
    cdef int *b, *c
    cdef int[3] a
    a[0] = 1
    a[1] = 2
    a[2] = 3

    b = c = a+1
    assert b[0] == 2
    assert c[1] == 3
    return a[0], b[0], c[1]


def pyobject_from_cvalue(table, key):
    """
    >>> table = {'X':0, 'Y':1}
    >>> pyobject_from_cvalue(table, 'Z')
    2
    >>> pyobject_from_cvalue(table, 'X')
    0
    """
    cdef int num
    num = table.get(key, -1)
    if num < 0:
        num = table[key] = len(table)
    return num
