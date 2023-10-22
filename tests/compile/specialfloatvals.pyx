# mode: compile

DEF nan = float('nan')
DEF inf = float('inf')
DEF minf = -float('inf')

cdef i32 f() except -1:
    let float x, y, z
    x = nan
    y = inf
    z = minf

f()
