"""
>>> am_i_buggy
False
>>> Foo
False
"""
def testme(func):
    try:
        am_i_buggy
        return True
    except NameError:
        return False
@testme
def am_i_buggy():
    pass

def testclass(klass):
    try:
        Foo
        return True
    except NameError:
        return False
@testclass
class Foo:
    pass

def class_in_closure(x):
    """
    >>> C1, c0 = class_in_closure(5)
    >>> C1().smeth1()
    (5, ())
    >>> C1.smeth1(1,2)
    (5, (1, 2))
    >>> C1.smeth1()
    (5, ())
    >>> c0.smeth0()
    1
    >>> c0.__class__.smeth0()
    1
    """
    class ClosureClass1(object):
        @staticmethod
        def smeth1(*args):
            return x, args

    class ClosureClass0(object):
        @staticmethod
        def smeth0():
            return 1

    return ClosureClass1, ClosureClass0()

def class_not_in_closure():
    """
    >>> c = class_not_in_closure()
    >>> c.smeth0()
    1
    >>> c.__class__.smeth0()
    1
    """
    class ClosureClass0(object):
        @staticmethod
        def smeth0():
            return 1

    return ClosureClass0()

class ODict(dict):
   def __init__(self):
       dict.__init__(self)
       self._order = []
       dict.__setitem__(self, '_order', self._order)
   def __setitem__(self, key, value):
       dict.__setitem__(self, key, value)
       self._order.append(key)

class Base(type):
   @staticmethod
   def __prepare__(*args, **kwargs):
       return ODict()

class Bar(metaclass=Base):
   """
   >>> Bar._order
   ['__module__', '__doc__', 'bar']
   """
   @property
   def bar(self):
       return 0
