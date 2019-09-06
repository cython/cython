# mode: run
# tag: pure3.0
# cython: language_level=3

# (don't add tag pure2.0 because
#  def method3(self, *args, __arg=None)
#  def method4(self, *, __arg=None)
# aren't supported)

import cython

error = """Traceback (most recent call last):
...
TypeError:
"""

class C:
    __doc__ = """
>>> instance = C()

Instance methods have their arguments mangled
>>> instance.method1(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method1(_C__arg=1)
1
>>> instance.method2(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method2(_C__arg=1)
1

Works when optional argument isn't passed
>>> instance.method2()
None

>>> instance.method3(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method3(_C__arg=1)
1
>>> instance.method4(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method4(_C__arg=1)
1

Where args are in the function's **kwargs dict, names aren't mangled
>>> instance.method5(__arg=1) # doctest:
1
>>> instance.method5(_C__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
KeyError:

Lambda functions behave in the same way:
>>> instance.method_lambda(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.method_lambda(_C__arg=1)
1

Class methods - have their arguments mangled
>>> instance.class_meth(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.class_meth(_C__arg=1)
1
>>> C.class_meth(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> C.class_meth(_C__arg=1)
1

Static methods - have their arguments mangled
>>> instance.static_meth(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> instance.static_meth(_C__arg=1)
1
>>> C.static_meth(__arg=1) # doctest: +IGNORE_EXCEPTION_DETAIL
{error}
>>> C.static_meth(_C__arg=1)
1

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

def free_function1(x, __arg):
    print(__arg)

def free_function2(__arg, dummy_arg=None):
    # dummy_arg is to mask https://github.com/cython/cython/issues/3090
    print(__arg)

C.class_assigned_function = free_function1

__global_arg = True

_D__arg1 = None
_D__global_arg = False # define these because otherwise Cython gives a compile-time error
       # while Python gives a runtime error (which is difficult to test)
def can_find_global_arg():
    """
    >>> can_find_global_arg()
    True
    """
    return __global_arg

def cant_find_global_arg():
    """
    Gets _D_global_arg instead
    >>> cant_find_global_arg()
    False
    """
    class D:
        def f(self):
            return __global_arg
    return D().f()

class CMultiplyNested:
    def f1(self, __arg, name=None, return_closure=False):
        """
        >>> inst = CMultiplyNested()
        >>> for name in [None, '__arg', '_CMultiplyNested__arg', '_D__arg']:
        ...    try:
        ...        print(inst.f1(1,name))
        ...    except TypeError:
        ...        print("TypeError") # not concerned about exact details
        ...    # now test behaviour is the same in closures
        ...    closure = inst.f1(1, return_closure=True)
        ...    try:
        ...        if name is None:
        ...            print(closure(2))
        ...        else:
        ...            print(closure(**{ name: 2}))
        ...    except TypeError:
        ...        print("TypeError")
        2
        2
        TypeError
        TypeError
        TypeError
        TypeError
        2
        2
        """
        class D:
            def g(self, __arg):
                return __arg
        if return_closure:
            return D().g
        if name is not None:
            return D().g(**{ name: 2 })
        else:
            return D().g(2)

    def f2(self, __arg1):
        """
        This finds the global name '_D__arg1'
        It's tested in this way because without the global
        Python gives a runtime error and Cython a compile error
        >>> print(CMultiplyNested().f2(1))
        None
        """
        class D:
            def g(self):
                return __arg1
        return D().g()

    def f3(self, arg, name):
        """
        >>> inst = CMultiplyNested()
        >>> inst.f3(1, None)
        2
        >>> inst.f3(1, '__arg') # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        TypeError:
        >>> inst.f3(1, '_CMultiplyNested__arg')
        2
        """
        def g(__arg, dummy=1):
            return __arg
        if name is not None:
            return g(**{ name: 2})
        else:
            return g(2)

    def f4(self, __arg):
        """
        >>> CMultiplyNested().f4(1)
        1
        """
        def g():
            return __arg
        return g()

    def f5(self, __arg):
        """
        Default values are found in the outer scope correcly
        >>> CMultiplyNested().f5(1)
        1
        """
        def g(x=__arg):
            return x
        return g()

    def f6(self, __arg1):
        """
        This will find the global name _D__arg1
        >>> print(CMultiplyNested().f6(1))
        None
        """
        class D:
            def g(self, x=__arg1):
                return x
        return D().g()

    def f7(self, __arg):
        """
        Lookup works in generator expressions
        >>> list(CMultiplyNested().f7(1))
        [1]
        """
        return (__arg for x in range(1))

class __NameWithDunder:
    pass

class Inherits(__NameWithDunder):
    """
    Compile check that it can find the base class
    >>> x = Inherits()
    """
    pass
