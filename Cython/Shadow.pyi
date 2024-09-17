import dataclasses as dataclasses
from builtins import (int as py_int, float as py_float,
                      bool as py_bool, str as py_str, complex as py_complex)
from types import TracebackType
from typing import (
    Any, Iterable, Sequence, Optional, Type, TypeVar, Generic, Callable, overload,
    TypeAlias, Annotated,
)

# Type checkers assume typing_extensions is always present
from typing_extensions import Literal, ParamSpec, overload, final as final

# Normally all imports aren't exported in stub files but we can explicitly expose
# imports by using import ... as ... (with the same name) which was done for
# dataclasses and the final decorator.

__version__: str

# Predefined types

Py_UCS4 = py_int | str
Py_UNICODE = py_int | str

bint = py_bool
void = Type[None]
basestring = py_str
unicode = py_str

compiled: bool


_T = TypeVar('_T')
_P = ParamSpec('_P')
_C = TypeVar('_C', bound='Callable')
_TypeT = TypeVar('_TypeT', bound='Type')
_Decorator = Callable[[_C], _C]


_func_deco: _Decorator

cfunc = ccall = compile = _func_deco

def locals(**kwargs: Any) -> _Decorator: ...

def _class_deco(__cls: _TypeT) -> _TypeT: ...

cclass = internal = c_api_binop_methods = type_version_tag = no_gc_clear = no_gc = _class_deco

# May be a bit hard to read but essentially means:
# > Returns a callable that takes another callable with these parameters and *some*
# > return value, then returns another callable with the same parameters but
# > the return type is the previous 'type' parameter.
# On Python 3.5, the latest version of Mypy available is 0.910 which doesn't understand ParamSpec
def returns(__type: Type[_T]) -> Callable[[Callable[_P, object]], Callable[_P, _T]]: ...  # type: ignore

def exceptval(__val: Any, *, check: bool = False) -> _Decorator: ...

class _EmptyDecoratorAndManager(object):
    @overload
    def __call__(self, __val: bool) -> _Decorator: ...

    @overload
    def __call__(self, __func: _C) -> _C: ...

    def __enter__(self) -> None: ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType]
    ) -> None: ...
_empty_decorator_and_manager: _EmptyDecoratorAndManager

@overload
def _compiler_directive(__func: _C) -> _C: ...

@overload
def _compiler_directive(__val: bool = ...) -> _Decorator: ...

# These all come from 'Compiler directives' on Source Files and Compilation.
# The following directives are missing as they need to be global:
# - annotation_typing
# - c_string_type
# - c_string_encoding
# Note that c_api_binop_methods and type_version_tag is defined above.

boundscheck = wraparound = initializedcheck = nonecheck = cdivision = \
    cdivision_warnings = profile = linetrace = infer_types = \
    emit_code_comments = _empty_decorator_and_manager

binding = embedsignature = always_allow_keywords = unraisable_tracebacks = \
    iterable_coroutine = cpp_locals = _compiler_directive

# overflowcheck() has to be specialized because there is also overflowcheck.fold
class _OverflowcheckClass:
    def __call__(self, __val: bool = ...) -> _Decorator: ...

    def fold(self, __val: bool = ...) -> _Decorator: ...

overflowcheck = _OverflowcheckClass()

class optimize:
    @staticmethod
    def use_switch(__val: bool = ...) -> _Decorator: ...

    @staticmethod
    def unpack_method_calls(__val: bool = ...) -> _Decorator: ...

class warn:
    @staticmethod
    def undeclared(__val: bool = ...) -> _Decorator: ...

    @staticmethod
    def unreachable(__val: bool = ...) -> _Decorator: ...

    @staticmethod
    def maybe_uninitialized(__val: bool = ...) -> _Decorator: ...

    @staticmethod
    def unused(__val: bool = ...) -> _Decorator: ...

    @staticmethod
    def unused_argument(__val: bool = ...) -> _Decorator: ...

    @staticmethod
    def multiple_declarators(__val: bool = ...) -> _Decorator: ...

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
def cast(__t: Type[_T], __value: Any) -> _T: ...

# On Python 3.5, the latest version of Mypy available is 0.910 which doesn't understand ParamSpec
@overload
def cast(__t: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs) -> _T: ...  # type: ignore

def sizeof(__obj: object) -> int: ...

def typeof(__obj: object) -> str: ...

def address(__obj: object) -> PointerType: ...

type const[T] = Annotated[T, "cython.const"]
type volatile[T] = Annotated[T, "cython.volatile"]


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
    def __call__(self, __val: bool) -> _Decorator: ...

    @overload
    def __call__(self, __func: _C) -> _C: ...

    @overload
    def __call__(self) -> '_nogil': ...

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

