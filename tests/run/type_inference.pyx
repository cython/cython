# cython: infer_types = True


cimport cython
from cython cimport typeof, infer_types

from cpython cimport bool

##################################################
# type inference tests in 'full' mode

cdef class MyType:
    pass

def simple():
    """
    >>> simple()
    """
    i = 3
    assert typeof(i) == "long", typeof(i)
    x = 1.41
    assert typeof(x) == "double", typeof(x)
    xptr = &x
    assert typeof(xptr) == "double *", typeof(xptr)
    xptrptr = &xptr
    assert typeof(xptrptr) == "double **", typeof(xptrptr)
    b = b"abc"
    assert typeof(b) == "bytes object", typeof(b)
    s = "abc"
    assert typeof(s) == "str object", typeof(s)
    u = u"xyz"
    assert typeof(u) == "unicode object", typeof(u)
    L = [1,2,3]
    assert typeof(L) == "list object", typeof(L)
    t = (4,5,6,())
    assert typeof(t) == "tuple object", typeof(t)
    t2 = (4, 5.0, 6)
    assert typeof(t2) == "(long, double, long)", typeof(t)

def builtin_types():
    """
    >>> builtin_types()
    """
    b = bytes()
    assert typeof(b) == "bytes object", typeof(b)
    u = unicode()
    assert typeof(u) == "unicode object", typeof(u)
    L = list()
    assert typeof(L) == "list object", typeof(L)
    t = tuple()
    assert typeof(t) == "tuple object", typeof(t)
    d = dict()
    assert typeof(d) == "dict object", typeof(d)
    B = bool()
    assert typeof(B) == "bool", typeof(B)

def slicing():
    """
    >>> slicing()
    """
    b = b"abc"
    assert typeof(b) == "bytes object", typeof(b)
    b1 = b[1:2]
    assert typeof(b1) == "bytes object", typeof(b1)
    b2 = b[1:2:2]
    assert typeof(b2) == "bytes object", typeof(b2)
    u = u"xyz"
    assert typeof(u) == "unicode object", typeof(u)
    u1 = u[1:2]
    assert typeof(u1) == "unicode object", typeof(u1)
    u2 = u[1:2:2]
    assert typeof(u2) == "unicode object", typeof(u2)
    s = "xyz"
    assert typeof(s) == "str object", typeof(s)
    s1 = s[1:2]
    assert typeof(s1) == "str object", typeof(s1)
    s2 = s[1:2:2]
    assert typeof(s2) == "str object", typeof(s2)
    L = [1,2,3]
    assert typeof(L) == "list object", typeof(L)
    L1 = L[1:2]
    assert typeof(L1) == "list object", typeof(L1)
    L2 = L[1:2:2]
    assert typeof(L2) == "list object", typeof(L2)
    t = (4,5,6,())
    assert typeof(t) == "tuple object", typeof(t)
    t1 = t[1:2]
    assert typeof(t1) == "tuple object", typeof(t1)
    t2 = t[1:2:2]
    assert typeof(t2) == "tuple object", typeof(t2)

def indexing():
    """
    >>> indexing()
    """
    b = b"abc"
    assert typeof(b) == "bytes object", typeof(b)
    b1 = b[1]
    assert typeof(b1) == "Python object", typeof(b1) # Py2: bytes, Py3: int
    u = u"xyz"
    assert typeof(u) == "unicode object", typeof(u)
    u1 = u[1]
    assert typeof(u1) == "Py_UCS4", typeof(u1)
    s = "xyz"
    assert typeof(s) == "str object", typeof(s)
    s1 = s[1]
    assert typeof(s1) == "str object", typeof(s1)
    L = [1,2,3]
    assert typeof(L) == "list object", typeof(L)
    L1 = L[1]
    assert typeof(L1) == "Python object", typeof(L1)
    t = (4,5,())
    assert typeof(t) == "tuple object", typeof(t)
    t1 = t[1]
    assert typeof(t1) == "long", typeof(t1)
    t2 = ('abc', 'def', 'ghi')
    assert typeof(t2) == "tuple object", typeof(t2)
    t2_1 = t2[1]
    assert typeof(t2_1) == "str object", typeof(t2_1)
    t2_2 = t2[t[0]-3]
    assert typeof(t2_2) == "str object", typeof(t2_2)
    t5 = (b'abc', 'def', u'ghi')
    t5_0 = t5[0]
    assert typeof(t5_0) == "bytes object", typeof(t5_0)
    t5_1 = t5[1]
    assert typeof(t5_1) == "str object", typeof(t5_1)
    t5_2 = t5[2]
    assert typeof(t5_2) == "unicode object", typeof(t5_2)
    t5_3 = t5[t[0]-3]
    assert typeof(t5_3) == "Python object", typeof(t5_3)


