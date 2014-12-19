# mode: run
# tag: lambda, attribute, regression

class TestClass(object):
    bar = 123


def test_attribute_and_lambda(f):
    """
    >>> test_attribute_and_lambda(lambda _: TestClass())
    123
    """
    return f(lambda x: x).bar
