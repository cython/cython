# mode: run
# cython: binding=True

"""
Test that fused functions can be used in the same way as CyFunctions with respect to
assigning them to class attributes. Previously they enforced extra type/argument checks
beyond those which CyFunctions did.
"""

import cython

ctypedef fused MyFusedClass:
    double
    Cdef
    object

def fused_func(MyFusedClass x):
    return (type(x).__name__, cython.typeof(x))

ctypedef fused IntOrFloat:
    int
    double

def fused_func_0(IntOrFloat x = 0):
    """
    Fused functions can legitimately take 0 arguments
    >>> fused_func_0()
    ('int', 'int')
    >>> fused_func_0['double']()
    ('float', 'double')
    """
    return (type(x).__name__, cython.typeof(x))

def regular_func(x):
    return (type(x).__name__, cython.typeof(x))

def regular_func_0():
    return

cdef class Cdef:
    """
    >>> import sys
    >>> c = Cdef()
    >>> c.fused_func()
    ('Cdef', 'Cdef')
    >>> c.regular_func()
    ('Cdef', 'Python object')
    >>> c.fused_in_class(1.5)
    ('float', 'double')
    >>> Cdef.fused_func(1.5)
    ('float', 'double')
    >>> Cdef.fused_in_class(c, 1.5)
    ('float', 'double')
    >>> Cdef.fused_func_0()
    ('int', 'int')
    >>> Cdef.fused_func_0['double']()
    ('float', 'double')
    >>> c.fused_func_0()
    Traceback (most recent call last):
    TypeError: No matching signature found
    >>> c.fused_func_0['double']()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError:
    >>> c.regular_func_0()
    Traceback (most recent call last):
    TypeError: regular_func_0() takes no arguments (1 given)
    """
    fused_func = fused_func
    fused_func_0 = fused_func_0
    regular_func = regular_func
    regular_func_0 = regular_func_0

    def fused_in_class(self, MyFusedClass x):
        return (type(x).__name__, cython.typeof(x))

    def regular_in_class(self):
        return type(self).__name__

class Regular(object):
    """
    >>> c = Regular()
    >>> c.fused_func()
    ('Regular', 'Python object')
    >>> c.regular_func()
    ('Regular', 'Python object')
    >>> Regular.fused_func(1.5)
    ('float', 'double')
    >>> Regular.fused_func_0()
    ('int', 'int')
    >>> Regular.fused_func_0['double']()
    ('float', 'double')
    >>> c.fused_func_0()
    Traceback (most recent call last):
    TypeError: No matching signature found
    >>> c.fused_func_0['double']()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError:
    >>> c.regular_func_0()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError:
    """
    fused_func = fused_func
    fused_func_0 = fused_func_0
    regular_func = regular_func
    regular_func_0 = regular_func_0

import sys
if sys.version_info[0] > 2:
    # extra Py3 only tests
    __doc__ = """
    >>> Cdef.regular_func(1.5)
    ('float', 'Python object')
    >>> Regular.regular_func(1.5)
    ('float', 'Python object')
    >>> Cdef.regular_func_0()
    >>> Regular.regular_func_0()
    """
else:
    __doc__ = """"""
