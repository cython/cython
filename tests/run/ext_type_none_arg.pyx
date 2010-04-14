
cimport cython


### extension types

cdef class MyExtType:
    cdef object attr
    def __cinit__(self):
        self.attr = 123

cdef attr(MyExtType x):
    return x is None and 321 or x.attr


# defaults, without 'not/or None'

def ext_default(MyExtType x):
    """
    >>> ext_default(MyExtType())
    123
    >>> ext_default(None)
    321
    """
    return attr(x)

@cython.allow_none_for_extension_args(True)
def ext_default_check_off(MyExtType x):
    """
    >>> ext_default_check_off(MyExtType())
    123
    >>> ext_default_check_off(None)
    321
    """
    return attr(x)

@cython.allow_none_for_extension_args(False)
def ext_default_check_on(MyExtType x):
    """
    >>> ext_default_check_on(MyExtType())
    123
    >>> ext_default_check_on(None)
    Traceback (most recent call last):
    TypeError: Argument 'x' has incorrect type (expected ext_type_none_arg.MyExtType, got NoneType)
    """
    return attr(x)


# with 'or/not None'

def ext_or_none(MyExtType x or None):
    """
    >>> ext_or_none(MyExtType())
    123
    >>> ext_or_none(None)
    321
    """
    return attr(x)

def ext_not_none(MyExtType x not None):
    """
    >>> ext_not_none(MyExtType())
    123
    >>> ext_not_none(None)
    Traceback (most recent call last):
    TypeError: Argument 'x' has incorrect type (expected ext_type_none_arg.MyExtType, got NoneType)
    """
    return attr(x)


### builtin types (using list)

cdef litem(list L, int item):
    return L is None and 321 or L[item]


# defaults, without 'not/or None'

def builtin_default(list L):
    """
    >>> builtin_default([123])
    123
    >>> builtin_default(None)
    321
    """
    return litem(L, 0)

@cython.allow_none_for_extension_args(True)
def builtin_default_check_off(list L):
    """
    >>> builtin_default_check_off([123])
    123
    >>> builtin_default_check_off(None)
    321
    """
    return litem(L, 0)

@cython.allow_none_for_extension_args(False)
def builtin_default_check_on(list L):
    """
    >>> builtin_default_check_on([123])
    123
    >>> builtin_default_check_on(None)
    Traceback (most recent call last):
    TypeError: Argument 'L' has incorrect type (expected list, got NoneType)
    """
    return litem(L, 0)


# with 'or/not None'

def builtin_or_none(list L or None):
    """
    >>> builtin_or_none([123])
    123
    >>> builtin_or_none(None)
    321
    """
    return litem(L, 0)

def builtin_not_none(list L not None):
    """
    >>> builtin_not_none([123])
    123
    >>> builtin_not_none(None)
    Traceback (most recent call last):
    TypeError: Argument 'L' has incorrect type (expected list, got NoneType)
    """
    return litem(L, 0)


## builtin type 'object' (which includes None!)  - currently unclear!

## def object_or_none(object o or None):
##     """
##     >>> object_or_none([])
##     list
##     >>> object_or_none(None)
##     NoneType
##     """
##     return type(o).__name__

## def object_not_none(object o not None):
##     """
##     >>> object_not_none([123])
##     123
##     >>> object_not_none(None)
##     Traceback (most recent call last):
##     TypeError: Argument 'o' has incorrect type (expected object, got NoneType)
##     """
##     return type(o).__name__
