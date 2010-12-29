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
