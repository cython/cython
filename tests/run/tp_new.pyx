# ticket: 808

cimport cython

cdef class MyType:
    cdef public args, kwargs
    def __cinit__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        print "CINIT"
    def __init__(self, *args, **kwargs):
        print "INIT"

cdef class MySubType(MyType):
    def __cinit__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        print "CINIT(SUB)"
    def __init__(self, *args, **kwargs):
        print "INIT"

class MyClass(object):
    def __cinit__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        print "CINIT"
    def __init__(self, *args, **kwargs):
        print "INIT"

class MyTypeSubClass(MyType):
    def __cinit__(self, *args, **kwargs):
        # not called: Python class!
        print "CINIT(PYSUB)"
    def __init__(self, *args, **kwargs):
        print "INIT"

# See ticket T808, vtab must be set even if there is no __cinit__.

cdef class Base(object):
    pass

cdef class Derived(Base):
    cpdef int f(self):
        return 42

def test_derived_vtab():
    """
    >>> test_derived_vtab()
    42
    """
    cdef Derived d = Derived.__new__(Derived)
    return d.f()


# only these can be safely optimised:

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//SimpleCallNode/AttributeNode',
    '//PyMethodCallNode',
)
def make_new():
    """
    >>> isinstance(make_new(), MyType)
    CINIT
    True
    """
    m = MyType.__new__(MyType)
    return m

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//SimpleCallNode/AttributeNode',
    '//PyMethodCallNode',
)
def make_new_typed_target():
    """
    >>> isinstance(make_new_typed_target(), MyType)
    CINIT
    True
    """
    cdef MyType m
    m = MyType.__new__(MyType)
    return m

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//SimpleCallNode/AttributeNode',
    '//PyMethodCallNode',
)
def make_new_with_args():
    """
    >>> isinstance(make_new_with_args(), MyType)
    CINIT
    (1, 2, 3)
    {}
    True
    """
    m = MyType.__new__(MyType, 1, 2 ,3)
    print m.args
    print m.kwargs
    return m

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//SimpleCallNode/AttributeNode',
    '//PyMethodCallNode',
)
def make_new_with_args_kwargs():
    """
    >>> isinstance(make_new_with_args_kwargs(), MyType)
    CINIT
    (1, 2, 3)
    {'a': 4}
    True
    """
    m = MyType.__new__(MyType, 1, 2 ,3, a=4)
    print m.args
    print m.kwargs
    return m

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//SimpleCallNode/AttributeNode',
    '//PyMethodCallNode',
)
def make_new_builtin():
    """
    >>> isinstance(make_new_builtin(), tuple)
    True
    """
    m = dict.__new__(dict)
    m = list.__new__(list)
    m = tuple.__new__(tuple)
    return m

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//SimpleCallNode/AttributeNode',
    '//PyMethodCallNode',
)
def make_new_none(type t=None):
    """
    >>> make_new_none()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ... is not a type object (NoneType)
    """
    m = t.__new__(t)
    return m

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//SimpleCallNode/AttributeNode',
    '//PyMethodCallNode',
)
def make_new_kwargs(type t=None):
    """
    >>> m = make_new_kwargs(MyType)
    CINIT
    >>> isinstance(m, MyType)
    True
    >>> m.args
    (1, 2, 3)
    >>> m.kwargs
    {'a': 5}
    """
    m = t.__new__(t, 1, 2, 3, a=5)
    return m

# these cannot:

@cython.test_assert_path_exists('//PyMethodCallNode/AttributeNode')
@cython.test_fail_if_path_exists('//PythonCapiCallNode')
def make_new_pyclass():
    """
    >>> isinstance(make_new_pyclass(), MyTypeSubClass)
    CINIT
    True
    """
    m = MyClass.__new__(MyClass)
    m = MyTypeSubClass.__new__(MyTypeSubClass)
    return m

@cython.test_assert_path_exists('//PyMethodCallNode/AttributeNode')
@cython.test_fail_if_path_exists('//PythonCapiCallNode')
def make_new_args(type t1=None, type t2=None):
    """
    >>> isinstance(make_new_args(), MyType)
    CINIT
    True
    >>> isinstance(make_new_args(MyType), MyType)
    CINIT
    True
    >>> isinstance(make_new_args(MyType, MyType), MyType)
    CINIT
    True

    >>> isinstance(make_new_args(MyType, MySubType), MySubType)
    Traceback (most recent call last):
    TypeError: tp_new.MyType.__new__(tp_new.MySubType) is not safe, use tp_new.MySubType.__new__()
    >>> isinstance(make_new_args(MySubType, MyType), MyType)
    Traceback (most recent call last):
    TypeError: tp_new.MySubType.__new__(tp_new.MyType): tp_new.MyType is not a subtype of tp_new.MySubType
    """
    if t1 is None:
        t1 = MyType
    if t2 is None:
        t2 = MyType
    m = t1.__new__(t2)
    return m

@cython.test_assert_path_exists('//PyMethodCallNode/AttributeNode')
@cython.test_fail_if_path_exists('//PythonCapiCallNode')
def make_new_none_typed(tuple t=None):
    """
    >>> make_new_none_typed()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ... is not a type object (NoneType)
    """
    m = t.__new__(t)
    return m

@cython.test_assert_path_exists('//PyMethodCallNode/AttributeNode')
@cython.test_fail_if_path_exists('//PythonCapiCallNode')
def make_new_untyped(t):
    """
    >>> make_new_untyped(None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ... is not a type object (NoneType)
    """
    m = t.__new__(t)
    return m