def multiple_assignments():
    """
    >>> multiple_assignments()
    """
    a = 3
    a = 4
    a = 5
    assert typeof(a) == "long", typeof(a)
    b = a
    b = 3.1
    b = 3.14159
    assert typeof(b) == "double", typeof(b)
    c = a
    c = b
    c = [1,2,3]
    assert typeof(c) == "Python object", typeof(c)
    d = b'abc'
    d = bytes()
    d = bytes(b'xyz')
    d = None
    assert typeof(d) == "bytes object", typeof(d)


def arithmetic():
    """
    >>> arithmetic()
    """
    a = 1 + 2
    assert typeof(a) == "long", typeof(a)
    b = 1 + 1.5
    assert typeof(b) == "double", typeof(b)
    c = 1 + <object>2
    assert typeof(c) == "Python object", typeof(c)
    d = 1 * 1.5 ** 2
    assert typeof(d) == "double", typeof(d)

cdef class some_class:
    pass

def unary_operators():
    """
    >>> unary_operators()
    """
    cdef int x = 1
    assert typeof(~x) == "int", typeof(~x)
    cdef some_class obj
    assert typeof(~obj) == "Python object", typeof(~obj)
    a = int(1)
    assert typeof(a) == "Python object", typeof(a)
    b = not int(3)
    assert typeof(b) == "bint", typeof(b)
    c = +int(3)
    assert typeof(c) == "Python object", typeof(c)
    d = -int(5)
    assert typeof(d) == "Python object", typeof(d)


def builtin_type_operations():
    """
    >>> builtin_type_operations()
    """
    b1 = b'a' * 10
    b1 = 10 * b'a'
    b1 = 10 * b'a' * 10
    assert typeof(b1) == "bytes object", typeof(b1)
    b2 = b'a' + b'b'
    assert typeof(b2) == "bytes object", typeof(b2)
    u1 = u'a' * 10
    u1 = 10 * u'a'
    assert typeof(u1) == "unicode object", typeof(u1)
    u2 = u'a' + u'b'
    assert typeof(u2) == "unicode object", typeof(u2)
    u3 = u'a%s' % u'b'
    u3 = u'a%s' % 10
    assert typeof(u3) == "unicode object", typeof(u3)
    s1 = "abc %s" % "x"
    s1 = "abc %s" % 10
    assert typeof(s1) == "str object", typeof(s1)
    s2 = "abc %s" + "x"
    assert typeof(s2) == "str object", typeof(s2)
    s3 = "abc %s" * 10
    s3 = "abc %s" * 10 * 10
    s3 = 10 * "abc %s" * 10
    assert typeof(s3) == "str object", typeof(s3)
    L1 = [] + []
    assert typeof(L1) == "list object", typeof(L1)
    L2 = [] * 2
    assert typeof(L2) == "list object", typeof(L2)
    T1 = () + ()
    assert typeof(T1) == "tuple object", typeof(T1)
    T2 = () * 2
    assert typeof(T2) == "tuple object", typeof(T2)

def builtin_type_methods():
    """
    >>> builtin_type_methods()
    """
    l = []
    assert typeof(l) == 'list object', typeof(l)
    append = l.append
    assert typeof(append) == 'Python object', typeof(append)
    append(1)
    assert l == [1], str(l)

cdef int cfunc(int x):
    return x+1

def c_functions():
    """
    >>> c_functions()
    """
    f = cfunc
    assert typeof(f) == 'int (*)(int)', typeof(f)
    assert 2 == f(1)

def builtin_functions():
    """
    >>> _abs, _getattr = builtin_functions()
    Python object
    Python object
    >>> _abs(-1)
    1
    >>> class o(object): pass
    >>> o.x = 1
    >>> _getattr(o, 'x')
    1
    """
    _abs = abs
    print(typeof(_abs))
    _getattr = getattr
    print(typeof(_getattr))
    return _abs, _getattr

