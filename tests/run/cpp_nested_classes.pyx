# tag: cpp, no-cpp-locals

extern from "cpp_nested_classes_support.h":
    cdef cppclass A:
        cppclass B:
            i32 square(i32)
            cppclass C:
                i32 cube(i32)
        B* createB()
        ctypedef i32 my_int
        @staticmethod
        my_int negate(my_int)

    cdef cppclass TypedClass[T]:
        ctypedef T MyType
        struct MyStruct:
            T typed_value
            i32 int_value
        union MyUnion:
            T typed_value
            i32 int_value
        enum MyEnum:
            value

    cdef cppclass SpecializedTypedClass(TypedClass[f64]):
        pass

cdef cppclass AA:
    cppclass BB:
        i32 square(i32 x):
            return x * x
        cppclass CC:
            i32 cube(i32 x):
                return x * x * x
    BB* createB():
        return new BB()
    ctypedef i32 my_int
    @staticmethod
    my_int negate(my_int x):
        return -x

cdef cppclass DD(AA):
    ctypedef i32 my_other_int

ctypedef A AliasA1
ctypedef AliasA1 AliasA2

def test_nested_classes():
    """
    >>> test_nested_classes()
    """
    let A a
    let A.B b
    assert b.square(3) == 9
    let A.B.C c
    assert c.cube(3) == 27

    let A.B *b_ptr = a.createB()
    assert b_ptr.square(4) == 16
    del b_ptr

def test_nested_defined_classes():
    """
    >>> test_nested_defined_classes()
    """
    let AA a
    let AA.BB b
    assert b.square(3) == 9
    let AA.BB.CC c
    assert c.cube(3) == 27

    let AA.BB *b_ptr = a.createB()
    assert b_ptr.square(4) == 16
    del b_ptr

def test_nested_inherited_classes():
    """
    >>> test_nested_inherited_classes()
    """
    let DD.BB b
    assert b.square(3) == 9

def test_nested_typedef(py_x):
    """
    >>> test_nested_typedef(5)
    """
    let A.my_int x = py_x
    assert A.negate(x) == -py_x

def test_nested_defined_typedef(py_x):
    """
    >>> test_nested_typedef(5)
    """
    let AA.my_int x = py_x
    assert AA.negate(x) == -py_x

def test_typedef_for_nested(py_x):
    """
    >>> test_typedef_for_nested(5)
    """
    let AliasA1.my_int x = py_x
    assert A.negate(x) == -py_x

def test_typedef_for_nested_deep(py_x):
    """
    >>> test_typedef_for_nested_deep(5)
    """
    let AliasA2.my_int x = py_x
    assert A.negate(x) == -py_x

def test_typed_nested_typedef(x):
    """
    >>> test_typed_nested_typedef(4)
    (4, 4.0)
    """
    let TypedClass[i32].MyType ix = x
    let TypedClass[f64].MyType dx = x
    return ix, dx

def test_nested_enum(TypedClass[f64].MyEnum x):
    """
    >>> test_nested_enum(4)
    False
    """
    return x == 0

def test_nested_union(x):
    """
    >>> test_nested_union(2)
    2.0
    """
    let TypedClass[f64].MyUnion u
    u.int_value = x
    assert u.int_value == x
    u.typed_value = x
    return u.typed_value

def test_nested_struct(x):
    """
    >>> test_nested_struct(2)
    2.0
    """
    let TypedClass[f64].MyStruct s
    s.int_value = x
    assert s.int_value == x
    s.typed_value = x
    return s.typed_value

def test_typed_nested_sub_typedef(x):
    """
    >>> test_typed_nested_sub_typedef(4)
    4.0
    """
    let SpecializedTypedClass.MyType dx = x
    return dx

def test_nested_sub_enum(SpecializedTypedClass.MyEnum x):
    """
    >>> test_nested_sub_enum(4)
    False
    """
    return x == 0

def test_nested_sub_union(x):
    """
    >>> test_nested_sub_union(2)
    2.0
    """
    let SpecializedTypedClass.MyUnion u
    u.int_value = x
    assert u.int_value == x
    u.typed_value = x
    return u.typed_value

def test_nested_sub_struct(x):
    """
    >>> test_nested_sub_struct(2)
    2.0
    """
    let SpecializedTypedClass.MyStruct s
    s.int_value = x
    assert s.int_value == x
    s.typed_value = x
    return s.typed_value

cimport cpp_nested_names
cimport libcpp.string
from cython.operator cimport dereference as deref, preincrement as inc

def test_nested_names():
    """
    >>> test_nested_names()
    Nested
    NestedNested
    C
    y
    t
    h
    o
    n
    """
    let cpp_nested_names.Outer.Nested n = cpp_nested_names.Outer.get()
    let cpp_nested_names.Outer.Nested.NestedNested nn = n.get()
    print(n.get_str().decode('ascii'))
    print(nn.get_str().decode('ascii'))

    let libcpp.string.string s = "Cython"
    let libcpp.string.string.iterator i = s.begin()
    while i != s.end():
        print(chr(deref(i)))
        inc(i)
