# mode: run
# tag: pure2.7

# cython: binding=True

import cython

def regular(x):
    """
    >>> hasattr(regular, "__self__")
    False
    >>> nested = regular(10)
    >>> hasattr(nested, "__self__")
    False
    """
    def nested(y):
        return x+y
    return nested

@cython.locals(x=cython.floating)
def fused(x):
    """
    >>> nested = fused(10.)
    >>> hasattr(nested, "__self__")
    False

    >>> hasattr(fused, "__self__")
    False
    """
    def nested_in_fused(y):
        return x+y
    return nested_in_fused

# FIXME - doesn't currently work at all
#def get_nested_fused(x):
#    @cython.locals(x=cython.floating)
#    def nested_fused(y):
#        return x+y
#    return nested_fused

class C:
    """
    >>> c = C()
    >>> c.regular.__self__ is c
    True
    >>> c.fused.__self__ is c
    True

    >>> hasattr(C.regular, "__self__")  # __self__==None on pure-python 2
    False

    >>> C.fused.__self__  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: ...__self__...
    """
    def regular(self):
        pass

    @cython.locals(x=cython.floating)
    def fused(self, x):
        return x


if cython.compiled:
    __doc__ = """
    >>> hasattr(fused['double'], '__self__')
    False

    >>> hasattr(C.fused['double'], '__self__')
    False

    >>> c = C()
    >>> c.fused['double'].__self__ is c
    True

    # The PR that changed __self__ also changed how __doc__ is set up slightly
    >>> fused['double'].__doc__ == fused.__doc__ and isinstance(fused.__doc__, str)
    True
"""