def cascade():
    """
    >>> cascade()
    """
    a = 1.0
    b = a + 2
    c = b + 3
    d = c + 4
    assert typeof(d) == "double"
    e = a + b + c + d
    assert typeof(e) == "double"

def cascaded_assignment():
    a = b = c = d = 1.0
    assert typeof(a) == "double"
    assert typeof(b) == "double"
    assert typeof(c) == "double"
    assert typeof(d) == "double"
    e = a + b + c + d
    assert typeof(e) == "double"

def increment():
    """
    >>> increment()
    """
    a = 5
    a += 1
    assert typeof(a) == "long"

def loop():
    """
    >>> loop()
    """
    for a in range(10):
        pass
    assert typeof(a) == "long"

    b = 1.0
    for b in range(5):
        pass
    assert typeof(b) == "double"

    for c from 0 <= c < 10 by .5:
        pass
    assert typeof(c) == "double"

    for d in range(0, 10L, 2):
        pass
    assert typeof(a) == "long"

def loop_over_charptr():
    """
    >>> print( loop_over_charptr() )
    char
    """
    cdef char* char_ptr_string = 'abcdefg'
    for c in char_ptr_string:
        pass
    return typeof(c)

def loop_over_bytes_literal():
    """
    >>> print( loop_over_bytes_literal() )
    Python object
    """
    for c in b'abcdefg':
        pass
    return typeof(c)

def loop_over_bytes():
    """
    >>> print( loop_over_bytes() )
    Python object
    """
    cdef bytes bytes_string = b'abcdefg'
    # bytes in Py2, int in Py3
    for c in bytes_string:
        pass
    return typeof(c)

def loop_over_str():
    """
    >>> print( loop_over_str() )
    str object
    """
    cdef str string = 'abcdefg'
    # str (bytes) in Py2, str (unicode) in Py3
    for c in string:
        pass
    return typeof(c)

def loop_over_unicode():
    """
    >>> print( loop_over_unicode() )
    Py_UCS4
    """
    cdef unicode ustring = u'abcdefg'
    # Py_UCS4 can represent any Unicode character
    for uchar in ustring:
        pass
    return typeof(uchar)

def loop_over_unicode_literal():
    """
    >>> print( loop_over_unicode_literal() )
    Py_UCS4
    """
    # Py_UCS4 can represent any Unicode character
    for uchar in u'abcdefg':
        pass
    return typeof(uchar)

def loop_over_int_array():
    """
    >>> print( loop_over_int_array() )
    int
    """
    cdef int[10] int_array
    for i in int_array:
        pass
    return typeof(i)

cdef struct MyStruct:
    int a

def loop_over_struct_ptr():
    """
    >>> print( loop_over_struct_ptr() )
    MyStruct
    """
    cdef MyStruct[10] a_list
    cdef MyStruct *a_ptr = a_list
    for i in a_list[:10]:
        pass
    return typeof(i)

cdef unicode retu():
    return u"12345"

cdef bytes retb():
    return b"12345"

def conditional(x):
    """
    >>> conditional(True)
    (True, 'Python object')
    >>> conditional(False)
    (False, 'Python object')
    """
    if x:
        a = retu()
    else:
        a = retb()
    return type(a) is unicode, typeof(a)

##################################################
# type inference tests that work in 'safe' mode

@infer_types(None)
def double_inference():
    """
    >>> values, types = double_inference()
    >>> values == (1.0, 1.0*2, 1.0*2.0+2.0*2.0, 1.0*2.0)
    True
    >>> types
    ('double', 'double', 'double', 'Python object')
    """
    d_a = 1.0
    d_b = d_a * float(2)
    d_c = d_a * float(some_float_value()) + d_b * float(some_float_value())
    o_d = d_a * some_float_value()
    return (d_a,d_b,d_c,o_d), (typeof(d_a), typeof(d_b), typeof(d_c), typeof(o_d))

cdef object some_float_value():
    return 2.0


@infer_types(None)
@cython.test_fail_if_path_exists('//DefNode//NameNode[@type.is_pyobject = True]')
@cython.test_assert_path_exists('//DefNode//NameNode[@type.is_pyobject]',
                                '//DefNode//NameNode[@type.is_pyobject = False]')
