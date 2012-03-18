# mode: error

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
#5:4: 'return' with argument inside generator
#9:4: 'yield' outside function
11:0: 'yield' not supported here
14:4: 'yield' not supported here
"""
