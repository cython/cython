# mode: compile

enum E:
    Spam, Eggs

fn E f() except Spam:
    return Eggs

f()
