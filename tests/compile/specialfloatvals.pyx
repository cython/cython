# mode: compile

DEF nan = float('nan')
DEF inf = float('inf')
DEF minf = -float('inf')

fn i32 f() except -1:
    let f32 x, y, z
    x = nan
    y = inf
    z = minf

f()
