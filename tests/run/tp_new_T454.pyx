# ticket: 454

cimport cython

cdef class TypeWithFactory:
    @cython.test_assert_path_exists('//PythonCapiCallNode')
    @cython.test_fail_if_path_exists('//SimpleCallNode/AttributeNode')
    @classmethod
    def new(cls):
        return cls.__new__(cls)

def make_new_factory():
    """
    >>> isinstance(make_new_factory(), TypeWithFactory)
    True
    """
    return TypeWithFactory.new()
