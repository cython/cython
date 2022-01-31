# mode: run
# tag: pep484, warnings

cimport cython
from cython cimport typeof
from cpython.ref cimport PyObject

try:
    from typing import Optional
except ImportError:
    pass


def old_dict_syntax(a: list, b: "int" = 2, c: {'ctype': 'long int'} = 3, d: {'type': 'long int'} = 4) -> list:
    """
    >>> old_dict_syntax([1])
    ('list object', 'int object', 'long', 'long')
    [1, 2, 3, 4]
    >>> old_dict_syntax([1], 3)
    ('list object', 'int object', 'long', 'long')
    [1, 3, 3, 4]
    >>> old_dict_syntax(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    >>> old_dict_syntax(None)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got NoneType)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def pytypes_def(a: list, b: int = 2, c: long = 3, d: float = 4.0, n: list = None, o: Optional[tuple] = ()) -> list:
    """
    >>> pytypes_def([1])
    ('list object', 'int object', 'long object', 'double', 'list object', 'tuple object')
    [1, 2, 3, 4.0, None, ()]
    >>> pytypes_def([1], 3)
    ('list object', 'int object', 'long object', 'double', 'list object', 'tuple object')
    [1, 3, 3, 4.0, None, ()]
    >>> pytypes_def([1], 3, 2, 1, [], None)
    ('list object', 'int object', 'long object', 'double', 'list object', 'tuple object')
    [1, 3, 2, 1.0, [], None]
    >>> pytypes_def(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    >>> pytypes_def(None)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got NoneType)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d), typeof(n), typeof(o))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(n)
    a.append(o)
    return a


cpdef pytypes_cpdef(a: list, b: int = 2, c: long = 3, d: float = 4.0, n: list = None, o: Optional[tuple] = ()):
    """
    >>> pytypes_cpdef([1])
    ('list object', 'int object', 'long object', 'double', 'list object', 'tuple object')
    [1, 2, 3, 4.0, None, ()]
    >>> pytypes_cpdef([1], 3)
    ('list object', 'int object', 'long object', 'double', 'list object', 'tuple object')
    [1, 3, 3, 4.0, None, ()]
    >>> pytypes_cpdef([1], 3, 2, 1, [], None)
    ('list object', 'int object', 'long object', 'double', 'list object', 'tuple object')
    [1, 3, 2, 1.0, [], None]
    >>> pytypes_cpdef(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    >>> pytypes_cpdef(None)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got NoneType)
    """
    print(typeof(a), typeof(b), typeof(c), typeof(d), typeof(n), typeof(o))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(n)
    a.append(o)
    return a


cdef c_pytypes_cdef(a: list, b: int = 2, c: long = 3, d: float = 4.0, n: list = None):
    print(typeof(a), typeof(b), typeof(c), typeof(d), typeof(n))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(n)
    return a


def pytypes_cdef(a, b=2, c=3, d=4):
    """
    >>> pytypes_cdef([1])
    ('list object', 'int object', 'long object', 'double', 'list object')
    [1, 2, 3, 4.0, None]
    >>> pytypes_cdef([1], 3)
    ('list object', 'int object', 'long object', 'double', 'list object')
    [1, 3, 3, 4.0, None]
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
    >>> d = struct_io(None)
    Traceback (most recent call last):
    TypeError: Expected a mapping, got NoneType
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
    >>> d = call_struct_io(None)
    Traceback (most recent call last):
    TypeError: Expected a mapping, got NoneType
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


@cython.test_assert_path_exists(
    "//CFuncDefNode",
    "//CFuncDefNode//DefNode",
    "//CFuncDefNode[@return_type]",
    "//CFuncDefNode[@return_type.is_int = True]",
)
@cython.ccall
def exception_default_uint(raise_exc : cython.bint = False) -> cython.uint:
    """
    >>> print(exception_default_uint(raise_exc=False))
    10
    >>> exception_default_uint(raise_exc=True)
    Traceback (most recent call last):
    ValueError: huhu!
    """
    if raise_exc:
        raise ValueError("huhu!")
    return 10


def call_exception_default_uint(raise_exc=False):
    """
    >>> print(call_exception_default_uint(raise_exc=False))
    10
    >>> call_exception_default_uint(raise_exc=True)
    Traceback (most recent call last):
    ValueError: huhu!
    """
    return exception_default_uint(raise_exc)


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
    >>> py_float_default(2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...float...
    >>> py_float_default(2.0)
    (2.0, 4)
    >>> py_float_default(2, 3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...float...
    """
    return price, ndigits


cdef class ClassAttribute:
    cls_attr : cython.float = 1.


@cython.cfunc
def take_ptr(obj: cython.pointer(PyObject)):
    pass

def call_take_ptr():
    """
    >>> call_take_ptr()  # really just a compile-test
    """
    python_dict = {"abc": 123}
    take_ptr(cython.cast(cython.pointer(PyObject), python_dict))

@cython.cclass
class HasPtr:
    """
    >>> HasPtr()
    HasPtr(1, 1)
    """
    a: cython.pointer(cython.int)
    b: cython.int

    def __init__(self):
        self.b = 1
        self.a = cython.address(self.b)
    def __repr__(self):
        return f"HasPtr({self.a[0]}, {self.b})"


_WARNINGS = """
14:32: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
14:47: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
14:56: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
14:77: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
14:85: Python type declaration in signature annotation does not refer to a Python type
14:85: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
36:64: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
63:68: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
90:68: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
274:44: Unknown type declaration in annotation, ignoring
300:15: Annotation ignored since class-level attributes must be Python objects. Were you trying to set up an instance attribute?
# BUG:
63:6: 'pytypes_cpdef' redeclared
146:0: 'struct_io' redeclared
181:0: 'struct_convert' redeclared
200:0: 'exception_default' redeclared
231:0: 'exception_default_uint' redeclared
"""
