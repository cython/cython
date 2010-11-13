
class Base(type):
    def __new__(cls, name, bases, attrs):
        attrs['metaclass_was_here'] = True
        return type.__new__(cls, name, bases, attrs)

class Foo(object):
    """
    >>> obj = Foo()
    >>> obj.metaclass_was_here
    True
    """
    __metaclass__ = Base


class Py3Base(type):
    def __new__(cls, name, bases, attrs, foo=None):
        attrs['foo'] = foo
        return type.__new__(cls, name, bases, attrs)

    def __init__(self, cls, attrs, obj, foo=None):
        pass
    @staticmethod
    def __prepare__(name, bases, **kwargs):
        return {'bar': 666, 'dirty': True}

class Py3Foo(object, metaclass=Py3Base, foo=123):
    """
    >>> obj = Py3Foo()
    >>> obj.foo
    123
    >>> obj.bar
    666
    >>> obj.dirty
    False
    """
    dirty = False
