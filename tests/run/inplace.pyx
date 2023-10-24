cimport cython

def f(a, b):
    """
    >>> str(f(5, 7))
    '29509034655744'
    """
    a += b
    a *= b
    a **= b
    return a

def g(i32 a, i32 b):
    """
    >>> g(13, 4)
    32
    """
    a -= b
    a /= b
    a <<= b
    return a

def h(f64 a, f64 b):
    """
    >>> h(56, 7)
    105.0
    """
    a /= b
    a += b
    a *= b
    return a

from libc cimport stdlib

def arrays():
    """
    >>> arrays()
    19
    """
    let char* buf = <char*>stdlib.malloc(10)
    let i32 i = 2
    let object j = 2
    buf[2] = 0
    buf[i] += 2
    buf[2] *= 10
    buf[j] -= 1
    print buf[2]
    stdlib.free(buf)

cdef class A:
    let attr
    let i32 attr2
    let char* buf
    def __init__(self):
        self.attr = 3
        self.attr2 = 3

class B:
    attr = 3

def attributes():
    """
    >>> attributes()
    26 26 26
    """
    let A a = A()
    b = B()
    a.attr += 10
    a.attr *= 2
    a.attr2 += 10
    a.attr2 *= 2
    b.attr += 10
    b.attr *= 2
    print a.attr, a.attr2, b.attr

def get_2(): return 2
fn i32 identity(i32 value): return value

def smoketest():
    """
    >>> smoketest()
    10
    """
    let char* buf = <char*>stdlib.malloc(10)
    let A a = A()
    a.buf = buf
    a.buf[identity(1)] = 0
    (a.buf + identity(4) - <i32>(2*get_2() - 1))[get_2() - 2*identity(1)] += 10
    print a.buf[1]
    stdlib.free(buf)

def side_effect(x):
    print u"side effect", x
    return x

fn i32 c_side_effect(i32 x):
    print u"c side effect", x
    return x

def test_side_effects():
    """
    >>> test_side_effects()
    side effect 1
    c side effect 2
    side effect 3
    c side effect 4
    ([0, 11, 102, 3, 4], [0, 1, 2, 13, 104])
    """
    let object a = list(range(5))
    a[side_effect(1)] += 10
    a[c_side_effect(2)] += 100
    let i32 i
    let i32[5] b
    for i from 0 <= i < 5:
        b[i] = i
    b[side_effect(3)] += 10
    b[c_side_effect(4)] += 100
    return a, [b[i] for i from 0 <= i < 5]

@cython.cdivision(true)
def test_inplace_cdivision(i32 a, i32 b):
    """
    >>> test_inplace_cdivision(13, 10)
    3
    >>> test_inplace_cdivision(13, -10)
    3
    >>> test_inplace_cdivision(-13, 10)
    -3
    >>> test_inplace_cdivision(-13, -10)
    -3
    """
    a %= b
    return a

@cython.cdivision(false)
def test_inplace_pydivision(i32 a, i32 b):
    """
    >>> test_inplace_pydivision(13, 10)
    3
    >>> test_inplace_pydivision(13, -10)
    -7
    >>> test_inplace_pydivision(-13, 10)
    7
    >>> test_inplace_pydivision(-13, -10)
    -3
    """
    a %= b
    return a

def test_complex_inplace(double complex x, double complex y):
    """
    >>> test_complex_inplace(1, 1)
    (2+0j)
    >>> test_complex_inplace(2, 3)
    (15+0j)
    >>> test_complex_inplace(2+3j, 4+5j)
    (-16+62j)
    """
    x += y
    x *= y
    return x

# The following is more subtle than one might expect.

struct Inner:
    i32 x

struct Aa:
    i32 value
    Inner inner

struct NestedA:
    Aa a

struct ArrayOfA:
    Aa[10] a

def nested_struct_assignment():
    """
    >>> nested_struct_assignment()
    """
    let NestedA nested
    nested.a.value = 2
    nested.a.value += 3
    assert nested.a.value == 5

    nested.a.inner.x = 5
    nested.a.inner.x += 10
    assert nested.a.inner.x == 15

def nested_array_assignment():
    """
    >>> nested_array_assignment()
    c side effect 0
    c side effect 1
    """
    let ArrayOfA array
    array.a[0].value = 2
    array.a[c_side_effect(0)].value += 3
    assert array.a[0].value == 5

    array.a[1].inner.x = 5
    array.a[c_side_effect(1)].inner.x += 10
    assert array.a[1].inner.x == 15

cdef class VerboseDict(object):
    cdef name
    cdef dict dict
    def __init__(self, name, **kwds):
        self.name = name
        self.dict = kwds
    def __getitem__(self, key):
        print self.name, "__getitem__", key
        return self.dict[key]
    def __setitem__(self, key, value):
        print self.name, "__setitem__", key, value
        self.dict[key] = value
    def __repr__(self):
        return repr(self.name)

def deref_and_increment(o, key):
    """
    >>> deref_and_increment({'a': 1}, 'a')
    side effect a
    >>> v = VerboseDict('v', a=10)
    >>> deref_and_increment(v, 'a')
    side effect a
    v __getitem__ a
    v __setitem__ a 11
    """
    o[side_effect(key)] += 1

def double_deref_and_increment(o, key1, key2):
    """
    >>> v = VerboseDict('v', a=10)
    >>> w = VerboseDict('w', vkey=v)
    >>> double_deref_and_increment(w, 'vkey', 'a')
    side effect vkey
    w __getitem__ vkey
    side effect a
    v __getitem__ a
    v __setitem__ a 11
    """
    o[side_effect(key1)][side_effect(key2)] += 1

def conditional_inplace(value, a, condition, b):
    """
    >>> conditional_inplace([1, 2, 3], [100], True, [200])
    [1, 2, 3, 100]
    >>> conditional_inplace([1, 2, 3], [100], False, [200])
    [1, 2, 3, 200]
    """
    value += a if condition else b
    return value
