# mode: run
# tag: pure3.0
# cython: binding=True

"""
Test that fused functions can be used in the same way as CyFunctions with respect to
assigning them to class attributes. Previously they enforced extra type/argument checks
beyond those which CyFunctions did.
"""

import cython

MyFusedClass = cython.fused_type(
    float,
    'Cdef',
    object)

def fused_func(x: MyFusedClass):
    return (type(x).__name__, cython.typeof(x))

IntOrFloat = cython.fused_type(int, float)

def fused_func_0(x: IntOrFloat = 0):
    """
    Fused functions can legitimately take 0 arguments
    >>> fused_func_0()
    ('int', 'int')

    # subscripted in module __doc__ conditionally
    """
    return (type(x).__name__, cython.typeof(x))

def regular_func(x):
    return (type(x).__name__, cython.typeof(x))

def regular_func_0():
    return

@classmethod
def fused_classmethod_free(cls, x: IntOrFloat):
    return (cls.__name__, type(x).__name__)

@cython.cclass
class Cdef:
    __doc__ = """
    >>> c = Cdef()

    # functions are callable with an instance of c
    >>> c.fused_func()
    ('Cdef', 'Cdef')
    >>> c.regular_func()
    ('Cdef', '{typeofCdef}')
    >>> c.fused_in_class(1.5)
    ('float', 'float')

    # Fused functions are callable without an instance
    # (This applies to everything in Py3 - see __doc__ below)
    >>> Cdef.fused_func(1.5)
    ('float', 'float')
    >>> Cdef.fused_in_class(c, 1.5)
    ('float', 'float')
    >>> Cdef.fused_func_0()
    ('int', 'int')

    # Functions not expecting an argument don't work with an instance
    >>> c.regular_func_0()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: regular_func_0() takes ... arguments ...1... given...

    # Looking up a class attribute doesn't go through all of __get__
    >>> Cdef.fused_in_class is Cdef.fused_in_class
    True

    # looking up a classmethod does go through __get__ though
    >>> Cdef.fused_classmethod is Cdef.fused_classmethod
    False
    >>> Cdef.fused_classmethod_free is Cdef.fused_classmethod_free
    False
    >>> Cdef.fused_classmethod(1)
    ('Cdef', 'int')
    >>> Cdef.fused_classmethod_free(1)
    ('Cdef', 'int')
    """.format(typeofCdef = 'Python object' if cython.compiled else 'Cdef')

    if cython.compiled:
        __doc__ += """

    # fused_func_0 does not accept a "Cdef" instance
    >>> c.fused_func_0()
    Traceback (most recent call last):
    TypeError: No matching signature found

    # subscripting requires fused methods (so  not pure Python)
    >>> Cdef.fused_func_0['float']()
    ('float', 'float')
    >>> c.fused_func_0['float']()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: (Exception looks quite different in Python2 and 3 so no way to match both)

    >>> Cdef.fused_classmethod['float'] is Cdef.fused_classmethod['float']
    False
    >>> Cdef.fused_classmethod_free['float'] is Cdef.fused_classmethod_free['float']
    False
    """
    fused_func = fused_func
    fused_func_0 = fused_func_0
    regular_func = regular_func
    regular_func_0 = regular_func_0

    fused_classmethod_free = fused_classmethod_free

    def fused_in_class(self, x: MyFusedClass):
        return (type(x).__name__, cython.typeof(x))

    def regular_in_class(self):
        return type(self).__name__

    @classmethod
    def fused_classmethod(cls, x: IntOrFloat):
        return (cls.__name__, type(x).__name__)

class Regular(object):
    __doc__ = """
    >>> c = Regular()

    # Functions are callable with an instance of C
    >>> c.fused_func()
    ('Regular', '{typeofRegular}')
    >>> c.regular_func()
    ('Regular', '{typeofRegular}')

    # Fused functions are callable without an instance
    # (This applies to everything in Py3 - see __doc__ below)
    >>> Regular.fused_func(1.5)
    ('float', 'float')
    >>> Regular.fused_func_0()
    ('int', 'int')

    # Functions not expecting an argument don't work with an instance
    >>> c.regular_func_0()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: regular_func_0() takes ... arguments ...1... given...

    # Looking up a class attribute doesn't go through all of __get__
    >>> Regular.fused_func is Regular.fused_func
    True

    # looking up a classmethod does go __get__ though
    >>> Regular.fused_classmethod is Regular.fused_classmethod
    False
    >>> Regular.fused_classmethod_free is Regular.fused_classmethod_free
    False
    >>> Regular.fused_classmethod(1)
    ('Regular', 'int')
    >>> Regular.fused_classmethod_free(1)
    ('Regular', 'int')
    """.format(typeofRegular = "Python object" if cython.compiled else 'Regular')
    if cython.compiled:
        __doc__ += """
    # fused_func_0 does not accept a "Regular" instance
    >>> c.fused_func_0()
    Traceback (most recent call last):
    TypeError: No matching signature found

    # subscripting requires fused methods (so  not pure Python)
    >>> c.fused_func_0['float']()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: (Exception looks quite different in Python2 and 3 so no way to match both)
    >>> Regular.fused_func_0['float']()
    ('float', 'float')

    >>> Regular.fused_classmethod['float'] is Regular.fused_classmethod['float']
    False
    >>> Regular.fused_classmethod_free['float'] is Regular.fused_classmethod_free['float']
    False
    """

    fused_func = fused_func
    fused_func_0 = fused_func_0
    regular_func = regular_func
    regular_func_0 = regular_func_0

    fused_classmethod_free = fused_classmethod_free

    @classmethod
    def fused_classmethod(cls, x: IntOrFloat):
        return (cls.__name__, type(x).__name__)


# extra Py3 only tests - shows that functions added to a class can be called
# with an type as the first argument
__doc__ = """
    >>> Cdef.regular_func(1.5)
    ('float', '{typeoffloat}')
    >>> Regular.regular_func(1.5)
    ('float', '{typeoffloat}')
    >>> Cdef.regular_func_0()
    >>> Regular.regular_func_0()
""".format(typeoffloat='Python object' if cython.compiled else 'float')

if cython.compiled:
    __doc__ += """
    >>> fused_func_0['float']()
    ('float', 'float')
    """
