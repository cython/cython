# cython.* namespace for pure mode.
from __future__ import annotations

# Possible version formats: "3.1.0", "3.1.0a1", "3.1.0a1.dev0"
__version__ = "3.3.0a0"

from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any, Iterable, Sequence, Optional, Type, TypeVar, Generic, Callable, overload,
)

if TYPE_CHECKING:
    from builtins import (int as py_int, float as py_float,
                          bool as py_bool, str as py_str, complex as py_complex)
    from typing import TypeAlias, Annotated, ParamSpec
    _P = ParamSpec('_P')

# TypeVars need to be defined at runtime for Generic types
_T = TypeVar('_T')
_C = TypeVar('_C', bound='Callable')
_TypeT = TypeVar('_TypeT', bound='Type')
_C_Or_TypeT = TypeVar('_C_Or_TypeT', _C, _TypeT)
_Decorator = Callable[[_C_Or_TypeT], _C_Or_TypeT]
_FuncDecorator = Callable[[_C], _C]
_ClassDecorator = Callable[[_TypeT], _TypeT]

# BEGIN shameless copy from Cython/minivect/minitypes.py

class _ArrayType(Generic[_T]):

    is_array: bool = True
    subtypes: Sequence[str] = ['dtype']
    dtype: _T
    ndim: int
    is_c_contig: bool
    is_f_contig: bool
    inner_contig: bool
    broadcasting: Any

    # broadcasting is not used, so it's not clear about its type
    def __init__(self, dtype: _T, ndim: int, is_c_contig: bool = False,
                 is_f_contig: bool = False, inner_contig: bool = False,
                 broadcasting: Any = None) -> None:
        self.dtype = dtype
        self.ndim = ndim
        self.is_c_contig = is_c_contig
        self.is_f_contig = is_f_contig
        self.inner_contig = inner_contig or is_c_contig or is_f_contig
        self.broadcasting = broadcasting

    def __repr__(self) -> str:
        axes = [":"] * self.ndim
        if self.is_c_contig:
            axes[-1] = "::1"
        elif self.is_f_contig:
            axes[0] = "::1"

        return "%s[%s]" % (self.dtype, ", ".join(axes))


def index_type(base_type: _T, item: tuple | slice | int) -> _ArrayType[_T]:
    """
    Support array type creation by slicing, e.g. double[:, :] specifies
    a 2D strided array of doubles. The syntax is the same as for
    Cython memoryviews.
    """
    class InvalidTypeSpecification(Exception):
        pass

    def verify_slice(s):
        if s.start or s.stop or s.step not in (None, 1):
            raise InvalidTypeSpecification(
                "Only a step of 1 may be provided to indicate C or "
                "Fortran contiguity")

    if isinstance(item, tuple):
        step_idx = None
        for idx, s in enumerate(item):
            verify_slice(s)
            if s.step and (step_idx or idx not in (0, len(item) - 1)):
                raise InvalidTypeSpecification(
                    "Step may only be provided once, and only in the "
                    "first or last dimension.")

            if s.step == 1:
                step_idx = idx

        return _ArrayType(base_type, len(item),
                          is_c_contig=step_idx == len(item) - 1,
                          is_f_contig=step_idx == 0)
    elif isinstance(item, slice):
        verify_slice(item)
        return _ArrayType(base_type, 1, is_c_contig=bool(item.step))
    else:
        # int[8] etc.
        assert int(item) == item  # array size must be a plain integer
        return array(base_type, item)

# END shameless copy


compiled: bool = False

_Unspecified = object()

# Function decorators

def _empty_decorator(x: _C_Or_TypeT) -> _C_Or_TypeT:
    return x

_empty_func_decorator: _FuncDecorator = _empty_decorator
_empty_class_decorator: _ClassDecorator = _empty_decorator

def _compiler_directive(val: bool = ...) -> _Decorator:
    return _empty_decorator

def locals(**arg_types: Any) -> _FuncDecorator:
    return _empty_func_decorator

def test_assert_path_exists(*paths: str) -> _Decorator:
    return _empty_decorator

def test_fail_if_path_exists(*paths: str) -> _Decorator:
    return _empty_decorator

class _EmptyDecoratorAndManager:
    @overload
    def __call__(self, __val: bool) -> _Decorator: ...

    @overload
    def __call__(self, __func: _C) -> _C: ...

    def __call__(self, x):
        return x
    def __enter__(self) -> None:
        pass
    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc: Optional[BaseException],
                 tb: Optional[TracebackType]) -> None:
        pass

