# ticket: t494

class A:
    """
    >>> A.foo = foo
    >>> A().foo()
    True
    """
    pass

def foo(self):
    return self is not None


def f_plus(a):
    return a + 1


class B:
    """
    >>> B.plus1(1)
    2
    """
    plus1 = f_plus


class C(object):
    """
    >>> C.plus1(1)
    2
    """
    plus1 = f_plus
