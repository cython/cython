# ticket: 650

cimport cython


@cython.test_assert_path_exists(
    '//RaiseStatNode',
    '//RaiseStatNode[@builtin_exc_name = "MemoryError"]')
def raise_me_type():
    """
    >>> try: raise_me_type()
    ... except MemoryError: pass
    ... else: print('NOT RAISED!')
    """
    raise MemoryError


@cython.test_assert_path_exists(
    '//RaiseStatNode',
    '//RaiseStatNode[@builtin_exc_name = "MemoryError"]')
def raise_me_instance():
    """
    >>> try: raise_me_instance()
    ... except MemoryError: pass
    ... else: print('NOT RAISED!')
    """
    raise MemoryError()


def raise_me_instance_value():
    """
    >>> raise_me_instance_value()
    Traceback (most recent call last):
        ...
    MemoryError: oom
    """
    raise MemoryError("oom")


def raise_me_instance_value_separate():
    """
    >>> raise_me_instance_value_separate()
    Traceback (most recent call last):
        ...
    MemoryError: oom
    """
    raise MemoryError, "oom"
