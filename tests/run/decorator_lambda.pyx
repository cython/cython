# mode: run
# tag: decorator, lambda

def decorate(f):
    return f

@decorate(lambda x: x)
class TestClassDecorator(object):
    """
    >>> obj = TestClassDecorator()
    >>> obj.hello()
    'Hello, world!'
    """
    def hello(self):
        return "Hello, world!"
