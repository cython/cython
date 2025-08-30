# mode: run
# tag: pyclass

class A(object):
    x = 1

class B(object):
    x = 2


def cond_if_bases(x):
    """
    >>> c = cond_if_bases(True)
    >>> c().p
    5
    >>> c().x
    1
    >>> c = cond_if_bases(False)
    >>> c().p
    5
    >>> c().x
    2
    """
    class PyClass(A if x else B):
        p = 5
    return PyClass


def make_subclass(*bases):
    """
    >>> cls = make_subclass(list)
    >>> issubclass(cls, list) or cls.__mro__
    True

    >>> class Cls(object): pass
    >>> cls = make_subclass(Cls, list)
    >>> issubclass(cls, list) or cls.__mro__
    True
    >>> issubclass(cls, Cls) or cls.__mro__
    True
    """
    # GH-3338
    class MadeClass(*bases):
        pass
    return MadeClass
