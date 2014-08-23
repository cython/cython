
cdef int[10] data
cdef int[:] myslice = data

def test_memoryview_namespace():
    """
    >>> test_memoryview_namespace()
    """
    namespace = dir(__import__(__name__))
    assert 'array' not in namespace, namespace
    assert 'memoryview' not in namespace, namespace
    assert '_memoryviewslice' not in namespace, namespace
    assert 'Enum' not in namespace, namespace
