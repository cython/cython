# mode: error
# tag: warnings

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

def subscripted_types_assignments():
    ta: tuple[str, cython.float] = ('a', 5.0)
    tb: tuple[str, cython.int] = ta
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


def subscripted_types_assignments_to_variable():
    ta: tuple[str, cython.float] = ('foo', 5.0)
    tb: tuple[str, cython.int] = ('bar', 1)
    z: cython.int = ta[1]
    zz: cython.float = 1.0
    tb[1] = zz
    h: cython.int
    for h in ta:
        pass

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
    l: cython.p_int
    for l in sa:
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

def allowed_subscripted_types_assignments():
    ta: tuple[cython.float, str] = (1.0, 'bar')
    tb: tuple[cython.float, str] = ta
    la: list[cython.float] = [5.0]
    lb: list[cython.float] = la
    sa: set[cython.int] = {5}
    sb: set[cython.int] = sa
    fa: frozenset[str] = frozenset({"bar"})
    fb: frozenset[str] = fa
    da: dict[cython.int, cython.int] = {1: 2}
    db: dict[cython.int, cython.int] = da

    t1: tuple = ta
    l1: list = la
    s1: set = sa
    f1: frozenset = fa
    d1: dict = da

    ta = t1
    la = l1
    sa = s1
    fa = f1
    da = d1

def forbidden_subscripted_types_assignments():
    ta: tuple[cython.float, str] = (1, 'bar')
    la: list[cython.int] = [5]
    sa: set[cython.int] = {5}
    fa: frozenset[cython.int] = frozenset({1})
    da: dict[cython.int, cython.int] = {1: 2}

    ta = la
    ta = sa
    ta = fa
    ta = da
    la = ta
    la = sa
    la = fa
    la = da
    sa = ta
    sa = la
    sa = fa
    sa = da
    fa = ta
    fa = la
    fa = sa
    fa = da
    da = ta
    da = la
    da = sa
    da = fa

    t: tuple = (1, 'foo')
    l: list = [1]
    s: set = {1}
    f: frozenset = frozenset({1})
    d: dict = {1:3}

    ta = l
    ta = d
    ta = f
    ta = s
    la = t
    la = d
    la = f
    la = s
    sa = t
    sa = l
    sa = d
    sa = f
    fa = t
    fa = l
    fa = s
    fa = d
    sa = t
    sa = l
    sa = f
    sa = d


cdef list_bytes(a: list[bytes]):
    pass

cdef dict_bytes(a: dict[str, bytes], b: dict[bytes, str], c: dict[bytes, bytes], d: dict[str, str]):
    pass

def forbidden_subscripted_types_args():
    la: list[str] = ['asdf']
    list_bytes(la)
    da: dict[bytes, str] = {}
    db: dict[str, bytes] = {}
    dc: dict[str, str] = {}
    dd: dict[bytes, bytes] = {}
    dict_bytes(da, db, dc, dd)


def forbidden_tuple_assignments():
    a: tuple[str, int] = ('bar', 1)
    b: tuple[int, str] = a
    c: tuple[None, int] = a
    d: tuple[str, ...] = a


def invalid_type_count():
    list2: list[int, int]
    list3: list[int, int, int]
    set2: set[int, int]
    set3: set[int, int, int]
    frozenset2: frozenset[int, int]
    frozenset3: frozenset[int, int, int]
    dict1: dict[int]
    dict2: dict[int, int, int]

def invalid_ellipsis():
    t1: tuple[..., str]
    t2: tuple[int, str, ...]
    t3: tuple[int, ..., str]
    l1: list[int, ...]
    l2: list[...]
    s1: set[str, ...]
    s2: set[...]
    s1: frozenset[str, ...]
    s2: frozenset[...]
    d1: dict[..., str]
    d2: dict[str, ...]
    d3: dict[..., ...]
    fd1: frozendict[str, ...]
    fd2: frozendict[..., str]
    fd3: frozendict[..., ...]

