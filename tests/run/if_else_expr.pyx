# mode: run
# tag: condexpr

cimport cython

cdef class Foo:
    cdef dict data

    def __repr__(self):
        return '<Foo>'


cpdef test_type_cast(Foo obj, cond):
    """
    # Regression test: obj must be cast to (PyObject *) here
    >>> test_type_cast(Foo(), True)
    [<Foo>]
    >>> test_type_cast(Foo(), False)
    <Foo>
    """
    return [obj] if cond else obj


cdef func(Foo foo, dict data):
    return foo, data


@cython.test_fail_if_path_exists('//PyTypeTestNode')
def test_cpp_pyobject_cast(Foo obj1, Foo obj2, cond):
    """
    >>> test_cpp_pyobject_cast(Foo(), Foo(), True)
    (<Foo>, None)
    """
    return func(obj1 if cond else obj2, obj1.data if cond else obj2.data)


def test_charptr_coercion(x):
    """
    >>> print(test_charptr_coercion(True))
    abc
    >>> print(test_charptr_coercion(False))
    def
    """
    cdef char* s = b'abc' if x else b'def'
    return s.decode('ascii')


def test_syntax():
    """
    >>> test_syntax()
    (0, 0, 0)
    """
    # Py3 allows the 'else' keyword to directly follow a number
    x = 0 if 1else 1
    y = 0 if 1.0else 1
    z = 0 if 1.else 1
    return x, y, z
