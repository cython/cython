__doc__ = u"""
    >>> f(20)
    '20'
    >>> f('test')
    "'test'"

    >>> g()
    '42'
"""

def f(obj2):
    obj1 = `obj2`
    return obj1

def g():
    obj1 = `42`
    return obj1
