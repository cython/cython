def foo():
    yield
    return 0

def bar(a):
    return 0
    yield

def xxx():
    yield
    return

yield

class Foo:
    yield

_ERRORS = u"""
3:4: 'return' with argument inside generator
7:4: 'yield' outside function
11:4: 'return' inside generators not yet supported
13:0: 'yield' not supported here
16:4: 'yield' not supported here
"""
