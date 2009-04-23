__doc__ = u"""
>>> f = add_n(3)
>>> f(2)
5

>>> a(5)()
8
"""

def add_n(int n):
    def f(int x):
        return x+n
    return f

def a(int x):
    def b():
        def c():
            return 3+x
        return c()
    return b
