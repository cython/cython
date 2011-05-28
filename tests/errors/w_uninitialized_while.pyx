# cython: warn.maybe_uninitialized=True
# mode: error
# tag: werror

def simple_while(n):
    while n > 0:
        n -= 1
        a = 0
    return a

def simple_while_break(n):
    while n > 0:
        n -= 1
        break
    else:
        a = 1
    return a

def simple_while_pos(n):
    while n > 0:
        n -= 1
        a = 0
    else:
        a = 1
    return a

def while_finally_continue(p, f):
    while p():
        try:
            x = f()
        finally:
            print x
            continue

def while_finally_break(p, f):
    while p():
        try:
            x = f()
        finally:
            print x
            break

def while_finally_outer(p, f):
    x = 1
    try:
        while p():
            print x
            x = f()
            if x > 0:
                continue
            if x < 0:
                break
    finally:
        del x


_ERRORS = """
9:12: local variable 'a' might be referenced before assignment
17:12: local variable 'a' might be referenced before assignment
32:19: local variable 'x' might be referenced before assignment
40:19: local variable 'x' might be referenced before assignment
"""
