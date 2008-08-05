__doc__ = u"""
  >>> f(1,2)
  4
  >>> f.HERE
  1

  >>> g(1,2)
  5
  >>> g.HERE
  5

  >>> h(1,2)
  6
  >>> h.HERE
  1
  >>> i(4)
  3
  >>> i.HERE
  1
"""

class wrap:
    def __init__(self, func):
        self.func = func
        self.HERE = 1
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def decorate(func):
    try:
        func.HERE += 1
    except AttributeError:
        func = wrap(func)
    return func

def decorate2(a,b):
    return decorate

@decorate
def f(a,b):
    return a+b+1

@decorate
@decorate
@decorate
@decorate
@decorate
def g(a,b):
    return a+b+2

@decorate2(1,2)
def h(a,b):
    return a+b+3

class A:
    def decorate(self, func):
        return decorate(func)


a = A()
@a.decorate
def i(x):
    return x - 1
