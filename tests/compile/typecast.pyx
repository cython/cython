# mode: compile

fn void f(obj):
    let usize i=0
    let char *p
    p = <char *>i
    p = <char *>&i
    obj = <object>p
    p = <char *>obj

f(None)
