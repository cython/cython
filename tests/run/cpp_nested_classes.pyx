# tag: cpp

cdef extern from "cpp_nested_classes_support.h":
    cdef cppclass A:
        cppclass B:
            int square(int)
            cppclass C:
                int cube(int)
        B* createB()
        ctypedef int my_int
        @staticmethod
        my_int negate(my_int)

    cdef cppclass TypedClass[T]:
        ctypedef T MyType
        struct MyStruct:
            T typed_value
            int int_value
        union MyUnion:
            T typed_value
            int int_value
        enum MyEnum:
            value

    cdef cppclass SpecializedTypedClass(TypedClass[double]):
        pass


def test_nested_classes():
    """
    >>> test_nested_classes()
    """
    cdef A a
    cdef A.B b
    assert b.square(3) == 9
    cdef A.B.C c
    assert c.cube(3) == 27

    cdef A.B *b_ptr = a.createB()
    assert b_ptr.square(4) == 16
    del b_ptr

def test_nested_typedef(py_x):
    """
    >>> test_nested_typedef(5)
    """
    cdef A.my_int x = py_x
    assert A.negate(x) == -py_x

def test_typed_nested_typedef(x):
    """
    >>> test_typed_nested_typedef(4)
    (4, 4.0)
    """
    cdef TypedClass[int].MyType ix = x
    cdef TypedClass[double].MyType dx = x
    return ix, dx

def test_nested_enum(TypedClass[double].MyEnum x):
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
    cdef TypedClass[double].MyUnion u
    u.int_value = x
    assert u.int_value == x
    u.typed_value = x
    return u.typed_value

def test_nested_struct(x):
    """
    >>> test_nested_struct(2)
    2.0
    """
    cdef TypedClass[double].MyStruct s
    s.int_value = x
    assert s.int_value == x
    s.typed_value = x
    return s.typed_value



def test_typed_nested_sub_typedef(x):
    """
    >>> test_typed_nested_sub_typedef(4)
    4.0
    """
    cdef SpecializedTypedClass.MyType dx = x
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
    cdef SpecializedTypedClass.MyUnion u
    u.int_value = x
    assert u.int_value == x
    u.typed_value = x
    return u.typed_value

def test_nested_sub_struct(x):
    """
    >>> test_nested_sub_struct(2)
    2.0
    """
    cdef SpecializedTypedClass.MyStruct s
    s.int_value = x
    assert s.int_value == x
    s.typed_value = x
    return s.typed_value