class _Optimization:
    def use_switch(val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()

    def unpack_method_calls(val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()

cclass = cfunc = ccall = _EmptyDecoratorAndManager()

ufunc = _empty_func_decorator

internal = c_api_binop_methods = type_version_tag = no_gc_clear = \
    no_gc = total_ordering = _empty_class_decorator

annotation_typing = returns = wraparound = boundscheck = initializedcheck = \
    nonecheck = cdivision = cdivision_warnings = collection_type = \
    profile = linetrace = infer_types = \
    freelist = auto_pickle = cpow = trashcan = auto_cpdef = \
    allow_none_for_extension_args = callspec = show_performance_hints = \
    py2_import = iterable_coroutine = remove_unreachable = \
    test_body_needs_exception_handling = \
        lambda _: _EmptyDecoratorAndManager()

binding = embedsignature = always_allow_keywords = unraisable_tracebacks = \
    cpp_locals = \
    _compiler_directive

# Note that fast_getattr is untested and undocumented!
fast_getattr = lambda _: _EmptyDecoratorAndManager()
# c_compile_guard is largely for internal use
c_compile_guard = lambda _:_EmptyDecoratorAndManager()

exceptval = lambda _=None, check=True: _EmptyDecoratorAndManager()

optimize = _Optimization()

class _OverflowcheckClass:
    def __call__(self, val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()

    def fold(self, val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()

overflowcheck = _OverflowcheckClass()

if TYPE_CHECKING:
    # May be a bit hard to read but essentially means:
    # > Returns a callable that takes another callable with these parameters and *some*
    # > return value, then returns another callable with the same parameters but
    # > the return type is the previous 'type' parameter.
    def returns(__type: Type[_T]) -> Callable[[Callable[_P, object]], Callable[_P, _T]]: ...

    def exceptval(__val: Any, *, check: bool = False) -> _Decorator: ...


embedsignature.format = overflowcheck.fold = optimize.use_switch = \
    optimize.unpack_method_calls = lambda arg: _EmptyDecoratorAndManager()

final = _empty_decorator

class warn:
    @staticmethod
    def undeclared(val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()

    @staticmethod
    def unreachable(val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()

    @staticmethod
    def maybe_uninitialized(val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()

    @staticmethod
    def unused(val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()

    @staticmethod
    def unused_argument(val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()

    @staticmethod
    def multiple_declarators(val: bool) -> _Decorator:
        return _EmptyDecoratorAndManager()


_cython_inline = None
@overload
def inline(__func: _C) -> _C: ...

@overload
def inline(__code: str, *, get_type: Callable[[object, object], str] = ...,
           lib_dir: str = ..., cython_include_dirs: Iterable[str] = ...,
           cython_compiler_directives: Iterable[str] = ..., force: bool = ...,
           quiet: bool = ..., locals: dict[str, str] = ...,
           globals: dict[str, str] = ..., language_level: str = ...) -> Any: ...

def inline(f, *args, **kwds):
    if isinstance(f, str):
        global _cython_inline
        if _cython_inline is None:
            from Cython.Build.Inline import cython_inline as _cython_inline
        return _cython_inline(f, *args, **kwds)
    else:
        assert len(args) == len(kwds) == 0
        return f

def inline_module(code, *args, **kwds):
    from Cython.Build.Inline import cython_inline_module
    return cython_inline_module(code, *args, **kwds)

def compile(f: _C) -> _C:
    from Cython.Build.Inline import RuntimeCompiledFunction
    return RuntimeCompiledFunction(f)


# Special functions

def cdiv(a: int, b: int) -> int:
    if a < 0:
        a = -a
        b = -b
    if b < 0:
        return (a + b + 1) // b
    return a // b

def cmod(a: int, b: int) -> int:
    r = a % b
    if (a * b) < 0 and r:
        r -= b
    return r


# Emulated language constructs

@overload
def cast(__t: Type[_T], __value: Any) -> _T: ...

@overload
def cast(__t: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs) -> _T: ...

def cast(t, *args, **kwargs):
    kwargs.pop('typecheck', None)
    assert not kwargs

    if isinstance(t, typedef):
        return t(*args)
    elif isinstance(t, type):  # Doesn't work with old-style classes of Python 2.x
        if len(args) != 1 or not (args[0] is None or isinstance(args[0], t)):
            return t(*args)

    return args[0]

def sizeof(obj: object) -> int:
    return 1

def typeof(obj: object) -> str:
    return obj.__class__.__name__
    # return type(arg)

def address(obj: object) -> PointerType:
    return pointer(type(obj))([obj])

def _is_value_type(t):
    if isinstance(t, typedef):
        return _is_value_type(t._basetype)

    return isinstance(t, type) and issubclass(t, (StructType, UnionType, ArrayType))

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

def declare(t=None, value=_Unspecified, **kwds):
    if value is not _Unspecified:
        return cast(t, value)
    elif _is_value_type(t):
        return t()
    else:
        return None

class _nogil:
    """Support for 'with nogil' statement and @nogil decorator.
    """
    @overload
    def __call__(self, __val: bool) -> _FuncDecorator: ...

    @overload
    def __call__(self, __func: _C) -> _C: ...

    def __call__(self, x):
        if callable(x):
            # Used as function decorator => return the function unchanged.
            return x
        # Used as conditional context manager or to create an "@nogil(True/False)" decorator => keep going.
        return self

    def __enter__(self) -> None:
        pass
    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc: Optional[BaseException],
                 tb: Optional[TracebackType]) -> bool:
        return exc_type is None

nogil = _nogil()
gil = _nogil()
with_gil = _nogil()  # Actually not a context manager, but compilation will give the right error.
del _nogil


class critical_section:
    def __init__(self, arg0, arg1=None):
        # It's ambiguous if this is being used as a decorator or context manager
        # even with a callable arg.
        self.arg0 = arg0
    def __call__(self, *args, **kwds):
        return self.arg0(*args, **kwds)
    def __enter__(self) -> None:
        pass
    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc: Optional[BaseException],
                 tb: Optional[TracebackType]) -> bool:
        return False


# Emulated types

if TYPE_CHECKING:
    class CythonTypeObject(object):
        ...
    class CythonType(CythonTypeObject):
        ...

class CythonMetaType(type):

    def __getitem__(type, ix):
        return array(type, ix)

CythonTypeObject = CythonMetaType('CythonTypeObject', (object,), {})

class CythonType(CythonTypeObject):

    def _pointer(self, n=1):
        for i in range(n):
            self = pointer(self)
        return self

if TYPE_CHECKING:
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

class PointerType(CythonType):

    def __init__(self, value=None):
        from .Shadow import cast
        if isinstance(value, (ArrayType, PointerType)):
            self._items = [cast(self._basetype, a) for a in value._items]
        elif isinstance(value, list):
            self._items = [cast(self._basetype, a) for a in value]
        elif value is None or value == 0:
            self._items = []
        else:
            raise ValueError

    def __getitem__(self, ix):
        if ix < 0:
            raise IndexError("negative indexing not allowed in C")
        return self._items[ix]

    def __setitem__(self, ix, value):
        if ix < 0:
            raise IndexError("negative indexing not allowed in C")
        from .Shadow import cast
        self._items[ix] = cast(self._basetype, value)

    def __eq__(self, value):
        if value is None and not self._items:
            return True
        elif type(self) != type(value):
            return False
        else:
            return not self._items and not value._items

    def __repr__(self):
        return f"{self._basetype} *"


class ArrayType(PointerType):

    def __init__(self, value=None):
        if value is None:
            self._items = [None] * self._n
        else:
            super().__init__(value)


class StructType(CythonType):

    def __init__(self, *posargs, **data):
        if not (posargs or data):
            return
        if posargs and data:
            raise ValueError('Cannot accept both positional and keyword arguments.')

        # Allow 'cast_from' as single positional or keyword argument.
        if data and len(data) == 1 and 'cast_from' in data:
            cast_from = data.pop('cast_from')
        elif len(posargs) == 1 and type(posargs[0]) is type(self):
            cast_from, posargs = posargs[0], ()
        elif posargs:
            for key, arg in zip(self._members, posargs):
                setattr(self, key, arg)
            return
        else:
            for key, value in data.items():
                if key not in self._members:
                    raise ValueError("Invalid struct attribute for %s: %s" % (
                        self.__class__.__name__, key))
                setattr(self, key, value)
            return

        # do cast
        if data:
            raise ValueError('Cannot accept keyword arguments when casting.')
        if type(cast_from) is not type(self):
            raise ValueError('Cannot cast from %s' % cast_from)
        for key, value in cast_from.__dict__.items():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if key in self._members:
            self.__dict__[key] = cast(self._members[key], value)
        else:
            raise AttributeError("Struct has no member '%s'" % key)


class UnionType(CythonType):

    def __init__(self, cast_from=_Unspecified, **data):
        if cast_from is not _Unspecified:
            # do type cast
            if len(data) > 0:
                raise ValueError('Cannot accept keyword arguments when casting.')
            if isinstance(cast_from, dict):
                datadict = cast_from
            elif type(cast_from) is type(self):
                datadict = cast_from.__dict__
            else:
                raise ValueError('Cannot cast from %s' % cast_from)
        else:
            datadict = data
        if len(datadict) > 1:
            raise AttributeError("Union can only store one field at a time.")
        for key, value in datadict.items():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if key == '__dict__':
            CythonType.__setattr__(self, key, value)
        elif key in self._members:
            self.__dict__ = {key: cast(self._members[key], value)}
        else:
            raise AttributeError("Union has no member '%s'" % key)


if TYPE_CHECKING:
    class pointer(PointerType[_T]):
        def __new__(cls, basetype: _T) -> Type[PointerType[_T]]: ...
        def __class_getitem__(cls, basetype: _T) -> Type[PointerType[_T]]: ...

    class array(ArrayType[_T]):
        def __new__(basetype: _T, n: int) -> Type[ArrayType[_T, int]]: ...
        def __class_getitem__(cls, item: tuple[_T, int]) -> Type[ArrayType[_T, int]]: ...

class pointer(PointerType):
    # Implemented as class to support both 'pointer(int)' and 'pointer[int]'.
    def __new__(cls, basetype):
        class PointerInstance(PointerType):
            _basetype = basetype
        return PointerInstance

    def __class_getitem__(cls, basetype):
        return cls(basetype)


class array(ArrayType):
    # Implemented as class to support both 'array(int, 5)' and 'array[int, 5]'.
    def __new__(cls, basetype, n):
        class ArrayInstance(ArrayType):
            _basetype = basetype
            _n = n
        return ArrayInstance

    def __class_getitem__(cls, item):
        basetype, n = item
        return cls(basetype, item)


def struct(**members: type) -> Type[Any]:
    class StructInstance(StructType):
        _members = members
    for key in members:
        setattr(StructInstance, key, None)
    return StructInstance

def union(**members: type) -> Type[Any]:
    class UnionInstance(UnionType):
        _members = members
    for key in members:
        setattr(UnionInstance, key, None)
    return UnionInstance


if TYPE_CHECKING:
    class typedef(CythonType, Generic[_T]):
        name: str

        def __init__(self, type: _T, name: Optional[str] = ...) -> None: ...
        def __call__(self, *arg: Any) -> _T: ...
        def __repr__(self) -> str: ...
        __getitem__ = index_type

class typedef(CythonType):
    name: str

    def __init__(self, type: _T, name: Optional[str] = None) -> None:
        self._basetype = type
        self.name = name

    def __call__(self, *arg: Any) -> _T:
        value = cast(self._basetype, *arg)
        return value

    def __repr__(self) -> str:
        return self.name or str(self._basetype)

    __getitem__ = index_type


if TYPE_CHECKING:
    const: TypeAlias = Annotated[_T, "cython.const"]
    volatile: TypeAlias = Annotated[_T, "cython.volatile"]

class const(typedef):
    def __init__(self, type, name=None):
        name = f"const {name or repr(type)}"
        super().__init__(type, name)

    def __class_getitem__(cls, base_type):
        return const(base_type)


class volatile(typedef):
    def __init__(self, type, name=None):
        name = f"volatile {name or repr(type)}"
        super().__init__(type, name)

    def __class_getitem__(cls, base_type):
        return volatile(base_type)


class _FusedType(CythonType):
    __getitem__ = index_type


def fused_type(*args: Any) -> Type[Any]:
    if not args:
        raise TypeError("Expected at least one type as argument")

    # Find the numeric type with biggest rank if all types are numeric
    rank = -1
    for type in args:
        if type not in (py_int, py_long, py_float, py_complex):
            break

        if type_ordering.index(type) > rank:
            result_type = type
    else:
        return result_type

    # Not a simple numeric type, return a fused type instance. The result
    # isn't really meant to be used, as we can't keep track of the context in
    # pure-mode. Casting won't do anything in this case.
    return _FusedType()


py_int = typedef(int, "int")
py_long = typedef(int, "long")  # for legacy Py2 code only
py_float = typedef(float, "float")
py_complex = typedef(complex, "double complex")


# Predefined types

int_types = [
    'char',
    'short',
    'Py_UNICODE',
    'int',
    'Py_UCS4',
    'long',
    'longlong',
    'Py_hash_t',
    'Py_ssize_t',
    'size_t',
    'ssize_t',
    'ptrdiff_t',
]
float_types = [
    'longdouble',
    'double',
    'float',
]
complex_types = [
    'longdoublecomplex',
    'doublecomplex',
    'floatcomplex',
    'complex',
]
other_types = [
    'bint',
    'void',
    'Py_tss_t',
]

to_repr = {
    'longlong': 'long long',
    'longdouble': 'long double',
    'longdoublecomplex': 'long double complex',
    'doublecomplex': 'double complex',
    'floatcomplex': 'float complex',
}.get

gs = globals()

gs['unicode'] = typedef(str, 'unicode')

for name in int_types:
    reprname = to_repr(name, name)
    gs[name] = typedef(py_int, reprname)
    if name not in ('Py_UNICODE', 'Py_UCS4', 'Py_hash_t', 'ptrdiff_t') and not name.endswith('size_t'):
        gs['u'+name] = typedef(py_int, "unsigned " + reprname)
        gs['s'+name] = typedef(py_int, "signed " + reprname)

for name in float_types:
    gs[name] = typedef(py_float, to_repr(name, name))

for name in complex_types:
    gs[name] = typedef(py_complex, to_repr(name, name))

del name, reprname

if TYPE_CHECKING:
    Py_UCS4 = py_int | str
    Py_UNICODE = py_int | str

    bint = py_bool
    void = Type[None]
    basestring = py_str
    unicode = py_str

bint = typedef(bool, "bint")
void = typedef(None, "void")
Py_tss_t = typedef(None, "Py_tss_t")

# Generate const types.
for t in int_types + float_types + complex_types + other_types:
    for t in (t, f'u{t}', f's{t}'):
        if t in gs:
            gs[f"const_{t}"] = const(gs[t], t)

# Generate pointer types: p_int, p_const_char, etc.
for i in range(1, 4):
    for const_ in ('', 'const_'):
        for t in int_types:
            for t in (t, f'u{t}', f's{t}'):
                if t in gs:
                    gs[f"{'p'*i}_{const_}{t}"] = pointer(gs[f"{'p'*(i-1)}{'_' if i > 1 else ''}{const_}{t}"])

        for t in float_types + complex_types:
            gs[f"{'p'*i}_{const_}{t}"] = pointer(gs[f"{'p'*(i-1)}{'_' if i > 1 else ''}{const_}{t}"])

    gs[f"{'p'*i}_const_bint"] = pointer(gs[f"{'p'*(i-1)}{'_' if i > 1 else ''}const_bint"])
    for t in other_types:
        gs[f"{'p'*i}_{t}"] = pointer(gs[f"{'p'*(i-1)}{'_' if i > 1 else ''}{t}"])

del t, const_, i

NULL: pointer[Any] = gs['p_void'](0)

del gs


def __getattr__(name):
    # looks like 'gs' has some users out there by now...
    if name == 'gs':
        import warnings
        warnings.warn(
            "'gs' is not a publicly exposed name in cython.*. Use vars() or globals() instead.",
            DeprecationWarning)
        return globals()
    raise AttributeError(f"'cython' has no attribute {name!r}")


integral = floating = numeric = _FusedType()

type_ordering = [py_int, py_long, py_float, py_complex]

class CythonDotParallel:
    """
    The cython.parallel module.
    """

    __all__ = ['parallel', 'prange', 'threadid']

    def parallel(self, num_threads=None):
        return nogil

    def prange(self, start=0, stop=None, step=1, nogil=False, schedule=None, chunksize=None, num_threads=None):
        if stop is None:
            stop = start
            start = 0
        return range(start, stop, step)

    def threadid(self):
        return 0

    # def threadsavailable(self):
        # return 1

class CythonDotImportedFromElsewhere:
    """
    cython.dataclasses just shadows the standard library modules of the same name
    """
    def __init__(self, module):
        self.__path__ = []
        self.__file__ = None
        self.__name__ = module
        self.__package__ = module

    def __getattr__(self, attr):
        # we typically only expect this to be called once
        from importlib import import_module
        import sys
        try:
            mod = import_module(self.__name__)
        except ImportError:
            # but if they don't exist (Python is not sufficiently up-to-date) then
            # you can't use them
            raise AttributeError("%s: the standard library module %s is not available" %
                                 (attr, self.__name__))
        sys.modules['cython.%s' % self.__name__] = mod
        return getattr(mod, attr)

class CythonCImports:
    """
    Simplistic module mock to make cimports sort-of work in Python code.
    """
    def __init__(self, module, **attributes):
        self.__path__ = []
        self.__file__ = None
        self.__name__ = module
        self.__package__ = module
        if attributes:
            self.__dict__.update(attributes)

    def __getattr__(self, item):
        if item.startswith('__') and item.endswith('__'):
            raise AttributeError(item)

        package = self.__package__[len('cython.cimports.'):]

        from importlib import import_module
        try:
            return import_module(item, package or None)
        except ImportError:
            ex = AttributeError(item)
            ex.__cause__ = None
            raise ex


import math, sys
sys.modules['cython.parallel'] = CythonDotParallel()
sys.modules['cython.cimports.libc.math'] = math
sys.modules['cython.cimports.libc'] = CythonCImports('cython.cimports.libc', math=math)
sys.modules['cython.cimports'] = CythonCImports('cython.cimports', libc=sys.modules['cython.cimports.libc'])

# In pure Python mode @cython.dataclasses.dataclass and dataclass field should just
# shadow the standard library ones (if they are available)
if TYPE_CHECKING:
    import dataclasses as dataclasses
dataclasses = sys.modules['cython.dataclasses'] = CythonDotImportedFromElsewhere('dataclasses')
del math, sys


class _pymutex_base:
    def __init__(self) -> None:
        import threading
        self._l = threading.Lock()

    def acquire(self) -> None:
        return self._l.acquire()

    def release(self) -> None:
        return self._l.release()

    def locked(self) -> bool:
        """
        Check if the lock is currently held.
        Returns True if locked, False otherwise.
        """
        return self._l.locked()

    def can_check_locked(self) -> bool:
        """
        Check if the locked() method is available.
        Always returns True - locked() is available on all Python versions.
        """
        return True

    def __enter__(self) -> None:
        return self._l.__enter__()

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc: Optional[BaseException],
                 tb: Optional[TracebackType]) -> None:
        return self._l.__exit__(exc_type, exc, tb)

class pymutex(_pymutex_base):
    """
    A low-cost mutex lock type.
    In Python 3.13+, it uses the fast PyMutex implementation. In older Python versions,
    it falls back to the heavier "PyThread_type_lock".
    Can be used in 'with' statements and supports nogil context.
    """
    pass

class pythread_type_lock(_pymutex_base):
    """
    A mutex lock type using PyThread_type_lock.
    Can be used in 'with' statements and supports nogil context.
    Compatible with the Limited API.
    """
    pass


if TYPE_CHECKING:
    const: TypeAlias = Annotated[_T, "cython.const"]
    volatile: TypeAlias = Annotated[_T, "cython.volatile"]

    ##### START: GENERATED LIST OF GENERATED TYPES #####
    # Generated by "Tools/cython-generate-shadow-pyi.py" on 2025-12-01 19:08:04.502148

    const_bint : TypeAlias = const[bint]
    p_const_bint = pointer[const[bint]]
    pp_const_bint = pointer[pointer[const[bint]]]
    ppp_const_bint = pointer[pointer[pointer[const[bint]]]]
    p_bint = pointer[bint]
    pp_bint = pointer[pointer[bint]]
    ppp_bint = pointer[pointer[pointer[bint]]]
    char : TypeAlias = py_int
    const_char : TypeAlias = const[py_int]
    p_const_char = pointer[const[py_int]]
    pp_const_char = pointer[pointer[const[py_int]]]
    ppp_const_char = pointer[pointer[pointer[const[py_int]]]]
    p_char = pointer[py_int]
    pp_char = pointer[pointer[py_int]]
    ppp_char = pointer[pointer[pointer[py_int]]]
    complex : TypeAlias = py_complex
    const_complex : TypeAlias = const[py_complex]
    p_const_complex = pointer[const[py_complex]]
    pp_const_complex = pointer[pointer[const[py_complex]]]
    ppp_const_complex = pointer[pointer[pointer[const[py_complex]]]]
    p_complex = pointer[py_complex]
    pp_complex = pointer[pointer[py_complex]]
    ppp_complex = pointer[pointer[pointer[py_complex]]]
    double : TypeAlias = py_float
    const_double : TypeAlias = const[py_float]
    p_const_double = pointer[const[py_float]]
    pp_const_double = pointer[pointer[const[py_float]]]
    ppp_const_double = pointer[pointer[pointer[const[py_float]]]]
    p_double = pointer[py_float]
    pp_double = pointer[pointer[py_float]]
    ppp_double = pointer[pointer[pointer[py_float]]]
    doublecomplex : TypeAlias = py_complex
    const_doublecomplex : TypeAlias = const[py_complex]
    p_const_doublecomplex = pointer[const[py_complex]]
    pp_const_doublecomplex = pointer[pointer[const[py_complex]]]
    ppp_const_doublecomplex = pointer[pointer[pointer[const[py_complex]]]]
    p_doublecomplex = pointer[py_complex]
    pp_doublecomplex = pointer[pointer[py_complex]]
    ppp_doublecomplex = pointer[pointer[pointer[py_complex]]]
    float : TypeAlias = py_float
    const_float : TypeAlias = const[py_float]
    p_const_float = pointer[const[py_float]]
    pp_const_float = pointer[pointer[const[py_float]]]
    ppp_const_float = pointer[pointer[pointer[const[py_float]]]]
    p_float = pointer[py_float]
    pp_float = pointer[pointer[py_float]]
    ppp_float = pointer[pointer[pointer[py_float]]]
    floatcomplex : TypeAlias = py_complex
    const_floatcomplex : TypeAlias = const[py_complex]
    p_const_floatcomplex = pointer[const[py_complex]]
    pp_const_floatcomplex = pointer[pointer[const[py_complex]]]
    ppp_const_floatcomplex = pointer[pointer[pointer[const[py_complex]]]]
    p_floatcomplex = pointer[py_complex]
    pp_floatcomplex = pointer[pointer[py_complex]]
    ppp_floatcomplex = pointer[pointer[pointer[py_complex]]]
    int : TypeAlias = py_int
    const_int : TypeAlias = const[py_int]
    p_const_int = pointer[const[py_int]]
    pp_const_int = pointer[pointer[const[py_int]]]
    ppp_const_int = pointer[pointer[pointer[const[py_int]]]]
    p_int = pointer[py_int]
    pp_int = pointer[pointer[py_int]]
    ppp_int = pointer[pointer[pointer[py_int]]]
    long : TypeAlias = py_int
    const_long : TypeAlias = const[py_int]
    p_const_long = pointer[const[py_int]]
    pp_const_long = pointer[pointer[const[py_int]]]
    ppp_const_long = pointer[pointer[pointer[const[py_int]]]]
    p_long = pointer[py_int]
    pp_long = pointer[pointer[py_int]]
    ppp_long = pointer[pointer[pointer[py_int]]]
    longdouble : TypeAlias = py_float
    const_longdouble : TypeAlias = const[py_float]
    p_const_longdouble = pointer[const[py_float]]
    pp_const_longdouble = pointer[pointer[const[py_float]]]
    ppp_const_longdouble = pointer[pointer[pointer[const[py_float]]]]
    p_longdouble = pointer[py_float]
    pp_longdouble = pointer[pointer[py_float]]
    ppp_longdouble = pointer[pointer[pointer[py_float]]]
    longdoublecomplex : TypeAlias = py_complex
    const_longdoublecomplex : TypeAlias = const[py_complex]
    p_const_longdoublecomplex = pointer[const[py_complex]]
    pp_const_longdoublecomplex = pointer[pointer[const[py_complex]]]
    ppp_const_longdoublecomplex = pointer[pointer[pointer[const[py_complex]]]]
    p_longdoublecomplex = pointer[py_complex]
    pp_longdoublecomplex = pointer[pointer[py_complex]]
    ppp_longdoublecomplex = pointer[pointer[pointer[py_complex]]]
    longlong : TypeAlias = py_int
    const_longlong : TypeAlias = const[py_int]
    p_const_longlong = pointer[const[py_int]]
    pp_const_longlong = pointer[pointer[const[py_int]]]
    ppp_const_longlong = pointer[pointer[pointer[const[py_int]]]]
    p_longlong = pointer[py_int]
    pp_longlong = pointer[pointer[py_int]]
    ppp_longlong = pointer[pointer[pointer[py_int]]]
    schar : TypeAlias = py_int
    const_schar : TypeAlias = const[py_int]
    p_const_schar = pointer[const[py_int]]
    pp_const_schar = pointer[pointer[const[py_int]]]
    ppp_const_schar = pointer[pointer[pointer[const[py_int]]]]
    p_schar = pointer[py_int]
    pp_schar = pointer[pointer[py_int]]
    ppp_schar = pointer[pointer[pointer[py_int]]]
    short : TypeAlias = py_int
    const_short : TypeAlias = const[py_int]
    p_const_short = pointer[const[py_int]]
    pp_const_short = pointer[pointer[const[py_int]]]
    ppp_const_short = pointer[pointer[pointer[const[py_int]]]]
    p_short = pointer[py_int]
    pp_short = pointer[pointer[py_int]]
    ppp_short = pointer[pointer[pointer[py_int]]]
    sint : TypeAlias = py_int
    const_sint : TypeAlias = const[py_int]
    p_const_sint = pointer[const[py_int]]
    pp_const_sint = pointer[pointer[const[py_int]]]
    ppp_const_sint = pointer[pointer[pointer[const[py_int]]]]
    p_sint = pointer[py_int]
    pp_sint = pointer[pointer[py_int]]
    ppp_sint = pointer[pointer[pointer[py_int]]]
    slong : TypeAlias = py_int
    const_slong : TypeAlias = const[py_int]
    p_const_slong = pointer[const[py_int]]
    pp_const_slong = pointer[pointer[const[py_int]]]
    ppp_const_slong = pointer[pointer[pointer[const[py_int]]]]
    p_slong = pointer[py_int]
    pp_slong = pointer[pointer[py_int]]
    ppp_slong = pointer[pointer[pointer[py_int]]]
    slonglong : TypeAlias = py_int
    const_slonglong : TypeAlias = const[py_int]
    p_const_slonglong = pointer[const[py_int]]
    pp_const_slonglong = pointer[pointer[const[py_int]]]
    ppp_const_slonglong = pointer[pointer[pointer[const[py_int]]]]
    p_slonglong = pointer[py_int]
    pp_slonglong = pointer[pointer[py_int]]
    ppp_slonglong = pointer[pointer[pointer[py_int]]]
    sshort : TypeAlias = py_int
    const_sshort : TypeAlias = const[py_int]
    p_const_sshort = pointer[const[py_int]]
    pp_const_sshort = pointer[pointer[const[py_int]]]
    ppp_const_sshort = pointer[pointer[pointer[const[py_int]]]]
    p_sshort = pointer[py_int]
    pp_sshort = pointer[pointer[py_int]]
    ppp_sshort = pointer[pointer[pointer[py_int]]]
    Py_hash_t : TypeAlias = py_int
    const_Py_hash_t : TypeAlias = const[py_int]
    p_const_Py_hash_t = pointer[const[py_int]]
    pp_const_Py_hash_t = pointer[pointer[const[py_int]]]
    ppp_const_Py_hash_t = pointer[pointer[pointer[const[py_int]]]]
    p_Py_hash_t = pointer[py_int]
    pp_Py_hash_t = pointer[pointer[py_int]]
    ppp_Py_hash_t = pointer[pointer[pointer[py_int]]]
    ptrdiff_t : TypeAlias = py_int
    const_ptrdiff_t : TypeAlias = const[py_int]
    p_const_ptrdiff_t = pointer[const[py_int]]
    pp_const_ptrdiff_t = pointer[pointer[const[py_int]]]
    ppp_const_ptrdiff_t = pointer[pointer[pointer[const[py_int]]]]
    p_ptrdiff_t = pointer[py_int]
    pp_ptrdiff_t = pointer[pointer[py_int]]
    ppp_ptrdiff_t = pointer[pointer[pointer[py_int]]]
    size_t : TypeAlias = py_int
    const_size_t : TypeAlias = const[py_int]
    p_const_size_t = pointer[const[py_int]]
    pp_const_size_t = pointer[pointer[const[py_int]]]
    ppp_const_size_t = pointer[pointer[pointer[const[py_int]]]]
    p_size_t = pointer[py_int]
    pp_size_t = pointer[pointer[py_int]]
    ppp_size_t = pointer[pointer[pointer[py_int]]]
    ssize_t : TypeAlias = py_int
    const_ssize_t : TypeAlias = const[py_int]
    p_const_ssize_t = pointer[const[py_int]]
    pp_const_ssize_t = pointer[pointer[const[py_int]]]
    ppp_const_ssize_t = pointer[pointer[pointer[const[py_int]]]]
    p_ssize_t = pointer[py_int]
    pp_ssize_t = pointer[pointer[py_int]]
    ppp_ssize_t = pointer[pointer[pointer[py_int]]]
    Py_ssize_t : TypeAlias = py_int
    const_Py_ssize_t : TypeAlias = const[py_int]
    p_const_Py_ssize_t = pointer[const[py_int]]
    pp_const_Py_ssize_t = pointer[pointer[const[py_int]]]
    ppp_const_Py_ssize_t = pointer[pointer[pointer[const[py_int]]]]
    p_Py_ssize_t = pointer[py_int]
    pp_Py_ssize_t = pointer[pointer[py_int]]
    ppp_Py_ssize_t = pointer[pointer[pointer[py_int]]]
    const_Py_tss_t : TypeAlias = const[Any]
    p_Py_tss_t = pointer[Any]
    pp_Py_tss_t = pointer[pointer[Any]]
    ppp_Py_tss_t = pointer[pointer[pointer[Any]]]
    uchar : TypeAlias = py_int
    const_uchar : TypeAlias = const[py_int]
    p_const_uchar = pointer[const[py_int]]
    pp_const_uchar = pointer[pointer[const[py_int]]]
    ppp_const_uchar = pointer[pointer[pointer[const[py_int]]]]
    p_uchar = pointer[py_int]
    pp_uchar = pointer[pointer[py_int]]
    ppp_uchar = pointer[pointer[pointer[py_int]]]
    const_Py_UCS4 : TypeAlias = const[py_int]
    p_const_Py_UCS4 = pointer[const[py_int]]
    pp_const_Py_UCS4 = pointer[pointer[const[py_int]]]
    ppp_const_Py_UCS4 = pointer[pointer[pointer[const[py_int]]]]
    p_Py_UCS4 = pointer[py_int]
    pp_Py_UCS4 = pointer[pointer[py_int]]
    ppp_Py_UCS4 = pointer[pointer[pointer[py_int]]]
    uint : TypeAlias = py_int
    const_uint : TypeAlias = const[py_int]
    p_const_uint = pointer[const[py_int]]
    pp_const_uint = pointer[pointer[const[py_int]]]
    ppp_const_uint = pointer[pointer[pointer[const[py_int]]]]
    p_uint = pointer[py_int]
    pp_uint = pointer[pointer[py_int]]
    ppp_uint = pointer[pointer[pointer[py_int]]]
    ulong : TypeAlias = py_int
    const_ulong : TypeAlias = const[py_int]
    p_const_ulong = pointer[const[py_int]]
    pp_const_ulong = pointer[pointer[const[py_int]]]
    ppp_const_ulong = pointer[pointer[pointer[const[py_int]]]]
    p_ulong = pointer[py_int]
    pp_ulong = pointer[pointer[py_int]]
    ppp_ulong = pointer[pointer[pointer[py_int]]]
    ulonglong : TypeAlias = py_int
    const_ulonglong : TypeAlias = const[py_int]
    p_const_ulonglong = pointer[const[py_int]]
    pp_const_ulonglong = pointer[pointer[const[py_int]]]
    ppp_const_ulonglong = pointer[pointer[pointer[const[py_int]]]]
    p_ulonglong = pointer[py_int]
    pp_ulonglong = pointer[pointer[py_int]]
    ppp_ulonglong = pointer[pointer[pointer[py_int]]]
    const_Py_UNICODE : TypeAlias = const[py_int]
    p_const_Py_UNICODE = pointer[const[py_int]]
    pp_const_Py_UNICODE = pointer[pointer[const[py_int]]]
    ppp_const_Py_UNICODE = pointer[pointer[pointer[const[py_int]]]]
    p_Py_UNICODE = pointer[py_int]
    pp_Py_UNICODE = pointer[pointer[py_int]]
    ppp_Py_UNICODE = pointer[pointer[pointer[py_int]]]
    ushort : TypeAlias = py_int
    const_ushort : TypeAlias = const[py_int]
    p_const_ushort = pointer[const[py_int]]
    pp_const_ushort = pointer[pointer[const[py_int]]]
    ppp_const_ushort = pointer[pointer[pointer[const[py_int]]]]
    p_ushort = pointer[py_int]
    pp_ushort = pointer[pointer[py_int]]
    ppp_ushort = pointer[pointer[pointer[py_int]]]
    const_void : TypeAlias = const[Any]
    p_void = pointer[Any]
    pp_void = pointer[pointer[Any]]
    ppp_void = pointer[pointer[pointer[Any]]]

    ##### END: GENERATED LIST OF GENERATED TYPES #####
    pass
