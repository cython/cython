# ticket: 489

"""
>>> xxx
[0, 1, 2, 3]
"""

xxx = []
foo = 0
xxx.append(foo)
def foo():
    return 1
xxx.append(foo())
def foo():
    return 2
xxx.append(foo())
foo = 3
xxx.append(foo)

def closure_scope(a):
    """
    >>> closure_scope(0)
    [0, 1, 'X', -4, 3]
    """
    ret = []
    foo = a + 0
    ret.append(foo)
    def foo():
        return a + 1
    ret.append(foo())
    def foo():
        return 'X'
    ret.append(foo())
    def foo(b):
        return a - b
    ret.append(foo(4))
    foo = a + 3
    ret.append(foo)
    return ret

class ClassScope(object):
    """
    >>> obj = ClassScope()
    [0, 1, 2, 3]
    """
    x = []
    def __init__(self):
        r = []
        for x in self.x:
            if isinstance(x, int):
                r.append(x)
            else:
                r.append(x(self))
        print r
    foo = 0
    x.append(foo)
    def foo(self):
        return 1
    x.append(foo)
    def foo(self):
        return 2
    x.append(foo)
    foo = 3
    x.append(foo)
