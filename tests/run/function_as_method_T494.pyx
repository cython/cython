# ticket: 494

__doc__ = """
    >>> A.foo = foo
    >>> print A().foo()

"""

class A:
    pass

def foo(self):
    return self is not None


