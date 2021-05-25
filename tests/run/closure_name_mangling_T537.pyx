# mode: run
# tag: closures
# ticket: t537

__doc__ = u"""
>>> f1 = nested1()
>>> f2 = nested2()
>>> f1 == f2      # inner functions (f)
False
>>> f1() == f2()  # inner-inner functions (g)
False
"""

def nested1():
   def f():
      def g():
         pass
      return g
   return f

def nested2():
   def f():
      def g():
         pass
      return g
   return f
