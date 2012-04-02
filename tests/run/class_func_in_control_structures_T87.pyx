# ticket: 87

__doc__ = u"""
>>> d = Defined()
>>> n = NotDefined()         # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'NotDefined' is not defined
"""

if True:
    class Defined(object):
        """
        >>> isinstance(Defined(), Defined)
        True
        """

if False:
    class NotDefined(object):
        """
        >>> NotDefined() # fails when defined
        """

def test_class_cond(x):
    """
    >>> Test, test = test_class_cond(True)
    >>> test.A
    1
    >>> Test().A
    1
    >>> Test, test = test_class_cond(False)
    >>> test.A
    2
    >>> Test().A
    2
    """
    if x:
        class Test(object):
            A = 1
    else:
        class Test(object):
            A = 2
    return Test, Test()

def test_func_cond(x):
    """
    >>> func = test_func_cond(True)
    >>> func()
    1
    >>> func = test_func_cond(False)
    >>> func()
    2
    """
    if x:
        def func():
            return 1
    else:
        def func():
            return 2
    return func
