# ticket: t422

"""
>>> Foo.incr.__module__ is not None
True
>>> Foo.incr.__module__ == Foo.__module__ == bar.__module__
True
>>> Simpleton.incr.__module__ == Simpleton.__module__ == bar.__module__
True

"""
class Foo(object):
   def incr(self,x):
       return x+1

def bar():
    pass


class Simpleton:
   def __str__(self):
       return "A simpleton"

   def incr(self,x):
       """Increment x by one.
       """
       return x+1

