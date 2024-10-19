# mode: run
# tag: pep484, warnings
# cython: language_level=3

cimport cython
from cython cimport typeof
from cpython.ref cimport PyObject

try:
    from typing import Optional, Union
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
    print((typeof(a), typeof(b), typeof(c), typeof(d)))
    a.append(b)
    a.append(c)
    a.append(d)
    return a


def pytypes_def(a: list, b: int = 2, c: long = 3, d: float = 4.0, n: list = None, o: Optional[tuple] = (), v: Union[tuple, None]=(), u: tuple | None = ()) -> list:
    """
    >>> pytypes_def([1])
    ('list object', 'int object', 'Python object', 'double', 'list object', 'tuple object', 'tuple object', 'tuple object')
    [1, 2, 3, 4.0, None, (), (), ()]
    >>> pytypes_def([1], 3)
    ('list object', 'int object', 'Python object', 'double', 'list object', 'tuple object', 'tuple object', 'tuple object')
    [1, 3, 3, 4.0, None, (), (), ()]
    >>> pytypes_def([1], 3, 2, 1, [], None, None, None)
    ('list object', 'int object', 'Python object', 'double', 'list object', 'tuple object', 'tuple object', 'tuple object')
    [1, 3, 2, 1.0, [], None, None, None]
    >>> pytypes_def([1], 3, 2, 1, [], 'a', (), ())
    Traceback (most recent call last):
    TypeError: Argument 'o' has incorrect type (expected tuple, got str)
    >>> pytypes_def([1], 3, 2, 1, [], (), 'a')
    Traceback (most recent call last):
    TypeError: Argument 'v' has incorrect type (expected tuple, got str)
    >>> pytypes_def([1], 3, 2, 1, [], (), (), 'a')
    Traceback (most recent call last):
    TypeError: Argument 'u' has incorrect type (expected tuple, got str)
    >>> pytypes_def(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    >>> pytypes_def(None)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got NoneType)
    """
    print((typeof(a), typeof(b), typeof(c), typeof(d), typeof(n), typeof(o), typeof(v), typeof(u)))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(n)
    a.append(o)
    a.append(v)
    a.append(u)
    return a


cpdef pytypes_cpdef(a: list, b: int = 2, c: long = 3, d: float = 4.0, n: list = None, o: Optional[tuple] = (), v: Union[tuple, None]=(), u: tuple | None = ()):
    """
    >>> pytypes_cpdef([1])
    ('list object', 'int object', 'Python object', 'double', 'list object', 'tuple object', 'tuple object', 'tuple object')
    [1, 2, 3, 4.0, None, (), (), ()]
    >>> pytypes_cpdef([1], 3)
    ('list object', 'int object', 'Python object', 'double', 'list object', 'tuple object', 'tuple object', 'tuple object')
    [1, 3, 3, 4.0, None, (), (), ()]
    >>> pytypes_cpdef([1], 3, 2, 1, [], None, None, None)
    ('list object', 'int object', 'Python object', 'double', 'list object', 'tuple object', 'tuple object', 'tuple object')
    [1, 3, 2, 1.0, [], None, None, None]
    >>> pytypes_cpdef([1], 3, 2, 1, [], 'a', (), ())
    Traceback (most recent call last):
    TypeError: Argument 'o' has incorrect type (expected tuple, got str)
    >>> pytypes_cpdef([1], 3, 2, 1, [], (), 'a', ())
    Traceback (most recent call last):
    TypeError: Argument 'v' has incorrect type (expected tuple, got str)
    >>> pytypes_cpdef([1], 3, 2, 1, [], (), (), 'a')
    Traceback (most recent call last):
    TypeError: Argument 'u' has incorrect type (expected tuple, got str)
    >>> pytypes_cpdef(123)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got int)
    >>> pytypes_cpdef(None)
    Traceback (most recent call last):
    TypeError: Argument 'a' has incorrect type (expected list, got NoneType)
    """
    print((typeof(a), typeof(b), typeof(c), typeof(d), typeof(n), typeof(o), typeof(v), typeof(u)))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(n)
    a.append(o)
    a.append(v)
    a.append(u)
    return a


cdef c_pytypes_cdef(a: list, b: int = 2, c: long = 3, d: float = 4.0, n: list = None):
    print((typeof(a), typeof(b), typeof(c), typeof(d), typeof(n)))
    a.append(b)
    a.append(c)
    a.append(d)
    a.append(n)
    return a


