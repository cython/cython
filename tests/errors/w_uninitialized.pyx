# cython: warn.maybe_uninitialized=True
# mode: error
# tag: werror

def simple():
    print a
    a = 0

def simple2(arg):
    if arg > 0:
        a = 1
    return a

def simple_pos(arg):
    if arg > 0:
        a = 1
    else:
        a = 0
    return a

def ifelif(c1, c2):
    if c1 == 1:
        if c2:
            a = 1
        else:
            a = 2
    elif c1 == 2:
        a = 3
    return a

def nowimpossible(a):
    if a:
        b = 1
    if a:
        print b

def fromclosure():
    def bar():
        print a
    a = 1
    return bar

# Should work ok in both py2 and py3
def list_comp(a):
    return [i for i in a]

def set_comp(a):
    return set(i for i in a)

def dict_comp(a):
    return {i: j for i, j in a}

# args and kwargs
def generic_args_call(*args, **kwargs):
    return args, kwargs

def cascaded(x):
    print a, b
    a = b = x

def from_import():
    print bar
    from foo import bar

def regular_import():
    print foo
    import foo

def raise_stat():
    try:
        raise exc, msg
    except:
        pass
    exc = ValueError
    msg = 'dummy'

def defnode_decorator():
    @decorator
    def foo():
        pass
    def decorator():
        pass

def defnode_default():
    def foo(arg=default()):
        pass
    def default():
        pass

def class_bases():
    class foo(bar):
        pass
    class bar(object):
        pass

def class_decorators():
    @decorator
    class foo(object):
        pass
    def decorator(cls):
        return cls

def class_py3k_metaclass():
    class foo(metaclass=Meta):
        pass
    class Meta(object):
        pass

def class_py3k_args():
    class foo(*args, **kwargs):
        pass
    args = []
    kwargs = {}

def uninitialized_in_sizeof():
    cdef int i
    print sizeof(i)

_ERRORS = """
6:10: local variable 'a' referenced before assignment
12:11: local variable 'a' might be referenced before assignment
29:11: local variable 'a' might be referenced before assignment
35:14: local variable 'b' might be referenced before assignment
58:10: local variable 'a' referenced before assignment
58:13: local variable 'b' referenced before assignment
62:10: local variable 'bar' referenced before assignment
66:10: local variable 'foo' referenced before assignment
71:14: local variable 'exc' referenced before assignment
71:19: local variable 'msg' referenced before assignment
78:5: local variable 'decorator' referenced before assignment
85:16: local variable 'default' referenced before assignment
91:14: local variable 'bar' referenced before assignment
97:5: local variable 'decorator' referenced before assignment
104:24: local variable 'Meta' referenced before assignment
110:15: local variable 'args' referenced before assignment
110:23: local variable 'kwargs' referenced before assignment
"""
