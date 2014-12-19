# cython: binding=True
# mode: run
# tag: cyfunction,qualname


def test_qualname():
    """
    >>> test_qualname.__qualname__
    'test_qualname'
    >>> test_qualname.__qualname__ = 123 #doctest:+ELLIPSIS
    Traceback (most recent call last):
    TypeError: __qualname__ must be set to a ... object
    >>> test_qualname.__qualname__ = 'foo'
    >>> test_qualname.__qualname__
    'foo'
    """


def test_nested_qualname():
    """
    >>> outer, lambda_func, XYZ = test_nested_qualname()

    >>> outer().__qualname__
    'test_nested_qualname.<locals>.outer.<locals>.Test'
    >>> outer().test.__qualname__
    'test_nested_qualname.<locals>.outer.<locals>.Test.test'
    >>> outer()().test.__qualname__
    'test_nested_qualname.<locals>.outer.<locals>.Test.test'

    >>> outer()().test().__qualname__
    'XYZinner'
    >>> outer()().test().Inner.__qualname__
    'XYZinner.Inner'
    >>> outer()().test().Inner.inner.__qualname__
    'XYZinner.Inner.inner'

    >>> lambda_func.__qualname__
    'test_nested_qualname.<locals>.<lambda>'

    >>> XYZ.__qualname__
    'XYZ'
    >>> XYZ.Inner.__qualname__
    'XYZ.Inner'
    >>> XYZ.Inner.inner.__qualname__
    'XYZ.Inner.inner'
    """
    def outer():
        class Test(object):
            def test(self):
                global XYZinner
                class XYZinner:
                    class Inner:
                        def inner(self):
                            pass

                return XYZinner
        return Test

    global XYZ
    class XYZ(object):
        class Inner(object):
            def inner(self):
                pass

    return outer, lambda:None, XYZ
