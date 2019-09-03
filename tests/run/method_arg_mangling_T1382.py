# mode: run
# tag: pure3.0
# cython: language_level=3

# (don't add tag pure2.0 because
#  def method3(self, *args, __arg=None)
#  def method4(self, *, __arg=None)
# aren't supported)

import cython

class C:
    def method1(self, __arg):
        print(__arg)

    def method2(self, __arg=None):
        # __arg is optional
        print(__arg)

    def method3(self, *args, __arg=None):
        # __arg is keyword only
        print(__arg)

    def method4(self, *, __arg=None):
        # __arg is keyword only
        print(__arg)

    def method5(self, **kwargs):
        print(kwargs['__arg'])

    method_lambda = lambda self, __arg: __arg

    def get_locals(self, __arg):
        return locals()

    @classmethod
    def class_meth(cls, __arg):
        print(__arg)

    @staticmethod
    def static_meth(__arg, dummy_arg=None):
        # dummy_arg is to mask https://github.com/cython/cython/issues/3090
        print(__arg)

@cython.cclass
class D:
    def method1(self, __arg, dummy_arg=None):
        # dummy_arg is to mask an issue probably related to https://github.com/cython/cython/issues/3090
        print(__arg)

    def method2(self, __arg=None):
        # __arg is optional
        print(__arg)

    def method3(self, *args, __arg=None):
        # __arg is keyword only
        print(__arg)

    def method4(self, *, __arg=None):
        # __arg is keyword only
        print(__arg)

    def method5(self, **kwargs):
        print(kwargs['__arg'])

    method_lambda = lambda self, __arg: __arg

    @classmethod
    def class_meth(cls, __arg, dummy_arg=None):
        # dummy_arg is to mask an issue probably related to https://github.com/cython/cython/issues/3090
        print(__arg)

    @staticmethod
    def static_meth(__arg, dummy_arg=None):
        # dummy_arg is to mask https://github.com/cython/cython/issues/3090
        print(__arg)

def free_function1(x, __arg):
    print(__arg)

def free_function2(__arg, dummy_arg=None):
    # dummy_arg is to mask https://github.com/cython/cython/issues/3090
    print(__arg)

C.class_assigned_function = free_function1

testcode = """
>>> instance = {classname}()

Instance methods have their arguments mangled
>>> instance.method1(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method1(_{classname}__arg=1)
1
>>> instance.method2(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method2(_{classname}__arg=1)
1

Works when optional argument isn't passed
>>> instance.method2()
None

>>> instance.method3(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method3(_{classname}__arg=1)
1
>>> instance.method4(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method4(_{classname}__arg=1)
1

Where args are in the function's **kwargs dict, names aren't mangled
>>> instance.method5(__arg=1) # doctest:
1
>>> instance.method5(_{classname}__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
KeyError:

Lambda functions behave in the same way:
>>> instance.method_lambda(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method_lambda(_{classname}__arg=1)
1

Class methods - have their arguments mangled
>>> instance.class_meth(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.class_meth(_{classname}__arg=1)
1
>>> {classname}.class_meth(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> {classname}.class_meth(_{classname}__arg=1)
1

Static methods - have their arguments mangled
>>> instance.static_meth(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.static_meth(_{classname}__arg=1)
1
>>> {classname}.static_meth(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> {classname}.static_meth(_{classname}__arg=1)
1
"""

error = """Traceback (most recent call last):
...
TypeError:
"""

# because you can't do D.class_assigned_function = ...
tests_only_for_C = """
Functions assigned to the class don't have their arguments mangled
>>> instance.class_assigned_function(__arg=1)
1
>>> instance.class_assigned_function(_C__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}

Functions assigned to an instance don't have their arguments mangled
>>> instance.instance_assigned_function = free_function2
>>> instance.instance_assigned_function(__arg=1)
1
>>> instance.instance_assigned_function(_C__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}

Locals are reported as mangled
>>> list(sorted(k for k in instance.get_locals(1).keys()))
['_C__arg', 'self']
""".format(error=error)

__doc__ = """
{0}

{1}

{2}
""".format(testcode.format(classname="C", error=error),
           tests_only_for_C,
           testcode.format(classname="D", error=error) if cython.compiled else "")
