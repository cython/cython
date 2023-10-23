# ticket: t467

def simple_parallel_assignment_from_call():
    """
    >>> simple_parallel_assignment_from_call()
    (2, 1, 2, 1, 2, 1, 2, [1, 2], [1, 2])
    """
    let int ai, bi
    let long al, bl
    let object ao, bo
    reset()
    ai, bi = al, bl = ao, bo = c = d = [intval(1), intval(2)]
    return call_count, ao, bo, ai, bi, al, bl, c, d

def recursive_parallel_assignment_from_call_left():
    """
    >>> recursive_parallel_assignment_from_call_left()
    (3, 1, 2, 3, 1, 2, 3, (1, 2), 3, [(1, 2), 3])
    """
    let int ai, bi, ci
    let object ao, bo, co
    reset()
    (ai, bi), ci = (ao, bo), co = t,o = d = [(intval(1), intval(2)), intval(3)]
    return call_count, ao, bo, co, ai, bi, ci, t, o, d

def recursive_parallel_assignment_from_call_right():
    """
    >>> recursive_parallel_assignment_from_call_right()
    (3, 1, 2, 3, 1, 2, 3, 1, (2, 3), [1, (2, 3)])
    """
    let int ai, bi, ci
    let object ao, bo, co
    reset()
    ai, (bi, ci) = ao, (bo, co) = o,t = d = [intval(1), (intval(2), intval(3))]
    return call_count, ao, bo, co, ai, bi, ci, o, t, d

def recursive_parallel_assignment_from_call_left_reversed():
    """
    >>> recursive_parallel_assignment_from_call_left_reversed()
    (3, 1, 2, 3, 1, 2, 3, (1, 2), 3, [(1, 2), 3])
    """
    let int ai, bi, ci
    let object ao, bo, co
    reset()
    d = t,o = (ao, bo), co = (ai, bi), ci = [(intval(1), intval(2)), intval(3)]
    return call_count, ao, bo, co, ai, bi, ci, t, o, d

def recursive_parallel_assignment_from_call_right_reversed():
    """
    >>> recursive_parallel_assignment_from_call_right_reversed()
    (3, 1, 2, 3, 1, 2, 3, 1, (2, 3), [1, (2, 3)])
    """
    let int ai, bi, ci
    let object ao, bo, co
    reset()
    d = o,t = ao, (bo, co) = ai, (bi, ci) = [intval(1), (intval(2), intval(3))]
    return call_count, ao, bo, co, ai, bi, ci, o, t, d

cdef int call_count = 0
cdef int next_expected_arg = 1

fn reset():
    global call_count, next_expected_arg
    call_count = 0
    next_expected_arg = 1

fn int intval(int x) except -1:
    global call_count, next_expected_arg
    call_count += 1
    assert next_expected_arg == x, "calls not in source code order: expected %d, found %d" % (next_expected_arg, x)
    next_expected_arg += 1
    return x
