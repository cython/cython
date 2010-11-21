
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
    (1, (2, 3), (3, (4, 5)))
    """
    return (1, (2, 3), (3, (4, 5)))

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
