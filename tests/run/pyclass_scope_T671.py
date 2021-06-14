# mode: run
# ticket: t671

A = 1234

class SimpleAssignment(object):
    """
    >>> SimpleAssignment.A
    1234
    """
    A = A

class SimpleRewrite(object):
    """
    >>> SimpleRewrite.A
    4321
    """
    A = 4321
    A = A

def simple_inner(a):
    """
    >>> simple_inner(4321).A
    1234
    """
    A = a
    class X(object):
        A = A
    return X

def conditional(a, cond):
    """
    >>> conditional(4321, False).A
    1234
    >>> conditional(4321, True).A
    4321
    """
    class X(object):
        if cond:
            A = a
        A = A
    return X

def name_error():
    """
    >>> name_error() #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    NameError: ...B...
    """
    class X(object):
        B = B

def conditional_name_error(cond):
    """
    >>> conditional_name_error(True).B
    4321
    >>> conditional_name_error(False).B #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    NameError: ...B...
    """
    class X(object):
        if cond:
            B = 4321
        B = B
    return X

C = 1111
del C

def name_error_deleted():
    """
    >>> name_error_deleted() #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    NameError: ...C...
    """
    class X(object):
        C = C

_set = set

def name_lookup_order():
    """
    >>> Scope = name_lookup_order()
    >>> Scope().set(2)
    42
    >>> Scope.test1 == _set()
    True
    >>> Scope.test2 == _set()
    True

    """
    class Scope(object):
        test1 = set()
        test2 = set()

        def set(self, x):
            return 42

    return Scope
