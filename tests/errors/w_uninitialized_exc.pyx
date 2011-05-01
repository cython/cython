# cython: warn.maybe_uninitialized=True
# mode: error
# tag: werror

def exc_target():
    try:
        {}['foo']
    except KeyError, e:
        pass
    except IndexError, i:
        pass
    return e, i

def exc_body():
    try:
        a = 1
    except Exception:
        pass
    return a

def exc_else_pos():
    try:
        pass
    except Exception, e:
        pass
    else:
        e = 1
    return e

def exc_body_pos(d):
    try:
        a = d['foo']
    except KeyError:
        a = None
    return a

def exc_pos():
    try:
        a = 1
    except Exception:
        a = 1
    return a

def exc_finally():
    try:
        a = 1
    finally:
        pass
    return a

def exc_finally2():
    try:
        pass
    finally:
        a = 1
    return a


def exc_assmt_except(a):
    try:
        x = a
    except:
        return x

def exc_assmt_finaly(a):
    try:
        x = a
    except:
        return x

_ERRORS = """
12:12: local variable 'e' might be referenced before assignment
12:15: local variable 'i' might be referenced before assignment
19:12: local variable 'a' might be referenced before assignment
63:16: local variable 'x' might be referenced before assignment
69:16: local variable 'x' might be referenced before assignment
"""