def pytypes_cdef(a, b=2, c=3, d=4):
    """
    >>> pytypes_cdef([1])
    ('list object', 'int object', 'Python object', 'double', 'list object')
    [1, 2, 3, 4.0, None]
    >>> pytypes_cdef([1], 3)
    ('list object', 'int object', 'Python object', 'double', 'list object')
    [1, 3, 3, 4.0, None]
    >>> pytypes_cdef(123)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return c_pytypes_cdef(a, b, c, d)


def pyint(a: int):
    """
    >>> large_int = eval('0x'+'F'*64)  # definitely bigger than C int64
    >>> pyint(large_int) == large_int
    True
    """
    return a


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
    print((typeof(a), typeof(b), typeof(c), typeof(d)))
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


def invalid_ctuple_syntax(a: (cython.int, cython.int), b: (int, int)):
    """
    >>> invalid_ctuple_syntax([1, 2], [3, 4])
    [1, 2, 3, 4]
    """
    result: (cython.int, cython.int, cython.int, cython.int) = a + b
    return result


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


def py_float_default(price : Optional[float]=None, bar: Union[float, None]=None, spam: float | None = None, ndigits=4):
    """
    Python default arguments should prevent C type inference.

    >>> py_float_default()
    (None, None, None, 4)
    >>> py_float_default(None)
    (None, None, None, 4)
    >>> py_float_default(2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...float...
    >>> py_float_default(2.0, 3.0, 4.0)
    (2.0, 3.0, 4.0, 4)
    >>> py_float_default(2, None, None, 4)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...float...
    >>> py_float_default(None, 2, None, 4)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...float...
    """
    return price, bar, spam, ndigits


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


@cython.annotation_typing(False)
def turn_off_typing(x: float, d: dict):
    """
    >>> turn_off_typing('not a float', [])  # ignore the typing
    ('Python object', 'Python object', 'not a float', [])
    """
    return typeof(x), typeof(d), x, d


@cython.annotation_typing(False)
cdef class ClassTurnOffTyping:
    x: float
    d: dict

    def get_var_types(self, arg: float):
        """
        >>> ClassTurnOffTyping().get_var_types(1.0)
        ('Python object', 'Python object', 'Python object')
        """
        return typeof(self.x), typeof(self.d), typeof(arg)

    @cython.annotation_typing(True)
    def and_turn_it_back_on_again(self, arg: float):
        """
        >>> ClassTurnOffTyping().and_turn_it_back_on_again(1.0)
        ('Python object', 'Python object', 'double')
        """
        return typeof(self.x), typeof(self.d), typeof(arg)


from cython cimport int as cy_i


def int_alias(a: cython.int, b: cy_i):
    """
    >>> int_alias(1, 2)
    int
    int
    """
    print(cython.typeof(a))
    print(cython.typeof(b))


def test_inexact_types(d: dict):
    """
    >>> test_inexact_types({})  # good

    Check that our custom pep484 warning is in either the error message
    or the exception notes
    >>> from collections import OrderedDict
    >>> try:
    ...    test_inexact_types(OrderedDict())
    ... except TypeError as e:
    ...    assert ("Cython is deliberately stricter than PEP-484" in e.args[0] or
    ...            any("Cython is deliberately stricter than PEP-484" in note for note in getattr(e, "__notes__", []))), e
    ... else:
    ...    assert False
    """
    pass


def pytypes_multi_union(a: Union[list, tuple, None], b: list | tuple | None):
    """
    >>> pytypes_multi_union([1], [2])
    ('Python object', 'Python object')
    [[1], [2]]
    >>> pytypes_multi_union((1,), (2,))
    ('Python object', 'Python object')
    [(1,), (2,)]
    >>> pytypes_multi_union(1, 2)
    ('Python object', 'Python object')
    [1, 2]
    """
    print((typeof(a), typeof(b)))
    return [a, b]

_WARNINGS = """
15:32: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
15:47: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
15:56: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
15:77: Dicts should no longer be used as type annotations. Use 'cython.int' etc. directly.
15:85: Python type declaration in signature annotation does not refer to a Python type
15:85: Strings should no longer be used for type declarations. Use 'cython.int' etc. directly.
37:40: Found C type name 'long' in a Python annotation. Did you mean to use 'cython.long'?
37:40: Unknown type declaration 'long' in annotation, ignoring
37:66: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
75:44: Found C type name 'long' in a Python annotation. Did you mean to use 'cython.long'?
75:44: Unknown type declaration 'long' in annotation, ignoring
75:70: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
113:44: Found C type name 'long' in a Python annotation. Did you mean to use 'cython.long'?
113:44: Unknown type declaration 'long' in annotation, ignoring
113:70: PEP-484 recommends 'typing.Optional[...]' for arguments that can be None.
175:30: Tuples cannot be declared as simple tuples of types. Use 'tuple[type1, type2, ...]'.
175:59: Tuples cannot be declared as simple tuples of types. Use 'tuple[type1, type2, ...]'.
180:13: Tuples cannot be declared as simple tuples of types. Use 'tuple[type1, type2, ...]'.
315:44: Unknown type declaration in annotation, ignoring
346:15: Annotation ignored since class-level attributes must be Python objects. Were you trying to set up an instance attribute?
437:32: Unknown type declaration in annotation, ignoring
437:69: Unknown type declaration in annotation, ignoring
# DUPLICATE:
75:44: Found C type name 'long' in a Python annotation. Did you mean to use 'cython.long'?
75:44: Unknown type declaration 'long' in annotation, ignoring
# BUG:
75:0: 'pytypes_cpdef' redeclared
187:0: 'struct_io' redeclared
222:0: 'struct_convert' redeclared
241:0: 'exception_default' redeclared
272:0: 'exception_default_uint' redeclared
"""
