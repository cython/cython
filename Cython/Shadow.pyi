from builtins import (int as py_int, float as py_float,
                      bool as py_bool, str as py_str, complex as py_complex)
from types import TracebackType
from typing import (Any, Sequence, Optional, Type,
                    TypeVar, Generic, Callable, overload)
# This is necessary so that type checkers don't ignore the 'dataclasses' import
# or the 'final' import from typing.
__all__ = (
    'dataclasses', 'final',  # from imports above
    'int', 'long', 'longlong', 'short', 'char', 'sint', 'slong', 'slonglong',
    'sshort', 'schar', 'uint', 'ulong', 'ulonglong', 'ushort', 'uchar',
    'size_t', 'Py_ssize_t',
    'Py_UCS4', 'Py_UNICODE',
    'float', 'double', 'longdouble',
    'complex', 'floatcomplex', 'doublecomplex', 'longdoublecomplex',
    'bint', 'void', 'basestring', 'unicode',
    'gs', 'compiled',
    'cfunc', 'compile', 'locals', 'returns',
    'cclass', 'c_api_binop_methods', 'type_version_tag',
    'boundscheck', 'wraparound', 'initializedcheck', 'nonecheck', 'cdivision', 'cdivision_warnings', 'profile',
    'linetrace', 'infer_types', 'emit_code_comments',
    'binding', 'embedsignature', 'always_allow_keywords', 'unraisable_tracebacks', 'iterable_coroutine', 'cpp_locals',
    'overflowcheck', 'optimize', 'warn',
    'inline', 'cdiv', 'cmod', 'cast', 'sizeof', 'typeof', 'address', 'declare',
    'nogil', 'gil',
    'CythonTypeObject', 'CythonType', 'PointerType', 'ArrayType',
    'pointer', 'array', 'struct', 'union', 'typedef', 'fused_type'
)

__version__: str

# Predefined types

int = py_int
long = py_int
longlong = py_int
short = py_int
char = py_int

sint = py_int
slong = py_int
slonglong = py_int
sshort = py_int
schar = py_int

uint = py_int
ulong = py_int
ulonglong = py_int
ushort = py_int
uchar = py_int

size_t = py_int
Py_ssize_t = py_int

Py_UCS4 = py_int | str
Py_UNICODE = py_int | str

float = py_float
double = py_float
longdouble = py_float

complex = py_complex
floatcomplex = py_complex
doublecomplex = py_complex
longdoublecomplex = py_complex

bint = py_bool
void = Type[None]
basestring = py_str
unicode = py_str

gs: dict[str, Any]  # Should match the return type of globals()

_T = TypeVar('_T')

compiled: bool

class _ArrayType(object, Generic[_T]):
    is_array: bool
    subtypes: Sequence[str]
    dtype: _T
    ndim: int
    is_c_contig: bool
    is_f_contig: bool
    inner_contig: bool
    broadcasting: Any

    # broadcasting is not used, so it's not clear about its type
    def __init__(self, dtype: _T, ndim: int, is_c_contig: bool = ...,
                 is_f_contig: bool = ..., inner_contig: bool = ...,
                 broadcasting: Any = ...) -> None: ...
    def __repr__(self) -> str: ...

class CythonTypeObject(object):
    ...

class CythonType(CythonTypeObject):
    ...

class PointerType(CythonType, Generic[_T]):
    def __init__(
        self,
        value: Optional[ArrayType[_T] | PointerType[_T] | list[_T] | int] = ...
    ) -> None: ...
    def __getitem__(self, ix: int) -> _T: ...
    def __setitem__(self, ix: int, value: _T) -> None: ...
    def __eq__(self, value: object) -> bool: ...
    def __repr__(self) -> str: ...

class ArrayType(PointerType[_T]):
    def __init__(self) -> None: ...

def index_type(
    base_type: _T, item: tuple | slice | int) -> _ArrayType[_T]: ...

def pointer(basetype: _T) -> Type[PointerType[_T]]: ...

def array(basetype: _T, n: int) -> Type[ArrayType[_T]]: ...

def struct(**members: type) -> Type[Any]: ...

def union(**members: type) -> Type[Any]: ...

class typedef(CythonType, Generic[_T]):
    name: str

    def __init__(self, type: _T, name: Optional[str] = ...) -> None: ...
    def __call__(self, *arg: Any) -> _T: ...
    def __repr__(self) -> str: ...
    __getitem__ = index_type

#class _FusedType(CythonType, Generic[_T]):
#    def __init__(self) -> None: ...

#def fused_type(*args: Tuple[_T]) -> Type[FusedType[_T]]: ...

def typeof(arg: Any) -> str: ...

_C = TypeVar('_C', bound='Callable')

class _EmptyDecoratorAndManager(object):
    def __call__(self, x: _C) -> _C: ...

    def __enter__(self) -> None: ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType]
    ) -> None: ...

cclass = ccall = cfunc = inline = _EmptyDecoratorAndManager()

def locals(**vars) -> Callable[[_C], _C]: ...

@overload
def declare(
    t: Optional[Callable[..., _T]] = ...,
    value: Any = ...,
    *,
    visibility: str = ...
) -> _T:
    ...

@overload
def declare(**kwargs: type) -> None: ...
