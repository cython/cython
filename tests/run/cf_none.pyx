
cimport cython

@cython.test_fail_if_path_exists('//NoneCheckNode')
def none_checks(a):
    """
    >>> none_checks(1)
    22
    >>> none_checks(None)
    True
    """
    c = None
    d = {11:22}
    if a is c:
        return True
    else:
        return d.get(11)

@cython.test_assert_path_exists('//NoneCheckNode')
def dict_arg(dict a):
    """
    >>> dict_arg({})
    >>> dict_arg({1:2})
    2
    """
    return a.get(1)

@cython.test_fail_if_path_exists('//NoneCheckNode')
def dict_arg_not_none(dict a not None):
    """
    >>> dict_arg_not_none({})
    >>> dict_arg_not_none({1:2})
    2
    """
    return a.get(1)

@cython.test_assert_path_exists('//NoneCheckNode')
def reassignment(dict d):
    """
    >>> reassignment({})
    (None, 2)
    >>> reassignment({1:3})
    (3, 2)
    """
    a = d.get(1)
    d = {1:2}
    b = d.get(1)
    return a, b

@cython.test_fail_if_path_exists('//NoneCheckNode')
def conditional(a):
    """
    >>> conditional(True)
    2
    >>> conditional(False)
    3
    """
    if a:
        d = {1:2}
    else:
        d = {1:3}
    return d.get(1)

@cython.test_assert_path_exists('//NoneCheckNode')
def conditional_arg(a, dict d):
    """
    >>> conditional_arg(True,  {1:2})
    >>> conditional_arg(False, {1:2})
    2
    """
    if a:
        d = {}
    return d.get(1)

@cython.test_fail_if_path_exists('//NoneCheckNode')
def conditional_not_none(a, dict d not None):
    """
    >>> conditional_not_none(True,  {1:2})
    >>> conditional_not_none(False, {1:2})
    2
    """
    if a:
        d = {}
    return d.get(1)

@cython.test_fail_if_path_exists('//NoneCheckNode')
def self_dependency(int x):
    """
    >>> self_dependency(1)
    (1, 2)
    >>> self_dependency(2)
    (None, None)
    """
    cdef dict a, b
    a = {1:2}
    b = {2:1}
    for i in range(x):
        a,b = b,a
    return a.get(2), b.get(1)

@cython.test_assert_path_exists('//NoneCheckNode')
def self_dependency_none(int x):
    """
    >>> self_dependency_none(False)
    1
    >>> self_dependency_none(True)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'get'
    """
    cdef dict a, b
    a = None
    b = {2:1}
    if x:
        a,b = b,a
    return b.get(2)

@cython.test_fail_if_path_exists('//NoneCheckNode')
def in_place_op():
    vals = [0]
    vals += [1]
    for x in vals:
        pass
