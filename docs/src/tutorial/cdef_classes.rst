Extension types (aka. cdef classes)
===================================

To support object-oriented programming, Cython supports writing normal
Python classes exactly as in Python::

    class MathFunction(object):
        def __init__(self, name, operator):
            self.name = name
            self.operator = operator

        def __call__(self, *operands):
            return self.operator(*operands)

Based on what Python calls a "built-in type", however, Cython supports
a second kind of class: *extension types*, sometimes referred to as
"cdef classes" due to the keywords used for their declaration.  They
are somewhat restricted compared to Python classes, but are generally
more memory efficient and faster than generic Python classes.  The
main difference is that they use a C struct to store their fields and methods
instead of a Python dict.  This allows them to store arbitrary C types
in their fields without requiring a Python wrapper for them, and to
access fields and methods directly at the C level without passing
through a Python dictionary lookup.

Normal Python classes can inherit from cdef classes, but not the other
way around.  Cython requires to know the complete inheritance
hierarchy in order to lay out their C structs, and restricts it to
single inheritance.  Normal Python classes, on the other hand, can
inherit from any number of Python classes and extension types, both in
Cython code and pure Python code.

So far our integration example has not been very useful as it only
integrates a single hard-coded function. In order to remedy this,
with hardly sacrificing speed, we will use a cdef class to represent a
function on floating point numbers::

  cdef class Function:
      cpdef double evaluate(self, double x) except *:
          return 0

The directive cpdef makes two versions of the method available; one
fast for use from Cython and one slower for use from Python. Then::

  cdef class SinOfSquareFunction(Function):
      cpdef double evaluate(self, double x) except *:
          return sin(x**2)

This does slightly more than providing a python wrapper for a cdef
method: unlike a cdef method, a cpdef method is fully overridable by
methods and instance attributes in Python subclasses.  It adds a
little calling overhead compared to a cdef method.

Using this, we can now change our integration example::

  def integrate(Function f, double a, double b, int N):
      cdef int i
      cdef double s, dx
      if f is None:
          raise ValueError("f cannot be None")
      s = 0
      dx = (b-a)/N
      for i in range(N):
          s += f.evaluate(a+i*dx)
      return s * dx

  print(integrate(SinOfSquareFunction(), 0, 1, 10000))

This is almost as fast as the previous code, however it is much more flexible
as the function to integrate can be changed. We can even pass in a new
function defined in Python-space::

  >>> import integrate
  >>> class MyPolynomial(integrate.Function):
  ...     def evaluate(self, x):
  ...         return 2*x*x + 3*x - 10
  ...
  >>> integrate(MyPolynomial(), 0, 1, 10000)
  -7.8335833300000077

This is about 20 times slower, but still about 10 times faster than
the original Python-only integration code.  This shows how large the
speed-ups can easily be when whole loops are moved from Python code
into a Cython module.

Some notes on our new implementation of ``evaluate``:

 - The fast method dispatch here only works because ``evaluate`` was
   declared in ``Function``. Had ``evaluate`` been introduced in
   ``SinOfSquareFunction``, the code would still work, but Cython
   would have used the slower Python method dispatch mechanism
   instead.

 - In the same way, had the argument ``f`` not been typed, but only
   been passed as a Python object, the slower Python dispatch would
   be used.

 - Since the argument is typed, we need to check whether it is
   ``None``. In Python, this would have resulted in an ``AttributeError``
   when the ``evaluate`` method was looked up, but Cython would instead
   try to access the (incompatible) internal structure of ``None`` as if
   it were a ``Function``, leading to a crash or data corruption.

There is a *compiler directive* ``nonecheck`` which turns on checks
for this, at the cost of decreased speed. Here's how compiler directives
are used to dynamically switch on or off ``nonecheck``::

  #cython: nonecheck=True
  #        ^^^ Turns on nonecheck globally

  import cython

  # Turn off nonecheck locally for the function
  @cython.nonecheck(False)
  def func():
      cdef MyClass obj = None
      try:
          # Turn nonecheck on again for a block
          with cython.nonecheck(True):
              print obj.myfunc() # Raises exception
      except AttributeError:
          pass
      print obj.myfunc() # Hope for a crash!



Attributes in cdef classes behave differently from attributes in regular classes:

 - All attributes must be pre-declared at compile-time
 - Attributes are by default only accessible from Cython (typed access)
 - Properties can be declared to expose dynamic attributes to Python-space

::

  cdef class WaveFunction(Function):
      # Not available in Python-space:
      cdef double offset
      # Available in Python-space:
      cdef public double freq
      # Available in Python-space:
      @property
      def period(self):
          return 1.0 / self.freq
      @period.setter
      def period(self, value):
          self.freq = 1.0 / value
      <...>
