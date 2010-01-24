
def simple_parallel_assignment_from_call():
    """
    >>> simple_parallel_assignment_from_call()
    (2, 1, 2, 1, 2, 1, 2, [1, 2], [1, 2])
    """
    cdef int ai, bi
    cdef long al, bl
    cdef object ao, bo
    cdef int side_effect_count = call_count
    ai, bi = al, bl = ao, bo = c = d = [intval(1), intval(2)]
    side_effect_count = call_count - side_effect_count
    return side_effect_count, ao, bo, ai, bi, al, bl, c, d

def recursive_parallel_assignment_from_call():
    """
    >>> recursive_parallel_assignment_from_call()
    (3, 1, 2, 3, 1, 2, 3, (1, 2), 3, [(1, 2), 3])
    """
    cdef int ai, bi, ci
    cdef object ao, bo, co
    cdef int side_effect_count = call_count
    (ai, bi), ci = (ao, bo), co = t,o = d = [(intval(1), intval(2)), intval(3)]
    side_effect_count = call_count - side_effect_count
    return side_effect_count, ao, bo, co, ai, bi, ci, t, o, d

cdef int call_count = 0

cdef int intval(int x):
    global call_count
    call_count += 1
    return x
