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

py_dict = {}
exec("""
def py_func(x):
    return type(x).__name__
def py_func_0():
    return
class PyClass(object):
    py_func = py_func
    py_func_0 = py_func_0
    def py_in_class(self):
        return type(self).__name__
""", py_dict)
py_func = py_dict['py_func']
py_func_0 = py_dict['py_func_0']
PyClass = py_dict['PyClass']

cdef class Cdef:
    """
    >>> c = Cdef()

    # functions are callable with an instance of c
    >>> c.fused_func()
    ('Cdef', 'Cdef')
    >>> c.regular_func()
    ('Cdef', 'Python object')
    >>> c.py_func()
    'Cdef'
    >>> c.fused_in_class(1.5)
    ('float', 'double')

    # Fused functions are callable without an instance
    # (This applies to everything in Py3 - see __doc__ below)
    >>> Cdef.fused_func(1.5)
    ('float', 'double')
    >>> Cdef.fused_in_class(c, 1.5)
    ('float', 'double')
    >>> Cdef.fused_func_0()
    ('int', 'int')
    >>> Cdef.fused_func_0['double']()
    ('float', 'double')

    # fused_func_0 does not accept a "Cdef" instance
    >>> c.fused_func_0()
    Traceback (most recent call last):
    TypeError: No matching signature found
    >>> c.fused_func_0['double']()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError:

    # Functions not expecting an argument don't work with an instance
    >>> c.regular_func_0()
    Traceback (most recent call last):
    TypeError: regular_func_0() takes no arguments (1 given)
    >>> c.py_func_0()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: py_func_0() takes ... arguments ...1 ...given...
    """
    fused_func = fused_func
    fused_func_0 = fused_func_0
    regular_func = regular_func
    regular_func_0 = regular_func_0
    py_func = py_func
    py_func_0 = py_func_0

    def fused_in_class(self, MyFusedClass x):
        return (type(x).__name__, cython.typeof(x))

    def regular_in_class(self):
        return type(self).__name__

class Regular(object):
    """
    >>> c = Regular()

    # Functions are callable with an instance of C
    >>> c.fused_func()
    ('Regular', 'Python object')
    >>> c.regular_func()
    ('Regular', 'Python object')
    >>> c.py_func()
    'Regular'

    # Fused functions are callable without an instance
    # (This applies to everything in Py3 - see __doc__ below)
    >>> Regular.fused_func(1.5)
    ('float', 'double')
    >>> Regular.fused_func_0()
    ('int', 'int')
    >>> Regular.fused_func_0['double']()
    ('float', 'double')

    # fused_func_0 does not accept a "Regular" instance
    >>> c.fused_func_0()
    Traceback (most recent call last):
    TypeError: No matching signature found
    >>> c.fused_func_0['double']()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError:

    # Functions not expecting an argument don't work with an instance
    >>> c.regular_func_0()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError:
    >>> c.py_func_0()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: py_func_0() takes ... arguments ...1 ...given...
    """
    fused_func = fused_func
    fused_func_0 = fused_func_0
    regular_func = regular_func
    regular_func_0 = regular_func_0
    py_func = py_func
    py_func_0 = py_func_0

__doc__ = """
# tests to show PyClass is the same
>>> c = PyClass()
>>> c.py_func()
'PyClass'
>>> c.py_in_class()
'PyClass'
>>> c.py_func_0()  # doctest: +ELLIPSIS
Traceback (most recent call last):
TypeError: py_func_0() takes ... arguments ...1 ...given...
"""

import sys
if sys.version_info[0] > 2:
    # extra Py3 only tests - shows that functions added to a class can be called
    # with an type as the first argument
    __doc__ += """
    >>> Cdef.regular_func(1.5)
    ('float', 'Python object')
    >>> Cdef.py_func(1.5)
    'float'
    >>> Regular.regular_func(1.5)
    ('float', 'Python object')
    >>> Regular.py_func(1.5)
    'float'
    >>> PyClass.py_func(1.5)
    'float'
    >>> Cdef.regular_func_0()
    >>> Regular.regular_func_0()
    >>> Cdef.py_func_0()
    >>> Regular.py_func_0()
    >>> PyClass.py_func_0()
    """