def double_loop():
    """
    >>> double_loop() == 1.0 * 10
    True
    """
    cdef int i
    d = 1.0
    for i in range(9):
        d += 1.0
    return d

@infer_types(None)
def safe_only():
    """
    >>> safe_only()
    """
    a = 1.0
    assert typeof(a) == "double", typeof(c)
    b = 1;
    assert typeof(b) == "long", typeof(b)
    c = MyType()
    assert typeof(c) == "MyType", typeof(c)
    for i in range(10): pass
    assert typeof(i) == "long", typeof(i)
    d = 1
    res = ~d
    assert typeof(d) == "long", typeof(d)

    # we special-case inference to type str, see
    # trac #553
    s = "abc"
    assert typeof(s) == "Python object", typeof(s)
    cdef str t = "def"
    assert typeof(t) == "str object", typeof(t)

    # potentially overflowing arithmetic
    e = 1
    e += 1
    assert typeof(e) == "Python object", typeof(e)
    f = 1
    res = f * 10
    assert typeof(f) == "Python object", typeof(f)
    g = 1
    res = 10*(~g)
    assert typeof(g) == "Python object", typeof(g)
    for j in range(10):
        res = -j
    assert typeof(j) == "Python object", typeof(j)
    h = 1
    res = abs(h)
    assert typeof(h) == "Python object", typeof(h)
    cdef int c_int = 1
    assert typeof(abs(c_int)) == "int", typeof(abs(c_int))

@infer_types(None)
def safe_c_functions():
    """
    >>> safe_c_functions()
    """
    f = cfunc
    assert typeof(f) == 'int (*)(int)', typeof(f)
    assert 2 == f(1)

@infer_types(None)
def ptr_types():
    """
    >>> ptr_types()
    """
    cdef int a
    a_ptr = &a
    assert typeof(a_ptr) == "int *", typeof(a_ptr)
    a_ptr_ptr = &a_ptr
    assert typeof(a_ptr_ptr) == "int **", typeof(a_ptr_ptr)
    cdef int[1] b
    b_ref = b
    assert typeof(b_ref) == "int *", typeof(b_ref)
    ptr = &a
    ptr = b
    assert typeof(ptr) == "int *", typeof(ptr)

def const_types(const double x, double y, double& z):
    """
    >>> const_types(1, 1, 1)
    """
    a = x
    a = y
    a = z
    assert typeof(a) == "double", typeof(a)

@infer_types(None)
def args_tuple_keywords(*args, **kwargs):
    """
    >>> args_tuple_keywords(1,2,3, a=1, b=2)
    """
    assert typeof(args) == "tuple object", typeof(args)
    assert typeof(kwargs) == "dict object", typeof(kwargs)

@infer_types(None)
def args_tuple_keywords_reassign_same(*args, **kwargs):
    """
    >>> args_tuple_keywords_reassign_same(1,2,3, a=1, b=2)
    """
    assert typeof(args) == "tuple object", typeof(args)
    assert typeof(kwargs) == "dict object", typeof(kwargs)

    args = ()
    kwargs = {}

@infer_types(None)
def args_tuple_keywords_reassign_pyobjects(*args, **kwargs):
    """
    >>> args_tuple_keywords_reassign_pyobjects(1,2,3, a=1, b=2)
    """
    assert typeof(args) == "Python object", typeof(args)
    assert typeof(kwargs) == "Python object", typeof(kwargs)

    args = []
    kwargs = "test"

#                 / A -> AA -> AAA
# Base0 -> Base -
#                 \ B -> BB
# C -> CC

cdef class Base0: pass
cdef class Base(Base0): pass
cdef class A(Base): pass
cdef class AA(A): pass
cdef class AAA(AA): pass
cdef class B(Base): pass
cdef class BB(B): pass
cdef class C: pass
cdef class CC(C): pass

@infer_types(None)
def common_extension_type_base():
    """
    >>> common_extension_type_base()
    """
    x = A()
    x = AA()
    assert typeof(x) == "A", typeof(x)
    y = A()
    y = B()
    assert typeof(y) == "Base", typeof(y)
    z = AAA()
    z = BB()
    assert typeof(z) == "Base", typeof(z)
    w = A()
    w = CC()
    assert typeof(w) == "Python object", typeof(w)

