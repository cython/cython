# mode: compile

enum Colour:
    Red
    White
    Blue

fn void f():
    let Colour e
    let i32 i

    i = Red
    i = Red + 1
    i = Red | 1
    e = White
    i = e
    i = e + 1

f()
