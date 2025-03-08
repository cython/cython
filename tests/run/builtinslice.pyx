cimport cython

def unbound_method_lookup():
    """
    >>> unbound_method_lookup()
    """
    ignore = slice.indices

# BuiltinProperty ends up as a simple call node
@cython.test_assert_path_exists('//SingleAssignmentNode//SimpleCallNode//NameNode[@name="start"]')
@cython.test_fail_if_path_exists('//SingleAssignmentNode//AttributeNode[@is_py_attr = True]')
def typed_slice():
    """
    >>> typed_slice()
    (1, 2, 3)
    """
    cdef slice s
    cdef object z
    cdef Py_ssize_t a,b,c

    z = slice
    s = slice(1, 2, 3)
    s.indices

    a = s.start
    b = s.stop
    c = s.step

    return (a,b,c)

@cython.test_fail_if_path_exists('//SingleAssignmentNode//AttributeNode[@is_py_attr = False]')
def plain_object_slice():
    """
    >>> plain_object_slice()
    (1, 2, 3)
    """
    cdef object s
    cdef object z
    cdef Py_ssize_t a,b,c

    s = slice(1, 2, 3)
    s.indices

    a = s.start
    b = s.stop
    c = s.step

    return (a,b,c)