def fused_type(*args: Any) -> Type[Any]: ...


class typedef(CythonType, Generic[_T]):
    name: str

    def __init__(self, type: _T, name: Optional[str] = ...) -> None: ...
    def __call__(self, *arg: Any) -> _T: ...
    def __repr__(self) -> str: ...
    __getitem__ = index_type


##### START: GENERATED LIST OF GENERATED TYPES #####
# Generated by "bin/cython-generate-shadow-pyi.py" on 2024-09-17 20:41:27.411413

p_const_bint = PointerType[const[bint]]
pp_const_bint = PointerType[PointerType[const[bint]]]
ppp_const_bint = PointerType[PointerType[PointerType[const[bint]]]]
p_bint = PointerType[bint]
pp_bint = PointerType[PointerType[bint]]
ppp_bint = PointerType[PointerType[PointerType[bint]]]
char : TypeAlias = py_int
p_const_char = PointerType[const[py_int]]
pp_const_char = PointerType[PointerType[const[py_int]]]
ppp_const_char = PointerType[PointerType[PointerType[const[py_int]]]]
p_char = PointerType[py_int]
pp_char = PointerType[PointerType[py_int]]
ppp_char = PointerType[PointerType[PointerType[py_int]]]
complex : TypeAlias = py_complex
p_const_complex = PointerType[const[py_complex]]
pp_const_complex = PointerType[PointerType[const[py_complex]]]
ppp_const_complex = PointerType[PointerType[PointerType[const[py_complex]]]]
p_complex = PointerType[py_complex]
pp_complex = PointerType[PointerType[py_complex]]
ppp_complex = PointerType[PointerType[PointerType[py_complex]]]
double : TypeAlias = py_float
p_const_double = PointerType[const[py_float]]
pp_const_double = PointerType[PointerType[const[py_float]]]
ppp_const_double = PointerType[PointerType[PointerType[const[py_float]]]]
p_double = PointerType[py_float]
pp_double = PointerType[PointerType[py_float]]
ppp_double = PointerType[PointerType[PointerType[py_float]]]
doublecomplex : TypeAlias = py_complex
p_const_doublecomplex = PointerType[const[py_complex]]
pp_const_doublecomplex = PointerType[PointerType[const[py_complex]]]
ppp_const_doublecomplex = PointerType[PointerType[PointerType[const[py_complex]]]]
p_doublecomplex = PointerType[py_complex]
pp_doublecomplex = PointerType[PointerType[py_complex]]
ppp_doublecomplex = PointerType[PointerType[PointerType[py_complex]]]
float : TypeAlias = py_float
p_const_float = PointerType[const[py_float]]
pp_const_float = PointerType[PointerType[const[py_float]]]
ppp_const_float = PointerType[PointerType[PointerType[const[py_float]]]]
p_float = PointerType[py_float]
pp_float = PointerType[PointerType[py_float]]
ppp_float = PointerType[PointerType[PointerType[py_float]]]
floatcomplex : TypeAlias = py_complex
p_const_floatcomplex = PointerType[const[py_complex]]
pp_const_floatcomplex = PointerType[PointerType[const[py_complex]]]
ppp_const_floatcomplex = PointerType[PointerType[PointerType[const[py_complex]]]]
p_floatcomplex = PointerType[py_complex]
pp_floatcomplex = PointerType[PointerType[py_complex]]
ppp_floatcomplex = PointerType[PointerType[PointerType[py_complex]]]
int : TypeAlias = py_int
p_const_int = PointerType[const[py_int]]
pp_const_int = PointerType[PointerType[const[py_int]]]
ppp_const_int = PointerType[PointerType[PointerType[const[py_int]]]]
p_int = PointerType[py_int]
pp_int = PointerType[PointerType[py_int]]
ppp_int = PointerType[PointerType[PointerType[py_int]]]
long : TypeAlias = py_int
p_const_long = PointerType[const[py_int]]
pp_const_long = PointerType[PointerType[const[py_int]]]
ppp_const_long = PointerType[PointerType[PointerType[const[py_int]]]]
p_long = PointerType[py_int]
pp_long = PointerType[PointerType[py_int]]
ppp_long = PointerType[PointerType[PointerType[py_int]]]
py_long : TypeAlias = py_int
longdouble : TypeAlias = py_float
p_const_longdouble = PointerType[const[py_float]]
pp_const_longdouble = PointerType[PointerType[const[py_float]]]
ppp_const_longdouble = PointerType[PointerType[PointerType[const[py_float]]]]
p_longdouble = PointerType[py_float]
pp_longdouble = PointerType[PointerType[py_float]]
ppp_longdouble = PointerType[PointerType[PointerType[py_float]]]
longdoublecomplex : TypeAlias = py_complex
p_const_longdoublecomplex = PointerType[const[py_complex]]
pp_const_longdoublecomplex = PointerType[PointerType[const[py_complex]]]
ppp_const_longdoublecomplex = PointerType[PointerType[PointerType[const[py_complex]]]]
p_longdoublecomplex = PointerType[py_complex]
pp_longdoublecomplex = PointerType[PointerType[py_complex]]
ppp_longdoublecomplex = PointerType[PointerType[PointerType[py_complex]]]
longlong : TypeAlias = py_int
p_const_longlong = PointerType[const[py_int]]
pp_const_longlong = PointerType[PointerType[const[py_int]]]
ppp_const_longlong = PointerType[PointerType[PointerType[const[py_int]]]]
p_longlong = PointerType[py_int]
pp_longlong = PointerType[PointerType[py_int]]
ppp_longlong = PointerType[PointerType[PointerType[py_int]]]
schar : TypeAlias = py_int
p_const_schar = PointerType[const[py_int]]
pp_const_schar = PointerType[PointerType[const[py_int]]]
ppp_const_schar = PointerType[PointerType[PointerType[const[py_int]]]]
p_schar = PointerType[py_int]
pp_schar = PointerType[PointerType[py_int]]
ppp_schar = PointerType[PointerType[PointerType[py_int]]]
short : TypeAlias = py_int
p_const_short = PointerType[const[py_int]]
pp_const_short = PointerType[PointerType[const[py_int]]]
ppp_const_short = PointerType[PointerType[PointerType[const[py_int]]]]
p_short = PointerType[py_int]
pp_short = PointerType[PointerType[py_int]]
ppp_short = PointerType[PointerType[PointerType[py_int]]]
sint : TypeAlias = py_int
p_const_sint = PointerType[const[py_int]]
pp_const_sint = PointerType[PointerType[const[py_int]]]
ppp_const_sint = PointerType[PointerType[PointerType[const[py_int]]]]
p_sint = PointerType[py_int]
pp_sint = PointerType[PointerType[py_int]]
ppp_sint = PointerType[PointerType[PointerType[py_int]]]
slong : TypeAlias = py_int
p_const_slong = PointerType[const[py_int]]
pp_const_slong = PointerType[PointerType[const[py_int]]]
ppp_const_slong = PointerType[PointerType[PointerType[const[py_int]]]]
p_slong = PointerType[py_int]
pp_slong = PointerType[PointerType[py_int]]
ppp_slong = PointerType[PointerType[PointerType[py_int]]]
slonglong : TypeAlias = py_int
p_const_slonglong = PointerType[const[py_int]]
pp_const_slonglong = PointerType[PointerType[const[py_int]]]
ppp_const_slonglong = PointerType[PointerType[PointerType[const[py_int]]]]
p_slonglong = PointerType[py_int]
pp_slonglong = PointerType[PointerType[py_int]]
ppp_slonglong = PointerType[PointerType[PointerType[py_int]]]
sshort : TypeAlias = py_int
p_const_sshort = PointerType[const[py_int]]
pp_const_sshort = PointerType[PointerType[const[py_int]]]
ppp_const_sshort = PointerType[PointerType[PointerType[const[py_int]]]]
p_sshort = PointerType[py_int]
pp_sshort = PointerType[PointerType[py_int]]
ppp_sshort = PointerType[PointerType[PointerType[py_int]]]
Py_hash_t : TypeAlias = py_int
p_const_Py_hash_t = PointerType[const[py_int]]
pp_const_Py_hash_t = PointerType[PointerType[const[py_int]]]
ppp_const_Py_hash_t = PointerType[PointerType[PointerType[const[py_int]]]]
p_Py_hash_t = PointerType[py_int]
pp_Py_hash_t = PointerType[PointerType[py_int]]
ppp_Py_hash_t = PointerType[PointerType[PointerType[py_int]]]
ptrdiff_t : TypeAlias = py_int
p_const_ptrdiff_t = PointerType[const[py_int]]
pp_const_ptrdiff_t = PointerType[PointerType[const[py_int]]]
ppp_const_ptrdiff_t = PointerType[PointerType[PointerType[const[py_int]]]]
p_ptrdiff_t = PointerType[py_int]
pp_ptrdiff_t = PointerType[PointerType[py_int]]
ppp_ptrdiff_t = PointerType[PointerType[PointerType[py_int]]]
size_t : TypeAlias = py_int
p_const_size_t = PointerType[const[py_int]]
pp_const_size_t = PointerType[PointerType[const[py_int]]]
ppp_const_size_t = PointerType[PointerType[PointerType[const[py_int]]]]
p_size_t = PointerType[py_int]
pp_size_t = PointerType[PointerType[py_int]]
ppp_size_t = PointerType[PointerType[PointerType[py_int]]]
ssize_t : TypeAlias = py_int
p_const_ssize_t = PointerType[const[py_int]]
pp_const_ssize_t = PointerType[PointerType[const[py_int]]]
ppp_const_ssize_t = PointerType[PointerType[PointerType[const[py_int]]]]
p_ssize_t = PointerType[py_int]
pp_ssize_t = PointerType[PointerType[py_int]]
ppp_ssize_t = PointerType[PointerType[PointerType[py_int]]]
Py_ssize_t : TypeAlias = py_int
p_const_Py_ssize_t = PointerType[const[py_int]]
pp_const_Py_ssize_t = PointerType[PointerType[const[py_int]]]
ppp_const_Py_ssize_t = PointerType[PointerType[PointerType[const[py_int]]]]
p_Py_ssize_t = PointerType[py_int]
pp_Py_ssize_t = PointerType[PointerType[py_int]]
ppp_Py_ssize_t = PointerType[PointerType[PointerType[py_int]]]
Py_tss_t : TypeAlias = Any
p_Py_tss_t = PointerType[Any]
pp_Py_tss_t = PointerType[PointerType[Any]]
ppp_Py_tss_t = PointerType[PointerType[PointerType[Any]]]
uchar : TypeAlias = py_int
p_const_uchar = PointerType[const[py_int]]
pp_const_uchar = PointerType[PointerType[const[py_int]]]
ppp_const_uchar = PointerType[PointerType[PointerType[const[py_int]]]]
p_uchar = PointerType[py_int]
pp_uchar = PointerType[PointerType[py_int]]
ppp_uchar = PointerType[PointerType[PointerType[py_int]]]
p_const_Py_UCS4 = PointerType[const[py_int]]
pp_const_Py_UCS4 = PointerType[PointerType[const[py_int]]]
ppp_const_Py_UCS4 = PointerType[PointerType[PointerType[const[py_int]]]]
p_Py_UCS4 = PointerType[py_int]
pp_Py_UCS4 = PointerType[PointerType[py_int]]
ppp_Py_UCS4 = PointerType[PointerType[PointerType[py_int]]]
uint : TypeAlias = py_int
p_const_uint = PointerType[const[py_int]]
pp_const_uint = PointerType[PointerType[const[py_int]]]
ppp_const_uint = PointerType[PointerType[PointerType[const[py_int]]]]
p_uint = PointerType[py_int]
pp_uint = PointerType[PointerType[py_int]]
ppp_uint = PointerType[PointerType[PointerType[py_int]]]
ulong : TypeAlias = py_int
p_const_ulong = PointerType[const[py_int]]
pp_const_ulong = PointerType[PointerType[const[py_int]]]
ppp_const_ulong = PointerType[PointerType[PointerType[const[py_int]]]]
p_ulong = PointerType[py_int]
pp_ulong = PointerType[PointerType[py_int]]
ppp_ulong = PointerType[PointerType[PointerType[py_int]]]
ulonglong : TypeAlias = py_int
p_const_ulonglong = PointerType[const[py_int]]
pp_const_ulonglong = PointerType[PointerType[const[py_int]]]
ppp_const_ulonglong = PointerType[PointerType[PointerType[const[py_int]]]]
p_ulonglong = PointerType[py_int]
pp_ulonglong = PointerType[PointerType[py_int]]
ppp_ulonglong = PointerType[PointerType[PointerType[py_int]]]
p_const_Py_UNICODE = PointerType[const[py_int]]
pp_const_Py_UNICODE = PointerType[PointerType[const[py_int]]]
ppp_const_Py_UNICODE = PointerType[PointerType[PointerType[const[py_int]]]]
p_Py_UNICODE = PointerType[py_int]
pp_Py_UNICODE = PointerType[PointerType[py_int]]
ppp_Py_UNICODE = PointerType[PointerType[PointerType[py_int]]]
ushort : TypeAlias = py_int
p_const_ushort = PointerType[const[py_int]]
pp_const_ushort = PointerType[PointerType[const[py_int]]]
ppp_const_ushort = PointerType[PointerType[PointerType[const[py_int]]]]
p_ushort = PointerType[py_int]
pp_ushort = PointerType[PointerType[py_int]]
ppp_ushort = PointerType[PointerType[PointerType[py_int]]]
p_void = PointerType[Any]
pp_void = PointerType[PointerType[Any]]
ppp_void = PointerType[PointerType[PointerType[Any]]]

##### END: GENERATED LIST OF GENERATED TYPES #####
