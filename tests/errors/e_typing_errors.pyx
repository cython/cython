# mode: error

import cython

try:
    from typing import Optional, ClassVar, Union
except ImportError:
    pass


# not OK

def optional_cython_types(Optional[cython.int] i, Optional[cython.double] d, Optional[cython.float] f,
                          Optional[cython.complex] c, Optional[cython.long] l, Optional[cython.longlong] ll):
    pass


MyStruct = cython.struct(a=cython.int, b=cython.double)

def optional_cstruct(Optional[MyStruct] x):
    pass


def optional_pytypes(Optional[int] i, Optional[float] f, Optional[complex] c, Optional[long] l):
    pass


cdef ClassVar[list] x

def union_pytypes(Union[int, None] i, Union[None, float] f, Union[complex, None] c, Union[long, None] l):
    pass

def bitwise_or_ctypes(i: cython.int | None, f: None | cython.float , c: cython.complex | None, l: cython.long | None):
    pass

def subscribed_types_assignments():
    la: list[cython.float] = [5.0]
    lb: list[cython.int] = la
    sa: set[cython.float] = {5.0}
    sb: set[cython.int] = sa
    fa: frozenset[cython.float] = frozenset({5.0})
    fb: frozenset[cython.int] = fa
    da: dict[cython.float, cython.float] = {5.0: 5.0}
    db: dict[cython.int, cython.int] = da
    dc: dict[cython.int, cython.float] = da
    dd: dict[cython.float, cython.int] = da
    sa = la
    sa = fa
    sa = da
    fa = la
    fa = sa
    fa = da
    la = sa
    la = fa
    la = da
    da = sa
    da = fa
    da = la


def subscribed_types_assignments_to_variable():
    la: list[cython.float] = [5.0]
    lb: list[cython.int] = [1]
    a: cython.int = la[0]
    aa: cython.float = 1.0
    lb[0] = aa
    i: cython.int
    for i in la:
        pass

    da: dict[cython.float, cython.float] = {1.0: 1.0}
    db: dict[str, cython.int] = {"a": 1.0}
    b: cython.int = da[1]
    bb: cython.float = 1.0
    db[0] = bb
    j: cython.int
    for j in da:
        pass

    sa: set[cython.int] = {1}
    k: cython.p_int
    for k in sa:
        pass

    fa: frozenset[cython.int] = {1}
    k: cython.p_int
    for k in sa:
        pass

# OK

def optional_memoryview(double[:] d, Optional[double[:]] o):
    pass

def union_memoryview(double[:] d, Union[double[:], None] o):
    pass

def bitwise_or_not_recognized_type(x: DummyType | None, y: None | DummyType):
    pass

cdef class Cls(object):
    cdef ClassVar[list] x

def bitwise_or_pytypes(i: int | None, f: None | float , c: complex | None):
    list[int | None]()
    list[None | int]()
    py_li: list[int | None] = []

    tuple[float | None]()
    tuple[None | float]()
    py_tf: tuple[None | float] = ()

    list[complex | None]()
    list[None | complex]()
    py_lc: list[complex | None] = []

def allowed_subscribed_types_assignments():
    la: list[cython.float] = [5.0]
    lb: list[cython.float] = la
    sa: set[cython.int] = {5}
    sb: set[cython.int] = sa
    fa: frozenset[str] = frozenset({"bar"})
    fb: frozenset[str] = fa
    da: dict[cython.int, cython.int] = {1: 2}
    db: dict[cython.int, cython.int] = da

    l1: list = la
    s1: set = sa
    f1: frozenset = fa
    d1: dict = da

    la = l1
    sa = s1
    fa = f1
    da = d1

def forbidden_subscribed_types_assignments():
    la: list[cython.int] = [5]
    sa: set[cython.int] = {5}
    fa: frozenset[cython.int] = frozenset({1})
    da: dict[cython.int, cython.int] = {1: 2}

    la = sa
    la = fa
    la = da
    sa = la
    sa = fa
    sa = da
    fa = la
    fa = sa
    fa = da
    da = la
    da = sa
    da = fa

    l: list = [1]
    s: set = {1}
    f: frozenset = frozenset({1})
    d: dict = {1:3}

    la = d
    la = f
    la = s
    sa = l
    sa = d
    sa = f
    fa = l
    fa = s
    fa = d
    sa = l
    sa = f
    sa = d


cdef list_bytes(a: list[bytes]):
    pass

cdef dict_bytes(a: dict[str, bytes], b: dict[bytes, str], c: dict[bytes, bytes], d: dict[str, str]):
    pass

def forbidden_subscribed_types_args():
    la: list[str] = ['asdf']
    list_bytes(la)
    da: dict[bytes, str] = {}
    db: dict[str, bytes] = {}
    dc: dict[str, str] = {}
    dd: dict[bytes, bytes] = {}
    dict_bytes(da, db, dc, dd)

