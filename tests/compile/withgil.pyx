# mode: compile

fn void f() with gil:
    x = 42

fn i32 g(void* x) with gil:
    pass

f()
g("test")
