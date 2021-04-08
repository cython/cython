cimport cython


def modify_in_function():
    """
    >>> modify_in_function()
    {'foo': 'bar'}
    {'foo': 'bar'}
    """
    def inner(**kwds):
        kwds['foo'] = 'modified'
    d = {'foo': 'bar'}
    print(d)
    inner(**d)
    print(d)


@cython.test_fail_if_path_exists('//MergedDictNode')
def unused(*args, **kwargs):
    """
    >>> unused()
    ()
    >>> unused(1, 2)
    (1, 2)
    """
    return args


@cython.test_fail_if_path_exists('//MergedDictNode')
def used_in_closure(**kwargs):
    """
    >>> used_in_closure()
    >>> d = {}
    >>> used_in_closure(**d)
    >>> d  # must not be modified
    {}
    """
    def func():
        kwargs['test'] = 1
    return func()


@cython.test_fail_if_path_exists('//MergedDictNode')
def modify_in_closure(**kwargs):
    """
    >>> func = modify_in_closure()
    >>> func()

    >>> d = {}
    >>> func = modify_in_closure(**d)
    >>> func()
    >>> d  # must not be modified
    {}
    """
    def func():
        kwargs['test'] = 1
    return func


@cython.test_assert_path_exists('//MergedDictNode')
def wrap_passthrough_more(f):
    """
    >>> def f(a=1, test=2):
    ...     return a, test
    >>> wrapped = wrap_passthrough_more(f)
    >>> wrapped(1)
    CALLED
    (1, 1)
    >>> wrapped(a=2)
    CALLED
    (2, 1)
    """
    def wrapper(*args, **kwargs):
        print("CALLED")
        return f(*args, test=1, **kwargs)
    return wrapper


@cython.test_assert_path_exists('//MergedDictNode')
def wrap_modify_func(f):
    """
    >>> def f(a=1, test=2):
    ...     return a, test

    >>> wrapped = wrap_modify_func(f)
    >>> wrapped(1)
    CALLED
    (1, 1)
    >>> wrapped(a=2)
    CALLED
    (2, 1)
    >>> wrapped(a=2, test=3)
    CALLED
    (2, 1)
    """
    def modify(kw):
        kw['test'] = 1
        return kw

    def wrapper(*args, **kwargs):
        print("CALLED")
        return f(*args, **modify(kwargs))
    return wrapper


@cython.test_assert_path_exists('//MergedDictNode')
def wrap_modify_func_mix(f):
    """
    >>> def f(a=1, test=2):
    ...     return a, test

    >>> wrapped = wrap_modify_func_mix(f)
    >>> wrapped(1)
    CALLED
    (1, 1)
    >>> wrapped(a=2)
    CALLED
    (2, 1)
    >>> wrapped(a=2, test=3)
    CALLED
    (2, 1)
    """
    def modify(kw):
        kw['test'] = 1
        return kw

    def wrapper(*args, **kwargs):
        print("CALLED")
        f(*args, **kwargs)
        return f(*args, **modify(kwargs))
    return wrapper
