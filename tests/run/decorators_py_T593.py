# mode: run
# ticket: 593
# tag: property, decorator

"""
>>> am_i_buggy
False
"""

def testme(func):
    try:
        am_i_buggy
        return True
    except NameError:
        return False

@testme
def am_i_buggy():
    pass

def called_deco(a,b,c):
    a.append( (1,b,c) )
    def count(f):
        a.append( (2,b,c) )
        return f
    return count

L = []

@called_deco(L, 5, c=6)
@called_deco(L, c=3, b=4)
@called_deco(L, 1, 2)
def wrapped_func(x):
    """
    >>> L
    [(1, 5, 6), (1, 4, 3), (1, 1, 2), (2, 1, 2), (2, 4, 3), (2, 5, 6)]
    >>> wrapped_func(99)
    99
    >>> L
    [(1, 5, 6), (1, 4, 3), (1, 1, 2), (2, 1, 2), (2, 4, 3), (2, 5, 6)]
    """
    return x


def class_in_closure(x):
    """
    >>> C1, c0 = class_in_closure(5)
    >>> C1().smeth1()
    (5, ())
    >>> C1.smeth1(1,2)
    (5, (1, 2))
    >>> C1.smeth1()
    (5, ())
    >>> c0.smeth0()
    1
    >>> c0.__class__.smeth0()
    1
    """
    class ClosureClass1(object):
        @staticmethod
        def smeth1(*args):
            return x, args

    class ClosureClass0(object):
        @staticmethod
        def smeth0():
            return 1

    return ClosureClass1, ClosureClass0()

def class_not_in_closure():
    """
    >>> c = class_not_in_closure()
    >>> c.smeth0()
    1
    >>> c.__class__.smeth0()
    1
    """
    class ClosureClass0(object):
        @staticmethod
        def smeth0():
            return 1

    return ClosureClass0()
