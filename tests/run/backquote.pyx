def f(obj2):
    """
    >>> f(20)
    '20'
    >>> f('test')
    "'test'"
    """
    obj1 = `obj2`
    return obj1

def g():
    """
    >>> g()
    '42'
    """
    obj1 = `42`
    return obj1
