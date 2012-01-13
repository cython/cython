# mode: run
# tag: if_else_expr

cdef class Foo:
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