_ERRORS = """
13:42: typing.Optional[...] cannot be applied to type int
13:66: typing.Optional[...] cannot be applied to type double
13:93: typing.Optional[...] cannot be applied to type float
14:42: typing.Optional[...] cannot be applied to type double complex
14:70: typing.Optional[...] cannot be applied to type long
14:95: typing.Optional[...] cannot be applied to type long long
24:30: typing.Optional[...] cannot be applied to type int
24:47: typing.Optional[...] cannot be applied to type float
24:87: typing.Optional[...] cannot be applied to type long

20:30: typing.Optional[...] cannot be applied to type MyStruct

28:20: Modifier 'typing.ClassVar' is not allowed here.
30:29: typing.Union[...] cannot be applied to type int
30:50: typing.Union[...] cannot be applied to type float
30:96: typing.Union[...] cannot be applied to type long
33:31: '[...] | None' cannot be applied to type int
33:60: '[...] | None' cannot be applied to type float
33:78: '[...] | None' cannot be applied to type double complex
33:104: '[...] | None' cannot be applied to type long
38:27: Cannot assign type 'list[float] object' to 'list[int] object'
40:26: Cannot assign type 'set[float] object' to 'set[int] object'
42:32: Cannot assign type 'frozenset[float] object' to 'frozenset[int] object'
44:39: Cannot assign type 'dict[float,float] object' to 'dict[int,int] object'
45:41: Cannot assign type 'dict[float,float] object' to 'dict[int,float] object'
46:41: Cannot assign type 'dict[float,float] object' to 'dict[float,int] object'
47:9: Cannot assign type 'list[float] object' to 'set[float] object'
48:9: Cannot assign type 'frozenset[float] object' to 'set[float] object'
49:9: Cannot assign type 'dict[float,float] object' to 'set[float] object'
50:9: Cannot assign type 'list[float] object' to 'frozenset[float] object'
51:9: Cannot assign type 'set[float] object' to 'frozenset[float] object'
52:9: Cannot assign type 'dict[float,float] object' to 'frozenset[float] object'
53:9: Cannot assign type 'set[float] object' to 'list[float] object'
54:9: Cannot assign type 'frozenset[float] object' to 'list[float] object'
55:9: Cannot assign type 'dict[float,float] object' to 'list[float] object'
56:9: Cannot assign type 'set[float] object' to 'dict[float,float] object'
57:9: Cannot assign type 'frozenset[float] object' to 'dict[float,float] object'
58:9: Cannot assign type 'list[float] object' to 'dict[float,float] object'
64:22: Cannot assign type 'float' to 'int'
66:12: Cannot assign type 'float' to 'int'
68:13: Cannot assign type 'float' to 'int'
73:22: Cannot assign type 'float' to 'int'
75:12: Cannot assign type 'float' to 'int'
77:13: Cannot assign type 'float' to 'int'
82:8: Cannot convert Python object to 'int *'
82:13: Cannot assign type 'int' to 'int *'
85:33: Cannot assign type 'set object' to 'frozenset[int] object'
87:8: Cannot convert Python object to 'int *'
87:13: Cannot assign type 'int' to 'int *'
143:9: Cannot assign type 'set[int] object' to 'list[int] object'
144:9: Cannot assign type 'frozenset[int] object' to 'list[int] object'
145:9: Cannot assign type 'dict[int,int] object' to 'list[int] object'
146:9: Cannot assign type 'list[int] object' to 'set[int] object'
147:9: Cannot assign type 'frozenset[int] object' to 'set[int] object'
148:9: Cannot assign type 'dict[int,int] object' to 'set[int] object'
149:9: Cannot assign type 'list[int] object' to 'frozenset[int] object'
150:9: Cannot assign type 'set[int] object' to 'frozenset[int] object'
151:9: Cannot assign type 'dict[int,int] object' to 'frozenset[int] object'
152:9: Cannot assign type 'list[int] object' to 'dict[int,int] object'
153:9: Cannot assign type 'set[int] object' to 'dict[int,int] object'
154:9: Cannot assign type 'frozenset[int] object' to 'dict[int,int] object'
161:9: Cannot assign type 'dict object' to 'list[int] object'
162:9: Cannot assign type 'frozenset object' to 'list[int] object'
163:9: Cannot assign type 'set object' to 'list[int] object'
164:9: Cannot assign type 'list object' to 'set[int] object'
165:9: Cannot assign type 'dict object' to 'set[int] object'
166:9: Cannot assign type 'frozenset object' to 'set[int] object'
167:9: Cannot assign type 'list object' to 'frozenset[int] object'
168:9: Cannot assign type 'set object' to 'frozenset[int] object'
169:9: Cannot assign type 'dict object' to 'frozenset[int] object'
170:9: Cannot assign type 'list object' to 'set[int] object'
171:9: Cannot assign type 'frozenset object' to 'set[int] object'
172:9: Cannot assign type 'dict object' to 'set[int] object'
183:15: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
188:15: Cannot convert 'bytes' object to str implicitly, decoding required
188:19: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
188:23: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
188:27: Cannot convert 'bytes' object to str implicitly, decoding required
"""
