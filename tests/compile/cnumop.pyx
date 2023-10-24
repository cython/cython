# mode: compile

def f():
    let i32 int1, int2 = 0, int3 = 1
    let i8 char1 = 0
    let i64 long1, long2 = 0
    let f32 float1, float2 = 0
    let f64 double1
    int1 = int2 * int3
    int1 = int2 / int3
    long1 = long2 * char1
    float1 = int1 * float2
    double1 = float1 * int2

f()
