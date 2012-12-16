# ticket: 494
# cython: binding=True

__doc__ = """
    >>> A.foo = foo
    >>> print A().foo()
    True
"""

class A:
    pass

def foo(self):
    return self is not None
