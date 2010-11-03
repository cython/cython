"""
>>> obj = Foo()
>>> obj.metaclass_was_here
True
"""
class Base(type):
    def __new__(cls, name, bases, attrs):
        attrs['metaclass_was_here'] = True
        return type.__new__(cls, name, bases, attrs)

class Foo(object):
    __metaclass__ = Base
