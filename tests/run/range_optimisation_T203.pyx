__doc__ = u"""
>>> for_from_range(5, 10)
range(5)
at 0
at 1
at 2
at 3
at 4
range(5, 10)
at 5
at 6
at 7
at 8
at 9
range(5, 10, 2)
at 5
at 7
at 9
9
>>> for_from_range(-5, -10)
range(-5)
range(-5, -10)
range(-5, -10, 2)
100
>>> for_from_bound_reassignment(5, 1)
at 0
at 1
at 2
at 3
at 4
5
>>> for_from_step_reassignment(15, 5, 2)
at 0
at 5
at 10
15
>>> for_from_target_reassignment(10, 2)
at 0
at 1
at 3
at 7
15
>>> for_from_py_target_reassignment(10, 2)
at 0
at 1
at 3
at 7
15
>>> for_in_target_reassignment(10, 2)
at 0
at 1
at 2
at 3
at 4
at 5
at 6
at 7
at 8
at 9
18
>>> test_func(5)
get_bound(5)
at 0
at 1
at 2
at 3
at 4
5
"""
cdef int get_bound(int m):
    print "get_bound(%s)"%m
    return m

def for_from_range(a, b):
    cdef int i = 100
    print "range(%s)" % a
    for i in range(a):
        print "at", i
    print "range(%s, %s)" % (a, b)
    for i in range(a, b):
        print "at", i
    print "range(%s, %s, %s)" % (a, b, 2)
    for i in range(a, b, 2):
        print "at", i
    return i

def for_from_bound_reassignment(int bound, int fake_bound):
    cdef int i = 100
    for i from 0 <= i < bound:
        print "at", i
        bound = fake_bound
    return i

def for_from_step_reassignment(int bound, int step, int fake_step):
    cdef int i = 100
    for i from 0 <= i < bound by step:
        print "at", i
        step = fake_step
    return i

def for_from_target_reassignment(int bound, int factor):
    cdef int i = 100
    for i from 0 <= i < bound:
        print "at", i
        i *= factor
    return i

def for_from_py_target_reassignment(int bound, int factor):
    cdef object i
    for i from 0 <= i < bound:
        print "at", i
        i *= factor
    return i

def for_in_target_reassignment(int bound, int factor):
    cdef int i = 100
    for i in range(bound):
        print "at", i
        i *= factor
    return i

def test_func(int n):
    cdef int i = 100
    for i from 0 <= i < get_bound(n):
        print "at", i
    return i
