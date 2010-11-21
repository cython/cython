
cimport cython

class Base(type):
    def __new__(cls, name, bases, attrs):
        attrs['metaclass_was_here'] = True
        return type.__new__(cls, name, bases, attrs)

@cython.test_fail_if_path_exists("//PyClassMetaclassNode", "//Py3ClassNode")
class Foo(object):
    """
    >>> obj = Foo()
    >>> obj.metaclass_was_here
    True
    """
    __metaclass__ = Base

class ODict(dict):
    def __init__(self):
        dict.__init__(self)
        self._order = []
        dict.__setitem__(self, '_order', self._order)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self._order.append(key)

class Py3MetaclassPlusAttr(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        for key, value in kwargs.items():
            attrs[key] = value
        attrs['metaclass_was_here'] = True
        return type.__new__(cls, name, bases, attrs)

    def __init__(self, cls, attrs, obj, **kwargs):
        pass

    @staticmethod
    def __prepare__(*args, **kwargs):
        return ODict()

@cython.test_fail_if_path_exists("//PyClassMetaclassNode")
@cython.test_assert_path_exists("//Py3ClassNode")
class Py3ClassMCOnly(object, metaclass=Py3MetaclassPlusAttr):
    """
    >>> obj = Py3ClassMCOnly()
    >>> obj.bar
    321
    >>> obj.metaclass_was_here
    True
    >>> obj._order
    ['__module__', '__doc__', 'bar', 'metaclass_was_here']
    """
    bar = 321

class Py3Base(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        for key, value in kwargs.items():
            attrs[key] = value
        return type.__new__(cls, name, bases, attrs)

    def __init__(self, cls, attrs, obj, **kwargs):
        pass

    @staticmethod
    def __prepare__(*args, **kwargs):
        return ODict()

@cython.test_fail_if_path_exists("//PyClassMetaclassNode")
@cython.test_assert_path_exists("//Py3ClassNode")
class Py3Foo(object, metaclass=Py3Base, foo=123):
    """
    >>> obj = Py3Foo()
    >>> obj.foo
    123
    >>> obj.bar
    321
    >>> obj._order
    ['__module__', '__doc__', 'bar', 'foo']
    """
    bar = 321

kwargs = {'foo': 123, 'bar': 456}

@cython.test_assert_path_exists("//PyClassMetaclassNode", "//Py3ClassNode")
class Py3Mixed(metaclass=Py3Base, **kwargs):
    """
    >>> Py3Mixed.foo
    123
    >>> Py3Mixed.bar
    456
    """

kwargs['metaclass'] = Py3Base

@cython.test_assert_path_exists("//PyClassMetaclassNode")
class Py3Kwargs(**kwargs):
    """
    >>> Py3Kwargs.foo
    123
    >>> Py3Kwargs.bar
    456
    """

class Base3(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        kwargs['b'] = 2
        return type.__new__(cls, name, bases, attrs)

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    @staticmethod
    def __prepare__(*args, **kwargs):
        kwargs['a'] = 1
        return {}

kwargs = {'c': 0}

@cython.test_assert_path_exists("//PyClassMetaclassNode", "//Py3ClassNode")
class Foo3(metaclass=Base3, a=0, b=0, **kwargs):
    """
    >>> Foo3.kwargs
    {'a': 0, 'c': 0, 'b': 0}
    """
