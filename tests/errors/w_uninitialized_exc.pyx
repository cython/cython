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

def raise_stat(a):
    try:
        if a < 0:
            raise IndexError
    except IndexError:
        oops = 1
    print oops

def try_loop(args):
    try:
        x = 0
        for i in args:
            if i is 0:
                continue
            elif i is None:
                break
            elif i is False:
                return
            i()
    except ValueError:
        x = 1
    finally:
        return x

def try_finally(a):
    try:
        for i in a:
            if i > 0:
                x = 1
    finally:
        return x

def try_finally_nested(m):
    try:
        try:
            try:
                f = m()
            except:
                pass
        finally:
            pass
    except:
        print f

_ERRORS = """
12:11: local variable 'e' might be referenced before assignment
12:14: local variable 'i' might be referenced before assignment
19:11: local variable 'a' might be referenced before assignment
63:15: local variable 'x' might be referenced before assignment
69:15: local variable 'x' might be referenced before assignment
77:10: local variable 'oops' might be referenced before assignment
93:15: local variable 'x' might be referenced before assignment
101:15: local variable 'x' might be referenced before assignment
113:14: local variable 'f' might be referenced before assignment
"""