_WARNINGS = """
231:15: Cannot specialise 'list' with 2 types, ignoring.
232:15: Cannot specialise 'list' with 3 types, ignoring.
233:13: Cannot specialise 'set' with 2 types, ignoring.
234:13: Cannot specialise 'set' with 3 types, ignoring.
235:25: Cannot specialise 'frozenset' with 2 types, ignoring.
236:25: Cannot specialise 'frozenset' with 3 types, ignoring.
237:15: Cannot specialise 'dict' with 1 types, ignoring.
238:15: Cannot specialise 'dict' with 3 types, ignoring.
"""

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
38:33: Cannot assign type 'tuple[str object,float] object' to 'tuple[str object,int] object'
40:27: Cannot assign type 'list[float] object' to 'list[int] object'
42:26: Cannot assign type 'set[float] object' to 'set[int] object'
44:32: Cannot assign type 'frozenset[float] object' to 'frozenset[int] object'
46:39: Cannot assign type 'dict[float,float] object' to 'dict[int,int] object'
47:41: Cannot assign type 'dict[float,float] object' to 'dict[int,float] object'
48:41: Cannot assign type 'dict[float,float] object' to 'dict[float,int] object'
49:9: Cannot assign type 'list[float] object' to 'set[float] object'
50:9: Cannot assign type 'frozenset[float] object' to 'set[float] object'
51:9: Cannot assign type 'dict[float,float] object' to 'set[float] object'
52:9: Cannot assign type 'list[float] object' to 'frozenset[float] object'
53:9: Cannot assign type 'set[float] object' to 'frozenset[float] object'
54:9: Cannot assign type 'dict[float,float] object' to 'frozenset[float] object'
55:9: Cannot assign type 'set[float] object' to 'list[float] object'
56:9: Cannot assign type 'frozenset[float] object' to 'list[float] object'
57:9: Cannot assign type 'dict[float,float] object' to 'list[float] object'
58:9: Cannot assign type 'set[float] object' to 'dict[float,float] object'
59:9: Cannot assign type 'frozenset[float] object' to 'dict[float,float] object'
60:9: Cannot assign type 'list[float] object' to 'dict[float,float] object'
66:22: Cannot assign type 'float' to 'int'
68:12: Cannot assign type 'float' to 'int'
75:22: Cannot assign type 'float' to 'int'
77:12: Cannot assign type 'float' to 'int'
79:13: Cannot assign type 'float' to 'int'
84:22: Cannot assign type 'float' to 'int'
86:12: Cannot assign type 'float' to 'int'
88:13: Cannot assign type 'float' to 'int'
93:8: Cannot convert Python object to 'int *'
93:13: Cannot assign type 'int' to 'int *'
96:33: Cannot assign type 'set object' to 'frozenset[int] object'
98:8: Cannot convert Python object to 'int *'
98:13: Cannot assign type 'int' to 'int *'
159:9: Cannot assign type 'list[int] object' to 'tuple[float,str object] object'
160:9: Cannot assign type 'set[int] object' to 'tuple[float,str object] object'
161:9: Cannot assign type 'frozenset[int] object' to 'tuple[float,str object] object'
162:9: Cannot assign type 'dict[int,int] object' to 'tuple[float,str object] object'
163:9: Cannot assign type 'tuple[float,str object] object' to 'list[int] object'
164:9: Cannot assign type 'set[int] object' to 'list[int] object'
165:9: Cannot assign type 'frozenset[int] object' to 'list[int] object'
166:9: Cannot assign type 'dict[int,int] object' to 'list[int] object'
167:9: Cannot assign type 'tuple[float,str object] object' to 'set[int] object'
168:9: Cannot assign type 'list[int] object' to 'set[int] object'
169:9: Cannot assign type 'frozenset[int] object' to 'set[int] object'
170:9: Cannot assign type 'dict[int,int] object' to 'set[int] object'
171:9: Cannot assign type 'tuple[float,str object] object' to 'frozenset[int] object'
172:9: Cannot assign type 'list[int] object' to 'frozenset[int] object'
173:9: Cannot assign type 'set[int] object' to 'frozenset[int] object'
174:9: Cannot assign type 'dict[int,int] object' to 'frozenset[int] object'
175:9: Cannot assign type 'tuple[float,str object] object' to 'dict[int,int] object'
176:9: Cannot assign type 'list[int] object' to 'dict[int,int] object'
177:9: Cannot assign type 'set[int] object' to 'dict[int,int] object'
178:9: Cannot assign type 'frozenset[int] object' to 'dict[int,int] object'
186:9: Cannot assign type 'list object' to 'tuple[float,str object] object'
187:9: Cannot assign type 'dict object' to 'tuple[float,str object] object'
188:9: Cannot assign type 'frozenset object' to 'tuple[float,str object] object'
189:9: Cannot assign type 'set object' to 'tuple[float,str object] object'
190:9: Cannot assign type 'tuple object' to 'list[int] object'
191:9: Cannot assign type 'dict object' to 'list[int] object'
192:9: Cannot assign type 'frozenset object' to 'list[int] object'
193:9: Cannot assign type 'set object' to 'list[int] object'
194:9: Cannot assign type 'tuple object' to 'set[int] object'
195:9: Cannot assign type 'list object' to 'set[int] object'
196:9: Cannot assign type 'dict object' to 'set[int] object'
197:9: Cannot assign type 'frozenset object' to 'set[int] object'
198:9: Cannot assign type 'tuple object' to 'frozenset[int] object'
199:9: Cannot assign type 'list object' to 'frozenset[int] object'
200:9: Cannot assign type 'set object' to 'frozenset[int] object'
201:9: Cannot assign type 'dict object' to 'frozenset[int] object'
202:9: Cannot assign type 'tuple object' to 'set[int] object'
203:9: Cannot assign type 'list object' to 'set[int] object'
204:9: Cannot assign type 'frozenset object' to 'set[int] object'
205:9: Cannot assign type 'dict object' to 'set[int] object'
216:15: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
221:15: Cannot convert 'bytes' object to str implicitly, decoding required
221:19: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
221:23: Cannot convert Unicode string to 'bytes' implicitly, encoding required.
221:27: Cannot convert 'bytes' object to str implicitly, decoding required
226:25: Cannot assign type 'tuple[str object,int object] object' to 'tuple[int object,str object] object'
227:26: Cannot assign type 'tuple[str object,int object] object' to 'tuple[int object] object'
228:25: Cannot assign type 'tuple[str object,int object] object' to 'tuple[str object,ellipsis object] object'
"""
