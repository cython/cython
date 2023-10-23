# mode: compile

ctypedef enum foo:
    FOO

fn void func():
    let foo x
    map = [FOO]
    x = map[0]

func()
