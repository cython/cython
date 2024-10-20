# mode: run
# tag: pure

class Foo:
    @property
    def foo(self):
        return None
    @property
    def bar(self):
        raise AttributeError
    @property
    def baz(self):
        return int(1)/int(0)


unicode_foo = u"foo"


def wrap_hasattr(obj, name):
    """
    >>> wrap_hasattr(None, "abc")
    False
    >>> wrap_hasattr(list, "append")
    True
    >>> wrap_hasattr(Foo(), "foo")
    True
    >>> wrap_hasattr(Foo(), unicode_foo)
    True
    >>> wrap_hasattr(Foo(), "spam")
    False
    >>> wrap_hasattr(Foo(), "bar")
    False
    >>> Foo().baz   #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...
    >>> wrap_hasattr(Foo(), "baz")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError...
    >>> hasattr(Foo(), None)   #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    TypeError: ...attribute name must be string...
    """
    return hasattr(obj, name)
