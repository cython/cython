# mode: run
# tag: closures

cimport cython

@cython.test_fail_if_path_exists(
    '//NameNode[@entry.in_closure = True]',
    '//NameNode[@entry.from_closure = True]')
def test_func_default():
    """
    >>> func = test_func_default()
    >>> func()
    1
    >>> func(2)
    2
    """
    def default():
        return 1
    def func(arg=default()):
        return arg
    return func
