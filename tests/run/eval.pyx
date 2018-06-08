# mode: run
# tag: eval

GLOBAL = 123

def eval_simple(local):
    """
    >>> eval_simple(321)
    (123, 321)
    """
    return eval('GLOBAL, local')

def eval_class_scope():
    """
    >>> eval_class_scope().c
    3
    """
    class TestClassScope:
        a = 1
        b = 2
        c = eval('a + b')
    return TestClassScope

def eval_locals(a, b):
    """
    >>> eval_locals(1, 2)
    (1, 2)
    """
    return eval('a, b', {}, locals())
