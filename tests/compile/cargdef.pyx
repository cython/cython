# mode: compile

def f(obj, i32 i, f64 f, i8 *s1, i8 s2[]):
    pass

fn g(obj, i32 i, f64 f, i8 *s1, i8 s2[]):
    pass

fn do_g(object (*func)(object, i32, f64, i8*, i8*)):
    return func(1, 2, 3.14159, "a", "b")

do_g(&g)
