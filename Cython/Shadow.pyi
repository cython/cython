import dataclasses
from builtins import (int as py_int, float as py_float,
                      bool as py_bool, str as py_str, complex as py_complex)
from types import TracebackType
from typing import (Any, ContextManager, Iterable, Literal, ParamSpec, Sequence, Optional, Type,
                    TypeVar, Generic, Callable, final, overload)

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
    'cclass', 'c_api_binop_methods', 'type_version_tag',
    'cfunc', 'ccall', 'compile', 'locals', 'returns', 'exceptval',
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
compiled: bool


_T = TypeVar('_T')
_P = ParamSpec('_P')
_C = TypeVar('_C', bound='Callable')
_TypeT = TypeVar('_TypeT', bound='Type')
Decorator = Callable[[_C], _C]


def _func_deco(__func: _C) -> _C: ...

cfunc = ccall = compile = _func_deco

def locals(**kwargs: Any) -> Decorator: ...

def _class_deco(__cls: _TypeT) -> _TypeT: ...

cclass = c_api_binop_methods = type_version_tag = _class_deco

# May be a bit hard to read but essentially means:
# > Returns a callable that takes another callable with these parameters and *some*
# > return value, then returns another callable with the same parameters but the
# > the return type is the previous 'type' parameter.
def returns(__type: _T) -> Callable[[Callable[_P, object]], Callable[_P, _T]]: ...

def exceptval(__val: Any, *, check: bool = False) -> Decorator: ...

class _EmptyDecoratorAndManager(object):
    @overload
    def __call__(self, __val: bool) -> Decorator: ...

    @overload
    def __call__(self, __func: _C) -> _C: ...

    def __enter__(self) -> None: ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType]
    ) -> None: ...

@overload
def _compiler_directive(__func: _C) -> _C: ...

@overload
def _compiler_directive(__val: bool = ...) -> Decorator: ...

# These all come from 'Compiler directives' on Source Files and Compilation.
# The following directives are missing as they need to be global:
# - annotation_typing
# - c_string_type
# - c_string_encoding
# Note that c_api_binop_methods and type_version_tag is defined above.

boundscheck = wraparound = initializedcheck = nonecheck = cdivision = \
    cdivision_warnings = profile = linetrace = infer_types = \
    emit_code_comments = _EmptyDecoratorAndManager()

binding = embedsignature = always_allow_keywords = unraisable_tracebacks = \
    iterable_coroutine = cpp_locals = _compiler_directive

# overflowcheck() has to be specialized because there is also overflowcheck.fold
class _OverflowcheckClass:
    def __call__(self, __val: bool = ...) -> Decorator: ...

    def fold(self, __val: bool = ...) -> Decorator: ...

overflowcheck = _OverflowcheckClass()

class optimize:
    @staticmethod
    def use_switch(__val: bool = ...) -> Decorator: ...

    @staticmethod
    def unpack_method_calls(__val: bool = ...) -> Decorator: ...

class warn:
    @staticmethod
    def undeclared(__val: bool = ...) -> Decorator: ...

    @staticmethod
    def unreachable(__val: bool = ...) -> Decorator: ...

    @staticmethod
    def maybe_uninitialized(__val: bool = ...) -> Decorator: ...

    @staticmethod
    def unused(__val: bool = ...) -> Decorator: ...

    @staticmethod
    def unused_argument(__val: bool = ...) -> Decorator: ...

    @staticmethod
    def multiple_declarators(__val: bool = ...) -> Decorator: ...

@overload
def inline(__func: _C) -> _C: ...

@overload
def inline(__code: str, *, get_type: Callable[[object, object], str] = ..., lib_dir: str = ...,
           cython_include_dirs: Iterable[str] = ..., cython_compiler_directives: Iterable[str] = ...,
           force: bool = ..., quiet: bool = ..., locals: dict[str, str] = ..., globals: dict[str, str] = ...,
           language_level: str = ...) -> Any: ...

def cdiv(__a: int, __b: int) -> int: ...

def cmod(__a: int, __b: int) -> int: ...

@overload
def cast(__t: _T, __value: Any) -> _T: ...

@overload
def cast(__t: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs) -> _T: ...

def sizeof(__obj: object) -> int: ...

def typeof(__obj: object) -> str: ...

def address(__obj: object) -> PointerType: ...


@overload
def declare(
    t: Optional[Callable[..., _T]] = ...,
    value: Any = ...,
) -> _T:
    ...

# This one is for attributes, they cannot have initializers through cython.declare() currently.
@overload
def declare(
    t: Callable[..., _T],
    *,
    visibility: Literal['public', 'readonly', 'private'] = ...,
) -> _T:
    ...

@overload
def declare(**kwargs: type) -> None: ...


class _nogil:
    @overload
    def __call__(self) -> ContextManager: ...

    @overload
    def __call__(self, __val: bool) -> Decorator: ...

    @overload
    def __call__(self, __func: _C) -> _C: ...

    def __enter__(self) -> None: ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType]
    ) -> None: ...

nogil = gil = _nogil


class _ArrayType(Generic[_T]):
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

def fused_type(*args: Any) -> Any: ...
