# mode: run
# tag: pep484, warnings

cimport cython
from cython cimport typeof


def old_dict_syntax(a: list, b: "int" = 2, c: {'ctype': 'long int'} = 3, d: {'type': 'float'} = 4) -> list:
    """
    >>> old_dict_syntax([1])
    ('list object', 'int', 'long', 'float')
    [1, 2, 3, 4.0]
    >>> old_dict_syntax([1], 3)
    ('list object', 'int', 'long', 'float')
    [1, 3, 3, 4.0]
    >>> old_dict_syntax(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def pytypes_def(a: list, b: int = 2, c: long = 3, d: float = 4) -> list:
    """
    >>> pytypes_def([1])
    ('list object', 'Python object', 'Python object', 'double')
    [1, 2, 3, 4.0]
    >>> pytypes_def([1], 3)
    ('list object', 'Python object', 'Python object', 'double')
    [1, 3, 3, 4.0]
    >>> pytypes_def(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


cpdef pytypes_cpdef(a: list, b: int = 2, c: long = 3, d: float = 4):
    """
    >>> pytypes_cpdef([1])
    ('list object', 'Python object', 'Python object', 'double')
    [1, 2, 3, 4.0]
    >>> pytypes_cpdef([1], 3)
    ('list object', 'Python object', 'Python object', 'double')
    [1, 3, 3, 4.0]
    >>> pytypes_cpdef(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


cdef c_pytypes_cdef(a: list, b: int = 2, c: long = 3, d: float = 4):
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def pytypes_cdef(a, b=2, c=3, d=4):
    """
    >>> pytypes_cdef([1])
    ('list object', 'Python object', 'Python object', 'double')
    [1, 2, 3, 4.0]
    >>> pytypes_cdef([1], 3)
    ('list object', 'Python object', 'Python object', 'double')
    [1, 3, 3, 4.0]
    >>> pytypes_cdef(123)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return c_pytypes_cdef(a, b, c, d)


def ctypes_def(a: list, b: cython.int = 2, c: cython.long = 3, d: cython.float = 4) -> list:
    """
    >>> ctypes_def([1])
    ('list object', 'int', 'long', 'float')
    [1, 2, 3, 4.0]
    >>> ctypes_def([1], 3)
    ('list object', 'int', 'long', 'float')
    [1, 3, 3, 4.0]
    >>> ctypes_def(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def return_tuple_for_carray() -> tuple:
    """
    >>> return_tuple_for_carray()
    (1, 2, 3)
    """
    cdef int[3] x
    x = [1, 2, 3]
    return x


MyStruct = cython.struct(x=cython.int, y=cython.int, data=cython.double)


@cython.ccall
def struct_io(s : MyStruct) -> MyStruct:
    """
    >>> d = struct_io(dict(x=1, y=2, data=3))
    >>> sorted(d.items())
    [('data', 3.0), ('x', 2), ('y', 1)]
    """
    t = s
    t.x, t.y = s.y, s.x
    return t


@cython.test_fail_if_path_exists(
    "//CoerceFromPyTypeNode",
    "//SimpleCallNode//CoerceToPyTypeNode",
)
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceToPyTypeNode//SimpleCallNode",
)
def call_struct_io(s : MyStruct) -> MyStruct:
    """
    >>> d = call_struct_io(dict(x=1, y=2, data=3))
    >>> sorted(d.items())
    [('data', 3.0), ('x', 2), ('y', 1)]
    """
    return struct_io(s)


@cython.test_assert_path_exists(
    "//CFuncDefNode",
    "//CFuncDefNode//DefNode",
    "//CFuncDefNode[@return_type]",
    "//CFuncDefNode[@return_type.is_struct_or_union = True]",
)
@cython.ccall
def struct_convert(d) -> MyStruct:
    """
    >>> d = struct_convert(dict(x=1, y=2, data=3))
    >>> sorted(d.items())
    [('data', 3.0), ('x', 1), ('y', 2)]
    >>> struct_convert({})  # make sure we can raise exceptions through struct return values
    Traceback (most recent call last):
    ValueError: No value specified for struct attribute 'x'
    """
    return d


@cython.test_assert_path_exists(
    "//CFuncDefNode",
    "//CFuncDefNode//DefNode",
    "//CFuncDefNode[@return_type]",
    "//CFuncDefNode[@return_type.is_int = True]",
)
@cython.ccall
def exception_default(raise_exc : cython.bint = False) -> cython.int:
    """
    >>> exception_default(raise_exc=False)
    10
    >>> exception_default(raise_exc=True)
    Traceback (most recent call last):
    ValueError: huhu!
    """
    if raise_exc:
        raise ValueError("huhu!")
    return 10


def call_exception_default(raise_exc=False):
    """
    >>> call_exception_default(raise_exc=False)
    10
    >>> call_exception_default(raise_exc=True)
    Traceback (most recent call last):
    ValueError: huhu!
    """
    return exception_default(raise_exc)


class EarlyClass(object):
    """
    >>> a = EarlyClass(1)
    >>> a.string_forward_declaration()  # should probably raise an error at some point
    1
    >>> x = LateClass()
    >>> a = EarlyClass(x)
    >>> x2 = a.string_forward_declaration()
    >>> assert x is x2, x2
    """
    def __init__(self, x):
        self.x = x
    def string_forward_declaration(self) -> 'LateClass':
        return self.x

class LateClass(object):
    pass


def py_float_default(price : float=None, ndigits=4):
    """
    Python default arguments should prevent C type inference.

    >>> py_float_default()
    (None, 4)
    >>> py_float_default(2)
    (2, 4)
    >>> py_float_default(2.0)
    (2.0, 4)
    >>> py_float_default(2, 3)
    (2, 3)
    """
    return price, ndigits


_WARNINGS = """
8:32: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
8:47: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
8:56: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
8:77: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
8:85: Python type declaration in signature annotation does not refer to a Python type
8:85: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
211:44: Unknown type declaration in annotation, ignoring
218:29: Ambiguous types in annotation, ignoring
# BUG:
46:6: 'pytypes_cpdef' redeclared
121:0: 'struct_io' redeclared
156:0: 'struct_convert' redeclared
175:0: 'exception_default' redeclared
"""
