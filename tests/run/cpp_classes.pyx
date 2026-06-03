# mode: run
# tag: cpp, werror, no-cpp-locals

from libcpp.vector cimport vector

cdef extern from "shapes.h" namespace "shapes":

    cdef cppclass Shape:
        float area()

    cdef cppclass Ellipse(Shape):
        Ellipse(int a, int b) except + nogil

    cdef cppclass Circle(Ellipse):
        int radius
        Circle(int r) except +

    cdef cppclass Rectangle(Shape):
        int width
        int height
        Rectangle() except +
        Rectangle(int h, int w) except +
        int method(int x)
        int method(bint b)

    cdef cppclass Square(Rectangle):
        int side
        Square(int s) except +

    cdef cppclass Empty(Shape):
        pass

    cdef cppclass EmptyWithDocstring(Shape):
        """
        This is a docstring !
        """


    int constructor_count, destructor_count


def test_new_del():
    """
    >>> test_new_del()
    2 0
    2 2
    """
    c,d = constructor_count, destructor_count
    cdef Rectangle *rect = new Rectangle(10, 20)
    cdef Circle *circ = new Circle(15)
    print constructor_count-c, destructor_count-d
    del rect, circ
    print constructor_count-c, destructor_count-d


def test_default_constructor():
    """
    >>> test_default_constructor()
    0.0
    """
    shape = new Empty()
    try:
        return shape.area()
    finally:
        del shape


def test_constructor_nogil():
    """
    >>> test_constructor_nogil()
    True
    """
    with nogil:
        shape = new Ellipse(4, 5)
    try:
        return 62 < shape.area() < 63 or shape.area()
    finally:
        del shape


def test_rect_area(w, h):
    """
    >>> test_rect_area(3, 4)
    12.0
    """
    cdef Rectangle *rect = new Rectangle(w, h)
    try:
        return rect.area()
    finally:
        del rect


def test_overload_bint_int():
    """
    >>> test_overload_bint_int()
    202
    201
    """
    cdef Rectangle *rect1 = new Rectangle(10, 20)
    cdef Rectangle *rect2 = new Rectangle(10, 20)

    try:
        print rect1.method(<int> 2)
        print rect2.method(<bint> True)
    finally:
        del rect1
        del rect2


def test_square_area(w):
    """
    >>> test_square_area(15)
    (225.0, 225.0)
    """
    cdef Square *sqr = new Square(w)
    cdef Rectangle *rect = sqr
    try:
        return rect.area(), sqr.area()
    finally:
        del sqr


cdef double get_area(Rectangle s):
    return s.area()

def test_value_call(int w):
    """
    >>> test_value_call(5)
    (25.0, 25.0)
    """
    cdef Square *sqr = new Square(w)
    cdef Rectangle *rect = sqr
    try:
        return get_area(sqr[0]), get_area(rect[0])
    finally:
        del sqr


cdef struct StructWithEmpty:
    Empty empty


def get_destructor_count():
    return destructor_count

def test_stack_allocation(int w, int h):
    """
    >>> d = test_stack_allocation(10, 12)
    125
    >>> get_destructor_count() - d
    1
    """
    cdef Rectangle rect
    rect.width = w
    rect.height = h
    print rect.method(<int>5)
    return destructor_count

def test_stack_allocation_in_struct():
    """
    >>> d = test_stack_allocation_in_struct()
    >>> get_destructor_count() - d
    1
    """
    cdef StructWithEmpty swe
    sizeof(swe.empty) # use it for something
    return destructor_count

cdef class EmptyHolder:
    cdef Empty empty

cdef class AnotherEmptyHolder(EmptyHolder):
    cdef Empty another_empty

cdef class EmptyViaStructHolder:
    cdef StructWithEmpty swe

def test_class_member():
    """
    >>> test_class_member()
    """
    start_constructor_count = constructor_count
    start_destructor_count = destructor_count
    e1 = EmptyHolder()
    assert constructor_count - start_constructor_count == 1, \
           constructor_count - start_constructor_count
    e2 = EmptyHolder()
    assert constructor_count - start_constructor_count == 2, \
           constructor_count - start_constructor_count
    del e1, e2
    assert destructor_count - start_destructor_count == 2, \
           destructor_count - start_destructor_count


def test_derived_class_member():
    """
    >>> test_derived_class_member()
    """
    start_constructor_count = constructor_count
    start_destructor_count = destructor_count
    e = AnotherEmptyHolder()
    assert constructor_count - start_constructor_count == 2, \
           constructor_count - start_constructor_count
    del e
    assert destructor_count - start_destructor_count == 2, \
           destructor_count - start_destructor_count

def test_class_in_struct_member():
    """
    >>> test_class_in_struct_member()
    """
    start_constructor_count = constructor_count
    start_destructor_count = destructor_count
    e = EmptyViaStructHolder()
    #assert constructor_count - start_constructor_count == 1, \
    #       constructor_count - start_constructor_count
    del e
    assert destructor_count - start_destructor_count == 1, \
           destructor_count - start_destructor_count

cdef class TemplateClassMember:
    cdef vector[int] x
    cdef vector[vector[Empty]] vec

def test_template_class_member():
    """
    >>> test_template_class_member()
    """
    cdef vector[Empty] inner
    inner.push_back(Empty())
    inner.push_back(Empty())
    o = TemplateClassMember()
    o.vec.push_back(inner)

    start_destructor_count = destructor_count
    del o
    assert destructor_count - start_destructor_count == 2, \
           destructor_count - start_destructor_count


ctypedef vector[int]* vector_int_ptr
cdef vector[vector_int_ptr] create_to_delete() except *:
    cdef vector[vector_int_ptr] v
    v.push_back(new vector[int]())
    return v
cdef int f(int x):
    return x


def test_nested_del():
    """
    >>> test_nested_del()
    """
    cdef vector[vector_int_ptr] v
    v.push_back(new vector[int]())
    del v[0]
    del create_to_delete()[f(f(0))]


def test_nested_del_repeat():
    """
    >>> test_nested_del_repeat()
    """
    cdef vector[vector_int_ptr] v
    v.push_back(new vector[int]())
    del v[0]
    del create_to_delete()[f(f(0))]
    del create_to_delete()[f(f(0))]
    del create_to_delete()[f(f(0))]

cdef extern from *:
    """
    class SomeClass {
      public:
        int some_value;
        SomeClass()
            : some_value(10101)
        {
        }
    };
    """
    cdef cppclass ThisClassDoesntExist:
        int some_value
    ctypedef ThisClassDoesntExist SomeClass

cdef class TestMisleadingName:
    """
    The code must be generated using SomeClass rather than ThisClassDoesntExist

    >>> x = TestMisleadingName()
    >>> x.get_some_value()
    10101
    >>> del x
    """
    cdef SomeClass a
    def get_some_value(self):
        return self.a.some_value
