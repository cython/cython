def foo():
    yield
    return 0

def bar(a):
    return 0
    yield

yield

class Foo:
    yield

_ERRORS = u"""
3:4: 'return' with argument inside generator
7:4: 'yield' outside function
9:0: 'yield' not supported here
12:4: 'yield' not supported here
"""
