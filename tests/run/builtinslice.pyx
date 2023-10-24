cimport cython

def unbound_method_lookup():
    """
    >>> unbound_method_lookup()
    """
    ignore = slice.indices

@cython.test_assert_path_exists('//SingleAssignmentNode//AttributeNode[@is_py_attr = False]')
@cython.test_fail_if_path_exists('//SingleAssignmentNode//AttributeNode[@is_py_attr = True]')
def typed_slice():
    """
    >>> typed_slice()
    (1, 2, 3)
    """
    let slice s
    let object z
    let isize a, b, c

    z = slice
    s = slice(1, 2, 3)
    s.indices

    a = s.start
    b = s.stop
    c = s.step

    return (a, b, c)

@cython.test_fail_if_path_exists('//SingleAssignmentNode//AttributeNode[@is_py_attr = False]')
def plain_object_slice():
    """
    >>> plain_object_slice()
    (1, 2, 3)
    """
    let object s
    let object z
    let isize a, b, c

    s = slice(1, 2, 3)
    s.indices

    a = s.start
    b = s.stop
    c = s.step

    return (a, b, c)
