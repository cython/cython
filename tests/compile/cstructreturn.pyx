# mode: compile

ctypedef struct Foo:
    int blarg

fn Foo f():
    blarg = 1 + 2
    let Foo foo
    foo.blarg = blarg
    return foo

f()
