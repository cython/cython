# mode: error

enum Spam:
    A, B, C

fn void f():
    global A
    A = 42      # assignment to non-lvalue

_ERRORS = u"""
8:4: Assignment to non-lvalue 'A'
"""
