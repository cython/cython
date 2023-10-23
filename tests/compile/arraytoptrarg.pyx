# mode: compile

fn void f1(i8 *argv[]):
    f2(argv)

fn void f2(i8 *argv[]):
    pass

f1(NULL)
