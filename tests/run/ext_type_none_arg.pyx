
cimport cython
try:
    import typing
    from typing import Optional
except ImportError:
    pass  # Cython can still identify the use of "typing" even if the module doesn't exist


### extension types

cdef class MyExtType:
    cdef object attr
    def __cinit__(self):
        self.attr = 123

cdef attr(MyExtType x):
    return x is None and 321 or x.attr


# defaults, without 'not/or None'

def ext_default(MyExtType x): # currently behaves like 'or None'
    """
    >>> ext_default(MyExtType())
    123
    >>> ext_default(None)
    321
    """
    return attr(x)

@cython.allow_none_for_extension_args(False)
def ext_default_none(MyExtType x=None): # special cased default arg
    """
    >>> ext_default_none(MyExtType())
    123
    >>> ext_default_none(None)
    321
    >>> ext_default_none()
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

def ext_annotations(x: MyExtType):
    """
    Behaves the same as "MyExtType x not None"
    >>> ext_annotations(MyExtType())
    123
    >>> ext_annotations(None)
    Traceback (most recent call last):
    TypeError: Argument 'x' has incorrect type (expected ext_type_none_arg.MyExtType, got NoneType)
    """
    return attr(x)

@cython.allow_none_for_extension_args(False)
def ext_annotations_check_on(x: MyExtType):
    """
    >>> ext_annotations_check_on(MyExtType())
    123
    >>> ext_annotations_check_on(None)
    Traceback (most recent call last):
    TypeError: Argument 'x' has incorrect type (expected ext_type_none_arg.MyExtType, got NoneType)
    """
    return attr(x)

def ext_optional(x: typing.Optional[MyExtType], y: Optional[MyExtType]):
    """
    Behaves the same as "or None"
    >>> ext_optional(MyExtType(), MyExtType())
    246
    >>> ext_optional(MyExtType(), None)
    444
    >>> ext_optional(None, MyExtType())
    444
    """
    return attr(x) + attr(y)

### builtin types (using list)

cdef litem(list L, int item):
    return L is None and 321 or L[item]


# defaults, without 'not/or None'

def builtin_default(list L): # currently behaves like 'or None'
    """
    >>> builtin_default([123])
    123
    >>> builtin_default(None)
    321
    """
    return litem(L, 0)

@cython.allow_none_for_extension_args(False)
def builtin_default_none(list L=None): # special cased default arg
    """
    >>> builtin_default_none([123])
    123
    >>> builtin_default_none(None)
    321
    >>> builtin_default_none()
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


## builtin type 'object' - isinstance(None, object) is True!

@cython.allow_none_for_extension_args(False)
def object_default(object o): # always behaves like 'or None'
    """
    >>> object_default(object())
    'object'
    >>> object_default([])
    'list'
    >>> object_default(None)
    'NoneType'
    """
    return type(o).__name__

@cython.allow_none_for_extension_args(False)
def object_default_annotation(o : object):
    """
    >>> object_default_annotation(object())
    'object'
    >>> object_default_annotation([])
    'list'
    >>> object_default_annotation(None)
    'NoneType'
    """
    return type(o).__name__

# no decorator
def object_default_annotation2(o : object):
    """
    >>> object_default_annotation2(object())
    'object'
    >>> object_default_annotation2([])
    'list'
    >>> object_default_annotation2(None)
    'NoneType'
    """
    return type(o).__name__

@cython.allow_none_for_extension_args(False)
def object_default_none(object o=None): # behaves like 'or None'
    """
    >>> object_default_none(object())
    'object'
    >>> object_default_none([])
    'list'
    >>> object_default_none(None)
    'NoneType'
    >>> object_default_none()
    'NoneType'
    """
    return type(o).__name__

@cython.allow_none_for_extension_args(False)
def object_or_none(object o or None):
    """
    >>> object_or_none(object())
    'object'
    >>> object_or_none([])
    'list'
    >>> object_or_none(None)
    'NoneType'
    """
    return type(o).__name__

@cython.allow_none_for_extension_args(False)
def object_not_none(object o not None):
    """
    >>> object_not_none(object())
    'object'
    >>> object_not_none([])
    'list'
    >>> object_not_none(None)
    Traceback (most recent call last):
    TypeError: Argument 'o' must not be None
    """
    return type(o).__name__


## untyped 'object' - isinstance(None, object) is True!

@cython.allow_none_for_extension_args(False)
def notype_default(o): # behaves like 'or None'
    """
    >>> notype_default(object())
    'object'
    >>> notype_default([])
    'list'
    >>> notype_default(None)
    'NoneType'
    """
    return type(o).__name__

@cython.allow_none_for_extension_args(False)
def notype_default_none(o=None): # behaves like 'or None'
    """
    >>> notype_default_none(object())
    'object'
    >>> notype_default_none([])
    'list'
    >>> notype_default_none(None)
    'NoneType'
    >>> notype_default_none()
    'NoneType'
    """
    return type(o).__name__

@cython.allow_none_for_extension_args(False)
def notype_or_none(o or None):
    """
    >>> notype_or_none(object())
    'object'
    >>> notype_or_none([])
    'list'
    >>> notype_or_none(None)
    'NoneType'
    """
    return type(o).__name__

@cython.allow_none_for_extension_args(False)
def notype_not_none(o not None):
    """
    >>> notype_not_none(object())
    'object'
    >>> notype_not_none([])
    'list'
    >>> notype_not_none(None)
    Traceback (most recent call last):
    TypeError: Argument 'o' must not be None
    """
    return type(o).__name__
