# mode: run
# tag: except

# test the code object cache that is being used in exception raising

### low level tests

cimport cython

cdef extern from *:
    # evil hack to access the internal utility function
    ctypedef struct PyCodeObject
    ctypedef struct __Pyx_CodeObjectCacheEntry:
        int code_line
        PyCodeObject* code_object
    int __pyx_bisect_code_objects(__Pyx_CodeObjectCacheEntry* entries, int count, int code_line)

def test_lowlevel_bisect2(*indices):
    """
    >>> test_lowlevel_bisect2(1, 2, 3, 4, 5, 6)
    [0, 0, 1, 1, 2, 2]
    """
    cdef __Pyx_CodeObjectCacheEntry* cache = [
        __Pyx_CodeObjectCacheEntry(2, NULL),
        __Pyx_CodeObjectCacheEntry(4, NULL),
        ]
    return [ __pyx_bisect_code_objects(cache, 2, i)
             for i in indices ]

def test_lowlevel_bisect5(*indices):
    """
    >>> test_lowlevel_bisect5(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    [0, 1, 2, 2, 2, 3, 3, 3, 4, 5, 5]
    """
    cdef __Pyx_CodeObjectCacheEntry* cache = [
        __Pyx_CodeObjectCacheEntry(1, NULL),
        __Pyx_CodeObjectCacheEntry(2, NULL),
        __Pyx_CodeObjectCacheEntry(5, NULL),
        __Pyx_CodeObjectCacheEntry(8, NULL),
        __Pyx_CodeObjectCacheEntry(9, NULL),
        ]
    return [ __pyx_bisect_code_objects(cache, 5, i)
             for i in indices ]

def test_lowlevel_bisect6(*indices):
    """
    >>> test_lowlevel_bisect6(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    [0, 0, 1, 2, 2, 2, 3, 3, 4, 5, 5, 5, 6]
    """
    cdef __Pyx_CodeObjectCacheEntry* cache = [
        __Pyx_CodeObjectCacheEntry(2, NULL),
        __Pyx_CodeObjectCacheEntry(3, NULL),
        __Pyx_CodeObjectCacheEntry(6, NULL),
        __Pyx_CodeObjectCacheEntry(8, NULL),
        __Pyx_CodeObjectCacheEntry(9, NULL),
        __Pyx_CodeObjectCacheEntry(12, NULL),
        ]
    return [ __pyx_bisect_code_objects(cache, 6, i)
             for i in indices ]

### Python level tests

import sys

def tb():
    return sys.exc_info()[-1]

def raise_keyerror():
    raise KeyError

def check_code_object_identity_recursively(tb1, tb2):
    if tb1 is None or tb2 is None:
        return
    code1, code2 = tb1.tb_frame.f_code, tb2.tb_frame.f_code
    if code1 is not code2:
        print('%s != %s' % (code1, code2))
    check_code_object_identity_recursively(tb1.tb_next, tb2.tb_next)

def assert_simple_code_object_reuse():
    """
    >>> try: assert_simple_code_object_reuse()
    ... except KeyError: t1 = tb()
    >>> try: assert_simple_code_object_reuse()
    ... except KeyError: t2 = tb()
    >>> check_code_object_identity_recursively(t1.tb_next, t2.tb_next)
    """
    raise KeyError

def assert_multi_step_code_object_reuse(recursions=0):
    """
    >>> for depth in range(5):
    ...     try: assert_multi_step_code_object_reuse(depth)
    ...     except KeyError: t1 = tb()
    ...     try: assert_multi_step_code_object_reuse(depth)
    ...     except KeyError: t2 = tb()
    ...     check_code_object_identity_recursively(t1.tb_next, t2.tb_next)
    """
    if recursions:
        assert_multi_step_code_object_reuse(recursions-1)
    else:
        raise_keyerror()

def assert_simple_code_object_reuse_fused(cython.floating dummy):
    """
    DISABLED: searching for code objects based on C lineno breaks for specializations

    >> try: assert_simple_code_object_reuse_fused["float"](1.0)
    ... except KeyError: t1 = tb()
    >> try: assert_simple_code_object_reuse_fused["double"](1.0)
    ... except KeyError: t2 = tb()
    >> check_code_object_identity_recursively(t1.tb_next, t2.tb_next)
    """
    raise KeyError

def assert_multi_step_code_object_reuse_fused(recursions=0, cython.floating dummy = 2.0):
    """
    DISABLED: searching for code objects based on C lineno breaks for specializations

    >> for depth in range(5):
    ...     try: assert_multi_step_code_object_reuse_fused(depth, 1.0)
    ...     except KeyError: t1 = tb()
    ...     try: assert_multi_step_code_object_reuse_fused(depth, 1.0)
    ...     except KeyError: t2 = tb()
    ...     check_code_object_identity_recursively(t1.tb_next, t2.tb_next)
    """
    if recursions:
        assert_multi_step_code_object_reuse(recursions-1)
    else:
        raise_keyerror()
