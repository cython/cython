cimport cython


@cython.test_assert_path_exists('//MergedDictNode')
def dict_unpacking_not_for_arg_return_a_copy():
    """
    >>> dict_unpacking_with_a_copy()
    {'a': 1, 'b': 0}
    {'a': 0, 'b': 0}
    """
    data = {'a': 0, 'b':0}

    func = lambda: {**data}

    call_once = func()
    call_once['a'] = 1

    call_twice = func()

    print(call_once)
    print(call_twice)