cdef class AcceptsKeywords:
    def __init__(self, *args, **kwds):
        pass

@infer_types(None)
def constructor_call():
    """
    >>> constructor_call()
    """
    x = AcceptsKeywords(a=1, b=2)
    assert typeof(x) == "AcceptsKeywords", typeof(x)


@infer_types(None)
def large_literals():
    """
    >>> large_literals()
    """
    # It's only safe to infer small integer literals.
    a = 10
    b = 100000000000000000000000000000000
    assert typeof(a) == "long", typeof(a)
    assert typeof(b) == "Python object", typeof(b)
    c, d = 10, 100000000000000000000000000000000
    assert typeof(c) == "long", typeof(c)
    assert typeof(d) == "Python object", typeof(d)


class EmptyContextManager(object):
    def __enter__(self):
        return None
    def __exit__(self, *args):
        return 0

def with_statement():
    """
    >>> with_statement()
    Python object
    Python object
    """
    x = 1.0
    with EmptyContextManager() as x:
        print(typeof(x))
    print(typeof(x))
    return x

@cython.final
cdef class TypedContextManager(object):
    cpdef double __enter__(self):
        return 2.0
    def __exit__(self, *args):
        return 0

def with_statement_typed():
    """
    >>> with_statement_typed()
    double
    double
    2.0
    """
    x = 1.0
    with TypedContextManager() as x:
        print(typeof(x))
    print(typeof(x))
    return x

def with_statement_untyped():
    """
    >>> with_statement_untyped()
    Python object
    Python object
    2.0
    """
    x = 1.0
    cdef object t = TypedContextManager()
    with t as x:
        print(typeof(x))
    print(typeof(x))
    return x

def self_lookup(a):
    b = a
    b = b.foo(keyword=None)
    print typeof(b)

# Regression test for trac #638.

def bar(foo):
    qux = foo
    quux = foo[qux.baz]


cdef enum MyEnum:
    enum_x = 1
    enum_y = 2

ctypedef long my_long
def test_int_typedef_inference():
    """
    >>> test_int_typedef_inference()
    """
    cdef long x = 1
    cdef my_long y = 2
    cdef long long z = 3
    assert typeof(x + y) == typeof(y + x) == 'my_long', typeof(x + y)
    assert typeof(y + z) == typeof(z + y) == 'long long', typeof(y + z)

from libc.stdint cimport int32_t, int64_t
def int64_long_sum():
    cdef long x = 1
    cdef int32_t x32 = 2
    cdef int64_t x64 = 3
    cdef unsigned long ux = 4
    assert typeof(x + x32) == typeof(x32 + x) == 'long', typeof(x + x32)
    assert typeof(x + x64) == typeof(x64 + x) == 'int64_t', typeof(x + x64)
    # The correct answer here is either unsigned long or int64_t, depending on
    # whether sizeof(long) == 64 or not.  Incorrect signedness is probably
    # preferable to incorrect width.
    assert typeof(ux + x64) == typeof(x64 + ux) == 'int64_t', typeof(ux + x64)

cdef class InferInProperties:
    """
    >>> InferInProperties().x
    ('double', 'unicode object', 'MyEnum', 'MyEnum')
    """
    cdef MyEnum attr
    def __cinit__(self):
        self.attr = enum_x

    property x:
        def __get__(self):
            a = 1.0
            b = u'abc'
            c = self.attr
            d = enum_y
            c = d
            return typeof(a), typeof(b), typeof(c), typeof(d)

cdef class WithMethods:
    cdef int offset
    def __init__(self, offset):
        self.offset = offset
    cpdef int one_arg(self, int x):
        return x + self.offset
    cpdef int default_arg(self, int x, int y=0):
        return x + y + self.offset

def test_bound_methods():
  """
  >>> test_bound_methods()
  """
  o = WithMethods(10)
  assert typeof(o) == 'WithMethods', typeof(o)

  one_arg = o.one_arg
  assert one_arg(2) == 12, one_arg(2)

  default_arg = o.default_arg
  assert default_arg(2) == 12, default_arg(2)
  assert default_arg(2, 3) == 15, default_arg(2, 2)
