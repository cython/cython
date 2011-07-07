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

def wrap_hasattr(obj, name):
    """
    >>> wrap_hasattr(None, "abc")
    False
    >>> wrap_hasattr(list, "append")
    True
    >>> wrap_hasattr(Foo(), "foo")
    True
    >>> wrap_hasattr(Foo(), "spam")
    False
    >>> wrap_hasattr(Foo(), "bar")
    False
    >>> Foo().baz   #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    ZeroDivisionError: ...
    >>> wrap_hasattr(Foo(), "baz")
    False
    """
    return hasattr(obj, name)
