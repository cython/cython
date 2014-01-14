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
