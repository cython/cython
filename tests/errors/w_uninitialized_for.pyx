# cython: warn.maybe_uninitialized=True
# mode: error
# tag: werror

def simple_for(n):
    for i in n:
        a = 1
    return a

def simple_for_break(n):
    for i in n:
        a = 1
        break
    return a

def simple_for_pos(n):
    for i in n:
        a = 1
    else:
        a = 0
    return a

def simple_target(n):
    for i in n:
        pass
    return i

def simple_target_f(n):
    for i in n:
        i *= i
    return i

def simple_for_from(n):
    for i from 0 <= i <= n:
        x = i
    else:
        return x

def for_continue(l):
    for i in l:
        if i > 0:
            continue
        x = i
    print x

def for_break(l):
    for i in l:
        if i > 0:
            break
        x = i
    print x

def for_finally_continue(f):
    for i in f:
        try:
            x = i()
        finally:
            print x
            continue

def for_finally_break(f):
    for i in f:
        try:
            x = i()
        finally:
            print x
            break

def for_finally_outer(p, f):
    x = 1
    try:
        for i in f:
            print x
            x = i()
            if x > 0:
                continue
            if x < 0:
                break
    finally:
        del x


_ERRORS = """
8:11: local variable 'a' might be referenced before assignment
14:11: local variable 'a' might be referenced before assignment
26:11: local variable 'i' might be referenced before assignment
31:11: local variable 'i' might be referenced before assignment
37:15: local variable 'x' might be referenced before assignment
44:10: local variable 'x' might be referenced before assignment
51:10: local variable 'x' might be referenced before assignment
58:18: local variable 'x' might be referenced before assignment
66:18: local variable 'x' might be referenced before assignment
"""
