"""
>>> range_loop_indices()
** Calculating step **
(9, 9, 8, 1, 2)
>>> from_loop_indices()
** Calculating step **
(10, 10, 0)
"""

cdef int get_step():
    """
    This should only be called once, when used in range().
    """
    print u"** Calculating step **"
    return 2

def range_loop_indices():
    """
    Optimized integer for loops using range() should follow Python behavior,
    and leave the index variable with the last value of the range.
    """
    cdef int i, j, k=0, l=10, m=10
    for i in range(10): pass
    for j in range(2,10): pass
    for k in range(0,10,get_step()): pass
    for l in range(10,0,-1): pass
    for m in range(10,0,-2): pass
    return i, j, k, l, m

def from_loop_indices():
    """
    for-from-loops should follow C behavior, and leave the index variable
    incremented one step after the last iteration.
    """
    cdef int i, j, k
    for i from 0 <= i < 5+5 by get_step(): pass
    for j from 0 <= j < 10: pass
    for k from 10 > k > 0: pass
    return i, j, k
