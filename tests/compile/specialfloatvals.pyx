# mode: compile

DEF nan = float('nan')
DEF inf = float('inf')
DEF minf = -float('inf')

cdef int f() except -1:
    cdef float x, y, z
    x = nan
    y = inf
    z = minf

f()
