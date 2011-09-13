# mode: run
# tags: eval

GLOBAL = 123

def eval_simple(local):
    """
    >>> eval_simple(321)
    (123, 321)
    """
    return eval('GLOBAL, local')


def eval_locals(a, b):
    """
    >>> eval_locals(1, 2)
    (1, 2)
    """
    return eval('a, b', {}, locals())
