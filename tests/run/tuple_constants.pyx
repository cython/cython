
cimport cython

module_level_tuple = (1,2,3)

def return_module_level_tuple():
    """
    >>> return_module_level_tuple()
    (1, 2, 3)
    """
    return module_level_tuple

@cython.test_assert_path_exists("//TupleNode",
                                "//TupleNode[@is_literal = true]")
@cython.test_fail_if_path_exists("//TupleNode[@is_literal = false]")
def return_empty_tuple():
    """
    >>> return_empty_tuple()
    ()
    """
    return ()

@cython.test_assert_path_exists("//TupleNode",
                                "//TupleNode[@is_literal = true]")
@cython.test_fail_if_path_exists("//TupleNode[@is_literal = false]")
def return_constant_tuple1():
    """
    >>> return_constant_tuple1()
    (1,)
    """
    return (1,)

@cython.test_assert_path_exists("//TupleNode",
                                "//TupleNode[@is_literal = true]")
@cython.test_fail_if_path_exists("//TupleNode[@is_literal = false]")
def return_folded_tuple():
    """
    >>> return_folded_tuple()
    (1, 2, 3)
    """
    return (1, 1+1, 1+1+1)

@cython.test_assert_path_exists("//TupleNode",
                                "//TupleNode[@is_literal = true]")
@cython.test_fail_if_path_exists("//TupleNode[@is_literal = false]")
def return_nested_tuple():
    """
    >>> return_nested_tuple()
    (1, (2, 3), (3, (4, 5), (2, 3, 2, 3)))
    """
    return (1, (2, 3), (3, (4, 5), (2, 3) * 2))

@cython.test_assert_path_exists("//TupleNode",
                                "//TupleNode[@is_literal = true]")
@cython.test_fail_if_path_exists("//TupleNode[@is_literal = false]")
def constant_tuple1():
    """
    >>> constant_tuple1()
    (1,)
    """
    tuple1 = (1,)
    return tuple1

@cython.test_assert_path_exists("//TupleNode",
                                "//TupleNode[@is_literal = true]")
@cython.test_fail_if_path_exists("//TupleNode[@is_literal = false]")
def return_constant_tuple2():
    """
    >>> return_constant_tuple2()
    (1, 2)
    """
    return (1,2)


def return_multiplied_constant_tuple(n):
    """
    >>> tuples = return_multiplied_constant_tuple(2)
    >>> type(tuples) is tuple
    True
    >>> for t in tuples: print(t)
    ()
    (1, 2, 3)
    (1, 2, 3, 1, 2, 3)
    (1, 2, 3, 1, 2, 3, 1, 2, 3)
    (1, 2, 3, 1, 2, 3)
    (1, 2, 3, 1, 2, 3)
    ((1, 2, 3, 1, 2, 3), (1, 2, 3), (1, 2, 3, 1, 2, 3))
    """
    return (
        (1, 2, 3) * 0,
        (1, 2, 3) * 1,
        (1, 2, 3) * 2,
        (1, 2, 3) * 3,
        (1, 2, 3) * 2,
        (1, 2, 3) * n,
        ((1, 2, 3) * n, (1, 2, 3), (1, 2, 3) * n),
    )


@cython.test_assert_path_exists("//TupleNode",
                                "//TupleNode[@is_literal = true]")
@cython.test_fail_if_path_exists("//TupleNode[@is_literal = false]")
def return_constant_tuple_strings():
    """
    >>> return_constant_tuple_strings()
    ('tuple_1', 'bc', 'tuple_2')
    """
    return ('tuple_1', 'bc', 'tuple_2')

@cython.test_assert_path_exists("//TupleNode",
                                "//TupleNode[@is_literal = true]")
@cython.test_fail_if_path_exists("//TupleNode[@is_literal = false]")
def return_constant_tuples_string_types():
    """
    >>> a,b,c = return_constant_tuples_string_types()
    >>> a is b
    False
    >>> a is c
    False
    >>> b is c
    False
    """
    return ('a', 'bc'), (u'a', u'bc'), (b'a', b'bc')

@cython.test_assert_path_exists("//ReturnStatNode//TupleNode",
                                "//ReturnStatNode//TupleNode[@is_literal = false]")
@cython.test_fail_if_path_exists("//ReturnStatNode//TupleNode[@is_literal = true]")
def return_nonconstant_tuple():
    """
    >>> return_nonconstant_tuple()
    ('a', 1, 'd')
    """
    a = eval("1")
    return ('a', a, 'd')


def constant_types_comparing_equal():
    """
    >>> constant_types_comparing_equal()
    ((False, False), (0, 0), (0.0, 0.0), (0, False), (False, 0.0), (0, 0.0))
    """
    bool_tuple= (False, False)
    int_tuple = (0, 0)
    float_tuple = (0.0, 0.0)
    int_bool = (0, False)
    bool_float = (False, 0.0)
    int_float = (0, 0.0)

    assert bool_tuple is (False, False)
    assert int_tuple is (0, 0)
    assert bool_tuple == int_tuple
    assert bool_tuple is not int_tuple
    assert float_tuple is (0., 0.)
    assert float_tuple == int_tuple
    assert float_tuple is not int_tuple
    assert int_bool is (0, False)
    assert int_bool == bool_tuple
    assert int_bool is not bool_tuple
    assert int_bool is not int_tuple
    assert bool_float is (False, 0.)
    assert bool_float == bool_tuple
    assert bool_float is not bool_tuple
    assert bool_float is not float_tuple
    assert int_float is (0, 0.)
    assert int_float == int_tuple
    assert int_float is not int_tuple
    assert int_float is not float_tuple

    return bool_tuple, int_tuple, float_tuple, int_bool, bool_float, int_float
