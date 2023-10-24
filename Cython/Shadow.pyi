from builtins import (int as py_int, float as py_float,
                      bool as py_bool, str as py_str, complex as py_complex)
from typing import (Union, Dict, Any, Sequence, Optional,
                    List, TypeVar, Type, Generic)


i32 = int = py_int
i64 = long = py_int
i128 = longlong = py_int
i16 = short = py_int
i8 = char = py_int
sint = py_int
slong = py_int
slonglong = py_int
sshort = py_int
schar = py_int
u32 = uint = py_int
u64 = ulong = py_int
u128 = ulonglong = py_int
u16 = ushort = py_int
u8 = uchar = py_int
usize = size_t = py_int
isize = Py_ssize_t = py_int
Py_UCS4 = Union[py_int, str]
Py_UNICODE = Union[py_int, str]
f32 = float = py_float
f64 = double = py_float
longdouble = py_float
complex = py_complex
floatcomplex = py_complex
doublecomplex = py_complex
longdoublecomplex = py_complex
bint = py_bool
void = Union[None]
basestring = py_str
unicode = py_str

gs: Dict[str, Any]  # Should match the return type of globals()

_T = TypeVar('_T')

class _ArrayType(object, Generic[_T]):
    is_array: bool
    subtypes: Sequence[str]
    dtype: _T
    ndim: i32
    is_c_contig: bool
    is_f_contig: bool
    inner_contig: bool
    broadcasting: Any

    # broadcasting is not used, so it's not clear about its type
    def __init__(self, dtype: _T, ndim: i32, is_c_contig: bool = ...,
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
        value: Optional[Union[ArrayType[_T], PointerType[_T], List[_T], i32]] = ...
    ) -> None: ...
    def __getitem__(self, ix: i32) -> _T: ...
    def __setitem__(self, ix: i32, value: _T) -> None: ...
    def __eq__(self, value: object) -> bool: ...
    def __repr__(self) -> str: ...

class ArrayType(PointerType[_T]):
    def __init__(self) -> None: ...

#class StructType(CythonType, Generic[_T]):
#    def __init__(
#        self,
#        value: List[Type[_T]] = ...
#    ) -> None: ...

def index_type(
    base_type: _T, item: Union[tuple, slice, i32]) -> _ArrayType[_T]: ...

def pointer(basetype: _T) -> Type[PointerType[_T]]: ...

def array(basetype: _T, n: i32) -> Type[ArrayType[_T]]: ...

# def r#struct(basetype: _T) -> Type[StructType[_T]]: ...

class typedef(CythonType, Generic[_T]):
    name: str

    def __init__(self, type: _T, name: Optional[str] = ...) -> None: ...
    def __call__(self, *arg: Any) -> _T: ...
    def __repr__(self) -> str: ...
    __getitem__ = index_type

#class _FusedType(CythonType, Generic[_T]):
#    def __init__(self) -> None: ...

#def fused_type(*args: Tuple[_T]) -> Type[FusedType[_T]]: ...
